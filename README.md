Auth Event Analyzer - Documentation
Overview

Auth Event Analyzer is a Python command-line application that analyzes authentication event logs stored in JSON format. Its primary purpose is to detect potential brute-force attacks by identifying repeated failed login attempts originating from the same IP address.

The application classifies detected attacks into two categories:

Type A – Brute-force attack detected, but no successful login occurred afterward.
Type B – Brute-force attack detected, followed by a successful login from the same IP address, indicating a possible account compromise.

The analyzer validates the input file before processing to ensure all records are correctly formatted.

Program Workflow
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

Detection Logic

The analyzer processes authentication logs using the following workflow:

Load authentication events from a JSON file.
Validate the structure of every record.
Convert timestamps into Python datetime objects.
Group all events by IP address.
Sort events chronologically.
Analyze every possible time window.
Count consecutive failed login attempts.
If the number of failures reaches the configured threshold:
mark the IP as Type A
If a successful login occurs after the threshold is exceeded:
convert the finding into Type B
Print the results.

Requirements
Python 3.10+ (or simply Python 3.x if you don't want to specify a minimum version)
Uses only the Python Standard Library
argparse
datetime
json
sys
Linux operating system or WSL (Windows Subsystem for Linux)
No third-party Python packages are required.
JSON authentication logs formatted according to the project specification.

Installation is not required.

Run directly with:

python3 main.py <input_file>

Usage
python3 main.py INPUT [WINDOW] [--threshold N] [--json]
Arguments
Argument	Description	Default
INPUT	Path to the JSON log file.	Required
WINDOW	Time window (minutes) used for brute-force detection.	15
--threshold	Minimum number of failed login attempts required to classify an attack.	5
--json	Print findings in JSON format instead of human-readable text.	Disabled
Examples
python3 main.py testing-data/type_a.json
python3 main.py testing-data/type_b.json 10
python3 main.py testing-data/type_b.json 10 --threshold 8
python3 main.py testing-data/type_b.json --json

Input Format

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
        "timestamp":"2026-07-24T09:00:00",
        "ip":"192.168.1.20",
        "user":"admin",
        "event":"failed_login"
    }
]
Command Line Arguments
python main.py INPUT [WINDOW] [--threshold N] [--json]
Argument	Description	Default
INPUT	Path to JSON log file	Required
WINDOW	Detection window in minutes	15
--threshold	Minimum failed logins considered an attack	5
--json	Output results as JSON	False

Example:

python main.py logs.json
python main.py logs.json 10
python main.py logs.json 10 --threshold 8
python main.py logs.json --json
Function Documentation
main()

Program entry point.

Responsibilities
Parse command-line arguments.
Load the JSON file.
Validate input.
Analyze events.
Print the final report.
get_args()

Reads command-line arguments using argparse.

Returns
(
    input_path,
    window,
    threshold,
    json_output
)
get_data(path)

Loads the JSON input file.

Parameters
Name	Type	Description
path	str	Path to JSON file
Returns
data, number_events

where

data is the parsed JSON array.
number_events is the total number of records.
Errors

The function exits with code 2 if:

file does not exist
permission denied
invalid JSON
validate(data)

Validates the entire dataset.

Checks include:

root element is a list
every record is a dictionary
required keys exist
event type is valid
timestamp is valid ISO-8601

During validation:

timestamps are converted into datetime
records are grouped by IP address
Returns
[
    {
        "ip": "...",
        "event": [
            [datetime(...), "failed_login"],
            ...
        ],
        "user": [
            "admin",
            "root"
        ]
    }
]
check_ip(ip, time, event, username, logs)

Groups authentication events by IP address.

If the IP already exists:

append event
append username if new

Otherwise:

create a new IP record

This reduces the number of structures that must be analyzed later.

analyze(data, time_window, threshold)

Performs brute-force detection.

For every IP:

Iterate through each event.
Create a sliding time window.
Count consecutive failed logins.
Reset the counter after a successful login.
When failures reach the threshold:
create or update a Type A finding.
If a successful login occurs after the threshold:
convert the finding into Type B.
Returns
type_a, type_b
in_type(type_list, ip_target)

Utility function.

Returns:

True

if the IP already exists in the specified finding list.

Otherwise:

False
print_result(type_a, type_b, to_scan, json_format)

Displays the final report.

Two output formats are supported:

Human-readable
=== TYPE B ===

192.168.1.20:
failed=6
last_success=...

=== TYPE A ===

203.0.113.10:
failed=5

=== SUMMARY ===

Finding: 2
Events processed: 15
JSON
[
    {
        "ip":"192.168.1.20",
        "failed":6,
        "users":[
            "admin"
        ],
        "last_success":"2026-07-24T09:09:30"
    }
]
Attack Classification
Type A

A Type A attack is detected when an IP address performs at least the configured number of consecutive failed login attempts within the specified time window without any subsequent successful login.

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

Error Handling

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

Exit Codes
Exit Code	Meaning
0	Program completed successfully and no suspicious activity was detected.
1	One or more brute-force findings (Type A or Type B) were detected.
2	Invalid input or execution error (invalid JSON, missing file, permission denied, malformed records, invalid timestamp, etc.).

Test Dataset

The project includes test files covering both normal operation and error handling.

Functional Tests
File	Purpose
clean.json	No attack
type_a.json	Detect Type A
type_b.json	Detect Type B
overlap.json	Multiple IPs with different outcomes
unordered.json	Verify event sorting
boundary.json	Threshold boundary conditions
mixed.json	Multiple users and IPs
success_before.json	Success before failures
scattered.json	Failures outside the time window
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
Exit Codes
Exit Code	Meaning
0	No findings; execution completed successfully
1	One or more Type A or Type B findings detected
2	Invalid input or execution error
Complexity

Assuming:

N = total number of authentication events
M = number of unique IP addresses

Approximate complexity:

Stage	Complexity
Loading JSON	O(N)
Validation	O(N)
Grouping by IP	O(N × M) in the current implementation (linear search per IP)
Sorting events	O(E log E) per IP, where E is the number of events for that IP
Attack analysis	Up to O(E²) per IP due to the sliding-window scan from each event

For typical authentication logs, this approach performs well, but replacing the list-based IP lookup in check_ip() with a dictionary and using a more efficient sliding-window technique could reduce runtime on very large datasets.