import json
from neo4j import GraphDatabase

def run_queries():
    driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'radarpncp123'))
    results = {}
    with driver.session() as s:
        # Dynamically find parameters
        orgao_cnpj = s.run("MATCH (o:OrgaoPublico) RETURN o.cnpj LIMIT 1").single()[0]
        modalidade_nome = s.run("MATCH (m:Modalidade) RETURN m.nome LIMIT 1").single()[0]
        
        # Q1
        q1 = """MATCH (o:OrgaoPublico {cnpj:$cnpj})-[:CONTRATOU]->(c:Contrato)
                RETURN o.nome AS orgao, c.numero_contrato AS contrato, c.objeto_contrato AS objeto, c.valor_global AS valor, c.data_assinatura AS data
                ORDER BY c.valor_global DESC LIMIT 10"""
        r1 = s.run(q1, cnpj=orgao_cnpj).data()
        results['Q1'] = r1
        
        # Q2
        q2 = """MATCH (o:OrgaoPublico {cnpj:$cnpj})-[:CONTRATOU]->(c:Contrato)<-[:FORNECEU]-(f:Fornecedor)
                RETURN f.nome AS fornecedor, count(c) AS qtd_contratos, sum(c.valor_global) AS valor_total
                ORDER BY valor_total DESC LIMIT 10"""
        r2 = s.run(q2, cnpj=orgao_cnpj).data()
        results['Q2'] = r2
        
        # Q3
        q3 = """MATCH (f:Fornecedor)-[:FORNECEU]->(:Contrato)<-[:CONTRATOU]-(o:OrgaoPublico)
                WITH f, count(DISTINCT o) AS qtd_orgaos
                WHERE qtd_orgaos > 1
                RETURN f.nome AS fornecedor, qtd_orgaos
                ORDER BY qtd_orgaos DESC LIMIT 10"""
        r3 = s.run(q3).data()
        results['Q3'] = r3
        
        # Q4
        q4 = """MATCH (f1:Fornecedor)-[:MESMO_ENDERECO]-(f2:Fornecedor)
                MATCH (f1)-[:FORNECEU]->(:Contrato)<-[:CONTRATOU]-(o:OrgaoPublico)-[:CONTRATOU]->(:Contrato)<-[:FORNECEU]-(f2)
                RETURN DISTINCT f1.nome AS fornecedor_a, f2.nome AS fornecedor_b, f1.endereco AS endereco, o.nome AS orgao_em_comum LIMIT 10"""
        r4 = s.run(q4).data()
        results['Q4'] = r4
        
        # Q5
        q5 = """MATCH (f1:Fornecedor)-[:MESMO_ENDERECO]->(f2:Fornecedor)
                RETURN f1.nome AS f1, f2.nome AS f2 LIMIT 1"""
        pair = s.run(q5).single()
        if pair:
            results['Q5'] = pair.data()
        else:
            results['Q5'] = []
            
        # Q6
        q6 = """MATCH (f:Fornecedor)-[:FORNECEU]->(c:Contrato)-[:DE_MODALIDADE]->(m:Modalidade {nome:$modalidade})
                RETURN f.nome AS fornecedor, sum(c.valor_global) AS valor_total
                ORDER BY valor_total DESC LIMIT 10"""
        r6 = s.run(q6, modalidade=modalidade_nome).data()
        results['Q6'] = r6
        
        # Q7
        q7 = """MATCH (f:Fornecedor)-[:FORNECEU]->(c:Contrato)<-[:CONTRATOU]-(o:OrgaoPublico)
                WITH f, o, c
                ORDER BY c.data_assinatura
                WITH f, o, collect(c) AS contratos
                UNWIND range(0, size(contratos)-2) AS i
                WITH f, o, contratos[i] AS c1, contratos[i+1] AS c2
                WHERE duration.between(c1.data_assinatura, c2.data_assinatura).days <= 30
                RETURN f.nome AS fornecedor, o.nome AS orgao, c1.numero_contrato AS contrato_1, c2.numero_contrato AS contrato_2,
                       duration.between(c1.data_assinatura, c2.data_assinatura).days AS dias_entre_contratos LIMIT 10"""
        r7 = s.run(q7).data()
        results['Q7'] = r7

    driver.close()
    
    # Serialização do JSON tratando datas
    def default_serializer(obj):
        from neo4j.time import Date
        if isinstance(obj, Date):
            return obj.iso_format()
        raise TypeError(f"Type {type(obj)} not serializable")
        
    print(json.dumps(results, default=default_serializer, indent=2))

if __name__ == '__main__':
    run_queries()
