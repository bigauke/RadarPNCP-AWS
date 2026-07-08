# -*- coding: utf-8 -*-
"""
ingest_postgres_to_neo4j.py
RadarPNCP - versão híbrida: contratos reais (Postgres Gold) + endereço
real de fornecedores PJ via Receita Federal (espelhado pela BrasilAPI).

Pré-requisitos:
    pip install psycopg2-binary requests neo4j --break-system-packages
"""
import time
import psycopg2
import psycopg2.extras
import requests
from neo4j import GraphDatabase

# ---------------- Config ----------------
PG_DSN = dict(host="localhost", port=5432, dbname="pncp_db", user="postgres", password="postgres")
NEO4J_URI = "bolt://32.192.83.243:7687"
NEO4J_AUTH = ("neo4j", "RadarPNCP2024!")

LIMITE_CONTRATOS = 200      # cap final de contratos — ainda é uma PoC, não o pipeline de 3,65M
TOP_FORNECEDORES_MULTIORGAO = 80  # quantos fornecedores "interessantes" (>1 órgão) considerar antes do LIMIT
BRASILAPI_DELAY_S = 1.3     # segundos entre chamadas — respeita o rate limit público

# ---------------- 1. Extração do Postgres (Gold real) ----------------
# Em vez de simplesmente pegar os 200 contratos de maior valor (o que poderia
# devolver 200 fornecedores distintos com 1 contrato cada, deixando Q3 vazia),
# primeiro seleciona os fornecedores que JÁ são multiórgão nos dados reais,
# e só então pega os contratos deles. Isso garante que a amostra alimenta
# Q3 (multiórgão) de verdade, e dá à BrasilAPI uma população onde vínculos
# de mesmo endereço (Q4/Q5) são mais prováveis de aparecer organicamente.
SQL_BASE = """
WITH top_fornecedores AS (
    SELECT cnpj_contratada,
           count(DISTINCT orgao_entidade_id) AS qtd_orgaos
    FROM fato_contratos
    GROUP BY cnpj_contratada
    HAVING count(DISTINCT orgao_entidade_id) > 1
    ORDER BY qtd_orgaos DESC, sum(valor_global) DESC
    LIMIT %(top_fornecedores)s
)
SELECT
    f.id_contrato_pncp, f.numero_contrato, f.processo,
    f.categoria_processo,
    -- TODO objeto: reincluir f.objeto_contrato aqui quando o campo
    -- for adicionado à fato_contratos (hoje não existe na Gold)
    f.valor_inicial, f.valor_global, f.valor_parcelas,
    f.data_assinatura, f.data_vigencia_inicio, f.data_vigencia_fim, f.data_publicacao,
    o.orgao_entidade_id           AS orgao_cnpj,
    o.nome_orgao                  AS orgao_nome,
    o.codigo_unidade, o.nome_unidade,
    TRIM(fo.cnpj_contratada)      AS fornecedor_ni,
    COALESCE(fo.nome_razao_social, fo.nome_contratada) AS fornecedor_nome,
    m.id_modalidade,
    m.nome_modalidade             AS modalidade_nome
FROM fato_contratos f
JOIN top_fornecedores  tf ON tf.cnpj_contratada  = f.cnpj_contratada
JOIN dim_orgaos        o  ON o.orgao_entidade_id = f.orgao_entidade_id
JOIN dim_fornecedores  fo ON fo.cnpj_contratada  = f.cnpj_contratada
JOIN dim_modalidades   m  ON m.id_modalidade     = f.id_modalidade
ORDER BY f.valor_global DESC
LIMIT %(limite)s;
"""

def extrair_contratos():
    params = {"limite": LIMITE_CONTRATOS, "top_fornecedores": TOP_FORNECEDORES_MULTIORGAO}
    with psycopg2.connect(**PG_DSN) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(SQL_BASE, params)
            return cur.fetchall()

