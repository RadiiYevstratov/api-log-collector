import os 
import argparse


def main():
    path, time, json_format = get_args()


def get_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("input", help="Enter a path where are the logs are", type=str)
    parser.add_argument("--time", help="Enter a time of interval you would like to check. (in minutes)", default=10, type=int)
    parser.add_argument("--json", help="Return result in json format", action="store_true")
    args = parser.parse_args()
    return args.input, args.time, args.json



if __name__== "__main__":
    main()