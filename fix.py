import os
import re

files = [
    "generate_relatorio_pdf.py",
    "generate_pdf.py",
    "generate_infra_pdf.py",
    "README.md",
    "infra.md",
    "Relatorio_RadarPNCP_Etapa3.md"
]

reps = {
    r"\bRelatorio\b": "Relatório",
    r"\brelatorio\b": "relatório",
    r"\bExecucao\b": "Execução",
    r"\bexecucao\b": "execução",
    r"\bTecnico\b": "Técnico",
    r"\btecnico\b": "técnico",
    r"\bOrgao\b": "Órgão",
    r"\borgaos\b": "órgãos",
    r"\banaliticas\b": "analíticas",
    r"\bextraidos\b": "extraídos",
    r"\benderecos\b": "endereços",
    r"\bendereco\b": "endereço",
    r"\bhistorico\b": "histórico",
    r"\bConcentracao\b": "Concentração",
    r"\bfisico\b": "físico",
    r"\bservicos\b": "serviços",
    r"\brestricao\b": "restrição",
    r"\bespecifica\b": "específica",
    r"\bpossivel\b": "possível",
    r"\blicitatorio\b": "licitatório",
    r"\bIndicio\b": "Indício",
    r"\bindicios\b": "indícios",
    r"\batraves\b": "através",
    r"\bUsuario\b": "Usuário",
    r"\bEncriptacao\b": "Encriptação",
    r"\bcubranca\b": "cobrança",
    r"\bcobranca\b": "cobrança",
    r"\binstancia\b": "instância",
    r"\bmes\b": "mês",
    r"\bpadroes\b": "padrões",
    r"\bcoligacao\b": "coligação",
    r"\baplicacao\b": "aplicação",
    r"\bespecifico\b": "específico",
    r"\bNao\b": "Não",
    r"\bnao\b": "não",
    r"\besta alocado\b": "está alocado",
    r"\ba auditoria\b": "à auditoria",
    r"\be significativamente\b": "é significativamente"
}

for filename in files:
    if not os.path.exists(filename): continue
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for o, n in reps.items():
        content = re.sub(o, n, content)
        
    content = re.sub(r'\borgao\b(?!")', 'órgão', content)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done")
