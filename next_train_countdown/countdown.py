#!/usr/bin/env python3
"""Display the next scheduled inbound service from the Sherwood timetable."""

from __future__ import annotations

import argparse
import json
import time as sltime

from datetime import datetime, time, timedelta
from pathlib import Path
from typing import Any

import requests
import RPi.GPIO as GPIO
from unicornhatmini import UnicornHATMini
hat = UnicornHATMini()
from gpiozero import Button
from signal import pause

GPIO.setmode(GPIO.BCM)

button_a = Button(5)
button_b = Button(6)
button_x = Button(16)
button_y = Button(24)

WEEKDAY_ORDER = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]

DIRECTION_DESTINATIONS = {
    "inbound": ("Nambour", "Kippa-Ring", "Caboolture", "Bowen Hills"),
    "outbound": ("Ipswich", "Springfield"),
}

DIGIT_FONT = {
    0: ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    1: ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    2: ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    3: ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    4: ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    5: ("11111", "10000", "10000", "11110", "00001", "00001", "11110"),
    6: ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    7: ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    8: ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    9: ("01110", "10001", "10001", "01111", "00001", "00010", "11100"),
}

MM_SS_MAX_SECONDS = 9 * 60 + 59
H_MM_MAX_SECONDS = 9 * 60 * 60 + 59 * 60

def parse_departure_minutes(value: str) -> int:
    """Return minutes after service-day midnight for a HH:MM departure."""
    hours, minutes = (int(part) for part in value.split(":", 1))
    return (hours * 60) + minutes

def load_timetable(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)

def build_service_index(
    timetable: list[dict[str, Any]],
    direction: str,
) -> dict[str, list[dict[str, Any]]]:
    services_by_day: dict[str, list[dict[str, Any]]] = {day: [] for day in WEEKDAY_ORDER}
    direction_name = str(direction).lower()
    destinations = DIRECTION_DESTINATIONS.get(direction_name, ())

    for service in timetable:
        destination = str(service.get("final_destination", ""))
        if not any(item.lower() in destination.lower() for item in destinations):
            continue

        day_name = str(service.get("day_of_week", "")).lower()
        if day_name not in services_by_day:
            continue

        services_by_day[day_name].append(service)

    for day_name, day_services in services_by_day.items():
        services_by_day[day_name] = sorted(
            day_services,
            key=lambda item: parse_departure_minutes(item["departure_time"]),
        )

    return services_by_day

def find_next_service(
    services_by_day: dict[str, list[dict[str, Any]]],
    now: datetime,
) -> tuple[datetime, dict[str, Any]]:
    """Return the next future service from the current day onward."""
    start_index = WEEKDAY_ORDER.index(now.strftime("%A").lower())
    now_minutes = (now.hour * 60) + now.minute

    for offset in range(7):
        day_name = WEEKDAY_ORDER[(start_index + offset) % 7]
        services = services_by_day.get(day_name, [])
        for service in services:
            departure_minutes = parse_departure_minutes(service["departure_time"])
            if offset == 0 and departure_minutes <= now_minutes:
                continue
            departure_dt = datetime.combine(
                now.date() + timedelta(days=offset),
                datetime.min.time(),
            ) + timedelta(minutes=departure_minutes)

            return departure_dt, service

    raise ValueError("No scheduled services found in the timetable.")

def render_number(value: int, hat=None, x: int = 0, y: int = 0, color=(255, 255, 255)) -> None:
    """Render a single decimal digit at the given x/y coordinate on the Unicorn HAT."""
    if not 0 <= value <= 9: 
        raise ValueError("render_number() supports digits 0-9 only")
    
    if hat is None:
        return
    
    rows = DIGIT_FONT[value]
    for row_index, row in enumerate(rows):
        for col_index, bit in enumerate(row):
            if bit == "1":
                hat.set_pixel(x + col_index, y + row_index, *color) 

def render_arrows(hat=None, color=(48, 16, 16), direction="inbound") -> None:
    """Render arrows on the Unicorn HAT Mini."""
    if hat is None:
        return

    outbound_arrow_pattern = [
        "00011",
        "00110",
        "01100",
        "11000",
        "01100",
        "00110",
        "00011",
    ]

    inbound_arrow_pattern = [
        "11000",
        "01100",
        "00110",
        "00011",
        "00110",
        "01100",
        "11000",
    ]
    
    if direction =="inbound":
        arrow_pattern = [(row * 3) + "0" for row in inbound_arrow_pattern]
    else:
        arrow_pattern = [(row * 3) + "0" for row in outbound_arrow_pattern]

    for row_index, row in enumerate(arrow_pattern):
        for col_index, bit in enumerate(row):
            if bit == "1":
                hat.set_pixel(col_index, row_index, *color)

def format_countdown_display(seconds_remaining: float) -> tuple[str, str]:
    """Return ('m_ss' or 'h_mm', formatted display) or ('blank', '') when out of range."""
    seconds = int(seconds_remaining)
    if seconds < 0:
        seconds = 0
    if seconds > H_MM_MAX_SECONDS:
        return "blank", ""
    if seconds <= MM_SS_MAX_SECONDS:
        minutes, secs = divmod(seconds, 60)
        return "m_ss", f"{minutes}:{secs:02d}"
    total_minutes = seconds // 60
    hours, minutes = divmod(total_minutes, 60)
    return "h_mm", f"{hours}:{minutes:02d}"

