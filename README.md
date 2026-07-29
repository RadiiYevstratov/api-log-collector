Auth Event Analyzer Documentation
Table of Contents
Overview
Program Workflow
Detection Logic
Requirements
Usage
Input Format
Function Documentation
Attack Classification
Error Handling
Exit Codes
Test Dataset
Complexity
1. Overview

Auth Event Analyzer is a Python command-line application that analyzes authentication event logs stored in JSON format. Its primary purpose is to detect potential brute-force attacks by identifying repeated failed login attempts originating from the same IP address.

The application classifies detected attacks into two categories:

Type A – Brute-force attack detected, but no successful login occurred afterward.
Type B – Brute-force attack detected, followed by a successful login from the same IP address, indicating a possible account compromise.

Before processing the logs, the analyzer validates the input file to ensure every record is correctly formatted.

2. Program Workflow
main()
│
├── get_args()
│       Read command-line arguments
│
├── get_data()
│       Load JSON file
│
├── validate()
│       Validate records
│       Convert timestamps
│       Group events by IP
│
├── analyze()
│       Detect Type A / Type B attacks
│
└── print_result()
        Display findings
3. Detection Logic

The analyzer processes authentication logs using the following workflow:

Load authentication events from a JSON file.
Validate the structure of every record.
Convert timestamps into Python datetime objects.
Group all events by IP address.
Sort events chronologically.
Analyze every possible time window.
Count consecutive failed login attempts.
If the number of failures reaches the configured threshold, classify the IP as Type A.
If a successful login occurs after the threshold has been reached, convert the finding to Type B.
Print the results.
4. Requirements
Python 3.10+
Uses only the Python Standard Library:
argparse
datetime
json
sys
Linux or WSL (Windows Subsystem for Linux)
No third-party Python packages are required.
JSON authentication logs formatted according to the project specification.

No installation is required.

Run directly with:

python3 main.py <input_file>
5. Usage
python3 main.py INPUT [WINDOW] [--threshold N] [--json]
Arguments
Argument	Description	Default
INPUT	Path to the JSON log file	Required
WINDOW	Detection time window (minutes)	15
--threshold	Minimum failed login attempts required to classify an attack	5
--json	Print findings in JSON format	Disabled
Examples
python3 main.py testing-data/type_a.json
python3 main.py testing-data/type_b.json 10
python3 main.py testing-data/type_b.json 10 --threshold 8
python3 main.py testing-data/type_b.json --json
6. Input Format

The application expects a JSON array.

Each object must contain the following fields:

Field	Type	Description
timestamp	string	ISO-8601 timestamp
ip	string	Source IP address
user	string	Username
event	string	failed_login or successful_login

Example:

[
    {
        "timestamp": "2026-07-24T09:00:00",
        "ip": "192.168.1.20",
        "user": "admin",
        "event": "failed_login"
    }
]
7. Function Documentation
main()

Program entry point.

Responsibilities
Parse command-line arguments.
Load the JSON file.
Validate the input.
Analyze events.
Print the final report.
get_args()

Reads command-line arguments using argparse.

Returns
(input_path, window, threshold, json_output)
get_data(path)

Loads the JSON input file.

Parameters
Name	Type	Description
path	str	Path to the JSON file
Returns
data, number_events

where:

data is the parsed JSON array.
number_events is the total number of records.
Errors

The function exits with code 2 if:

the file does not exist,
permission is denied,
the JSON is invalid.
validate(data)

Validates the entire dataset.

Validation includes:

Root element is a list.
Every record is a dictionary.
Required keys exist.
Event type is valid.
Timestamp is a valid ISO-8601 value.

During validation:

timestamps are converted to datetime objects,
events are grouped by IP address.
Returns

A list grouped by IP address.

check_ip(ip, time, event, username, logs)

Groups authentication events by IP address.

If the IP already exists:

append the event,
append the username if it has not been seen before.

Otherwise:

create a new IP record.
analyze(data, time_window, threshold)

Performs brute-force detection.

For every IP address:

Iterate through events.
Create a sliding time window.
Count consecutive failed logins.
Reset the counter after a successful login.
If the threshold is reached:
create or update a Type A finding.
If a successful login occurs afterward:
convert the finding to Type B.
Returns
type_a, type_b
in_type(type_list, ip_target)

Utility function that checks whether an IP address already exists in a finding list.

Returns:

True
False
print_result(type_a, type_b, to_scan, json_format)

Prints the final report.

Supports two output formats:

Human-readable text
JSON
8. Attack Classification
Type A

A Type A attack is detected when an IP address performs at least the configured number of failed login attempts within the specified time window and no successful login occurs afterward.

Example:

09:00 failed
09:01 failed
09:02 failed
09:03 failed
09:04 failed

Result:

Type A
Type B

A Type B attack is detected when the threshold is reached and a successful login occurs afterward.

Example:

09:00 failed
09:01 failed
09:02 failed
09:03 failed
09:04 failed
09:05 successful

Result:

Type B

This may indicate that the attacker successfully guessed valid credentials.

9. Error Handling

The analyzer performs strict validation and exits with status code 2 whenever invalid input is encountered.

Error	Description
FileNotFoundError	Input file does not exist
PermissionError	File cannot be opened
JSONDecodeError	Invalid JSON syntax
Invalid root	JSON root is not an array
Invalid record	Array element is not an object
Missing key	Required field is absent
Unknown event	Event is not failed_login or successful_login
Invalid timestamp	Timestamp is not valid ISO-8601
10. Exit Codes
Exit Code	Meaning
0	Program completed successfully and no suspicious activity was detected.
1	One or more Type A or Type B findings were detected.
2	Invalid input or execution error (invalid JSON, missing file, permission denied, malformed records, invalid timestamp, etc.).
11. Test Dataset

The project includes test files covering both normal execution and error handling.

Functional Tests
File	Purpose
clean.json	No attack
type_a.json	Detect Type A
type_b.json	Detect Type B
overlap.json	Multiple IPs with different outcomes
unordered.json	Verify event sorting
boundary.json	Threshold boundary conditions
mixed.json	Multiple users and IPs
success_before.json	Successful login before failed attempts
scattered.json	Failed attempts outside the detection window
Error Tests
File	Validation
empty.json	Empty file
malformed.json	Invalid JSON
not_a_list.json	Root is not an array
missing_key.json	Missing required field
element_not_dict.json	Invalid element type
unknown_event.json	Invalid event value
bad_timestamp.json	Invalid timestamp
no_permission.json	Permission denied
12. Complexity

Assuming:

N = total number of authentication events
M = number of unique IP addresses
Stage	Complexity
Loading JSON	O(N)
Validation	O(N)
Grouping by IP	O(N × M) (current implementation uses a linear search)
Sorting events	O(E log E) per IP
Attack analysis	Up to O(E²) per IP

Where E is the number of events associated with a single IP address.

For typical authentication logs, this implementation performs well. However, replacing the list-based IP lookup in check_ip() with a dictionary and implementing a more efficient sliding-window algorithm would significantly improve performance on very large datasets.