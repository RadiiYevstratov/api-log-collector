import os 
import sys
import argparse
import json


def main():
    path, time, json_format = get_args()
    get_data(path=path)

def get_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("input", help="Enter a path where are the logs are", type=str)
    parser.add_argument("--time", help="Enter a time of interval you would like to check. (in minutes)", default=10, type=int)
    parser.add_argument("--json", help="Return result in json format", action="store_true")
    args = parser.parse_args()
    return args.input, args.time, args.json

def get_data(path):
    try:
        with open (path, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, FileExistsError) as e:
        print(e)
        sys.exit(2)
    except json.decoder.JSONDecodeError as e:
        print(e)
        sys.exit(2)
if __name__== "__main__":
    main()