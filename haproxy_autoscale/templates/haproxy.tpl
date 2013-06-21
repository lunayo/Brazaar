global  
    daemon
    maxconn 1024
    pidfile /var/run/haproxy.pid

defaults
    log global
    mode    http
    option  httplog
    option  dontlognull
    retries 3
    option redispatch
    contimeout  5000
    clitimeout  50000
    srvtimeout  50000

frontend proxy
    bind 0.0.0.0:8080
    default_backend servers

backend servers
    balance roundrobin
    option httpchk GET /
    option forwardfor
    option httpclose
    stats enable
    stats refresh 10s
    stats hide-version
    stats uri /admin?stats
    stats auth admin:admin
    stats realm Haproxy\ Statistics

    % for instance in instances['autoscale_group']:
    server ${ instance.id } ${ instance.public_dns_name }:8080 check inter 5000
    % endfor