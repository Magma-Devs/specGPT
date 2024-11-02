import subprocess
from functools import lru_cache

# Cache dictionary to store successful grpcurl descriptions by URL
cache = {}

def run_grpcurl(url: str) -> str:
    """
    Runs the grpcurl command to describe a gRPC service at the provided URL.
    Tries with -plaintext first, then without it if that fails.
    Caches successful results using the URL as the key.

    :param url: The gRPC server URL to describe.
    :return: The description output from grpcurl.
    :raises RuntimeError: If grpcurl fails with both attempts.
    """
    # Return the cached result if it exists
    if url in cache:
        return cache[url]
    
    # Define the commands to try
    commands = [
        ["grpcurl", "-plaintext", url, "describe"],
        ["grpcurl", url, "describe"]
    ]
    
    # Try each command until one succeeds
    for command in commands:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        
        # If the command succeeds, cache and return the output
        if process.returncode == 0:
            cache[url] = stdout  # Cache the successful response
            return stdout

    # If both commands fail, raise an error without caching
    raise RuntimeError(f"grpcurl error: {stderr}")
