#!/usr/bin/env python3
#
# Copyright 2019 James Pace
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
import sys
import subprocess
import dev_contain.common as common

def run(in_args):
    parser = argparse.ArgumentParser(prog=sys.argv[0]+' run', description='Run a provided container.')
    parser.add_argument('--image', '-i', help='Name of image to launch.')
    parser.add_argument('--container', '-c', help='Name of the new container.')
    parser.add_argument('--volume', '-v', action='append', help='Volume on local machine to mount at same location in container.')
    parser.add_argument('--workdir', '-d', help='Directory to start in.')
    parser.add_argument('--user', '-u', help='Username to login into container as.')
    parser.add_argument('--graphics', '-X', action='store_true', help='Forward graphics.')
    args = parser.parse_args(in_args)

    manager = common.get_manager()

    username = args.user
    if not args.user:
        username = os.environ['USER']

    image = args.image
    if not args.image:
        image = 'jwp-build-latest'

    volumes = args.volume
    if not args.volume:
        volumes = ['/home/{}/Develop'.format(username)]

    container = args.container
    if not args.container:
        container = 'dev'

    workdir = args.workdir
    if not workdir:
        workdir = '/home/{}'.format(username)

    graphics_text = ''
    if args.graphics:
        graphics_text = set_up_graphics_forwards()

    # podman needs userns set to keep-id for volumes to work.
    userns_text = ''
    if manager == 'podman':
        userns_text = '--userns=keep-id'

    # Include volume for ssh keys if it exists.
    ssh_text = ''
    if os.path.exists('/home/{}/.ssh'.format(username)):
        ssh_text = '--volume /home/{}/.ssh:/home/{}/.ssh:Z'.format(username, username)

    volume_text = ''
    for volume in volumes:
        volume_text = volume_text + ' --volume {volume}:{volume}:Z'.format(volume=volume)

    command = ('{manager} run -d'
               ' --user {username}'
               ' --name {container}'
               ' {userns_text}'
               ' --workdir {workdir}'
               ' --ipc=host'
               ' --net=host'
               ' -e DEV_CONTAIN_CONTAINER_NAME={container}'
               ' {volume_text}'
               ' {ssh_text} {graphics_text}'
               ' {image}').format(
                       manager=manager,
                       username=username,
                       image=image,
                       volume_text=volume_text,
                       ssh_text=ssh_text,
                       graphics_text=graphics_text,
                       container=container,
                       workdir=workdir,
                       userns_text=userns_text)
    print('Running: {}'.format(command))
    subprocess.run(command, shell=True)

def set_up_graphics_forwards():
    # XOrg
    xorg = (' -e DISPLAY=$DISPLAY'
            ' -v /tmp/.X11-unix:/tmp/.X11-unix:rw')
    # Wayland
    wayland = (' -e XDG_RUNTIME_DIR=/tmp'
               ' -e WAYLAND_DISPLAY=$WAYLAND_DISPLAY'
               ' -v $XDG_RUNTIME_DIR/$WAYLAND_DISPLAY:/tmp/$WAYLAND_DISPLAY')
    # (User) dbus socket.
    dbus = ''
    # What kind of socket is it?
    dbus_address = os.environ.get('DBUS_SESSION_BUS_ADDRESS')
    # If a real path, need to mount it. Otherwise --net=host takes care of it.
    if 'unix:path' in dbus_address:
        dbus_path = dbus_address.split('=')[1]
        dbus = dbus + '--volume {path}:{path}'.format(path=dbus_path)
    # Regardless need to know where to look.
    dbus = dbus + ' --env DBUS_SESSION_BUS_ADDRESS="$DBUS_SESSION_BUS_ADDRESS"'

    return xorg + ' ' + wayland + ' ' + dbus


if __name__ == '__main__':
    run(sys.argv[1:])
