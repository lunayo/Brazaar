#!/bin/bash -ex
# logging
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
echo BEGIN
date '+%Y-%m-%d %H:%M:%S'
echo END

# initialize memcached
memcached -d -m 1500 -p 11211 -l 0.0.0.0 -u root