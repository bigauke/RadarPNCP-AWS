import boto3
import time
import json

s3 = boto3.client('s3', region_name='us-east-1')
url = s3.generate_presigned_url(
    ClientMethod='get_object',
    Params={
        'Bucket': 'food-establishment-case-linhares',
        'Key': 'pncc_db.sql'
    },
    ExpiresIn=3600
)

ssm = boto3.client('ssm', region_name='us-east-1')

script = f"""#!/bin/bash
set -e

# 1. Setup 1GB swap
if [ ! -f /swapfile ]; then
    sudo fallocate -l 1G /swapfile || sudo dd if=/dev/zero of=/swapfile bs=1M count=1024
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
fi

# 2. Free memory
sudo sync; sudo sysctl -w vm.drop_caches=3

# 3. Download the dump directly (if not exists or if it is too small)
if [ ! -f /home/ubuntu/pncc_db.sql ] || [ $(stat -c%s /home/ubuntu/pncc_db.sql) -lt 150000000 ]; then
    rm -f /home/ubuntu/pncc_db.sql
    curl -o /home/ubuntu/pncc_db.sql "{url}"
fi

cd /home/ubuntu

# 4. Update docker-compose.yml to limit memory
cat << 'EOF' > docker-compose.yml
services:
  postgres:
    image: postgres:17
    container_name: postgres-radarpncp
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: mysecretpassword
      POSTGRES_DB: pncp_db
    ports:
      - "5432:5432"
    volumes:
      - ./data:/var/lib/postgresql/data
    deploy:
      resources:
        limits:
          memory: 300M
    restart: unless-stopped

  neo4j:
    image: neo4j:5
    container_name: neo4j-radarpncp
    environment:
      NEO4J_AUTH: neo4j/mysecretpassword
      NEO4J_server_memory_heap_initial__size: 128m
      NEO4J_server_memory_heap_max__size: 128m
      NEO4J_server_memory_pagecache_size: 64m
    ports:
      - "7474:7474"
      - "7687:7687"
    volumes:
      - ./neo4j/data:/data
    deploy:
      resources:
        limits:
          memory: 300M
    restart: unless-stopped
EOF

# 5. Start containers
docker rm -f postgres-radarpncp neo4j-radarpncp || true
docker-compose down || true
rm -rf ./data
docker-compose up -d

# 6. Wait for postgres to be ready
echo "Waiting for postgres..."
for i in {{1..30}}; do
    if docker exec postgres-radarpncp pg_isready -U postgres; then
        echo "Postgres is ready!"
        break
    fi
    sleep 2
done
sleep 5 # extra wait for init

# 7. Restore the database by streaming the file
echo "Restoring database..."
docker exec -i postgres-radarpncp pg_restore -U postgres -d pncp_db -Fc < /home/ubuntu/pncc_db.sql > /home/ubuntu/restore.log 2>&1 || true

echo "Restore finished!"
"""

commands = [script]

response = ssm.send_command(
    InstanceIds=['i-0ef7c1e9bedfe0b2d'],
    DocumentName='AWS-RunShellScript',
    Parameters={'commands': commands}
)

command_id = response['Command']['CommandId']
print(f"Command ID: {command_id}")

while True:
    time.sleep(5)
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
            print(json.dumps(cp, default=str, indent=2))
        break
