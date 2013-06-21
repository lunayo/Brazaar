#!/bin/sh
# update the haproxy for every 1 minute

# windows
PATH=/usr/bin:/usr/sbin:.:/usr/local/sbin
python /home/ec2-user/Server/Brazaar/haproxy_autoscale/update-haproxy.py --haproxy="/usr/sbin/haproxy" --template="/home/ec2-user/Server/Brazaar/haproxy_autoscale/templates/haproxy.tpl" --access-key="AKIAICFC5TP7NVT6MK4A" --secret-key="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" --security-group="autoscale_group" --region="eu-west-1"  --output "/home/ec2-user/Server/Brazaar/haproxy_autoscale/gateway.cfg"

# # local mac
# sudo python "~/Documents/Personal/Code Collections/Python/Brazaar/haproxy-autoscale/update-haproxy.py" --template="/Users/Lunayo/Documents/Personal/Code Collections/Python/Brazaar/haproxy-autoscale/templates/haproxy.tpl" --access-key="AKIAICFC5TP7NVT6MK4A" --secret-key="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" --security-group="autoscale_group" --region="eu-west-1"  --output="/Users/Lunayo/Documents/Personal/Code Collections/Python/Brazaar/haproxy-autoscale/gateway.cfg"