import paramiko
import time

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
cmd_dl = "wget -qO /tmp/db.sql 'https://food-establishment-case-linhares.s3.us-east-1.amazonaws.com/pncc_db.sql?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIARJU2YGYBW7LNX7NR%2F20260702%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260702T000616Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEB4aCXVzLXdlc3QtMiJGMEQCIBfFafBIrquBqahPdIgMZoJFhk5ri5Y7wGUudsGmiCxlAiA6X8t4JiBqa1dRyaA1mM7kS%2FkUtaJ3gyEpqT2AS%2Bz7fSrDAgjn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAEaDDA4OTQ0NTExOTQ5MSIMs46PKjuwNhWAS3i6KpcC7DlqcLe%2B6qAw%2Fh58EELHc3AmLS%2BMPLOn5hsGzxe7HWpwUZMLn3QhAccSGrN1dp7gyykfW%2BzvZye%2BgH%2BY8V%2FR5fVx8bpejQkRRABSMVDZPj2XkscaZbyUqot1NBYILoEsxGLXeVUU6SUnWVxC%2FEzMVcceEugOvOdX5nPv57CoWQO7Eq0whPoyG5Jt6KIfsYV4zJ9thTCiCE1XsBt6INkmPrOh4ZSgm3GZyr50EjFPuKBmiwMuVIVkB8DKB5Ah1FRvmjaURKXcobLP7VPIiGu6wDC17Y8FApbtMQKYUz8xu%2F1NYf8cuR3LNaHklRRMKZeMGomdDJcTQzGwl7G81vbVtsK4skrOTQbfYsH6qwi6woNx0hwpMXmvMOaQltIGOp4BI6BgTIciTjtAxK6NFLVqwEjVh6ILthHgYY2jS9HNbki3fEC%2BTbkbaqJ%2BNluyTBDPEu7IdfWiCqSMm0T9WbXCs9oFY7PUYkJCrHo2iFMuXcxzx%2B7XXOThKhAqqOJwV320eigNJCe4soNCoUa9Mle%2FORLT7AXyxvP%2Fq05lhq%2Ffv8LW4eTm64AnEHV0dNUk%2FlHvL85kNc%2Bnlj8zxagPT6U%3D&X-Amz-Signature=c02396aa7c6df9821d8d3265410692bfeb5457cfec70228f1ccd9f8eb5d31e0b'"
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
