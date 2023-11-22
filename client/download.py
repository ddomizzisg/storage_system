import urllib.request
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

def download_file(file, url):
    times_ms = []
    for i in range(10):
        start = time.perf_counter_ns()
        destination_path = "downloads/" + file
        urllib.request.urlretrieve(url, destination_path)
        end = time.perf_counter_ns()
        times_ms.append((end - start) / 1e6)

    payload_size = int(file)
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

payload_size = sys.argv[1]

# URL of the file to download
url = "http://54.85.1.57:20006/c/%s" % payload_size

print(url)

run_stats = download_file(payload_size, url)

logger.log(TESTING_LOG_LEVEL, run_stats)

csv_logger = CSVLogger("results_download.csv", RunStats)
csv_logger.log(run_stats)
csv_logger.close()