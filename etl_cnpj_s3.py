import os
import zipfile
import boto3
import sys

# IMPORTANTE: Coloque o nome do seu bucket S3 criado pelo Terraform aqui
S3_BUCKET = "radarpncp-hub-dados-a2e68685"
BD_DIR = r"d:\Especialização Engenharia de Dados e Big Data USP\2° Ciclo\eEDB-016-2026-2 - Repositório de dados e NoSQL\Aula 6.1 - Projeto\bd"

def process_local_zips(bd_dir, bucket):
    print(f"[*] Iniciando processamento dos arquivos ZIP locais em: {bd_dir}")
    s3_client = boto3.client('s3')
    
    print("[*] Listando arquivos já processados no S3 (para retomar de onde parou)...")
    existing_csvs = set()
    paginator = s3_client.get_paginator('list_objects_v2')
    for prefix in ['empresas', 'estabelecimentos', 'socios']:
        for page in paginator.paginate(Bucket=bucket, Prefix=f'receita_federal/{prefix}/'):
            if 'Contents' in page:
                for obj in page['Contents']:
                    existing_csvs.add(obj['Key'].split('/')[-1])
    print(f"[*] Encontrados {len(existing_csvs)} arquivos já no S3. Eles serão pulados!")

    if not os.path.exists(bd_dir):
        print(f"[ERROR] O diretório {bd_dir} não existe.")
        sys.exit(1)

    for filename in os.listdir(bd_dir):
        if not filename.endswith('.zip'):
            continue
            
        # Ignorar dicionarios / metadados que não vamos mapear no Neo4j/Athena
        if any(lixo in filename for lixo in ["Motivos", "Municipios", "Naturezas", "Paises", "Qualificacoes", "Simples", "Cnaes"]):
            continue
            
        zip_path = os.path.join(bd_dir, filename)
        print(f"\n[+] Encontrou arquivo ZIP local: {filename}")
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as z:
                for csv_filename in z.namelist():
                    # Formata o nome final no S3 garantindo que tem a extensão csv
                    s3_final_filename = csv_filename if csv_filename.endswith('.csv') else csv_filename + '.csv'
                    
                    if s3_final_filename in existing_csvs:
                        print(f"    [SKIPPED] O arquivo {s3_final_filename} já está no S3. Avançando rápido...")
                        continue
                        
                    if "Empresas" in filename: folder = "empresas"
                    elif "Estabelecimentos" in filename: folder = "estabelecimentos"
                    elif "Socios" in filename: folder = "socios"
                    else: continue
                        
                    print(f"    -> Fazendo upload de {csv_filename} contido em {filename} para s3://{bucket}/receita_federal/{folder}/{s3_final_filename} ...")
                    with z.open(csv_filename) as csv_file:
                        s3_key = f"receita_federal/{folder}/{s3_final_filename}"
                        s3_client.upload_fileobj(csv_file, bucket, s3_key)
                    print(f"    [OK] Upload de {s3_final_filename} concluído!")
                    existing_csvs.add(s3_final_filename)
        except Exception as e:
            print(f"[ERROR] Falha ao processar {filename}: {e}")

if __name__ == "__main__":
    print(f"=== ETL LOCAL ZIPS CNPJ -> S3 ===")
    print(f"Destino: S3 Bucket -> {S3_BUCKET}")
    process_local_zips(BD_DIR, S3_BUCKET)
    print("\n=== SUCESSO! Todos os arquivos foram migrados para o S3 ===")
