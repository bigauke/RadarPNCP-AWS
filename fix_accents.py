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
    r'\bDocumentacao\b': 'Documentação',
    r'\bTecnica\b': 'Técnica',
    r'\bEspecificacoes\b': 'Especificações',
    r'\bAplicacao\b': 'Aplicação',
    r'\bConexao\b': 'Conexão',
    r'\bAvaliacao\b': 'Avaliação',
    r'\bPolitecnica\b': 'Politécnica',
    r'\bEspecializacao\b': 'Especialização',
    r'\bmultiorgao\b': 'multiórgão',
    r'\bpadrao\b': 'padrão',
    r'\batencao\b': 'atenção',
    r'\bconexao\b': 'conexão',
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
    r'\bnao\b': 'não',
    r'\bNao\b': 'Não',
    r'\bContratacao\b': 'Contratação',
    r'\bPublica\b': 'Pública',
    r'\bRepositorios\b': 'Repositórios',
    r'\bContratacoes\b': 'Contratações',
    r'\bInstrucoes\b': 'Instruções',
    r'\bImplantacao\b': 'Implantação',
    r'\bRelatorios\b': 'Relatórios',
    r'\bEvidencias\b': 'Evidências',
    r'\bLicitacao\b': 'Licitação',
    r'\bexecucoes\b': 'execuções',
    r'\bórgaos\b': 'órgãos'
}

for file_name in files_to_check:
    if not os.path.exists(file_name):
        continue
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for pattern, replacement in replacements.items():
        # Avoid replacing in filenames like Relatorio_RadarPNCP_Etapa3.md
        # We should only replace words, but the regex \bRelatorios\b matches "Relatorios". "Relatorio_" won't match "\bRelatorios\b".
        new_content = re.sub(pattern, replacement, new_content)
        
    if new_content != content:
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {file_name}")

print("Done!")
