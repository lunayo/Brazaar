#!/bin/bash -ex
# logging
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
echo BEGIN
date '+%Y-%m-%d %H:%M:%S'
echo END

#initialise and edit the crontab settings
# run every 1 minute
(/usr/bin/crontab -l 2>/dev/null; echo "*/1 * * * * /home/ec2-user/Server/Brazaar/haproxy_autoscale/update-haproxy.sh") | /usr/bin/crontab -

# start the cron process if it is not initialised
/etc/init.d/crond restart

# start the haproxy process
/usr/sbin/haproxy -f "/home/ec2-user/Server/Brazaar/haproxy_autoscale/gateway.cfg"