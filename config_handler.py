import csv
import json
import logging
import argparse

def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Web Server Benchmark")
    parser.add_argument("--config", default="config.json", help="Path to configuration file")
    return parser.parse_args()

def write_results_to_csv(results, filename='response_data.csv'):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['timestamp', 'response_time', 'status_code', 'error']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)