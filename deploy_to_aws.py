import boto3
import time
import urllib.parse
from botocore.exceptions import ClientError

s3 = boto3.client('s3', region_name='us-east-1')
ssm = boto3.client('ssm', region_name='us-east-1')

bucket = 'radarpncp-hub-dados-a2e68685'
instance_id = 'i-03d3f044e8ede0bca'
rds_host = 'radarpncp-gold-db.crlngyuimjw7.us-east-1.rds.amazonaws.com'

print("Uploading pncc_db.sql...")
s3.upload_file('data/pncc_db.sql', bucket, 'tmp/pncc_db.sql')

print("Uploading ingest script...")
s3.upload_file('ingest_postgres_to_neo4j.py', bucket, 'tmp/ingest.py')

print("Generating presigned URLs...")
url_db = s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': 'tmp/pncc_db.sql'}, ExpiresIn=3600)
url_script = s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': 'tmp/ingest.py'}, ExpiresIn=3600)

script = f"""#!/bin/bash
sudo apt-get update
sudo apt-get install -y curl ca-certificates lsb-release
sudo install -d /usr/share/postgresql-common/pgdg
sudo curl -o /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc --fail https://www.postgresql.org/media/keys/ACCC4CF8.asc
echo "deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list
sudo apt-get update
sudo apt-get install -y postgresql-client-17 python3-pip
pip3 install psycopg2-binary neo4j requests boto3 --break-system-packages

wget -q -O /tmp/pncc_db.sql "{url_db}"
wget -q -O /tmp/ingest.py "{url_script}"

export PGPASSWORD=radarpncp123
psql -h {rds_host} -U postgres -d postgres -c "CREATE DATABASE pncp_db;" || true
pg_restore -h {rds_host} -p 5432 -U postgres -d pncp_db -Fc /tmp/pncc_db.sql || true

# Change the connection strings in the python script to run locally on EC2
sed -i 's/host="localhost"/host="{rds_host}"/g' /tmp/ingest.py
sed -i 's/password="postgres"/password="radarpncp123"/g' /tmp/ingest.py
sed -i 's/32.192.83.243/localhost/g' /tmp/ingest.py
sed -i 's/RadarPNCP2024!/radarpncp123/g' /tmp/ingest.py

python3 /tmp/ingest.py
"""

print("Sending SSM command...")
response = ssm.send_command(
    InstanceIds=[instance_id],
    DocumentName='AWS-RunShellScript',
    Parameters={'commands': [script]}
)

command_id = response['Command']['CommandId']
print(f"Command ID: {command_id}")

while True:
    time.sleep(5)
    result = ssm.list_command_invocations(CommandId=command_id, Details=True)
    if not result['CommandInvocations']:
        continue
    
    invocation = result['CommandInvocations'][0]
    status = invocation['Status']
    print(f"Status: {status}")
    if status in ['Success', 'Failed', 'Cancelled', 'TimedOut']:
        for cp in invocation['CommandPlugins']:
            import sys
            sys.stdout.buffer.write(cp.get('Output', '').encode('utf-8', 'ignore'))
            print("\n\nDone.")
        break
