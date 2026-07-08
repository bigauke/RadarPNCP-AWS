-- Script DDL para criar as tabelas externas no AWS Athena
-- O Athena lerá diretamente os arquivos CSV do S3, sem precisar importá-los para um banco.

-- Tabela 1: Empresas
-- Necessário que no S3 os arquivos estejam na pasta s3://radarpncp-hub-dados-a2e68685/receita_federal/empresas/
CREATE EXTERNAL TABLE IF NOT EXISTS radarpncp_db.empresas (
  cnpj_basico STRING,
  razao_social STRING,
  natureza_juridica STRING,
  qualificacao_responsavel STRING,
  capital_social STRING,
  porte_empresa STRING,
  ente_federativo STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ';'
ESCAPED BY '\\'
LINES TERMINATED BY '\n'
LOCATION 's3://radarpncp-hub-dados-a2e68685/receita_federal/empresas/'
TBLPROPERTIES ('skip.header.line.count'='0');

-- Tabela 2: Estabelecimentos
-- Necessário que no S3 os arquivos estejam na pasta s3://radarpncp-hub-dados-a2e68685/receita_federal/estabelecimentos/
CREATE EXTERNAL TABLE IF NOT EXISTS radarpncp_db.estabelecimentos (
  cnpj_basico STRING,
  cnpj_ordem STRING,
  cnpj_dv STRING,
  identificador_matriz_filial STRING,
  nome_fantasia STRING,
  situacao_cadastral STRING,
  data_situacao_cadastral STRING,
  motivo_situacao_cadastral STRING,
  nome_cidade_exterior STRING,
  pais STRING,
  data_inicio_atividade STRING,
  cnae_fiscal_principal STRING,
  cnae_fiscal_secundaria STRING,
  tipo_logradouro STRING,
  logradouro STRING,
  numero STRING,
  complemento STRING,
  bairro STRING,
  cep STRING,
  uf STRING,
  municipio STRING,
  ddd_1 STRING,
  telefone_1 STRING,
  ddd_2 STRING,
  telefone_2 STRING,
  ddd_fax STRING,
  fax STRING,
  correio_eletronico STRING,
  situacao_especial STRING,
  data_situacao_especial STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ';'
ESCAPED BY '\\'
LINES TERMINATED BY '\n'
LOCATION 's3://radarpncp-hub-dados-a2e68685/receita_federal/estabelecimentos/'
TBLPROPERTIES ('skip.header.line.count'='0');

-- Tabela 3: Socios
CREATE EXTERNAL TABLE IF NOT EXISTS radarpncp_db.socios (
  cnpj_basico STRING,
  identificador_socio STRING,
  nome_socio STRING,
  cnpj_cpf_socio STRING,
  qualificacao_socio STRING,
  data_entrada_sociedade STRING,
  pais STRING,
  representante_legal STRING,
  nome_representante STRING,
  qualificacao_representante STRING,
  faixa_etaria STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ';'
ESCAPED BY '\\'
LINES TERMINATED BY '\n'
LOCATION 's3://radarpncp-hub-dados-a2e68685/receita_federal/socios/'
TBLPROPERTIES ('skip.header.line.count'='0');
