#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy

Return: False if the file at the path archive_path does not exist
        True if all operations have been done correctly
        otherwise returns False
"""

from fabric.api import local, env, task, run, put, runs_once
from datetime import datetime
import os

env.hosts = ["35.175.126.167", "18.206.197.223"]


@runs_once
def do_pack():
    """Create a .tgz archive from the contents of the web_static folder."""

    # Get the current timestamp for the archive name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Define the archive name
    archive_name = f"web_static_{timestamp}.tgz"

    # Define the archive path
    archive_path = f"versions/{archive_name}"

    # Create the versions folder if it doesn't exist
    local("mkdir -p versions")

    # Compress the contents of the web_static folder into the archive
    result = local(f"tar -cvzf {archive_path} web_static")

    # Check if the archive was created successfully
    if result.succeeded:
        return archive_path
    else:
        return None


@task
def do_deploy(archive_path):
    """Deploy archive file to server and serve it to the respective folder."""

    try:
        if not os.path.exists(archive_path):
            return False
        fileNameExt = os.path.basename(archive_path)
        filename, _ = os.path.splitext(fileNameExt)
        folderPath = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run("rm -fr {}{}".format(folderPath, filename))
        run("mkdir -p {}{}/".format(folderPath, filename))
        run("tar -xzf /tmp/{} -C {}{}/".format(fileNameExt, folderPath, filename))
        run("rm -rf /tmp/{}".format(fileNameExt))
        run("mv {0}{1}/web_static/* {0}{1}/".format(folderPath, filename))
        run("rm -rf /data/web_static/current")
        run("rm -rf {}{}/web_static".format(folderPath, filename))
        run("ln -s {}{}/ /data/web_static/current".format(folderPath, filename))
        print("New version deployed!")
        return True
    except Exception:
        return False


@task
def deploy():
    archive_path = do_pack()
    if archive_path:
        return do_deploy(archive_path)
    else:
        return False
