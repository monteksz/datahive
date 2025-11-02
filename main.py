import requests
import aiohttp
import asyncio
import urllib3
from http.client import HTTPSConnection
import json
import platform
import os
import uuid
import cpuinfo
import random
from fake_useragent import UserAgent
from colorama import init, Fore, Style
from datetime import datetime

# Initialize colorama
init(autoreset=True)

def read_auth_token():
    try:
        with open('auth.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"{Fore.RED}Error: auth.txt file not found!")
        exit(1)
    except Exception as e:
        print(f"{Fore.RED}Error reading auth.txt: {str(e)}")
        exit(1)

class ResourceManager:
    def __init__(self):
        self.ua = UserAgent()
        self.user_agent = self._get_android_user_agent()
        self.cpu_info = self._get_cpu_info()
        self.device_id = self._get_device_id()
        self.app_version = "0.2.30"
        self.auth_token = read_auth_token()
        self.headers = self._create_headers()
        self.session = None
        self.http_pool = urllib3.PoolManager()

    def _get_android_user_agent(self):
        android_versions = ['10', '11', '12', '13']
        devices = [
            'SM-A525F', 'SM-G998B', 'Pixel 6', 'Pixel 7',
            'OnePlus 9', 'Redmi Note 10', 'POCO X3', 'MI 11'
        ]
        chrome_versions = ['110.0.0.0', '111.0.0.0', '112.0.0.0', '113.0.0.0']
        
        device = random.choice(devices)
        android_ver = random.choice(android_versions)
        chrome_ver = random.choice(chrome_versions)
        
        return f'Mozilla/5.0 (Linux; Android {android_ver}; {device}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Mobile Safari/537.36'

    def _get_cpu_info(self):
        try:
            info = cpuinfo.get_cpu_info()
            return {
                'architecture': 'arm64-v8a',
                'model': 'Qualcomm Snapdragon',
                'count': 8
            }
        except:
            return {
                'architecture': 'arm64-v8a',
                'model': 'Unknown',
                'count': 8
            }

    def _get_device_id(self):
        return f"DH-{str(uuid.getnode())}"

    def _create_headers(self):
        return {
            'authority': 'api.datahive.ai',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': f'Bearer {self.auth_token}',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Chromium";v="112"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'none',
            'sec-fetch-storage-access': 'active',
            'user-agent': self.user_agent,
            'x-app-version': self.app_version,
            'x-cpu-architecture': self.cpu_info['architecture'],
            'x-cpu-model': self.cpu_info['model'],
            'x-cpu-processor-count': str(self.cpu_info['count']),
            'x-device-id': self.device_id,
            'x-device-os': 'Android 13',
            'x-device-type': 'android',
            'x-s': 'f',
            'x-user-agent': self.user_agent,
            'x-user-language': 'en-US'
        }

def print_response(title, data, color):
    now = datetime.now().strftime("%H:%M:%S")
    if isinstance(data, str):
        status = data
    else:
        status = data.get('error', data.get('status', 'Success'))
    status_color = Fore.RED if 'error' in str(status) else Fore.GREEN
    print(f"{color}[{now}] {title:<25} | Status: {status_color}{status}")

async def get_job(session, headers):
    try:
        retries = 3
        for attempt in range(retries):
            async with session.get('https://api.datahive.ai/api/job', headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if data and 'id' in data:
                        print_response("Job API", {"status": f"Job received: {data['id']}"}, Fore.BLUE)
                        return data
                    if attempt < retries - 1:
                        await asyncio.sleep(0.5)
        print_response("Job API", {"status": "No job available"}, Fore.YELLOW)
        return None
    except Exception as e:
        print(f"{Fore.RED}Job API Error: {str(e)}")
        return None

async def submit_job(session, headers, job_data):
    try:
        job_id = job_data['id']
        timestamp = int(datetime.now().timestamp())
        
        payload = {
            "executionContext": {},
            "status": "completed",
            "result": {
                "success": True,
                "data": {},
                "error": None,
                "timestamp": timestamp
            },
            "metadata": {
                "timestamp": timestamp,
                "source": "android",
                "device": "mobile"
            },
            "children": []
        }

        submit_headers = headers.copy()
        submit_headers['content-type'] = 'application/json'

        async with session.post(
            f'https://api.datahive.ai/api/job/{job_id}',
            headers=submit_headers,
            json=payload
        ) as response:
            if response.status == 200:
                data = await response.json()
                print_response("Job Submit", {"status": "Success"}, Fore.MAGENTA)
                return True
            else:
                error_text = await response.text()
                print_response("Job Submit", f"Failed with status {response.status}: {error_text}", Fore.RED)
                return False
    except Exception as e:
        print(f"{Fore.RED}Job Submit Error: {str(e)}")
        return False

async def get_worker_requests(session, headers):
    try:
        async with session.get('https://api.datahive.ai/api/worker', headers=headers) as response:
            data = await response.json()
            print_response("Worker API (requests)", data, Fore.CYAN)
    except Exception as e:
        print(f"{Fore.RED}Worker API Error: {str(e)}")

async def get_uptime_aiohttp(session, headers):
    try:
        async with session.get('https://api.datahive.ai/api/ping/uptime', headers=headers) as response:
            data = await response.json()
            print_response("Uptime API (aiohttp)", data, Fore.GREEN)
    except Exception as e:
        print(f"{Fore.RED}Uptime API Error: {str(e)}")

async def get_worker_ip_aiohttp(session, headers):
    try:
        async with session.get('https://api.datahive.ai/api/network/worker-ip', headers=headers) as response:
            data = await response.json()
            print_response("Worker IP API", data, Fore.YELLOW)
    except Exception as e:
        print(f"{Fore.RED}Worker IP API Error: {str(e)}")

async def main():
    resources = ResourceManager()
    job_delay = 2  
    regular_delay = 5 
    
    try:
        print(f"{Fore.CYAN}{Style.BRIGHT}Starting DataHive API Monitor...")
        print(f"{Fore.CYAN}Using User-Agent: {resources.user_agent}\n")
        count = 1

        async with aiohttp.ClientSession() as session:
            while True:
                print(f"{Fore.WHITE}{Style.BRIGHT}Request Cycle #{count}")
                print(f"{Style.BRIGHT}{'-' * 50}")

                job = await get_job(session, resources.headers)
                if job and 'id' in job:
                    success = await submit_job(session, resources.headers, job)
                    await asyncio.sleep(job_delay if success else regular_delay)
                else:
                    await asyncio.gather(
                        get_worker_requests(session, resources.headers),
                        get_uptime_aiohttp(session, resources.headers),
                        get_worker_ip_aiohttp(session, resources.headers)
                    )
                    await asyncio.sleep(regular_delay)

                print(f"{Style.BRIGHT}{'-' * 50}")
                print(f"{Fore.WHITE}Waiting for next cycle...\n")
                count += 1

    except KeyboardInterrupt:
        print(f"{Fore.RED}{Style.BRIGHT}\nProgram stopped by user")
    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}Main loop error: {str(e)}")

if __name__ == "__main__":
    os.system("pip install colorama fake-useragent py-cpuinfo requests aiohttp urllib3")
    asyncio.run(main())
