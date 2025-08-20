import requests
import time
import datetime
import asyncio

from config_handler import *

async def send_request(url, method='GET', data=None, headers=None):
    start_time = time.time()
    error_msg = ""
    status_code = None
    try:
        response = await asyncio.to_thread(requests.get, url, headers=headers)
        status_code = response.status_code
        response.raise_for_status()
    except requests.RequestException as e:
        error_msg = str(e)
    end_time = time.time()
    response_time = end_time - start_time
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "response_time": response_time,
        "status_code": status_code,
        "error": error_msg
    }

async def send_requests(url, num_requests, ramp_up_time=0, peak_load=0, method='GET', data=None, headers=None):
    tasks = []
    if peak_load > 0:
        # Spike test: Introduce a sudden increase to peak load
        for i in range(peak_load):
            task = asyncio.create_task(send_request(url, method=method, data=data, headers=headers))
            tasks.append(task)
        await asyncio.sleep(1)  # Hold peak for a second
    elif ramp_up_time > 0:
        # Gradual ramp-up
        sleep_time = ramp_up_time / num_requests
        for i in range(num_requests):
            task = asyncio.create_task(send_request(url, method=method, data=data, headers=headers))
            tasks.append(task)
            await asyncio.sleep(sleep_time)
    else:
        # Constant load
        for i in range(num_requests):
            task = asyncio.create_task(send_request(url, method=method, data=data, headers=headers))
            tasks.append(task)

    return await asyncio.gather(*tasks)

