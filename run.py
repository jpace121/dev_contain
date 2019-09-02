#!/usr/bin/env python3

import argparse
import os
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Run a provided container using podman.")
    parser.add_argument("--container", "-c", help="Name of container to launch.")
    parser.add_argument("--volume", "-v", help="Volume on local machine to mount at same location in container.")
    args = parser.parse_args()

    username = os.environ["USER"]

    container = args.container
    if not args.container:
        container = "jwp-build-latest"
        
    volume = args.volume
    if not args.volume:
        volume = "/home/{}/Develop".format(username)

    command = ('podman run --rm'
               ' --workdir /home/{username}'
               ' --user {username}'
               ' --userns=keep-id'
               ' --volume {volume}:{volume}:Z'
               ' -it {container} bash').format(username=username, container=container, volume=volume)
    
    print('Running: {}'.format(command))
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    main()
    
