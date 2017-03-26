#!/usr/bin/env python3

import os
import argparse


CONTAINER_NAME = 'pyar'


parser = argparse.ArgumentParser(
    prog='webcmd',
    description='Helper to start a Pyarweb development instance.')

parser.add_argument(
    '--build-image',
    action='store_true',
    help='Build PyAr web docker image')

parser.add_argument(
    '--run-container',
    action='store_true',
    help='Build PyAr web docker image')

parser.add_argument(
    '--del-container',
    action='store_true',
    help='Removes PyAr web container')

parser.add_argument(
    '--shell',
    action='store_true',
    help='Exec a bash interpreter on a running container')


def build():
    """Run docker build, then docker run."""
    curdir = os.path.abspath(os.path.curdir)
    dockerfile = os.path.join(curdir, 'Dockerfile')
    assert os.path.isfile(dockerfile), "{} file not found.".format(dockerfile)

    cmd = "docker build -t pyarweb/django ."
    os.system(cmd)


def run():
    """Run docker run to create a container from pyarweb/django image."""
    curdir = os.path.abspath(os.path.curdir)
    dockerfile = os.path.join(curdir, 'Dockerfile')
    assert os.path.isfile(dockerfile), "{} file not found.".format(dockerfile)

    cmd = "docker run -it -v {}:/opt/code -p 8000:8000 --name {} pyarweb/django".format(
        curdir, CONTAINER_NAME)
    os.system(cmd)


def delete_container():
    """Removes PyAr ."""
    cmd = "docker rm {}".format(CONTAINER_NAME)
    os.system(cmd)


def shell():
    """Get a bash shell in docker container."""
    cmd = "docker exec -it {} /bin/bash".format(CONTAINER_NAME)
    os.system(cmd)


args = parser.parse_args()
if args.build_image:
    build()
elif args.run_container:
    run()
elif args.shell:
    shell()
elif args.del_container:
    delete_container()
