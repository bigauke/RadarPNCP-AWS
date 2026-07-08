# Infraestrutura AWS — RadarPNCP

> Documentação técnica completa dos recursos cloud do projeto, coletada automaticamente via `boto3` em **08/07/2026 às 14:21 UTC-3**.
> Account ID: `089445119491` | Region: `us-east-1` (N. Virginia)

---

## Visão Geral da Arquitetura

```
┌────────────────────────────────────────────────────────────────────────────┐
│                  AWS Region: us-east-1 (N. Virginia)                       │
│                                                                            │
│  ┌──────────────────────────────┐  ┌──────────────────────────────────┐   │
│  │  S3: radarpncp-hub-dados     │  │  S3: radarpncp-athena-results    │   │
│  │  ~4.8 GB (dados Receita Fed.)│  │  Resultados Athena (reservado)   │   │
│  └──────────────────────────────┘  └──────────────────────────────────┘   │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  VPC: vpc-0da7d8e58d69c379c (Default) CIDR: 172.31.0.0/16           │  │
│  │  IGW: igw-0b8e038bbb3a06c0b                                          │  │
│  │                                                                      │  │
│  │  ┌────────────────────────────────┐  ┌──────────────────────────┐   │  │
│  │  │  EC2: RadarPNCP-Neo4j          │  │  RDS: radarpncp-gold-db  │   │  │
│  │  │  t3.medium (4GB RAM, 2vCPU)    │  │  db.t3.micro (1GB RAM)   │   │  │
│  │  │  IP: 100.59.221.217            │  │  PostgreSQL 18.3         │   │  │
│  │  │  AZ: us-east-1b                │  │  AZ: us-east-1c          │   │  │
│  │  │  sg: neo4j_sg                  │  │  sg: default             │   │  │
│  │  │  Docker → Neo4j 5              │  │  Port: 5432              │   │  │
│  │  │   :7474 Browser                │  │  Endpoint: ...rds...     │   │  │
│  │  │   :7687 Bolt                   │  └──────────────────────────┘   │  │
│  │  └────────────────────────────────┘                                  │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                            │
│  IAM Role: LabRole (SSM + EKS + EC2 + VocLab policies)                    │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. EC2 — RadarPNCP-Neo4j

### 1.1 Especificações da Instância

| Campo | Valor |
|:---|:---|
| **Nome** | `RadarPNCP-Neo4j` |
| **Instance ID** | `i-03d3f044e8ede0bca` |
| **Tipo** | `t3.medium` |
| **vCPUs** | 2 |
| **RAM** | **4 GB** |
| **Arquitetura** | `x86_64` |
| **Plataforma** | `Linux/UNIX` (Ubuntu 22.04 LTS) |
| **AMI** | `ami-0a02a779008fa3b99` |
| **Estado** | 🟢 `running` |
| **Iniciada em** | 08/07/2026 às 14:32 UTC |
| **AZ** | `us-east-1b` |
| **IP Público** | `100.59.221.217` |
| **DNS Público** | `ec2-100-59-221-217.compute-1.amazonaws.com` |
| **IP Privado** | `172.31.9.197` |
| **VPC** | `vpc-0da7d8e58d69c379c` |
| **Subnet** | `subnet-06b090d44ec12cae3` (172.31.0.0/20) |
| **Key Pair** | `vockey` |
| **Security Group** | `sg-0807c93cf1fb07789` — `neo4j_sg` |

### 1.2 Volume EBS

| Campo | Valor |
|:---|:---|
| **Volume ID** | `vol-096ba68536bd5069e` |
| **Tipo** | `gp3` (SSD) |
| **Tamanho** | 20 GB |
| **IOPS** | 3.000 (base garantida) |
| **Throughput** | 125 MB/s |
| **Device** | `/dev/sda1` (root) |

### 1.3 Security Group — `neo4j_sg`

**ID:** `sg-0807c93cf1fb07789`

**Regras de Entrada (Inbound):**

| Porta | Protocolo | Origem | Serviço |
|:---|:---|:---|:---|
| `22` | TCP | `0.0.0.0/0` | SSH |
| `7474` | TCP | `0.0.0.0/0` | Neo4j Browser (HTTP) |
| `7687` | TCP | `0.0.0.0/0` | Neo4j Bolt Driver |

**Regras de Saída (Outbound):**

| Porta | Protocolo | Destino |
|:---|:---|:---|
| `ALL` | ALL | `0.0.0.0/0` |

> [!WARNING]
> SSH (`22`) está aberto para qualquer IP (`0.0.0.0/0`). Em produção, restringir ao IP corporativo ou usar AWS Systems Manager Session Manager sem SSH.

### 1.4 Acesso Neo4j

```
Browser URL:  http://100.59.221.217:7474
Bolt URI:     bolt://100.59.221.217:7687
Usuário:      neo4j
Senha:        radarpncp123
```

---

## 2. RDS — PostgreSQL (Gold Layer)

| Campo | Valor |
|:---|:---|
| **Identifier** | `radarpncp-gold-db` |
| **Classe** | `db.t3.micro` |
| **vCPUs** | 2 |
| **RAM** | 1 GB |
| **Engine** | PostgreSQL `18.3` |
| **Endpoint** | `radarpncp-gold-db.crlngyuimjw7.us-east-1.rds.amazonaws.com` |
| **Porta** | `5432` |
| **Usuário Master** | `postgres` |
| **Storage** | 20 GB — `gp2` (SSD) |
| **Encrypted** | ❌ Não |
| **AZ** | `us-east-1c` |
| **Multi-AZ** | ❌ Não (acadêmico) |
| **Backup Retention** | 0 dias (sem backup automático) |
| **Acesso Público** | ✅ Sim |
| **VPC** | `vpc-0da7d8e58d69c379c` |
| **Security Group** | `sg-0bfd0d5393863161b` — `default` (porta 5432 aberta) |
| **Parameter Group** | `default.postgres18` |
| **Status** | 🟢 `available` |

### 2.1 Connection String

```python
import psycopg2

