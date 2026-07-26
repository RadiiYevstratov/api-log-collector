import os 
import sys
import argparse
import json
from datetime import datetime, timedelta



def main():
    path, window, json_format = get_args()
    data = get_data(path=path)
    data = validate(data=data)


def get_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("input", help="Enter a path where are the logs are", type=str)
    parser.add_argument("window", help="Enter a window of interval you would like to check. (in minutes)", default=10, type=int, nargs="?")
    parser.add_argument("--json", help="Return result in json format", action="store_true")
    args = parser.parse_args()
    return args.input, args.window, args.json

def get_data(path):

    # if not os.path.isdir(path):
    #     print(f"Error: '{path}' is not a directory or does not exist.", file=sys.stderr)
    #     sys.exit(1)

    try:
        with open (path, "r") as file:
            data = json.load(file)
        return data
    except json.decoder.JSONDecodeError as e:
        print(e)
        sys.exit(2)
    except PermissionError as e:
        print(e)
        sys.exit(2)


def validate(data):
    EVENT_TYPES = ["successful_login", "failed_login"]
    CHECK_LOGS_BY_IP = [{}]
    for l in data:
        ip_dict = {}
        if type(l) is not dict:
            print("not dict")
            sys.exit(2)

        elif len(l) != 4:
            print("Missing key")
            sys.exit(2)

        else:
            for key, value in l.items():
                if key == "event" and value not in EVENT_TYPES:
                    print("bad event ttype")
                    sys.exit(2)
                    
                elif key == "timestamp":
                    try:
                        value = datetime.fromisoformat(value)
                        l["timestamp"] = value
                    except ValueError as e:
                        print(e)
                        sys.exit(2)
            data = check_ip(l["ip"], l["timestamp"], l["event"], CHECK_LOGS_BY_IP)

    return data


def check_ip(ip, time, event, logs):
    for d in logs:
        if  ip in d:
            d[ip].append([time, event])
            for d in logs:
                for ip, events in d.items():
                    events.sort(key=lambda x: x[0])
            return logs
    logs.append({ip: [[time, event]]})
    return logs





if __name__== "__main__":
    main()

