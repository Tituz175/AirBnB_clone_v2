# server configuration via puppet

$dummyhtml = '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>'

exec { 'Install and configure nginx':
  command  => 'sudo apt-get update -y &&
               sudo apt-get install nginx -y &&
               sudo mkdir -p /data/web_static/releases/test/ &&
               sudo mkdir -p /data/web_static/shared/ &&
               sudo echo $dummyhtml > /data/web_static/releases/test/index.html &&
               sudo ln -sf /data/web_static/releases/test/ /data/web_static/current && 
               sudo chown -R ubuntu:ubuntu /data/ &&
               sudo service nginx start &&
               hbnb_alias_link="server_name _;\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}" && 
               sudo sed -i "s|server_name _;|$hbnb_alias_link|" /etc/nginx/sites-enabled/default &&
               sudo service nginx restart',
  provider => 'shell',
}