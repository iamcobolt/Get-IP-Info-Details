# IP Information Fetcher

This script reads a list of IP addresses and IP ranges from a file, fetches detailed information about each IP using the IPinfo API, and writes the results to a CSV file.

## Prerequisites

- Python 3.x
- `requests` library
- `python-dotenv` library

You can install the required libraries using pip:
sh
pip install requests python-dotenv


## Setup

1. **Environment Variables**: Create a `.env` file in the same directory as the script and add your IPinfo API token:

   ```
   IPINFO_API_TOKEN=your_api_token_here
   ```

2. **Input File**: Prepare a file named `ips_and_ranges.txt` in the same directory. This file should contain IP addresses and/or IP ranges, one per line. For example:

   ```
   192.168.1.1
   192.168.1.10 - 192.168.1.20
   192.168.2.0/24
   ```

## Usage

Run the script using Python:
sh
python main.py


## Output

The script will create or append to a file named `ip_details.csv` in the same directory, containing the following columns for each IP:

- IP Address
- Hostname
- City
- Region
- Country
- Location (latitude and longitude)
- Organization
- Postal Code
- Timezone

## Notes

- Ensure your IPinfo API token is valid and has sufficient permissions to fetch the required data.
- The script loads the environment variables for each IP request, which might be optimized by loading them once at the start.
