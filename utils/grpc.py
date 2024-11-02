import subprocess

def run_grpcurl(url: str) -> str:
    """
    Runs the grpcurl command to describe a gRPC service at the provided URL.
    Tries with -plaintext first, then without it if that fails.

    :param url: The gRPC server URL to describe.
    :return: The description output from grpcurl.
    :raises RuntimeError: If grpcurl fails with both attempts.
    """
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
        
        # Return output if the command succeeds
        if process.returncode == 0:
            return stdout

    # If both commands fail, raise an error
    raise RuntimeError(f"grpcurl error: {stderr}")
