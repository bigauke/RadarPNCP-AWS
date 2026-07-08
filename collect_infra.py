"""
Coleta completa de toda a infraestrutura AWS do projeto RadarPNCP.
Gera saída estruturada para documentação.
"""
import boto3
import json
from datetime import datetime

REGION = 'us-east-1'

ec2_c  = boto3.client('ec2',  region_name=REGION)
rds_c  = boto3.client('rds',  region_name=REGION)
s3_c   = boto3.client('s3')
iam_c  = boto3.client('iam')
ssm_c  = boto3.client('ssm',  region_name=REGION)
cw_c   = boto3.client('cloudwatch', region_name=REGION)

sep = lambda title: print(f"\n{'='*60}\n{title}\n{'='*60}")

# ─── EC2 ─────────────────────────────────────────────────────
sep("EC2 INSTANCES")
res = ec2_c.describe_instances()
for r in res['Reservations']:
    for i in r['Instances']:
        tags  = {t['Key']:t['Value'] for t in i.get('Tags',[])}
        state = i['State']['Name']
        sgs   = [(sg['GroupId'], sg['GroupName']) for sg in i.get('SecurityGroups',[])]
        print(f"Name:        {tags.get('Name','(sem tag)')}")
        print(f"Instance ID: {i['InstanceId']}")
        print(f"Type:        {i['InstanceType']}")
        print(f"State:       {state}")
        print(f"AZ:          {i['Placement']['AvailabilityZone']}")
        print(f"AMI:         {i['ImageId']}")
        print(f"PublicIP:    {i.get('PublicIpAddress','N/A')}")
        print(f"PrivateIP:   {i.get('PrivateIpAddress','N/A')}")
        print(f"PublicDNS:   {i.get('PublicDnsName','N/A')}")
        print(f"VPC:         {i.get('VpcId','N/A')}")
        print(f"Subnet:      {i.get('SubnetId','N/A')}")
        print(f"KeyPair:     {i.get('KeyName','N/A')}")
        print(f"Arch:        {i.get('Architecture','N/A')}")
        print(f"Platform:    {i.get('PlatformDetails','N/A')}")
        print(f"LaunchTime:  {i.get('LaunchTime','N/A')}")
        print(f"SGs:         {sgs}")
        for bm in i.get('BlockDeviceMappings',[]):
            vid = bm.get('Ebs',{}).get('VolumeId')
            if vid:
                v = ec2_c.describe_volumes(VolumeIds=[vid])['Volumes'][0]
                print(f"Volume:      {vid} | {v['Size']}GB | {v['VolumeType']} | IOPS:{v.get('Iops','?')} | Throughput:{v.get('Throughput','?')}MB/s | device:{bm['DeviceName']}")
        print()

# ─── VPC ──────────────────────────────────────────────────────
sep("VPCs")
vpcs = ec2_c.describe_vpcs()['Vpcs']
for v in vpcs:
    tags = {t['Key']:t['Value'] for t in v.get('Tags',[])}
    print(f"VPC: {v['VpcId']} | CIDR:{v['CidrBlock']} | Default:{v['IsDefault']} | Name:{tags.get('Name','?')}")

# ─── SUBNETS ──────────────────────────────────────────────────
sep("SUBNETS")
subnets = ec2_c.describe_subnets()['Subnets']
for s in subnets:
    tags = {t['Key']:t['Value'] for t in s.get('Tags',[])}
    print(f"Subnet: {s['SubnetId']} | CIDR:{s['CidrBlock']} | AZ:{s['AvailabilityZone']} | AvailIPs:{s['AvailableIpAddressCount']} | Name:{tags.get('Name','?')}")

# ─── SECURITY GROUPS ──────────────────────────────────────────
sep("SECURITY GROUPS")
sgs = ec2_c.describe_security_groups()['SecurityGroups']
for sg in sgs:
    tags = {t['Key']:t['Value'] for t in sg.get('Tags',[])}
    print(f"\nSG: {sg['GroupId']} | Name:{sg['GroupName']} | VPC:{sg['VpcId']}")
    print(f"  Desc: {sg['Description']}")
    print(f"  INBOUND:")
    for r in sg.get('IpPermissions',[]):
        proto = r.get('IpProtocol','-1')
        from_p = r.get('FromPort','*')
        to_p   = r.get('ToPort','*')
        cidrs  = [c['CidrIp'] for c in r.get('IpRanges',[])]
        print(f"    {proto} {from_p}-{to_p} from {cidrs}")
    print(f"  OUTBOUND:")
    for r in sg.get('IpPermissionsEgress',[]):
        proto = r.get('IpProtocol','-1')
        from_p = r.get('FromPort','*')
        to_p   = r.get('ToPort','*')
        cidrs  = [c['CidrIp'] for c in r.get('IpRanges',[])]
        print(f"    {proto} {from_p}-{to_p} to {cidrs}")

# ─── INTERNET GATEWAYS ────────────────────────────────────────
sep("INTERNET GATEWAYS")
try:
    igws = ec2_c.describe_internet_gateways()['InternetGateways']
    for igw in igws:
        tags = {t['Key']:t['Value'] for t in igw.get('Tags',[])}
        attached = [a['VpcId'] for a in igw.get('Attachments',[])]
        print(f"IGW: {igw['InternetGatewayId']} | Attached to VPCs: {attached} | Name:{tags.get('Name','?')}")
