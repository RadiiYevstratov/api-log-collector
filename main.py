import os 
import sys
import argparse
import json
from datetime import datetime, timedelta



def main():
    path, window, json_format = get_args()
    data = get_data(path=path)
    data = validate(data=data)
    analyze(data=data, time_window=window)

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
    CHECK_LOGS_BY_IP = []

    for l in data:
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
            
            data = check_ip(l["ip"], l["timestamp"], l["event"], l["user"], CHECK_LOGS_BY_IP)

    return data


def check_ip(ip, time, event, username, logs):
    for d in logs:
        if  ip in d["ip"]:
            d["event"].append([time, event])
            if username not in d["user"]:
                d["user"].append(username)

            for d in logs:
                for ip, events in d.items():
                    d["event"].sort(key=lambda event: event[0])
            return logs
    logs.append({"ip": ip, "event": [[time, event]], "user": [username]})

    return logs

def analyze(data, time_window):

    type_b = []
    type_a = []
    for d in data:
        failed_count = 0
        error_type = None
        ip = d["ip"]
        events = d["event"]
        users = d["user"]
        print(ip)
        print(events)
        print(users)
        # for key, values in d.items():    
        #         for i, value in enumerate(values):
        #             time = value[0]
        #             event =  value[1]

        #             j = i
        #             max_time = None
        #             finishing_time = time + timedelta(minutes=time_window)
        #             while j < len(values) and values[j][0] < finishing_time:

        #                 if max_time is None or values[j][0] > max_time:
        #                     max_time = values[j][0]
        #                 j+= 1

        #                 if event == "failed_login":
        #                     failed_count += 1
        #                 if failed_count >= 5 and event == "successful_login":
        #                     error_type = "Type B"
        #                     type_b.append({"ip": key, "failed": failed_count, "users": d["user"]})
        #                     failed_count = 0
        #                 elif failed_count >= 5 and event != "successful_login":
        #                     error_type = "Type A"
        #                 elif failed_count < 5 and event == "successful_login":
        #                     failed_count = 0








if __name__== "__main__":
    main()