# ---------------- 2. Enriquecimento de endereço (Receita Federal via BrasilAPI) ----------------
# ---------------- 2. Enriquecimento de endereço (Data Lake / S3 via Athena) ----------------
import boto3

athena = boto3.client('athena', region_name='us-east-1')
S3_OUTPUT = "s3://radarpncp-athena-results-a2e68685/"

def buscar_enderecos_athena(cnpjs):
    """
    Realiza uma única consulta (em lote) no Data Lake (Athena) para buscar
    endereços de múltiplos CNPJs diretamente dos CSVs da Receita Federal.
    Retorna um dicionário: {cnpj: endereco_formatado}
    """
    validos = [c for c in cnpjs if c and len("".join(filter(str.isdigit, c))) == 14]
    if not validos:
        return {}
    
    docs_limpos = ["".join(filter(str.isdigit, c)) for c in validos]
    in_clause = ", ".join(f"'{c}'" for c in docs_limpos)
    
    query = f"""
        SELECT 
            cnpj_base || cnpj_ordem || cnpj_dv AS cnpj,
            tipo_logradouro, logradouro, numero, bairro, municipio, uf
        FROM estabelecimentos
        WHERE (cnpj_base || cnpj_ordem || cnpj_dv) IN ({in_clause})
    """
    
    print(f"  -> Disparando query no Athena para {len(docs_limpos)} CNPJs (Data Lake S3)...")
    resp = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': 'radarpncp_dl'},
        ResultConfiguration={'OutputLocation': S3_OUTPUT}
    )
    qid = resp['QueryExecutionId']
    
    while True:
        stat = athena.get_query_execution(QueryExecutionId=qid)['QueryExecution']['Status']
        state = stat['State']
        if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(2)
        
    enderecos = {}
    if state == 'SUCCEEDED':
        # Paginação opcional (neste caso o volume de retorno é pequeno < 200)
        res = athena.get_query_results(QueryExecutionId=qid)
        rows = res['ResultSet']['Rows'][1:] # pular header
        for r in rows:
            data = r['Data']
            # data: [cnpj, tipo_log, logradouro, numero, bairro, municipio, uf]
            # tratar valores nulos / missing (col.get('VarCharValue'))
            vals = [col.get('VarCharValue', '').strip() for col in data]
            if len(vals) < 7:
                continue
            cnpj, tipo_log, logradouro, num, bairro, mun, uf = vals[:7]
            
            rua = f"{tipo_log} {logradouro}".strip()
            endereco = f"{rua}, {num} - {bairro}, {mun}/{uf}"
            enderecos[cnpj] = endereco
        print(f"  -> Athena concluiu. {len(enderecos)} endereços encontrados nos 4,8GB de CSVs!")
    else:
        print(f"  -> Falha no Athena: {stat.get('StateChangeReason')}")
        
    return enderecos

# ---------------- 3. Carga no Neo4j ----------------
CYPHER_UPSERT = """
MERGE (o:OrgaoPublico {cnpj: $orgao_cnpj})
  ON CREATE SET o.nome = $orgao_nome, o.codigo_unidade = $codigo_unidade, o.nome_unidade = $nome_unidade

MERGE (f:Fornecedor {ni_fornecedor: $fornecedor_ni})
  ON CREATE SET f.nome = $fornecedor_nome,
                f.tipo_pessoa = CASE WHEN size(replace(replace($fornecedor_ni,'.',''),'-','')) = 14
                                     THEN 'PJ' ELSE 'PF' END,
                f.endereco = $endereco

MERGE (m:Modalidade {id_modalidade: $id_modalidade})
  ON CREATE SET m.nome = $modalidade_nome

MERGE (c:Contrato {id_contrato_pncp: $id_contrato_pncp})
  ON CREATE SET c.numero_contrato = $numero_contrato, c.processo = $processo,
                c.categoria_processo = $categoria_processo,
                // TODO objeto: reincluir c.objeto_contrato = $objeto_contrato
                // quando o campo voltar à fato_contratos
                c.valor_inicial = $valor_inicial, c.valor_global = $valor_global,
                c.valor_parcelas = $valor_parcelas,
                c.data_assinatura = CASE WHEN $data_assinatura IS NULL THEN null ELSE date($data_assinatura) END,
                c.data_vigencia_inicio = CASE WHEN $data_vigencia_inicio IS NULL THEN null ELSE date($data_vigencia_inicio) END,
                c.data_vigencia_fim = CASE WHEN $data_vigencia_fim IS NULL THEN null ELSE date($data_vigencia_fim) END,
                c.data_publicacao = CASE WHEN $data_publicacao IS NULL THEN null ELSE date($data_publicacao) END

MERGE (o)-[:CONTRATOU]->(c)
MERGE (f)-[:FORNECEU]->(c)
MERGE (c)-[:DE_MODALIDADE]->(m)
"""

