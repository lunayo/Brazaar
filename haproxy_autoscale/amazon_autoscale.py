from boto.ec2.autoscale import AutoScaleConnection
from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale import AutoScalingGroup
from boto.ec2.autoscale import ScalingPolicy
from boto.ec2.cloudwatch import MetricAlarm
import amazon_key
import time
import boto.ec2
import boto.ec2.cloudwatch
import boto.ec2.autoscale
from boto.ec2.autoscale.scheduled import ScheduledUpdateGroupAction

availability_zones = ["eu-west-1a", "eu-west-1b"]
config_name = "autoscale_config"
group_name = "autoscale_group"
security_groups = ["autoscale_group"]
user_data_name = "init-autoscale.sh"

server_image = "ami-01594775"
instance_type = "m1.small"

def get_autoscale_connection() :
    conn = boto.ec2.autoscale.connect_to_region(amazon_key.REGION,
                                        aws_access_key_id=amazon_key.ACCESS_KEY,
                                        aws_secret_access_key=amazon_key.SECRET_KEY)
    return conn

def get_instances() :
    conn = get_autoscale_connection()

    ec2 = boto.ec2.connect_to_region(REGION)
    conn.get_all_groups(names=[group_name])[0]
    instance_ids = [i.instance_id for i in group.instances]
    reservations = ec2.get_all_instances(instance_ids)
    instances = [i for r in reservations for i in r.instances]

    return instances

def delete_launch_configuration() :
    conn = get_autoscale_connection()
    return conn.delete_launch_configuration(config_name)

def delete_autoscale_group() :
    conn = get_autoscale_connection()
    ag = conn.get_all_groups(names=[group_name])[0]
    ag.shutdown_instances()
    is_deleted = None
    while not is_deleted:
        print "Waiting for delete"
        #assign elastic ip to selected instances
        try :
            is_deleted = ag.delete()        
        except Exception:
            # delay for 20 seconds
            time.sleep(20)
            continue 
    print "Shutdown Successfully"
    conn.delete_auto_scaling_group(group_name)
    delete_launch_configuration()

def delete_schedule() :
    conn = get_autoscale_connection()
    conn.delete_scheduled_action("schedule-start", autoscale_group=group_name)
    conn.delete_scheduled_action("schedule-stop", autoscale_group=group_name)

def create_autoscale_group() :
    conn = get_autoscale_connection()

    # get user data script
    user_data = open(user_data_name, 'r').read()

    # create new launch configuration for auto scaling
    lc = LaunchConfiguration(name=config_name, image_id=server_image,
                            instance_type=instance_type, 
                            security_groups=security_groups,
                            user_data=user_data,
                            key_name=amazon_key.KEY_PAIR,
                            instance_monitoring=True)
    conn.create_launch_configuration(lc)

    # create auto scaling group assigned with launch configuration
    ag = AutoScalingGroup(group_name=group_name, availability_zones=availability_zones,
                            launch_config=lc, max_size=1, min_size=1,
                            connection=conn)
    conn.create_auto_scaling_group(ag)

    # print ag.get_activities()

def create_schedule() :
    conn = get_autoscale_connection()
    conn.create_scheduled_group_action(as_group=group_name, name="schedule-start",
                                        min_size=1, max_size=3, desired_capacity=3,
                                        recurrence="00 01,07,13,19 * * *")
    conn.create_scheduled_group_action(as_group=group_name, name="schedule-stop",
                                        min_size=1, max_size=1, desired_capacity=1,
                                        recurrence="55 01,07,13,19 * * *")

def create_alarm() :
    conn = get_autoscale_connection()
    # create scaling policy for scaling up and down
    scale_up_policy = ScalingPolicy(name='scale_up', adjustment_type='ChangeInCapacity',
                                     as_name=group_name, scaling_adjustment=1, 
                                     cooldown=5)
    scale_down_policy = ScalingPolicy(name='scale_down', adjustment_type='ChangeInCapacity',
                                        as_name=group_name, scaling_adjustment=-1, 
                                        cooldown=5)
    conn.create_scaling_policy(scale_up_policy)
    conn.create_scaling_policy(scale_down_policy)

    # refresh the policy
    scale_up_policy = conn.get_all_policies(
        as_group=group_name, policy_names=['scale_up'])[0]
    scale_down_policy = conn.get_all_policies(
        as_group=group_name, policy_names=['scale_down'])[0]
    # create cloud watch to assign the policy
    cloudwatch = boto.ec2.cloudwatch.connect_to_region(amazon_key.REGION,
                                        aws_access_key_id=amazon_key.ACCESS_KEY,
                                        aws_secret_access_key=amazon_key.SECRET_KEY)

    alarm_dimensions = {"AutoScalingGroupName": group_name}

    scale_up_alarm = MetricAlarm(
        name='scale_up_on_cpu', namespace='AWS/EC2',
        metric='CPUUtilization', statistic='Average',
        comparison='>', threshold='60',
        period='60', evaluation_periods=1,
        alarm_actions=[scale_up_policy.policy_arn],
        dimensions=alarm_dimensions)
    cloudwatch.create_alarm(scale_up_alarm)

    scale_down_alarm = MetricAlarm(
        name='scale_down_on_cpu', namespace='AWS/EC2',
        metric='CPUUtilization', statistic='Average',
        comparison='<', threshold='30',
        period='60', evaluation_periods=1,
        alarm_actions=[scale_down_policy.policy_arn],
        dimensions=alarm_dimensions)
    cloudwatch.create_alarm(scale_down_alarm)


def main() :
    # get_autoscale_connection()
    delete_autoscale_group()
    # delete_launch_configuration()
    # delete_schedule() python
    # create_autoscale_group()
    # create_schedule()
    # create_alarm()

main()