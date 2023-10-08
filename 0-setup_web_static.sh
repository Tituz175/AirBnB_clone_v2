#!/usr/bin/env bash
# This Bash script that sets up your web servers for the deployment of web_static

# check for nginx installed
if ! nginx -v; then
apt-get update
apt-get install -y nginx
fi

# create the need folders
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

# dummy html content
html="<html>
    <head>
    </head>
    <body>
        Holberton School
    </body>
</html>"

# appending into the index.html file
echo "$html" | sudo tee /data/web_static/releases/test/index.html

# creating a symbolic link
if  ls /data/web_static/current;
then
    sudo rm -r /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test /data/web_static/current

# setting the ownership
sudo chown -R ubuntu:ubuntu /data

# modifing the nginx config file
sudo service nginx start

hbnb_alias_link="server_name _;\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}"
sudo sed -i "s|server_name _;|$hbnb_alias_link|" /etc/nginx/sites-enabled/default

sudo service nginx restart
