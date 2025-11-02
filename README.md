# DataHive API Monitor (DWYOR)

An automated tool to interact with DataHive's API system for collecting Hive Points and Data Points through job processing.

## Features

- Automatic job retrieval and submission
- Continuous uptime monitoring
- Random Android User-Agent generation
- Persistent device identification
- Configurable delays for optimal performance
- Color-coded console output
- Auth token management via external file

## Requirements

- Python 3.7+
- Required Python packages:
  - requests
  - aiohttp
  - urllib3
  - py-cpuinfo
  - fake-useragent
  - colorama
- DataHive account

## Getting Started

### Obtaining Auth Token

1. Go to [DataHive Dashboard](https://dashboard.datahive.ai/)
2. Login to your account
3. Open Developer Tools (F12 or Ctrl+Shift+I)
4. Go to Network tab
5. Filter requests by "Fetch/XHR"
6. Refresh the page
7. Look for "user" request
8. In the request headers, find the "authorization" header
9. Copy the token value (without "Bearer" prefix)
10. Save this token in `auth.txt`

### Installation

1. Clone the repository:
```bash
git https://github.com/monteksz/datahive
cd datahive
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create `auth.txt` file and paste your auth token:
```bash
echo "your_copied_token_here" > auth.txt
```

## Usage

Run the script:
```bash
python main.py
```

The program will:
- Generate a random Android User-Agent
- Attempt to retrieve jobs from DataHive
- Submit completed jobs automatically
- Maintain uptime monitoring

## Configuration

- `job_delay`: Time between successful job submissions (default: 2 seconds)
- `regular_delay`: Time between regular API calls (default: 5 seconds)
- `retries`: Number of job retrieval attempts per cycle (default: 3)

## Output Format

```
Starting DataHive API Monitor...
Using User-Agent: Mozilla/5.0 (Linux; Android 13; Pixel 6)...

Request Cycle #1
--------------------------------------------------
[HH:MM:SS] Job API                    | Status: Job received: {job_id}
[HH:MM:SS] Job Submit                 | Status: Success
--------------------------------------------------
Waiting for next cycle...
```

## Features Explained

- **Job Processing**: Automatically retrieves and submits jobs
- **Uptime Monitoring**: Maintains connection with DataHive servers
- **Device Simulation**: Emulates Android device characteristics
- **Error Handling**: Robust error handling and retry mechanism
- **Console Output**: Clear, color-coded status messages

## Security Note

- Never share your auth token
- Regenerate token if compromised

## Error Handling

The script handles various error scenarios:
- Missing auth.txt file
- Network connectivity issues
- Invalid API responses
- Job submission failures
- Invalid auth tokens

## Contribution

Feel free to fork this repository and submit pull requests for any improvements.

## Disclaimer

This tool is for educational purposes only.