except Exception as e:
    print(f"Error: {e}")

# ─── ELASTIC IPs ──────────────────────────────────────────────
sep("ELASTIC IPs")
try:
    eips = ec2_c.describe_addresses()['Addresses']
    if eips:
        for eip in eips:
            print(f"EIP: {eip.get('PublicIp')} | AllocationId:{eip.get('AllocationId')} | AssocTo:{eip.get('InstanceId','unassociated')}")
    else:
        print("Nenhum Elastic IP alocado.")
except Exception as e:
    print(f"Error: {e}")

# ─── KEY PAIRS ────────────────────────────────────────────────
sep("KEY PAIRS")
try:
    kps = ec2_c.describe_key_pairs()['KeyPairs']
    for kp in kps:
        print(f"KeyPair: {kp['KeyName']} | ID:{kp['KeyPairId']} | Type:{kp.get('KeyType','?')} | Fingerprint:{kp.get('KeyFingerprint','?')[:20]}...")
except Exception as e:
    print(f"Error: {e}")

# ─── RDS ──────────────────────────────────────────────────────
sep("RDS INSTANCES")
try:
    dbs = rds_c.describe_db_instances()['DBInstances']
    for db in dbs:
        ep = db.get('Endpoint',{})
        print(f"ID:           {db['DBInstanceIdentifier']}")
        print(f"Class:        {db['DBInstanceClass']}")
        print(f"Engine:       {db['Engine']} {db['EngineVersion']}")
        print(f"Status:       {db['DBInstanceStatus']}")
        print(f"Endpoint:     {ep.get('Address','?')}:{ep.get('Port','?')}")
        print(f"DB Name:      {db.get('DBName','?')}")
        print(f"Master User:  {db.get('MasterUsername','?')}")
        print(f"Storage:      {db['AllocatedStorage']} GB | {db['StorageType']} | Encrypted:{db.get('StorageEncrypted',False)}")
        print(f"AZ:           {db['AvailabilityZone']}")
        print(f"MultiAZ:      {db['MultiAZ']}")
        print(f"BackupRetent: {db['BackupRetentionPeriod']} days")
        print(f"VPC:          {db.get('DBSubnetGroup',{}).get('VpcId','?')}")
        print(f"PublicAccess: {db.get('PubliclyAccessible',False)}")
        print(f"Params Group: {[p['DBParameterGroupName'] for p in db.get('DBParameterGroups',[])]}")
        sgs_rds = [(sg['VpcSecurityGroupId'],sg['Status']) for sg in db.get('VpcSecurityGroups',[])]
        print(f"SGs:          {sgs_rds}")
        print()
except Exception as e:
    print(f"RDS error: {e}")

# ─── S3 ───────────────────────────────────────────────────────
sep("S3 BUCKETS")
try:
    buckets = s3_c.list_buckets()['Buckets']
    for b in buckets:
        name    = b['Name']
        created = b['CreationDate']
        try:
            loc = s3_c.get_bucket_location(Bucket=name)['LocationConstraint'] or 'us-east-1'
        except Exception:
            loc = '?'
        try:
            versioning = s3_c.get_bucket_versioning(Bucket=name).get('Status','Disabled')
        except Exception:
            versioning = '?'
        try:
            # Tamanho aproximado via CloudWatch (últimas 24h)
            pass
        except Exception:
            pass
        print(f"Bucket:     {name}")
        print(f"Region:     {loc}")
        print(f"Created:    {created}")
        print(f"Versioning: {versioning}")
        # Listar objetos (top 5)
        try:
            objs = s3_c.list_objects_v2(Bucket=name, MaxKeys=5)
            contents = objs.get('Contents',[])
            total = objs.get('KeyCount',0)
            print(f"Objects:    {total} (top 5 listados)")
            for obj in contents:
                kb = round(obj['Size']/1024, 1)
                print(f"  - {obj['Key']} ({kb} KB) | {obj['LastModified']}")
        except Exception as ex:
            print(f"  (sem acesso a listagem: {ex})")
        print()
except Exception as e:
    print(f"S3 error: {e}")

# ─── IAM ROLES ────────────────────────────────────────────────
sep("IAM ROLES (RadarPNCP / LabRole)")
try:
    roles = iam_c.list_roles()['Roles']
    for role in roles:
        name = role['RoleName']
        if any(kw in name.lower() for kw in ['radar','lab','ec2','neo4j','rds','ssm']):
            print(f"Role: {name}")
            print(f"  ARN:     {role['Arn']}")
            print(f"  Created: {role['CreateDate']}")
            try:
                attached = iam_c.list_attached_role_policies(RoleName=name)['AttachedPolicies']
                for p in attached:
                    print(f"  Policy: {p['PolicyName']}")
            except Exception:
                pass
except Exception as e:
    print(f"IAM error: {e}")

# ─── SSM PARAMETERS ───────────────────────────────────────────
sep("SSM PARAMETERS")
try:
    params = ssm_c.describe_parameters()['Parameters']
    if params:
        for p in params:
            print(f"Param: {p['Name']} | Type:{p['Type']} | Modified:{p.get('LastModifiedDate','?')}")
    else:
        print("Nenhum parâmetro SSM encontrado.")
except Exception as e:
    print(f"SSM error: {e}")

print(f"\n{'='*60}")
print(f"Coleta concluída: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"{'='*60}")