CYPHER_MESMO_ENDERECO = """
MATCH (f1:Fornecedor), (f2:Fornecedor)
WHERE f1.ni_fornecedor < f2.ni_fornecedor
  AND f1.endereco IS NOT NULL AND f1.endereco = f2.endereco
MERGE (f1)-[:MESMO_ENDERECO]->(f2)
RETURN count(*) AS arestas_criadas
"""

def _data_ou_none(valor):
    return valor.isoformat() if valor is not None else None

def carregar_no_neo4j(registros):
    # Buscar todos os endereços via Athena (S3 Data Lake) de uma só vez
    cnpjs_unicos = {r["fornecedor_ni"] for r in registros}
    mapa_enderecos = buscar_enderecos_athena(cnpjs_unicos)

    driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)
    with driver.session() as session:
        for r in registros:
            doc = "".join(filter(str.isdigit, r["fornecedor_ni"] or ""))
            endereco = mapa_enderecos.get(doc)
            
            session.run(CYPHER_UPSERT, {
                "orgao_cnpj": r["orgao_cnpj"], "orgao_nome": r["orgao_nome"],
                "codigo_unidade": r["codigo_unidade"], "nome_unidade": r["nome_unidade"],
                "fornecedor_ni": r["fornecedor_ni"], "fornecedor_nome": r["fornecedor_nome"],
                "endereco": endereco,
                "id_modalidade": r["id_modalidade"], "modalidade_nome": r["modalidade_nome"],
                "id_contrato_pncp": r["id_contrato_pncp"], "numero_contrato": r["numero_contrato"],
                "processo": r["processo"],
                "categoria_processo": r["categoria_processo"],
                "valor_inicial": float(r["valor_inicial"] or 0),
                "valor_global": float(r["valor_global"] or 0),
                "valor_parcelas": float(r["valor_parcelas"] or 0),
                "data_assinatura": _data_ou_none(r["data_assinatura"]),
                "data_vigencia_inicio": _data_ou_none(r["data_vigencia_inicio"]),
                "data_vigencia_fim": _data_ou_none(r["data_vigencia_fim"]),
                "data_publicacao": _data_ou_none(r["data_publicacao"]),
            })
            nome = (r["fornecedor_nome"] or "?")[:40]
            orgao = (r["orgao_nome"] or "?")[:30]
            print(f"  + {nome:40s} -> {orgao:30s} | endereco: {endereco or '-'}")

        print("Conectando fornecedores com o mesmo endereço (MESMO_ENDERECO)...")
        result = session.run(CYPHER_MESMO_ENDERECO).single()
        print(f"  arestas MESMO_ENDERECO criadas: {result['arestas_criadas']}")
    driver.close()

# ---------------- main ----------------
if __name__ == "__main__":
    print(f"Extraindo até {LIMITE_CONTRATOS} contratos reais do Postgres...")
    registros = extrair_contratos()
    distintos = len({r["fornecedor_ni"] for r in registros})
    print(f"  {len(registros)} contratos, {distintos} fornecedores distintos")
    carregar_no_neo4j(registros)
    print("Concluído. Veja em http://localhost:7474")
