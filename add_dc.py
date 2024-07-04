import sys
import socket
import requests
import subprocess

def execute_bash_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout, result.stderr

def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def get_external_ip():
    response = requests.get('https://api.ipify.org?format=json')
    ip_address = response.json()['ip']
    return ip_address

base_dc = "  datacontainer%d:\n    image: dynostore/datacontainer:v1\n    ports:\n      - \"%d:5000\"\n    volumes:\n      - ./datacontainer/objects%d/:/data/objects:rw\n      - ./datacontainer/code:/app\n    environment:\n      APIGATEWAY_HOST: 129.114.26.127:8095\n      AUTH_HOST: 129.114.26.127:8090"

start_container = int(sys.argv[1])
start_port = int(sys.argv[2])
n_containers = int(sys.argv[3])

f = open("docker-compose-varying-dc.yml", "w")
f.write("services:\n")
for i in range(start_container, n_containers + 1):
    dc = base_dc % (i, start_port + i - 1, i)
    f.write(dc + "\n")
    
f.close()

stdout, stderr = execute_bash_command("docker compose -f docker-compose-varying-dc.yml up -d")

if stdout:
    print("Standard Output:")
    print(stdout)

if stderr:
    print("Standard Error:")
    print(stderr)

base_cmd = "sudo docker compose -f docker-compose-varying-dc.yml exec datacontainer2 python3 regist_on_metadata.py 322eda4b1d1da49d141ee00b8f1279f9b8af3f9266d27923fa8797fd64f75655 http://%s:%d/ -m 1000000000 -s 75000000000"

ip = get_external_ip()

for i in range(start_container, n_containers + 1):
    cmd = base_cmd % (ip, start_port + i - 1)
    print(cmd)
    stdout, stderr = execute_bash_command(cmd)
    
    if stdout:
        print("Standard Output:")
        print(stdout)
    
    if stderr:
        print("Standard Error:")
        print(stderr)