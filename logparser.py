#!/usr/bin/python
import sys
from datetime import datetime, timedelta
import re
import pprint

# Define initial values
interval = 60
response_time_ranges = [500, 1000, 10000, 60000]

api_re = re.compile('passkey=[a-z0-9]*')
api_keys = {}
total_request_number = 0
api_request_number = 0
display_request_number = 0
api_stats = {}
display_stats = {}
for r in response_time_ranges:
    api_stats[r] = 0
    display_stats[r] = 0


line = sys.stdin.readline()
start_datetime = datetime.strptime(line.split(' ')[3].lstrip('['), '%d/%b/%Y:%H:%M:%S')
start_datetime = start_datetime - timedelta(minutes=start_datetime.minute, seconds=start_datetime.second)\
                 + timedelta(minutes=interval)


for line in sys.stdin.readlines():
    #27/May/2014:00:19:26
    total_request_number += 1
    request = line.split(' ')
    request_response_time = int(request[-5])
    request_datetime = datetime.strptime(request[3].lstrip('['), '%d/%b/%Y:%H:%M:%S')

    # Distinguish API and display requests
    match = api_re.search(request[6])
    if match:
        stats = api_stats
        key = match.group(0).split('=')[1]
        api_keys.setdefault(key, 0)
        api_keys[key] += 1
    else:
        stats = display_stats

    if request_datetime <= (start_datetime + timedelta(minutes=interval)):
        for time in response_time_ranges:
            if request_response_time < time:
                stats[time] += 1
                break
    else:
        print("{}".format(start_datetime))

        # Print display request statistics
        overall_display_number = 0
        for i in response_time_ranges:
            overall_display_number += display_stats[i]
        print("Display\t{}:".format(overall_display_number)),
        if overall_display_number > 0:
            for time in response_time_ranges:
                print("{:.2%}<{:d}ms".format(float(display_stats[time])/overall_display_number, time)),
        print ("")

        # Print API request statistics
        overall_api_number = 0
        for i in response_time_ranges:
            overall_api_number += api_stats[i]
        print("API\t{}:".format(overall_api_number)),
        if overall_api_number > 0:
            for time in response_time_ranges:
                print("{:.2%}<{:d}ms".format(float(api_stats[time])/overall_api_number, time)),
        print("")

        # Clear all counters
        for r in response_time_ranges:
            api_stats[r] = 0
            display_stats[r] = 0
        start_datetime = start_datetime + timedelta(minutes=interval)

pprint.pprint(sorted(api_keys.iteritems()))