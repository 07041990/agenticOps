import argparse
import csv
import json
import sys

import boto3


REGION = "us-east-1"


def list_cloudwatch_alarms(region=REGION, state=None):

    cloudwatch = boto3.client("cloudwatch", region_name=region)

    params = {"AlarmTypes": ["MetricAlarm", "CompositeAlarm"]}
    if state:
        params["StateValue"] = state

    paginator = cloudwatch.get_paginator("describe_alarms")

    alarms = []

    for page in paginator.paginate(**params):

        for alarm in page.get("MetricAlarms", []):
            alarms.append(
                {
                    "AlarmName": alarm["AlarmName"],
                    "AlarmType": "Metric",
                    "State": alarm["StateValue"],
                    "Namespace": alarm.get("Namespace", ""),
                    "MetricName": alarm.get("MetricName", ""),
                    "Dimensions": ",".join(
                        f"{d['Name']}={d['Value']}" for d in alarm.get("Dimensions", [])
                    ),
                    "Threshold": alarm.get("Threshold", ""),
                    "ComparisonOperator": alarm.get("ComparisonOperator", ""),
                    "ActionsEnabled": alarm.get("ActionsEnabled"),
                    "AlarmActions": ",".join(alarm.get("AlarmActions", [])),
                    "StateUpdated": str(alarm.get("StateUpdatedTimestamp", "")),
                    "AlarmArn": alarm["AlarmArn"],
                }
            )

        for alarm in page.get("CompositeAlarms", []):
            alarms.append(
                {
                    "AlarmName": alarm["AlarmName"],
                    "AlarmType": "Composite",
                    "State": alarm["StateValue"],
                    "Namespace": "",
                    "MetricName": "",
                    "Dimensions": "",
                    "Threshold": "",
                    "ComparisonOperator": alarm.get("AlarmRule", ""),
                    "ActionsEnabled": alarm.get("ActionsEnabled"),
                    "AlarmActions": ",".join(alarm.get("AlarmActions", [])),
                    "StateUpdated": str(alarm.get("StateUpdatedTimestamp", "")),
                    "AlarmArn": alarm["AlarmArn"],
                }
            )

    return alarms


def main():

    parser = argparse.ArgumentParser(description="Fetch all CloudWatch alarms in a region.")
    parser.add_argument("--region", default=REGION, help=f"AWS region (default: {REGION})")
    parser.add_argument(
        "--state",
        choices=["OK", "ALARM", "INSUFFICIENT_DATA"],
        help="Only return alarms in this state",
    )
    parser.add_argument(
        "--output",
        choices=["table", "json", "csv"],
        default="table",
        help="Output format (default: table)",
    )
    args = parser.parse_args()

    alarms = list_cloudwatch_alarms(region=args.region, state=args.state)

    if args.output == "json":
        print(json.dumps(alarms, indent=2, default=str))
    elif args.output == "csv":
        if alarms:
            writer = csv.DictWriter(sys.stdout, fieldnames=alarms[0].keys())
            writer.writeheader()
            writer.writerows(alarms)
    else:
        print(f"{'AlarmName':<60} {'Type':<10} {'State':<18} {'Namespace/Metric'}")
        print("-" * 120)
        for a in alarms:
            metric = f"{a['Namespace']}/{a['MetricName']}" if a["MetricName"] else "-"
            print(f"{a['AlarmName'][:59]:<60} {a['AlarmType']:<10} {a['State']:<18} {metric}")
        print(f"\nTotal alarms in {args.region}: {len(alarms)}")


if __name__ == "__main__":
    main()
