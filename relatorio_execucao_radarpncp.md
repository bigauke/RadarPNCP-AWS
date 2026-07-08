# Relatório de Execução Técnica - Pipeline de Dados RadarPNCP

**Projeto:** RadarPNCP - Sistema de Apoio à Auditoria de Contratos Públicos
**Disciplina:** Repositórios de Dados e NoSQL (eEDB-016)
**Equipe:** Antonio Daniel, Hercules Freitas, Yuri Barbosa Rodrigues

---

## 1. Validação Arquitetural: Estamos no caminho certo?
**Absolutamente sim.** A essência da Engenharia de Dados não é apenas usar ferramentas caras, mas sim construir soluções resilientes diante de restrições de infraestrutura. 

A arquitetura alvo desenhada (S3 -> RDS -> Athena -> Banco de Grafos) está perfeitamente alinhada com a modelagem *Query-First Design* exigida pelo domínio do projeto (travessias multi-salto e análise de redes de relacionamento para detecção de fraudes). 

Durante a execução da PoC, enfrentamos restrições severas do ambiente de laboratório, mas a adoção de um **Padrão de Ingestão por Streaming em Memória (Serverless)** elevou a maturidade técnica do projeto.

---

## 2. Problemas Encontrados e Soluções Aplicadas

Durante a fase de ingestão da base massiva de CNPJs (aprox. 60GB descompactados) da Receita Federal, enfrentamos dois bloqueios críticos:

### Problema 1: Restrições de Quota e IAM na AWS Academy (VocLabs)
* **Incidente:** O provisionamento inicial da infraestrutura via Terraform falhou. O script tentou subir uma instância EC2 (`t3.large`) com um volume EBS de 150GB para baixar e processar os dados. A política da AWS Academy bloqueou explicitamente a ação `iam:CreateRole` e a alocação de discos grandes (`ec2:RunInstances` com `explicit deny` no recurso de volume).
* **Solução (Pivot Arquitetural):** Descartamos o uso de máquinas virtuais (EC2) para o ETL. Desenvolvemos o script `stream_cnpj_s3.py` para ser executado no **AWS CloudShell**. O script realiza o download, descompressão em tempo real e o upload multipart diretamente para o Amazon S3. 
* **Resultado:** Reduzimos a necessidade de disco de 150GB para **Zero** (operação puramente em memória RAM) e evitamos tráfego na rede local do usuário, utilizando a banda de altíssima velocidade interna da AWS.

*(Sugestão de Print 1: Tirar print da tela preta do AWS CloudShell mostrando o script rodando e descompactando arquivos como "Empresas0.zip" na memória)*

### Problema 2: Incompatibilidade de Streaming com o NextCloud da Receita
* **Incidente:** A Receita Federal hospeda os arquivos públicos em um servidor NextCloud. Ao tentar ler o stream pela URL de `/download`, o NextCloud encapsulava o diretório em um arquivo ZIP gerado dinamicamente ou forçava um redirecionamento 303. O módulo `tarfile` do Python quebrava com o erro `invalid header`, impedindo a leitura contínua.
* **Solução:** Aplicamos engenharia reversa no endpoint. Descobrimos que o NextCloud suporta **WebDAV**. Alteramos o código para bater diretamente na URL estática `.../public.php/webdav/cnpj.tar.gz`, implementando Autenticação Básica onde o "usuário" era o token de compartilhamento. Mudamos o modo de leitura do tarfile para `r|gz`.
* **Resultado:** O script conseguiu capturar o fluxo bruto (Raw Stream) do servidor da Receita, permitindo a extração dos CSVs internos instantaneamente, sem baixar o pacote externo completo.

*(Sugestão de Print 2: Tirar print do S3 Console na AWS mostrando a pasta `receita_federal/csv/` sendo populada com os arquivos)*

---

## 3. Estruturação do Data Lake (Athena)

Com a ingestão contínua para o bucket S3 (camada Bronze/Raw), preparamos a estrutura lógica utilizando o **AWS Athena**.

Como o RadarPNCP exige análises em cima de entidades separadas (Empresas, Estabelecimentos, Sócios), criamos o arquivo `athena_ddl.sql` que contém os comandos `CREATE EXTERNAL TABLE`. 
O Athena atuará como nosso motor de consulta Serverless. Ele não move os dados; ele apenas aplica um "esquema sob leitura" (Schema-on-Read) em cima dos arquivos CSV armazenados no S3.

*(Sugestão de Print 3: Print da interface do AWS Athena mostrando a execução de uma consulta (ex: `SELECT * FROM radarpncp_db.empresas LIMIT 10`) após os dados serem mapeados)*

---

## 4. Próximos Passos: O Grafo (RF3 a RF7)

A documentação do projeto (PDF) define que as consultas complexas (ex: Q4 - Rede de mesmo endereço, Q7 - Indícios de fracionamento temporal) necessitam de travessias multi-salto. 

Como o laboratório bloqueia o Amazon Neptune, utilizaremos o **Neo4j** (provavelmente via Neo4j AuraDB Free) como banco de grafos. A arquitetura futura consistirá em:
1. Usar o Athena para limpar e filtrar os nós (Nodes) e arestas (Edges) que importam para o domínio (ex: apenas fornecedores que ganharam contratos).
2. Exportar esse subconjunto.
3. Ingerir no Neo4j para mapear os vértices `(Órgão)`, `(Fornecedor)` e a aresta `[:FIRMOU_CONTRATO]`, satisfazendo totalmente os requisitos da disciplina.

---
*Gerado por Automação de Engenharia de Dados - 2026*
