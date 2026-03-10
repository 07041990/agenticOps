from bedrock_agentcore.runtime import AgentRuntime
from tools import TOOLS


SYSTEM_PROMPT = """
You are an AWS Cloud assistant.

If the user asks about EC2 instances,
call the tool list_ec2_instances.
"""


runtime = AgentRuntime(
    model="anthropic.claude-3-sonnet",
    system_prompt=SYSTEM_PROMPT,
    tools=TOOLS
)


def handler(event, context):

    user_input = event["input"]

    response = runtime.invoke(user_input)

    return {
        "statusCode": 200,
        "body": response
    }