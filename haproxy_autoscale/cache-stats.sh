#!/bin/bash -ex

echo 'stats' | nc ec2-54-217-229-240.eu-west-1.compute.amazonaws.com 11211 > ~/Desktop/cache.txt
echo 'flush_all' | nc ec2-54-217-229-240.eu-west-1.compute.amazonaws.com 11211
echo 'stats reset' | nc ec2-54-217-229-240.eu-west-1.compute.amazonaws.com 11211