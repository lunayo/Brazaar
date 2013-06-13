#!/bin/bash -ex
# logging
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
echo BEGIN
date '+%Y-%m-%d %H:%M:%S'
echo END

#initialise the application server and database in background
mongod --fork --logpath="/log/mongod.log"
nohup python /Users/ec2-user/Server/Brazaar/product.py &

# update the haproxy for every 1 minute
cd ../haproxy/
python update-haproxy.py --access-key="AKIAICFC5TP7NVT6MK4A" --secret-key="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" --security-group="default" --region="eu-west-1"  --output gateway.cfg