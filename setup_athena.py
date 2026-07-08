import boto3
import time

athena = boto3.client('athena', region_name='us-east-1')

S3_OUTPUT = "s3://radarpncp-athena-results-a2e68685/"

def run_query(query, db=None):
    print(f"Executando:\n{query[:100]}...")
    params = {
        'QueryString': query,
        'ResultConfiguration': {'OutputLocation': S3_OUTPUT}
    }
    if db:
        params['QueryExecutionContext'] = {'Database': db}
        
    response = athena.start_query_execution(**params)
    execution_id = response['QueryExecutionId']
    
    while True:
        status = athena.get_query_execution(QueryExecutionId=execution_id)['QueryExecution']['Status']
        state = status['State']
        if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(1)
        
    if state == 'SUCCEEDED':
        print("-> SUCESSO\n")
    else:
        print(f"-> FALHA: {status['StateChangeReason']}\n")

if __name__ == "__main__":
    run_query("CREATE DATABASE IF NOT EXISTS radarpncp_dl;")
    
    ddl_estabelecimentos = """
    CREATE EXTERNAL TABLE IF NOT EXISTS estabelecimentos (
      cnpj_base STRING,
      cnpj_ordem STRING,
      cnpj_dv STRING,
      matriz_filial STRING,
      nome_fantasia STRING,
      situacao_cadastral STRING,
      data_situacao STRING,
      motivo_situacao STRING,
      cidade_exterior STRING,
      pais STRING,
      data_inicio_ativ STRING,
      cnae_principal STRING,
      cnae_secundaria STRING,
      tipo_logradouro STRING,
      logradouro STRING,
      numero STRING,
      complemento STRING,
      bairro STRING,
      cep STRING,
      uf STRING,
      municipio STRING,
      ddd1 STRING,
      telefone1 STRING,
      ddd2 STRING,
      telefone2 STRING,
      ddd_fax STRING,
      fax STRING,
      email STRING,
      situacao_especial STRING,
      data_situacao_esp STRING
    )
    ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
    WITH SERDEPROPERTIES (
      'separatorChar' = ';',
      'quoteChar' = '"',
      'escapeChar' = '\\\\'
    )
    LOCATION 's3://radarpncp-hub-dados-a2e68685/receita_federal/estabelecimentos/'
    """
    run_query(ddl_estabelecimentos, db='radarpncp_dl')
    
    # Test query
    print("Testando query via Athena...")
    resp = athena.start_query_execution(
        QueryString="SELECT cnpj_base, cnpj_ordem, cnpj_dv, logradouro, municipio, uf FROM estabelecimentos LIMIT 5;",
        QueryExecutionContext={'Database': 'radarpncp_dl'},
        ResultConfiguration={'OutputLocation': S3_OUTPUT}
    )
    qid = resp['QueryExecutionId']
    while True:
        stat = athena.get_query_execution(QueryExecutionId=qid)['QueryExecution']['Status']['State']
        if stat in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(1)
        
    if stat == 'SUCCEEDED':
        res = athena.get_query_results(QueryExecutionId=qid)
        for row in res['ResultSet']['Rows']:
            print([col.get('VarCharValue', '') for col in row['Data']])
    else:
        print("Falha no teste.")
