import argparse, json
from sys import stderr
from os import path

def cli(): # Making the code more maintenable
    parser = argparse.ArgumentParser(description='BYTop a cli dash to show up RAM and CPU stats 🚀')
    parser.add_argument('--config', nargs='?',
                        help='load a custom color config file')
    
    args = parser.parse_args()
    configValue = args.config
    if configValue:
        if path.isfile(configValue):
            with open(configValue, 'r') as file:
                data = json.load(file)
            return data
        else:
            stderr.write(f"ERROR: No such file or directory {configValue}")
            exit()
    else:
        data = {
                "STATUS_TITLE": "\u001b[33m",
                "KERNEL": "\u001b[33m",
                "SYSTEM": "\u001b[36m",
                "UPTIME": "\u001b[31m",
                "CPU_MODEL": "\u001b[35m",
                "PROGRESS_BARS": "\u001b[33m",
                "RAM_TITLE": "\u001b[31m",
                "PERCENTAJE": "\u001b[36m",
                "CPU_TITLE": "\u001b[34m",
                "THREADS": "\u001b[32m"
               }
        return data
