import threading
import requests
import json
import time
import os
from concurrent.futures import ThreadPoolExecutor

# Create a lock for thread-safe writing
lock = threading.Lock()

# This function fetches post from source individually and appends in json file
def fetch_and_write_post(post_id):
    # Getting data
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    response = requests.get(url)

    if response.status_code == 200:
        post = response.json()
        # Writing data with lock
        with lock:
            with open("data.json", "a") as json_file:
                json.dump(post, json_file, indent=4)
                json_file.write(",\n")
    else:
        print(f"Failed to fetch post {post_id}")

start_time = time.perf_counter()

# Writing first line for json structure
with open("data.json", "w") as f:
    f.write("[\n")

# Method 1 for creating threads using threading module
# threads = []
#
# # Starting threads
# for i in range(1, 78):
#     thread = threading.Thread(target=fetch_and_write_post, args=(i))
#     threads.append(thread)
#     thread.start()
#
# # Join threads to main thread
# for thread in threads:
#     thread.join()

# Method 2 for creating threads using concurrent module
with ThreadPoolExecutor() as executor:
    executor.map(fetch_and_write_post, range(1, 78))

# This step removes last trailing comma from json file
with open("data.json", 'rb+') as f:
    f.seek(-2, os.SEEK_END)
    f.truncate()

# Finish writing json file structure
with open("data.json", "a") as f:
    f.write("\n]")

end_time = time.perf_counter()

# Print taken time for my task
print(f"Time Elapsed: {end_time - start_time:.2f} seconds")