conn = psycopg2.connect(
    host="radarpncp-gold-db.crlngyuimjw7.us-east-1.rds.amazonaws.com",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="<senha_configurada>"
)
```

---

## 3. Amazon S3 — Data Lake

### Bucket 1: `radarpncp-hub-dados-a2e68685`

| Campo | Valor |
|:---|:---|
| **Região** | `us-east-1` |
| **Criado em** | 08/07/2026 às 02:24 UTC |
| **Versioning** | Desativado |
| **Uso** | Dados brutos da Receita Federal, dumps PostgreSQL, artefatos |

**Objetos armazenados (amostra):**

| Arquivo | Tamanho | Última modificação |
|:---|:---|:---|
| `receita_federal/empresas/K3241.K03200Y0.D50510.EMPRECSV.csv` | **1,6 GB** | 08/07/2026 13:29 |
| `receita_federal/empresas/K3241.K03200Y0.D60613.EMPRECSV.csv` | **2,1 GB** | 08/07/2026 14:20 |
| `receita_federal/empresas/K3241.K03200Y1.D60613.EMPRECSV.csv` | 311 MB | 08/07/2026 14:26 |
| `receita_federal/empresas/K3241.K03200Y2.D60613.EMPRECSV.csv` | 328 MB | 08/07/2026 14:27 |
| `receita_federal/empresas/K3241.K03200Y3.D60613.EMPRECSV.csv` | 333 MB | 08/07/2026 14:28 |

> **Volume total estimado:** ~4,8 GB de dados brutos da Receita Federal de Empresas.

### Bucket 2: `radarpncp-athena-results-a2e68685`

| Campo | Valor |
|:---|:---|
| **Região** | `us-east-1` |
| **Criado em** | 08/07/2026 às 02:24 UTC |
| **Versioning** | Desativado |
| **Uso** | Armazenamento de resultados de queries Amazon Athena (reservado para expansão) |

---

## 4. Rede — VPC e Subnets

### VPC Principal

| Campo | Valor |
|:---|:---|
| **VPC ID** | `vpc-0da7d8e58d69c379c` |
| **CIDR Block** | `172.31.0.0/16` |
| **Tipo** | Default VPC |
| **Internet Gateway** | `igw-0b8e038bbb3a06c0b` |

### Subnets Disponíveis

| Subnet ID | CIDR | AZ | IPs Disponíveis |
|:---|:---|:---|:---|
| `subnet-07c3894de41615ae9` | `172.31.32.0/20` | `us-east-1a` | 4.091 |
| `subnet-06b090d44ec12cae3` | `172.31.0.0/20` | `us-east-1b` ★ | 4.090 |
| `subnet-09a8adb227bee398e` | `172.31.80.0/20` | `us-east-1c` | 4.090 |
| `subnet-02fcf691b6fc8b482` | `172.31.16.0/20` | `us-east-1d` | 4.091 |
| `subnet-06165d60348b47018` | `172.31.48.0/20` | `us-east-1e` | 4.091 |
| `subnet-0ed00d3048f712014` | `172.31.64.0/20` | `us-east-1f` | 4.091 |

★ Subnet em uso pela EC2 (Neo4j).

### Elastic IP (não associado)

| EIP | Allocation ID | Status |
|:---|:---|:---|
| `34.197.181.255` | `eipalloc-017e9ca6702d76a6d` | Não associado (disponível) |

---

## 5. Security Groups

| SG ID | Nome | Uso |
|:---|:---|:---|
| `sg-0807c93cf1fb07789` | `neo4j_sg` | EC2 Neo4j (portas 22, 7474, 7687) |
| `sg-0bfd0d5393863161b` | `default` | RDS PostgreSQL (porta 5432 aberta) |
| `sg-05a422814ee06b596` | `etl_sg` | Instância ETL (sem inbound — só outbound) |
| `sg-017972d61c212019b` | `ElasticMapReduce-slave` | Legado EMR (outro projeto) |
| `sg-02410227f4657048e` | `ElasticMapReduce-master` | Legado EMR (outro projeto) |

---

## 6. IAM

### Role Principal: `LabRole`

| Campo | Valor |
|:---|:---|
| **ARN** | `arn:aws:iam::089445119491:role/LabRole` |
| **Criado em** | 20/05/2026 |

**Policies Anexadas:**

| Policy | Função |
|:---|:---|
| `AmazonSSMManagedInstanceCore` | Acesso via SSM (sem SSH) |
| `AmazonEKSClusterPolicy` | Kubernetes (EKS) |
| `AmazonEC2ContainerRegistryReadOnly` | ECR Pull |
| `AmazonEKSWorkerNodePolicy` | EKS Worker |
| `VocLabPolicy1/2/3` | Políticas restritas do Lab (AWS Academy) |

---

## 7. Key Pair

| Campo | Valor |
|:---|:---|
| **Nome** | `vockey` |
| **ID** | `key-00a13bc20484b26b9` |
| **Tipo** | RSA |
| **Uso** | Acesso SSH à EC2 (alternativo ao SSM) |

---

## 8. Estimativa de Custo (us-east-1)

| Recurso | Tipo | USD/hora | USD/mês estimado |
|:---|:---|:---|:---|
| EC2 | `t3.medium` | $0,0416 | ~$30 |
| RDS | `db.t3.micro` | $0,017 | ~$12 |
| EBS gp3 | 20 GB | — | ~$1,60 |
| RDS Storage gp2 | 20 GB | — | ~$2,30 |
| S3 | ~5 GB | — | ~$0,12 |
| Elastic IP (não usado) | — | $0,005/h | ~$3,60 |
| **Total Estimado** | | | **~$50/mês** |

> [!TIP]
> **Dica de economia:** Parar EC2 e RDS quando não estiver usando. O Elastic IP não associado gera cobrança contínua de $3,60/mês — liberar se não for usar.

---

## 9. Recomendações de Produção

| Componente | Atual (Acadêmico) | Produção Sugerida |
|:---|:---|:---|
| EC2 (Neo4j) | `t3.medium` — 4 GB | `r5.xlarge` — 32 GB |
| RDS (Postgres) | `db.t3.micro` — 1 GB | `db.r5.large` — 16 GB |
| EBS | 20 GB gp3 | 500 GB gp3 + snapshot automatizado |
| RDS Storage | 20 GB gp2 | 200 GB gp3 + Multi-AZ |
| Backup | ❌ Sem backup | ✅ 7 dias retenção |
| Encryption | ❌ Não | ✅ KMS habilitado |
| SSH público | ⚠️ `0.0.0.0/0` | ✅ Somente SSM Session Manager |
| IAM | LabRole (amplo) | Role granular por serviço |
| Custo estimado | ~$50/mês | ~$800/mês |

---

*Coletado por: `collect_infra.py` via boto3 | 08/07/2026 | Projeto: RadarPNCP — eEDB-016 — Escola Politécnica da USP*
