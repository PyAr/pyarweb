#!/usr/bin/env python3

import os
import shlex
import argparse
import subprocess


parser = argparse.ArgumentParser(
    prog='webcmd',
    description='Helper to start a Pyarweb development instance.')

parser.add_argument(
    '--docker-run',
    action='store_true',
    help='Run command: docker run -it -v ...')


def check_dockerfile():
    """Check if Dockerfile exists in current path """
    curdir = os.path.abspath(os.path.curdir)
    dockerfile = os.path.join(curdir, 'Dockerfile')
    assert os.path.isfile(dockerfile), "{} file not found.".format(dockerfile)


def docker_run():
    """Run docker build, then docker run."""
    check_dockerfile()
    cmd = "docker build -t pyarweb/django ."
    subprocess.run(shlex.split(cmd))
    cmd = "docker run -it -v {}:/opt/code -p 8000:8000 --name pyar pyarweb/django".format(curdir)
    completed_process = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stderr = completed_process.stderr
    if bytes('Conflict. The name "/pyar" is already in use by container', 'utf-8') in stderr:
        # Lets try again a second time, in a very,... slowly,... dirty,... way
        # Remove docker container
        cmd = "docker rm pyar"
        subprocess.run(shlex.split(cmd))
        # Try again
        cmd = "docker run -it -v {}:/opt/code -p 8000:8000 --name pyar pyarweb/django".format(curdir)
        print(cmd)
        # This time, if it fails, drop to the terminal showing the error
        subprocess.run(shlex.split(cmd))


def docker_shell():
    """Get a bash shell in docker container."""
    cmd = "docker exec -it pyar /bin/bash"
    subprocess.run(shlex.split(cmd))


args = parser.parse_args()
if args.docker_run:
    docker_run()
