import boto3
import time

ssm = boto3.client('ssm', region_name='us-east-1')

script = """#!/bin/bash
free -h
"""
commands = [script]

response = ssm.send_command(
    InstanceIds=['i-0ef7c1e9bedfe0b2d'],
    DocumentName='AWS-RunShellScript',
    Parameters={'commands': commands}
)

command_id = response['Command']['CommandId']

while True:
    time.sleep(2)
    result = ssm.list_command_invocations(
        CommandId=command_id,
        Details=True
    )
    if not result['CommandInvocations']:
        continue
    
    invocation = result['CommandInvocations'][0]
    status = invocation['Status']
    if status in ['Success', 'Failed', 'Cancelled', 'TimedOut']:
        print("Status:", status)
        for cp in invocation['CommandPlugins']:
            print(cp.get('Output', ''))
        break
