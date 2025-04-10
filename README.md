# Top-Workplaces Monitor

This project implements a script to monitor the health of various endpoints based on a YAML configuration file. The script checks each endpoint's availability and tracks performance metrics (availability percentage per domain). An endpoint is considered "UP" only if it responds with a 2xx status code **and** the response time is under 500 milliseconds.

## Features

- YAML Configuration: Load endpoints from a YAML file.
- Health Check: Verifies endpoint status by evaluating both HTTP response code and response time.
- Domain-Based Aggregation: Aggregates stats per domain and logs cumulative availability percentages.
- Automated Cycling: Continuously runs checks on a 15-second interval.

## Setup and Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/fetch-the-most-active-workplaces-yourfork.git