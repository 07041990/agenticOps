from ec2_tool import list_ec2_instances


TOOLS = {
    "list_ec2_instances": {
        "description": "Returns a list of EC2 instances in the AWS account",
        "function": list_ec2_instances
    }
}