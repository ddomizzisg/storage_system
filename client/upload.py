import requests
import time
from utils import randbytes
from typing import NamedTuple
import statistics
import logging
from pslogging import init_logging
from pslogging import TESTING_LOG_LEVEL
from pscsv import CSVLogger
import sys

logger = logging.getLogger('remote-ops')

class RunStats(NamedTuple):
    """Stats for a given run configuration."""

    payload_size_bytes: int | None
    total_time_ms: float
    avg_time_ms: float
    min_time_ms: float
    max_time_ms: float
    stdev_time_ms: float
    avg_bandwidth_mbps: float | None

def upload_file( url, payload_size=1000000):
    times_ms = []

    file_path = '%d' % payload_size 
    data = randbytes(payload_size)

    with open(file_path, 'wb') as file:
        file.write(data)

    #time.sleep(5)

    with open(file_path, 'rb') as file:
        print(file)
        for i in range(10):
            start = time.perf_counter_ns()
            response = requests.post(url, files={'file': data}, data={'name': file_path})
            print(response.text)
            if response.status_code == 200:
                print("File uploaded successfully!")
            else:
                print("File upload failed.")
            end = time.perf_counter_ns()
            times_ms.append((end - start) / 1e6)
        
    avg_time_s = sum(times_ms) / 1000 / len(times_ms)
    payload_mb = payload_size / 1e6
    avg_bandwidth_mbps = payload_mb / avg_time_s
    print(avg_time_s,payload_mb,avg_bandwidth_mbps)

    return RunStats(
        payload_size_bytes=payload_size,
        total_time_ms=sum(times_ms),
        avg_time_ms=sum(times_ms) / len(times_ms),
        min_time_ms=min(times_ms),
        max_time_ms=max(times_ms),
        stdev_time_ms=(
            statistics.stdev(times_ms) if len(times_ms) > 1 else 0.0
        ),
        avg_bandwidth_mbps=avg_bandwidth_mbps,
    )

# Example usage
payload_size = int(sys.argv[1])
file_path = 'test.txt'
url = 'http://3.227.249.11:20006/set.php?file=%s' % file_path  # Replace with the PHP service URL
run_stats = upload_file(url, payload_size=payload_size)
logger.log(TESTING_LOG_LEVEL, run_stats)

csv_logger = CSVLogger("results_upload.csv", RunStats)
csv_logger.log(run_stats)
csv_logger.close()