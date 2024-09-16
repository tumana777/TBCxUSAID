import aiohttp
import asyncio
import json
import time

# This function fetches post from the source individually and appends it in the json file
async def fetch_and_write_post(session, post_id, first_post_lock):
    # Getting data
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    async with session.get(url) as response:
        if response.status == 200:
            post = await response.json()

            async with first_post_lock:
                with open("data.json", "a") as json_file:
                    # Add a comma before the post if it's not the first one
                    if json_file.tell() > 2:  # If the file already contains data (after opening '[')
                        json_file.write(",\n")
                    json.dump(post, json_file, indent=4)
        else:
            print(f"Failed to fetch post {post_id}")

async def main():
    start_time = time.perf_counter()

    # A lock to control the first post logic
    first_post_lock = asyncio.Lock()

    # Writing the first line for JSON structure
    with open("data.json", "w") as f:
        f.write("[\n")

    async with aiohttp.ClientSession() as session:
        # Creating tasks to fetch posts asynchronously
        tasks = [fetch_and_write_post(session, post_id, first_post_lock) for post_id in range(1, 78)]
        await asyncio.gather(*tasks)

    # Finish writing JSON structure
    with open("data.json", "a") as f:
        f.write("\n]")

    end_time = time.perf_counter()

    # Print the time taken for the task
    print(f"Time Elapsed: {end_time - start_time:.2f} seconds")

# Run the main coroutine
asyncio.run(main())