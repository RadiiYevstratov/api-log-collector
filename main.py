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

def analyze(data, time_window):

    type_b = []
    type_a = []
    for d in data:
        ip = d["ip"]
        events = d["event"]
        users = d["user"]

    
        for i, value in enumerate(events):
            time = value[0]
            event =  value[1]

            j = i
            max_time = None
            finishing_time = time + timedelta(minutes=time_window)
            failed_count = 0
            while j < len(events) and events[j][0] < finishing_time:

                event = events[j][1]
                if event == "failed_login":
                    failed_count += 1

                    if failed_count > 4:
                        if not in_type(type_a, ip) and not in_type(type_b, ip):
                            type_a.append({"ip": ip, "failed": failed_count, "users": users})

                        if in_type(type_a, ip) and not in_type(type_b, ip):
                            for i in type_a:
                                    if ip == i["ip"]:
                                        if failed_count > i["failed"]:
                                            i["failed"]=failed_count

                if event == "successful_login" and failed_count > 4:
                    if in_type(type_a, ip) and not in_type(type_b, ip):
                        for i in type_a:
                                if ip == i["ip"]:
                                    type_b.append({"ip": ip, "failed": failed_count, "users": users})
                                    type_a.remove(i)
                    
                    if not in_type(type_a, ip) and  in_type(type_b, ip):
                        for i in type_b:
                                if ip == i["ip"]:
                                    if failed_count > i["failed"]:
                                        i["failed"]=failed_count
                    failed_count = 0


                if max_time is None or events[j][0] > max_time:
                    max_time = events[j][0]
                j+= 1
    for i in type_b:
        print(i, "b")
    for i in type_a:
        print(i, "a")


def in_type(type_list, ip_target):
    for d in type_list:
        if ip_target == d["ip"]:
            return True

    return False

def move_to_typeB(type_a, type_b, ip_target):
    for i, d in enumerate(type_a):
        if ip_target in d["ip"]:
            type_b.append(d)
            type_a.remove(d)




if __name__== "__main__":
    main()

