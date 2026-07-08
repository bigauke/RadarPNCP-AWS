import os
import re

files_to_check = [
    'generate_pdf.py',
    'generate_infra_pdf.py',
    'generate_relatorio_pdf.py',
    'README.md',
    'infra.md',
    'Relatorio_RadarPNCP_Etapa3.md',
    'readme_to_pdf.py'
]

replacements = {
    r'\bDominio\b': 'Domínio',
    r'\bpublicos\b': 'públicos',
    r'\bpublico\b': 'público',
    r'\bconcentracao\b': 'concentração',
    r'\bdidaticos\b': 'didáticos',
    r'\bdocumentacao\b': 'documentação',
    r'\bproducao\b': 'produção',
    r'\bVisualizacao\b': 'Visualização',
    r'\bInstancia\b': 'Instância',
    r'\bIdentificacao\b': 'Identificação',
    r'\bMonopolio\b': 'Monopólio',
    r'\bFisico\b': 'Físico',
    r'nao encontrado': 'não encontrado',
    r'nao gerado': 'não gerado',
    r'esta exposta': 'está exposta',
    r'\bRadarPNCP\b e uma aplicação': 'RadarPNCP é uma aplicação',
    r'Contrato publico': 'Contrato público'
}

for file_name in files_to_check:
    if not os.path.exists(file_name):
        continue
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for pattern, replacement in replacements.items():
        new_content = re.sub(pattern, replacement, new_content)
        
    if new_content != content:
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {file_name}")

print("Done!")
