import urllib.request

file = "test.txt"

# URL of the file to download
url = "http://localhost:20006/c/%s" % file

print(url)

# Destination path to save the downloaded file
destination_path = file

# Download the file
urllib.request.urlretrieve(url, destination_path)
