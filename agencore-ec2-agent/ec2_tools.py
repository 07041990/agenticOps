import boto3


def list_ec2_instances():

    ec2 = boto3.client("ec2")

    response = ec2.describe_instances()

    instances = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:

            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            state = instance["State"]["Name"]

            instances.append(
                {
                    "InstanceId": instance_id,
                    "InstanceType": instance_type,
                    "State": state
                }
            )

    return instances