import yaml
import requests
import time
from collections import defaultdict
import math

# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to perform health checks and measure response time
def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET')
    headers = endpoint.get('headers', {})
    body = endpoint.get('body', None)

    # Record start time
    start_time = time.time()

    try:
        # Using requests.request with a timeout for safety
        response = requests.request(method, url, headers=headers, json=body, timeout=1)
        # Calculate elapsed time in milliseconds
        elapsed_time = (time.time() - start_time) * 1000

        # Check if status is 2xx and response time is within 500 ms
        if 200 <= response.status_code < 300 and elapsed_time < 500:
            return "UP", elapsed_time
        else:
            return "DOWN", elapsed_time
    except requests.RequestException:
        elapsed_time = (time.time() - start_time) * 1000
        return "DOWN", elapsed_time

# Main function to monitor endpoints continuously
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    # Prepare the stats buckets for each endpoint's domain
    for endpoint in config:
        domain = endpoint["url"].split("//")[-1].split("/")[0]
        if domain not in domain_stats:
            domain_stats[domain] = {"up": 0, "total": 0}

    # Continuously monitor all endpoints in a loop
    while True:
        for endpoint in config:
            domain = endpoint["url"].split("//")[-1].split("/")[0]
            result, elapsed = check_health(endpoint)
            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1
            # Optionally, you can print the individual endpoint result details:
            # print(f"Checked {domain}: Status {result}, Response Time: {elapsed:.2f}ms")

        # Log cumulative availability percentages for each domain
        for domain, stats in domain_stats.items():
            availability = round(100 * stats["up"] / stats["total"])
            print(f"{domain} has {availability}% availability percentage")
        print("---")
        time.sleep(15)

# Entry point of the program
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python main.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")