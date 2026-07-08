import boto3
import time
import webbrowser
import sys

S3_BUCKET = "radarpncp-hub-dados-a2e68685"
TARGET_FILE = "Socios0.csv"

def watch_s3():
    s3 = boto3.client('s3')
    print(f"Vigiando o S3 aguardando o arquivo {TARGET_FILE}...")
    
    while True:
        paginator = s3.get_paginator('list_objects_v2')
        found = False
        try:
            for page in paginator.paginate(Bucket=S3_BUCKET, Prefix='receita_federal/csv/'):
                if 'Contents' in page:
                    for obj in page['Contents']:
                        if TARGET_FILE in obj['Key']:
                            found = True
                            break
                if found:
                    break
        except Exception as e:
            print(f"Erro ao checar S3: {e}")
        
        if found:
            # Chama o Chrome forçando ele a ignorar as regras de autoplay
            import os
            os.system('start chrome "https://www.youtube.com/watch?v=nUCodt4zVw4&autoplay=1" --autoplay-policy=no-user-gesture-required')
            break
            
        # Espera 2 minutos antes de checar de novo para não floodar a API
        time.sleep(120)

if __name__ == "__main__":
    watch_s3()
