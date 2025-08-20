from benchmark import send_requests
import asyncio

async def run_constant_load_test(url, num_requests=100, method='GET', data=None):
    """Simulates a constant load on the server."""
    return await send_requests(url, num_requests, ramp_up_time=0, method=method, data=data)

async def run_ramp_up_test(url, num_requests=200, ramp_up_time=60, method='GET', data=None):
    """Gradually increases the load on the server over a specified ramp-up time."""
    return await send_requests(url, num_requests, ramp_up_time=ramp_up_time, method=method, data=data)

async def run_spike_test(url, peak_load, num_spikes=10, rest_period=5, method='GET', data=None):
    """Creates sudden spikes in load followed by rest periods."""
    results = []
    for _ in range(num_spikes):
        partial_results = await send_requests(url, peak_load, ramp_up_time=0, method=method, data=data)
        results.extend(partial_results)
        await asyncio.sleep(rest_period)  # Wait for a specified rest period between spikes
    return results

async def run_stress_test(url, start_requests=50, max_requests=500, step=50, threshold_errors=20, method='GET', data=None):
    """Increases load until server fails consistently or reaches max_requests."""
    current_load = start_requests
    results = []
    error_count = 0
    while current_load <= max_requests and error_count < threshold_errors:
        partial_results = await send_requests(url, current_load, method=method, data=data)
        results.extend(partial_results)
        error_count += sum(1 for res in partial_results if res['status_code'] >= 400)
        if error_count >= threshold_errors:
            print("Aborting test due to high error rate")
            break
        current_load += step
    return results
