from neo4j import GraphDatabase

URI = "bolt://100.59.221.217:7687"
AUTH = ("neo4j", "radarpncp123")
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    with driver.session() as session:
        result = session.run('''
            MATCH (f:Fornecedor)
            WHERE f.endereco IS NOT NULL
            RETURN f.nome AS Fornecedor, f.endereco AS Endereco
            LIMIT 5
        ''')
        print("RESULTADOS DO NEO4J COM ENDEREÇOS (ATHENA):")
        print("="*60)
        for record in result:
            print(f"Fornecedor: {record['Fornecedor']}")
            print(f"Endereço: {record['Endereco']}")
            print('-'*60)
