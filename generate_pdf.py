"""
Gera README_RadarPNCP.pdf usando Chrome headless.
Requer: Google Chrome instalado.
"""
import subprocess, os, sys
from pathlib import Path

BASE = Path(__file__).parent.resolve()
HTML_FILE = BASE / "readme_premium.html"
PDF_FILE  = BASE / "README_RadarPNCP.pdf"
CHROME    = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# ── HTML PREMIUM ──────────────────────────────────────────────────────────────
HTML = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"/>
<title>RadarPNCP - Documentacao Tecnica</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<style>
:root{--bd:#0d1b4b;--bm:#1a3a8f;--bl:#3b82f6;--bp:#eff6ff;--acc:#f59e0b;--tx:#1e293b;--mu:#64748b;--br:#e2e8f0;--cb:#0f172a;--ct:#e2e8f0;--wh:#ffffff}
*{box-sizing:border-box;margin:0;padding:0}
@page{size:A4;margin:0}
body{font-family:'Inter',sans-serif;font-size:10.5pt;line-height:1.7;color:var(--tx);background:var(--wh)}

/* COVER */
.cover{width:210mm;height:297mm;background:linear-gradient(145deg,#0d1b4b 0%,#1a3a8f 60%,#1d4ed8 100%);display:flex;flex-direction:column;justify-content:center;align-items:flex-start;padding:60px 70px;page-break-after:always;position:relative;overflow:hidden}
.cover::before{content:'';position:absolute;top:-80px;right:-80px;width:400px;height:400px;border-radius:50%;background:rgba(255,255,255,0.04)}
.cover::after{content:'';position:absolute;bottom:-60px;left:-50px;width:300px;height:300px;border-radius:50%;background:rgba(245,158,11,0.07)}
.cb{background:rgba(245,158,11,0.18);border:1px solid rgba(245,158,11,0.5);color:#f59e0b;font-size:8pt;font-weight:600;letter-spacing:2px;text-transform:uppercase;padding:5px 14px;border-radius:20px;margin-bottom:28px;display:inline-block}
.cover h1{color:#fff;font-size:38pt;font-weight:700;line-height:1.1;margin-bottom:14px;letter-spacing:-0.5px}
.cover h1 span{color:#f59e0b}
.cs{color:rgba(255,255,255,0.7);font-size:13pt;font-weight:300;margin-bottom:48px;max-width:480px}
.cd{width:56px;height:3px;background:#f59e0b;border-radius:2px;margin-bottom:34px}
.cm{display:flex;flex-direction:column;gap:9px}
.ci{display:flex;align-items:flex-start;gap:10px;color:rgba(255,255,255,0.75);font-size:9.5pt}
.cl{color:rgba(255,255,255,0.42);font-size:7.5pt;font-weight:600;letter-spacing:1px;text-transform:uppercase;min-width:95px;padding-top:1px}
.cv{color:rgba(255,255,255,0.9);font-weight:500}
.cf{position:absolute;bottom:38px;left:70px;right:70px;display:flex;justify-content:space-between;align-items:center;border-top:1px solid rgba(255,255,255,0.1);padding-top:18px}
.cfl{color:rgba(255,255,255,0.45);font-size:8pt}
.ct2{background:rgba(59,130,246,0.28);color:rgba(255,255,255,0.8);font-size:7.5pt;padding:4px 10px;border-radius:10px;font-weight:500}

/* HEADER BAR */
.ph{background:var(--bd);color:rgba(255,255,255,0.55);font-size:7.5pt;letter-spacing:1.5px;text-transform:uppercase;padding:8px 58px;display:flex;justify-content:space-between}
.ph em{color:#f59e0b;font-style:normal}

/* CONTENT */
.content{padding:44px 58px;max-width:210mm}

h2{font-size:15pt;font-weight:700;color:var(--bd);margin-top:38px;margin-bottom:14px;padding-bottom:9px;border-bottom:2px solid var(--bl);display:flex;align-items:center;gap:10px;page-break-after:avoid}
.sn{background:var(--bm);color:#fff;font-size:8.5pt;font-weight:700;padding:2px 9px;border-radius:11px;letter-spacing:.4px}
h3{font-size:11pt;font-weight:600;color:var(--bm);margin-top:22px;margin-bottom:9px;page-break-after:avoid}
p{margin-bottom:11px}
strong{color:var(--bd)}

/* BOXES */
.warn{background:#fffbeb;border-left:4px solid #f59e0b;border-radius:0 8px 8px 0;padding:13px 17px;margin:14px 0;font-size:9.5pt;color:#92400e}

/* CODE */
pre{background:var(--cb);color:var(--ct);border-radius:8px;padding:15px 19px;font-family:'JetBrains Mono','Courier New',monospace;font-size:8pt;line-height:1.6;white-space:pre-wrap;word-break:break-all;margin:13px 0;page-break-inside:avoid}
code{font-family:'JetBrains Mono','Courier New',monospace;background:#f1f5f9;color:#0f172a;padding:1px 5px;border-radius:4px;font-size:8.5pt;word-break:break-all}

/* LISTS */
ul,ol{padding-left:22px;margin-bottom:11px}
li{margin-bottom:4px}
li strong{color:var(--bd)}

/* TABLE */
table{width:100%;border-collapse:collapse;margin:14px 0;font-size:9pt;page-break-inside:avoid}
thead th{background:var(--bd);color:#fff;padding:9px 13px;text-align:left;font-weight:600}
tbody td{padding:7px 13px;border-bottom:1px solid var(--br);color:var(--tx)}
tbody tr:nth-child(even) td{background:#f8fafc}
tbody tr:last-child td{border-bottom:none}

/* SCHEMA */
.schema{background:#0f172a;border-radius:10px;padding:19px 23px;margin:14px 0;font-family:'JetBrains Mono',monospace;font-size:9pt;color:#94a3b8;line-height:2.1}
.schema .nd{color:#67e8f9}
.schema .rl{color:#f9a8d4}
.schema .ar{color:#fbbf24}
.schema .cm{color:#64748b}

/* QUERY CARDS */
.qc{border:1px solid var(--br);border-radius:10px;overflow:hidden;margin:18px 0;page-break-inside:avoid}
.qh{background:linear-gradient(90deg,var(--bm),#2563eb);color:#fff;padding:9px 17px;font-size:9pt;font-weight:600;display:flex;justify-content:space-between;align-items:center}
.qb{background:rgba(255,255,255,0.18);font-size:7.5pt;padding:2px 8px;border-radius:8px}
.qc pre{margin:0;border-radius:0;font-size:8pt}

/* IMAGE */
.arch-img{width:100%;border-radius:9px;margin:18px 0;border:1px solid var(--br)}
.shot{border-radius:9px;overflow:hidden;border:1px solid var(--br);margin:18px 0}
.shot img{width:100%;display:block}
.shot-cap{background:#f8fafc;border-top:1px solid var(--br);padding:7px 13px;font-size:8pt;color:var(--mu);text-align:center;font-style:italic}

/* FOOTER */
hr{border:none;border-top:1px solid var(--br);margin:26px 0}
.pf{margin-top:46px;padding-top:14px;border-top:1px solid var(--br);display:flex;justify-content:space-between;font-size:8pt;color:var(--mu)}
</style>
</head>
<body>

<!-- COVER -->
<div class="cover">
  <div class="cb">Documentacao Tecnica &middot; eEDB-016 &middot; 2026</div>
  <h1><span>Radar</span>PNCP</h1>
  <p class="cs">Mapeamento de Redes de Contratacao Publica em Grafo &mdash; implantado na nuvem AWS com Neo4j</p>
  <div class="cd"></div>
  <div class="cm">
    <div class="ci"><span class="cl">Curso</span><span class="cv">Especializacao em Big Data &mdash; Escola Politecnica da USP</span></div>
    <div class="ci"><span class="cl">Disciplina</span><span class="cv">Repositorios de Dados e NoSQL (eEDB-016)</span></div>
    <div class="ci"><span class="cl">Docentes</span><span class="cv">Prof. Dr. Pedro Luiz Pizzigatti Correa &middot; Prof. Dra. Jeaneth Machicao</span></div>
    <div class="ci"><span class="cl">Tecnologia</span><span class="cv">Neo4j 5 (grafos) &middot; AWS S3 + RDS + EC2 &middot; Python &middot; Cypher</span></div>
    <div class="ci"><span class="cl">Dominio</span><span class="cv">Contratacoes publicas do PNCP modeladas como rede de relacionamentos</span></div>
  </div>
  <div class="cf">
    <span class="cfl">Julho 2026 &middot; Repositorio: eEDB-016proj</span>
    <span class="ct2">Neo4j &middot; AWS &middot; Python</span>
  </div>
</div>

<!-- HEADER -->
<div class="ph">
  <span>RadarPNCP &mdash; Documentacao Tecnica</span>
  <span>eEDB-016 &middot; Escola Politecnica da USP &middot; <em>2026</em></span>
</div>

<div class="content">

<div class="warn"><strong>Aviso sobre os Dados:</strong> Os dados combinam uma amostra de dados reais do PNCP (extraídos via pipeline para AWS RDS) e registros simulados para fins didaticos (testar travessias de grafo).</div>

<h2><span class="sn">01</span> Dominio e Justificativa</h2>
<p>O <strong>RadarPNCP</strong> e uma aplicação de apoio à auditoria de contratos publicos. Permite buscar um órgão publico ou fornecedor e visualizar a rede de relacionamentos entre contratos, destacando padrões de risco como: concentracao de fornecimento, coligação pelo mesmo endereço e indícios de fracionamento de despesa.</p>
<p>A tecnologia escolhida foi o <strong>Neo4j</strong> porque o padrao de acesso do negocio exige navegacao multi-salto sobre uma teia de conexoes &mdash; algo computacionalmente custoso no modelo relacional, mas natural e eficiente no modelo de grafos.</p>

<h2><span class="sn">02</span> Arquitetura na Nuvem (AWS)</h2>
<p>O projeto esta implantado na <strong>AWS us-east-1 (N. Virginia)</strong>, account <code>089445119491</code>, com os seguintes recursos provisionados e verificados em 08/07/2026:</p>
<img class="arch-img" src="beautiful_arch.png" alt="Arquitetura AWS"/>
<table>
  <thead><tr><th>Recurso</th><th>Tipo / Specs</th><th>Endpoint / ID</th></tr></thead>
  <tbody>
    <tr><td><strong>EC2 (Neo4j)</strong></td><td>t3.medium &mdash; 4 GB RAM, 2 vCPU &mdash; Ubuntu 22.04 LTS<br/>EBS gp3: 20 GB / 3000 IOPS</td><td>IP: <code>100.59.221.217</code><br/>ID: <code>i-03d3f044e8ede0bca</code></td></tr>
    <tr><td><strong>RDS PostgreSQL</strong></td><td>db.t3.micro &mdash; 1 GB RAM<br/>PostgreSQL 18.3 &mdash; 20 GB gp2</td><td><code>radarpncp-gold-db.crlngyuimjw7<br/>.us-east-1.rds.amazonaws.com:5432</code></td></tr>
    <tr><td><strong>S3 (Data Lake)</strong></td><td>2 buckets &mdash; ~4,8 GB dados Receita Federal</td><td><code>radarpncp-hub-dados-a2e68685</code><br/><code>radarpncp-athena-results-a2e68685</code></td></tr>
    <tr><td><strong>Neo4j Browser</strong></td><td>Docker na EC2, porta 7474 (HTTP) e 7687 (Bolt)</td><td><code>http://100.59.221.217:7474</code></td></tr>
    <tr><td><strong>VPC / Rede</strong></td><td>Default VPC &mdash; CIDR 172.31.0.0/16</td><td><code>vpc-0da7d8e58d69c379c</code> &mdash; us-east-1b</td></tr>
  </tbody>
</table>
<p style="font-size:8.5pt;color:#64748b;margin-top:6px">Especificacoes completas: <em>Infra_RadarPNCP_AWS.pdf</em> (gerado em 08/07/2026).</p>

<h2><span class="sn">03</span> Estrutura de Diretorios</h2>
<pre>eEDB-016proj/
&#x251C;&#x2500;&#x2500; deploy_to_aws.py              # Automacao de infraestrutura via SSM
&#x251C;&#x2500;&#x2500; ingest_postgres_to_neo4j.py   # Ingestao RDS (Postgres) -&gt; Neo4j via EC2
&#x251C;&#x2500;&#x2500; extract_queries.py            # Executa queries Q1-Q7 no Neo4j e salva JSON
&#x251C;&#x2500;&#x2500; Relatorio_RadarPNCP_Etapa3.md # Relatório técnico completo
&#x251C;&#x2500;&#x2500; beautiful_arch.png            # Diagrama arquitetural
&#x251C;&#x2500;&#x2500; docker-compose.yml            # Neo4j 5 local (desenvolvimento)
&#x251C;&#x2500;&#x2500; etapa3_poc_radarpncp.cypher   # Consultas Q1-Q7 em Cypher
&#x2514;&#x2500;&#x2500; screenshots/                  # Evidencias visuais das execucoes</pre>

<h2><span class="sn">04</span> Esquema do Grafo</h2>
<div class="schema">
  <span class="nd">(OrgaoPublico)</span> <span class="ar">-[:CONTRATOU]-&gt;</span> <span class="nd">(Contrato)</span> <span class="ar">&lt;-[:FORNECEU]-</span> <span class="nd">(Fornecedor)</span><br/>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="ar">|</span><br/>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="rl">[:DE_MODALIDADE]</span><br/>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="ar">v</span><br/>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="nd">(Modalidade)</span><br/><br/>
  <span class="nd">(Fornecedor)</span> <span class="ar">-[:MESMO_ENDERECO]-&gt;</span> <span class="nd">(Fornecedor)</span> &nbsp;<span class="cm">// rede de risco</span>
</div>
<table>
  <thead><tr><th>Elemento</th><th>Tipo</th><th>Descricao</th></tr></thead>
  <tbody>
    <tr><td><code>OrgaoPublico</code></td><td>No</td><td>Entidade governamental contratante</td></tr>
    <tr><td><code>Fornecedor</code></td><td>No</td><td>Empresa ou pessoa juridica fornecedora</td></tr>
    <tr><td><code>Contrato</code></td><td>No</td><td>Contrato publico com numero, valor e data</td></tr>
    <tr><td><code>Modalidade</code></td><td>No</td><td>Tipo de licitacao (Pregao, Dispensa etc.)</td></tr>
    <tr><td><code>CONTRATOU</code></td><td>Relacionamento</td><td>Órgão &rarr; Contrato</td></tr>
    <tr><td><code>FORNECEU</code></td><td>Relacionamento</td><td>Fornecedor &rarr; Contrato</td></tr>
    <tr><td><code>MESMO_ENDERECO</code></td><td>Relacionamento</td><td>Coligacao de risco por endereço compartilhado</td></tr>
  </tbody>
</table>

<h2><span class="sn">05</span> Consultas Analiticas (Q1-Q7)</h2>
<ol>
  <li><strong>Q1</strong> &mdash; Contratos de um órgão específico com valores e datas</li>
  <li><strong>Q2</strong> &mdash; Fornecedores de um órgão, agregados por volume financeiro</li>
  <li><strong>Q3</strong> &mdash; Fornecedores multiorgao (grau de conexao)</li>
  <li><strong>Q4</strong> &mdash; Rede de mesmo endereço: fornecedores coligados atendendo o mesmo órgão</li>
  <li><strong>Q5</strong> &mdash; Menor caminho (shortest path) entre dois fornecedores</li>
  <li><strong>Q6</strong> &mdash; Top fornecedores por valor global</li>
  <li><strong>Q7</strong> &mdash; Indício de fracionamento de despesa (mesmo fornecedor/órgão, janela &lt;30 dias)</li>
</ol>

<h2><span class="sn">06</span> Instrucoes de Implantacao</h2>
<p>A implantacao na nuvem foi totalmente automatizada com <strong>boto3</strong> e Python:</p>
<ol>
  <li>Conecta na AWS e configura o Security Group</li>
  <li>Restaura o dump da base no PostgreSQL (RDS)</li>
  <li>Sobe o container do Neo4j na EC2 via Docker</li>
  <li>Executa a ingestao <code>ingest_postgres_to_neo4j.py</code> via AWS Systems Manager (SSM)</li>
</ol>
<pre>$ python deploy_to_aws.py
# Neo4j disponivel em: http://&lt;IP_EC2&gt;:7474
# Login: neo4j / radarpncp123</pre>

<h2><span class="sn">07</span> Relatorios e Resultados</h2>
<ul>
  <li><strong>Relatorio_RadarPNCP_Etapa3.md / .pdf</strong> &mdash; Relatório técnico completo</li>
  <li><strong>RadarPNCP_apresentacao_.pptx</strong> &mdash; Slides com arquitetura e prints do grafo</li>
  <li><strong>README_RadarPNCP.pdf</strong> &mdash; Esta documentacao de entrega</li>
</ul>

<h2><span class="sn">08</span> Evidencias de Execução</h2>
<p>Retornos literais das queries executadas na instância de producao (AWS EC2 + Neo4j):</p>

<div class="qc">
  <div class="qh">Q1 &mdash; Contratos do Ministerio da Gestao <span class="qb">MATCH / RETURN</span></div>
  <pre>[
  {
    "orgao": "MINISTERIO DA GESTAO E DA INOVACAO EM SERVICOS PUBLICOS",
    "contrato": "00065",
    "valor": 3862241222.22,
    "data": "2025-12-12"
  }
]</pre>
</div>

<div class="qc">
  <div class="qh">Q2 &mdash; Fornecedores por Órgão (agregado) <span class="qb">MATCH / WITH / RETURN</span></div>
  <pre>[
  {
    "fornecedor": "SERVICO FEDERAL DE PROCESSAMENTO DE DADOS (SERPRO)",
    "qtd_contratos": 1,
    "valor_total": 3862241222.22
  }
]</pre>
</div>

<div class="qc">
  <div class="qh">Q3 &mdash; Fornecedores Multiorgao (grau &gt; 2) <span class="qb">MATCH / WITH / WHERE</span></div>
  <pre>[
  { "fornecedor": "SERPRO",                         "qtd_orgaos": 45 },
  { "fornecedor": "PRIME CONSULTORIA E ASSESSORIA", "qtd_orgaos": 35 },
  { "fornecedor": "CAIXA ECONOMICA FEDERAL",        "qtd_orgaos": 35 },
  { "fornecedor": "BANCO DO BRASIL SA",             "qtd_orgaos": 25 },
  { "fornecedor": "TELEFONICA BRASIL S.A.",         "qtd_orgaos":  5 }
]</pre>
</div>

<div class="qc">
  <div class="qh">Q6 &mdash; Top Fornecedores por Valor Global <span class="qb">ORDER BY DESC</span></div>
  <pre>[
  { "fornecedor": "SERPRO",                  "valor_total": 8478844194.75 },
  { "fornecedor": "CAIXA ECONOMICA FEDERAL", "valor_total": 4108106600.86 },
  { "fornecedor": "BANCO DO BRASIL SA",      "valor_total": 2629355332.56 }
]</pre>
</div>

<div class="qc">
  <div class="qh">Q7 &mdash; Indício de Fracionamento (janela &lt;30 dias) <span class="qb">TEMPORAL</span></div>
  <pre>[
  { "fornecedor": "SERPRO", "orgao": "MINISTERIO DA FAZENDA",
    "contrato_1": "00009", "contrato_2": "00001", "dias_entre_contratos": 26 },
  { "fornecedor": "TELEFONICA BRASIL S.A.", "orgao": "TRIBUNAL DE CONTAS DO ESTADO DO PARANA",
    "contrato_1": "799",   "contrato_2": "26",    "dias_entre_contratos": 0 }
]</pre>
</div>

<h3>Visualizacao do Grafo no Neo4j Browser (AWS)</h3>
<div class="shot">
  <img src="screenshots/neo4j_graph_visualization_1783524735421.png" alt="Grafo Neo4j"/>
  <div class="shot-cap">Figura: Rede de contratos publicos do RadarPNCP &mdash; Neo4j Browser na instância AWS EC2 (Julho 2026)</div>
</div>

<hr/>
<div class="pf">
  <span>RadarPNCP &middot; Escola Politecnica da USP &middot; eEDB-016 &middot; 2026</span>
  <span>Documentacao Tecnica &mdash; Gerada via script Python + Chrome headless</span>
</div>

</div>
</body>
</html>"""

# Write HTML
HTML_FILE.write_text(HTML, encoding='utf-8')
print(f"HTML written: {HTML_FILE}")

# Generate PDF via Chrome headless
cmd = [
    CHROME,
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--disable-extensions",
    "--disable-dev-shm-usage",
    f"--print-to-pdf={PDF_FILE}",
    "--print-to-pdf-no-header",
    "--no-pdf-header-footer",
    f"--run-all-compositor-stages-before-draw",
    str(HTML_FILE),
]

print("Generating PDF via Chrome headless...")
result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
if result.returncode == 0 and PDF_FILE.exists():
    size_kb = PDF_FILE.stat().st_size // 1024
    print(f"PDF generated: {PDF_FILE} ({size_kb} KB)")
else:
    print("STDOUT:", result.stdout[:500])
    print("STDERR:", result.stderr[:500])
    print("Exit code:", result.returncode)
