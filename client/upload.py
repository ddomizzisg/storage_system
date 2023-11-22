import requests
import time
from utils import randbytes

def upload_file( url, payload_size=1000000):
    times_ms = []

    file_path = '%d' % payload_size 
    data = randbytes(payload_size)

    with open(file_path, 'wb') as file:
        file.write(data)

    with open(file_path, 'rb') as file:
        for i in range(10):
            start = time.perf_counter_ns()
            response = requests.post(url, files={'file': file})
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

# Example usage
file_path = 'test.txt'
url = 'http://localhost:20006/set.php?file=%s' % file_path  # Replace with the PHP service URL
upload_file(url, payload_size=100000000)
