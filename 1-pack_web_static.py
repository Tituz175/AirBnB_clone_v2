#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo, using the function do_pack.

Return: archive path if the archive has been correctly generated
        else None.
"""
from fabric.api import local, env, task
from datetime import datetime

env.hosts = ['localhost']

@task
def do_pack():
    """Create a .tgz archive from the contents of the web_static folder."""

    # Get the current timestamp for the archive name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Define the archive name
    archive_name = "web_static_{}.tgz".format(timestamp)

    # Define the archive path
    archive_path = "versions/{}".format(archive_name)

    # Create the versions folder if it doesn't exist
    local("mkdir -p versions")

    # Compress the contents of the web_static folder into the archive
    result = local("tar -cvzf {} web_static".format(archive_path))

    # Check if the archive was created successfully
    if result.succeeded:
        return archive_path
    else:
        return None
