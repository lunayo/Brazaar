#!/bin/bash -ex
# logging
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
echo BEGIN
date '+%Y-%m-%d %H:%M:%S'
echo END

#initialise the application server in the background
python /home/ec2-user/Server/Brazaar/notification.py