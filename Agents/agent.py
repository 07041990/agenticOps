import boto3
import json
from tools import TOOLS

bedrock_runtime = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1"
)


SYSTEM_PROMPT = """
You are an AWS Cloud Operations assistant.

When the user asks about EC2 instances,
use the tool 'list_ec2_instances'.
"""


def run_agent(user_prompt):

    if "ec2" in user_prompt.lower() or "instance" in user_prompt.lower():

        result = TOOLS["list_ec2_instances"]["function"]()

        return result

    else:

        response = bedrock_runtime.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=json.dumps({
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": 300
            })
        )

        body = json.loads(response["body"].read())

        return body


if __name__ == "__main__":

    prompt = "List all EC2 instances in my AWS account"

    result = run_agent(prompt)

    print("\nEC2 Instances:\n")

    for i in result:
        print(f"InstanceId: {i['InstanceId']}")
        print(f"Type: {i['InstanceType']}")
        print(f"State: {i['State']}")
        print("-" * 30)