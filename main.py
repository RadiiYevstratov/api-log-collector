import os 
import sys
import argparse
import json
from datetime import datetime, timedelta



def main():
    path, window, threschold, json_format = get_args()
    data, number_events = get_data(path=path)
    data = validate(data=data)
    type_a, type_b = analyze(data=data, time_window=window, threshold=threschold)
    print_result(type_a=type_a, type_b=type_b, to_scan=number_events, json_format=json_format)

def get_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("input", help="Enter a path where are the logs are", type=str)
    parser.add_argument("window", help="Enter a window of interval you would like to check. (in minutes)", default=15, type=int, nargs="?")
    parser.add_argument("--threshold", help="Enter number of failed attemps for program to identify as atack", default=5, type=int, nargs="?")
    parser.add_argument("--json", help="Return result in json format", action="store_true")
    args = parser.parse_args()
    return args.input, args.window, args.threshold, args.json

def get_data(path):

    try:
        with open (path, "r") as file:
            data = json.load(file)
            number_events = len(data)
        return data, number_events
    
    except json.decoder.JSONDecodeError as e:
        print(f"ERROR: invalid JSON: {e}", file=sys.stderr)
        sys.exit(2)
    except PermissionError as e:
        print(f"ERROR: {e.strerror}: <{e.filename}>", file=sys.stderr)
        sys.exit(2)
    except FileNotFoundError as e:
        print(f"ERROR: {e.strerror}: {e.filename}", file=sys.stderr)
        sys.exit(2)

def validate(data):

    EVENT_TYPES = ["successful_login", "failed_login"]
    CHECK_LOGS_BY_IP = []

    for l in data:
        if type(l) is not dict:
            print("There is an elemnt in the file, which is not a dictionary type or JSON format.")
            sys.exit(2)

        elif len(l) != 4:
            print("Missing key")
            sys.exit(2)

        else:
            for key, value in l.items():
                if key == "event" and value not in EVENT_TYPES:
                    print(f"{value} is unknown event type.")
                    sys.exit(2)
                    
                elif key == "timestamp":
                    try:
                        value = datetime.fromisoformat(value)
                        l["timestamp"] = value
                    except ValueError as e:
                        print(e)
                        sys.exit(2)
            
            data = check_ip(l["ip"], l["timestamp"], l["event"], l["user"], CHECK_LOGS_BY_IP)

    return data


def check_ip(ip, time, event, username, logs):

    for d in logs:
        if ip == d["ip"]:
            d["event"].append([time, event])
            d["event"].sort(key=lambda event: event[0])

            if username not in d["user"]:
                d["user"].append(username)

            return logs

    logs.append({"ip": ip, "event": [[time, event]], "user": [username]})
    return logs

def analyze(data, time_window, threshold):

    type_b = []
    type_a = []

    for d in data:

        ip = d["ip"]
        events = d["event"]
        users = d["user"]
    
        for i, value in enumerate(events):
            time = value[0]

            j = i
            max_time = None
            finishing_time = time + timedelta(minutes=time_window)
            failed_count = 0
            error_type = None
            breach_time = None
            failed_before_success = 0
            while j < len(events) and events[j][0] < finishing_time:

                event = events[j][1]
                event_time = events[j][0]

                if event == "failed_login":
                    failed_count += 1

                    if failed_count >= threshold:
                        if not in_type(type_a, ip) and not in_type(type_b, ip):
                            type_a.append({"ip": ip, "failed": failed_count, "users": users})
                            breach_time = event_time
                            error_type = "A"

                        if in_type(type_a, ip) and not in_type(type_b, ip):
                            for item in type_a:
                                    if ip == item["ip"]:
                                        if failed_count > item["failed"]:
                                            item["failed"]=failed_count
                            error_type = "A"
                            breach_time = event_time
                            failed_before_success = failed_count

                if event == "successful_login":
                    failed_count = 0


                if max_time is None or events[j][0] > max_time:
                    max_time = events[j][0]
                j+= 1
            
            if error_type == "A":
                for value in events:
                    if value[0] > breach_time and value[1] == "successful_login":
                        type_b.append({"ip": ip, "failed": failed_before_success, "users": users, "last_success": value[0]})
                        item = next((x for x in type_a if x["ip"] == ip), None)
                        if item is not None:
                            type_a.remove(item)

                        break

    return type_a, type_b


def in_type(type_list, ip_target):
    for d in type_list:
        if ip_target == d["ip"]:
            return True

    return False


def print_result(type_a, type_b, to_scan, json_format):
    if json_format:
        if type_a != []:
            print(json.dumps(type_a, indent=4))
        if type_b != []:
            print(json.dumps(type_b, indent=4))
    else:
        if type_b != []:
            print(f"=== TYPE B: SUCCESSFUL LOGIN AFTER BRUTE FORCE ({len(type_b)}) === \n")
            for d in type_b:
                print(f"{d["ip"]}:    failed={d["failed"]};    last_success={d["last_success"]};    users={d["users"]}")
            print("\n")
        if type_a!= []:
            print(f"=== TYPE A: BRUTE FORCE ATTEMPTS ({len(type_a)}) === \n")
            for d in type_a:
                print(f"{d["ip"]}:    failed={d["failed"]};    users={d["users"]}")
        print("\n")
        print("=== SUMMARY ===")
        print(f"Finding: {len(type_a) + len(type_b)}")
        print(f"Events processed: {to_scan}")



if __name__== "__main__":
    main()

