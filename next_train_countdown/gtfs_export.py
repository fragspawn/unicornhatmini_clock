#!/usr/bin/env python3

import argparse
import csv
import json
from pathlib import Path


TARGET_STOPS = {"600309", "600310", "600311", "600312"}
WEEKDAYS = (
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
)


def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def format_departure_time(value):
    hour, minute, _seconds = value.split(":")
    return f"{int(hour):02d}:{minute}"


def export_timetable(gtfs_directory, output_file):
    gtfs_directory = Path(gtfs_directory)
    output_file = Path(output_file)

    stops = {
        row["stop_id"]: row
        for row in read_csv(gtfs_directory / "stops.txt")
        if row["stop_id"] in TARGET_STOPS
    }

    trips = {
        row["trip_id"]: row
        for row in read_csv(gtfs_directory / "trips.txt")
    }

    calendar = {
        row["service_id"]: row
        for row in read_csv(gtfs_directory / "calendar.txt")
    }

    calendar_dates = read_csv(gtfs_directory / "calendar_dates.txt")

    removed_dates = set()
    added_dates = set()
    for row in calendar_dates:
        if row["exception_type"] == "1":
            added_dates.add((row["service_id"], row["date"]))
        elif row["exception_type"] == "2":
            removed_dates.add((row["service_id"], row["date"]))

    services_for_day = {day: set() for day in WEEKDAYS}

    for service_id, row in calendar.items():
        for day in WEEKDAYS:
            if row[day] == "1":
                services_for_day[day].add(service_id)

    for service_id, date in added_dates:
        if len(date) == 8:
            day_number = int(date)
            # Calendar exception services are added under all applicable trips.
            for day in WEEKDAYS:
                services_for_day[day].add(service_id)

    services_to_remove_by_day = set()
    for service_id, date in removed_dates:
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:8])
        from datetime import date as calendar_date

        weekday = calendar_date(year, month, day).strftime("%A").lower()
        services_to_remove_by_day.add((weekday, service_id))

    entries = set()

    for stop_time in read_csv(gtfs_directory / "stop_times.txt"):
        stop_id = stop_time["stop_id"]
        if stop_id not in stops:
            continue

        trip = trips.get(stop_time["trip_id"])
        if not trip:
            continue

        service_id = trip["service_id"]
        departure_time = format_departure_time(stop_time["departure_time"])
        platform = stops[stop_id]["platform_code"]
        destination = trip["trip_headsign"]

        for day in WEEKDAYS:
            if service_id not in services_for_day[day]:
                continue
            if (day, service_id) in services_to_remove_by_day:
                continue

            entries.add((
                day,
                departure_time,
                platform,
                destination,
            ))

    day_index = {day: index for index, day in enumerate(WEEKDAYS)}

    output = [
        {
            "day_of_week": day,
            "departure_time": departure_time,
            "platform": platform,
            "destination": destination,
        }
        for day, departure_time, platform, destination in sorted(
            entries,
            key=lambda entry: (
                day_index[entry[0]],
                entry[1],
                int(entry[2]) if entry[2].isdigit() else entry[2],
                entry[3],
            ),
        )
    ]

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8") as handle:
        json.dump(output, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    print(f"Wrote {len(output)} entries to {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Export Sherwood station GTFS stops to JSON."
    )
    parser.add_argument(
        "--gtfs",
        type=Path,
        default=Path(__file__).parent / "GTFS",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent / "sherwood_services.json",
    )
    args = parser.parse_args()

    export_timetable(args.gtfs, args.output)


if __name__ == "__main__":
    main()