global  
    daemon
    maxconn 1024
    ulimit-n 2060
    pidfile /var/run/haproxy.pid

defaults
    log global
    mode    http
    option  httplog
    option  dontlognull
    retries 3
    option redispatch
    contimeout  9s
    clitimeout  60s
    srvtimeout  30s

listen proxy
    bind 0.0.0.0:8080
    acl image_content path_end .jpg .gif .png
    acl image_path path_beg /product/getImages/
    reqrep ^([^\ ]*)\ /product/getImages/(.*)     \1\ /\2 if image_content image_path
    redirect prefix http://brazaar.s3.amazonaws.com if image_content
    default_backend servers

listen stats 
    mode http
    bind 0.0.0.0:9090
    stats enable
    stats refresh 10s
    stats hide-version
    stats uri /admin?stats
    stats auth admin:admin
    stats realm Haproxy\ Statistics

backend servers
    balance roundrobin
    option httpchk GET /

    % for instance in instances['autoscale_group']:
    server ${ instance.id } ${ instance.public_dns_name }:8080 check inter 5000
    % endfor