def render_mm_ss_on_hat(display_value: str, mode: str, hat=None, color=(255, 255, 255), platform=2, direction="inbound") -> None:
    """Render M:SS or H:MM on the Unicorn HAT Mini using exactly three digits."""
    try:
        left_text, right_text = display_value.split(":")
        left = int(left_text)
        right = int(right_text)
    except (ValueError, AttributeError):
        raise ValueError("render_mm_ss_on_hat() expects H:MM or M:SS")

    if mode == "m_ss" and (left < 0 or left > 9 or right < 0 or right > 59):
        raise ValueError("M:SS mode supports 0:00-9:59")
    if mode == "h_mm" and (left < 0 or left > 9 or right < 0 or right > 59):
        raise ValueError("H:MM mode supports 0:00-9:59")
    if mode not in {"m_ss", "h_mm"}:
        raise ValueError("mode must be 'm_ss' or 'h_mm'")

    if hat is None:
        return

    hat.clear()

    render_arrows(hat=hat, direction=direction)

    right_tens = right // 10
    right_ones = right % 10
    render_number(left, hat=hat, x=0, y=0, color=color)
    render_number(right_tens, hat=hat, x=6, y=0, color=color)
    render_number(right_ones, hat=hat, x=12, y=0, color=color)
    hat.show()


def render_air_quality_on_hat(hat=None) -> None:
    """Fetch the current air-quality reading from the local sensor and show it briefly."""
    if hat is None:
        return

    try:
        response = requests.get("http://192.168.1.132/json", timeout=5)
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError):
        payload = {}
        return False

    p25aqic_b = payload.get("p25aqic_b", "rgb(0,0,0)")
    if isinstance(p25aqic_b, str):
        if p25aqic_b.lower().startswith("rgb(") and p25aqic_b.endswith(")"):
            p25aqic_b = tuple(
                int(part.strip()) for part in p25aqic_b[4:-1].split(",") if part.strip()
            )
        else:
            p25aqic_b = (0, 0, 0)
    elif isinstance(p25aqic_b, (list, tuple)):
        p25aqic_b = tuple(int(component) for component in p25aqic_b)
    else:
        p25aqic_b = (0, 0, 0)

    air_quality = int(payload.get("pm2.5_aqi", 0))

    hat.clear()
    for x in range(17):
        for y in range(7):
            hat.set_pixel(x, y, *p25aqic_b)

    digits = [int(digit) for digit in str(abs(air_quality)) or "0"]
    x_offset = 0
    for digit in digits[:3]:
        render_number(digit, hat=hat, x=x_offset, y=0, color=(0, 0, 0))
        x_offset += 5

    hat.show()
    sltime.sleep(3)
    hat.clear()

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "timetable",
        nargs="?",
        default=str(Path(__file__).resolve().with_name("sherwood_services.json")),
        help="Path to the Sherwood timetable JSON file.",
    )
    parser.add_argument(
        "--direction",
        choices=sorted(DIRECTION_DESTINATIONS),
        default="inbound",
        help="Direction to display services for. Default: inbound",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Seconds between refreshes. Default: 1.0",
    )
    args = parser.parse_args()

    timetable_path = Path(args.timetable)
    timetable = load_timetable(timetable_path)
    current_direction = args.direction
    services_by_day = build_service_index(timetable, current_direction)
    direction_toggle_requested = False
    air_quality_requested = False

    def on_button_a_pressed() -> None:
        nonlocal direction_toggle_requested
        direction_toggle_requested = True

    def on_button_x_pressed() -> None:
        nonlocal air_quality_requested
        air_quality_requested = True

    button_a.when_pressed = on_button_a_pressed
    button_x.when_pressed = on_button_x_pressed

    while True:
        if direction_toggle_requested:
            current_direction = "outbound" if current_direction == "inbound" else "inbound"
            services_by_day = build_service_index(timetable, current_direction)
            direction_toggle_requested = False

        if air_quality_requested:
            render_air_quality_on_hat(hat=hat)
            air_quality_requested = False

        now = datetime.now()
        departure_dt, service = find_next_service(services_by_day, now)
        remaining = (departure_dt - now).total_seconds()
        display_mode, display_value = format_countdown_display(remaining)

        if service.get('final_destination') in {'Caboolture station', 'Ipswich station'}:
            color = (64, 255, 64) 
        if service.get('final_destination') in {'Nambour station'}:
            color = (0, 255, 0)             
        if service.get('final_destination') in {'Springfield Central station', 'Kippa-Ring station'}:
            color = (64, 64, 255)
        if service.get('final_destination') == 'Bowen Hills station':
            color = (255, 255, 255)

        render_mm_ss_on_hat(display_value, mode=display_mode, hat=hat, color=color, platform=service.get('platform'), direction=current_direction)
        sltime.sleep(1)

if __name__ == "__main__":
    main()
