# Next Train Countdown 

Based on timetable countdown to the next scheduled train arriving at the local station.
pulled open data: https://www.data.qld.gov.au/dataset/general-transit-feed-specification-gtfs-translink/resource/e43b6b9f-fc2b-4630-a7c9-86dd5483552b

# Hardware

* Pi Zero 2
* Pimoroni Unicorn HAT Mini PIM498SKU

# Files

* README.md - This file
* countdown.py - code to render MM:SS counting down to the next train
* .sh - dependancy install 
* .initd - Service Unit for execution on boot
* sherwood_services.json - timetable entries with day_of_week, platform, departure_time, and final_destination

# Program Structure

* Function to render M:SS or H:MM to LED Hat
* Function to return the next scheduled train based on current time
* base loop to read schedule calculate total minutes until arrival and print to Hat

# Rules

* Show hours and minutes reamining above 9m 59s
* Show seconds and and minute below or equal to 9m 59s
* only show three numbers at any one time on the screen
* blank the screen if the next train is longer than 9h 59m away
* Assign a different color to each timetabled service destination
* https://gtfsrt.api.translink.com.au/api/realtime/SEQ/TripUpdates

# Init.d

```
sudo cp /home/ubuntu/next_train_countdown/next_train_countdown.initd /etc/init.d/next_train_countdown
sudo chmod 755 /etc/init.d/next_train_countdown
sudo /etc/init.d/next_train_countdown enable
sudo /etc/init.d/next_train_countdown start
```

# TODO
* Write conversion script that takes latest translink GTFS data to JSON
* Print platform #1 on-screen
* Provide other functions on other buttons. 
