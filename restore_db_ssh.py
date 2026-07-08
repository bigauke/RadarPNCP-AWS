import paramiko
import time
import os

host = "54.163.201.142"
user = "ubuntu"
key_file = r"C:\Users\auke3\.ssh\labsuser.pem"

print("Connecting to", host)
key = paramiko.RSAKey.from_private_key_file(key_file)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=host, username=user, pkey=key)
print("Connected!")

# 1. Download file
print("Downloading DB dump from S3 via presigned URL...")
presigned_url = os.environ.get("S3_PRESIGNED_URL", "https://replace-with-your-url")
cmd_dl = f"wget -qO /tmp/db.sql '{presigned_url}'"
stdin, stdout, stderr = ssh.exec_command(cmd_dl)
exit_status = stdout.channel.recv_exit_status()
print("Download exit status:", exit_status)

# 2. Copy to docker
print("Copying to Docker...")
cmd_cp = "docker cp /tmp/db.sql postgres-radarpncp:/tmp/db.sql"
stdin, stdout, stderr = ssh.exec_command(cmd_cp)
exit_status = stdout.channel.recv_exit_status()
print("Copy exit status:", exit_status)

# 3. Restore DB
print("Restoring database...")
cmd_restore = "docker exec postgres-radarpncp pg_restore -U postgres -d pncp_db -Fc /tmp/db.sql"
stdin, stdout, stderr = ssh.exec_command(cmd_restore)
exit_status = stdout.channel.recv_exit_status()
print("Restore exit status:", exit_status)
print("Restore stderr:", stderr.read().decode())
print("Restore stdout:", stdout.read().decode())

ssh.close()
