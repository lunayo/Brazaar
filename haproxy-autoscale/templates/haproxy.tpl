global  
    daemon
    maxconn 4096
    log 127.0.0.1 local0 
    log 127.0.0.1 local1 notice

defaults
    log global
    mode    http
    option  httplog
    option  dontlognull
    retries 3
    option redispatch
    maxconn 2000
    contimeout  5000
    clitimeout  50000
    srvtimeout  50000

frontend http-in
    bind *:8080
    default_backend servers

backend servers
    balance roundrobin
    stats enable
    stats refresh 10s
    stats hide-version
    stats scope .
    stats uri /admin?stats
    stats realm Haproxy\ Statistics

    % for instance in instances['default']:
    server ${ instance.id } ${ instance.private_dns_name } check inter 5000
    % endfor