import boto3
import time

s3 = boto3.client('s3', region_name='us-east-1')
ssm = boto3.client('ssm', region_name='us-east-1')

bucket = 'radarpncp-hub-dados-a2e68685'
instance_id = 'i-03d3f044e8ede0bca'

print("Uploading extract script...")
s3.upload_file('extract_queries.py', bucket, 'tmp/extract_queries.py')
url_script = s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': 'tmp/extract_queries.py'}, ExpiresIn=3600)

script = f"""#!/bin/bash
wget -q -O /tmp/extract_queries.py "{url_script}"
python3 /tmp/extract_queries.py
"""

print("Sending SSM command...")
resp = ssm.send_command(
    InstanceIds=[instance_id],
    DocumentName="AWS-RunShellScript",
    Parameters={'commands': [script]}
)

command_id = resp['Command']['CommandId']
print(f"Command ID: {command_id}")

while True:
    time.sleep(3)
    invocation = ssm.get_command_invocation(CommandId=command_id, InstanceId=instance_id)
    status = invocation['Status']
    print(f"Status: {status}")
    if status in ['Success', 'Failed', 'Cancelled', 'TimedOut']:
        with open('queries_output.json', 'w', encoding='utf-8') as f:
            f.write(invocation['StandardOutputContent'])
        with open('queries_error.txt', 'w', encoding='utf-8') as f:
            f.write(invocation['StandardErrorContent'])
        print("Done. Saved to queries_output.json")
        break
