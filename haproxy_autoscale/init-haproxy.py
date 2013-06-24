import boto.ec2
import amazon_key
import time

server_image = "ami-af9f8ddb"
instance_type = "t1.micro"
security_groups = ["default"]
user_data_name = "init-haproxy.sh"
elastic_ip = "54.217.232.119"

def get_connection() :
    conn = boto.ec2.connect_to_region(amazon_key.REGION,
                                      aws_access_key_id=amazon_key.ACCESS_KEY,
                                      aws_secret_access_key=amazon_key.SECRET_KEY)
    return conn

def initialise_instances() :
    conn = get_connection()

    # get user data script
    user_data = open(user_data_name, 'r').read()

    conn.run_instances(server_image, key_name=amazon_key.KEY_PAIR,
                        instance_type=instance_type, security_groups=security_groups,
                        user_data=user_data)

def get_instances() :
    conn = get_connection()
    # get load balancer instances by image id
    reservations = conn.get_all_instances(filters={'image-id' : server_image})
    instance = [i for r in reservations for i in r.instances if i.state == "running"]
    return instance[0]

def assign_elastic_ip() :
    conn = get_connection()
    is_allocated = None
    while not is_allocated:
        print "Waiting for Allocation"
        #assign elastic ip to selected instances
        try :
            elastic_ip_address = conn.get_all_addresses([elastic_ip])[0]
            is_allocated = elastic_ip_address.associate(get_instances().id)
        except Exception:
            # delay for half minute
            time.sleep(30)
            continue 
    print "Allocated Successfully"

def main() :
    initialise_instances()
    assign_elastic_ip()

main()