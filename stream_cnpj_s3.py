import urllib.request
import tarfile
import zipfile
import boto3
import io
import sys

# IMPORTANTE: Coloque o nome do seu bucket S3 criado pelo Terraform aqui
S3_BUCKET = "radarpncp-hub-dados-a2e68685"

# Endpoint correto WebDAV da Receita Federal (evita redirecionamentos)
URL_RECEITA = "https://arquivos.receitafederal.gov.br/public.php/webdav/cnpj.tar.gz"
# Token do NextCloud usado como usuário
TOKEN_NEXTCLOUD = "YggdBLfdninEJX9"

import base64

def stream_tar_to_s3(url, bucket):
    print(f"[*] Iniciando conexão de streaming com a Receita Federal via WebDAV...")
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

    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    # Autenticação exigida pelo WebDAV do NextCloud (Usuário = Token, Senha = Vazio)
    auth_str = f"{TOKEN_NEXTCLOUD}:".encode("utf-8")
    b64_auth = base64.b64encode(auth_str).decode("utf-8")
    req.add_header("Authorization", f"Basic {b64_auth}")
    
    try:
        with urllib.request.urlopen(req) as response:
            print("[*] Conexão estabelecida. Lendo o stream do TAR.GZ...")
            # Modo 'r|gz' descompacta e lê o tar como fluxo contínuo
            with tarfile.open(fileobj=response, mode='r|gz') as tar:
                for tarinfo in tar:
                    if tarinfo.isreg(): # Se for um arquivo normal
                        
                        # FILTRO MESTRE: Parar se passar do mês alvo para não gastar gigas a mais
                        if not tarinfo.name.startswith("2025-05/"):
                            if "2025-06" in tarinfo.name or "2025-07" in tarinfo.name:
                                print(f"\n[+] Encontrou arquivo {tarinfo.name}. Ignorando arquivos futuros pois a base de 2025-05 está completa!")
                                break
                            continue
                            
                        # Ignorar lixos / zips que não vamos mapear no Neo4j
                        if any(lixo in tarinfo.name for lixo in ["Motivos", "Municipios", "Naturezas", "Paises", "Qualificacoes", "Simples", "Cnaes"]):
                            continue
                            
                        print(f"\n[+] Encontrou arquivo no TAR: {tarinfo.name} ({tarinfo.size / 1024 / 1024:.2f} MB)")
                        
                        if tarinfo.name.endswith('.zip'):
                            print(f"    Lendo ZIP...")
                            zip_data = tar.extractfile(tarinfo).read()
                            with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
                                for csv_filename in z.namelist():
                                    
                                    # Formata o nome final no S3 garantindo que tem a extensão csv
                                    s3_final_filename = csv_filename if csv_filename.endswith('.csv') else csv_filename + '.csv'
                                    
                                    if s3_final_filename in existing_csvs:
                                        print(f"    [SKIPPED] O arquivo {s3_final_filename} já está no S3. Avançando rápido...")
                                        continue
                                        
                                    if "Empresas" in tarinfo.name: folder = "empresas"
                                    elif "Estabelecimentos" in tarinfo.name: folder = "estabelecimentos"
                                    elif "Socios" in tarinfo.name: folder = "socios"
                                    else: continue
                                        
                                    print(f"    -> Fazendo upload de {csv_filename} para s3://{bucket}/receita_federal/{folder}/{s3_final_filename} ...")
                                    with z.open(csv_filename) as csv_file:
                                        s3_key = f"receita_federal/{folder}/{s3_final_filename}"
                                        s3_client.upload_fileobj(csv_file, bucket, s3_key)
                                    print(f"    [OK] Upload de {s3_final_filename} concluído!")
                                    existing_csvs.add(s3_final_filename)
                            
    except Exception as e:
        print(f"[ERROR] Falha durante o processamento: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print(f"=== ETL STREAMING CNPJ RECEITA FEDERAL ===")
    print(f"Destino: S3 Bucket -> {S3_BUCKET}")
    stream_tar_to_s3(URL_RECEITA, S3_BUCKET)
    print("\n=== SUCESSO! Todos os arquivos foram migrados para o S3 ===")
