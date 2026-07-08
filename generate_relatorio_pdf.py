"""
Gera Relatorio_RadarPNCP_Etapa3.pdf usando Chrome headless.
"""
import subprocess
from pathlib import Path

BASE    = Path(__file__).parent.resolve()
HTML_F  = BASE / "relatorio_premium.html"
PDF_F   = BASE / "Relatorio_RadarPNCP_Etapa3.pdf"
CHROME  = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SHOT    = BASE / "screenshots" / "neo4j_graph_visualization_1783524735421.png"

HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"/>
<title>Relatório RadarPNCP - Etapa 3</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<style>
:root{
  --bd:#0d1b4b;--bm:#1a3a8f;--bl:#3b82f6;--bp:#eff6ff;
  --acc:#f59e0b;--tx:#1e293b;--mu:#64748b;--br:#e2e8f0;
  --cb:#0f172a;--ct:#e2e8f0;--wh:#ffffff;
  --ok:#059669;--warn:#d97706;--danger:#dc2626;--info:#0284c7;
}
*{box-sizing:border-box;margin:0;padding:0}
@page{size:A4;margin:0}
body{font-family:'Inter',sans-serif;font-size:10.5pt;line-height:1.7;color:var(--tx);background:var(--wh)}

/* COVER */
.cover{
  width:210mm;height:297mm;
  background:linear-gradient(135deg,#020c2b 0%,#0d1b4b 40%,#1a3a8f 75%,#1e40af 100%);
  display:flex;flex-direction:column;justify-content:flex-end;
  padding:0 0 70px 0;page-break-after:always;position:relative;overflow:hidden
}
.cover-bg-circle1{position:absolute;top:-120px;right:-100px;width:500px;height:500px;
  border-radius:50%;background:rgba(59,130,246,0.07)}
.cover-bg-circle2{position:absolute;top:80px;right:60px;width:220px;height:220px;
  border-radius:50%;background:rgba(245,158,11,0.06)}
.cover-bg-circle3{position:absolute;bottom:-60px;left:-80px;width:380px;height:380px;
  border-radius:50%;background:rgba(255,255,255,0.03)}

/* top banner */
.cover-top{
  position:absolute;top:0;left:0;right:0;
  background:rgba(255,255,255,0.04);
  padding:18px 60px;
  display:flex;justify-content:space-between;align-items:center;
  border-bottom:1px solid rgba(255,255,255,0.08)
}
.cover-top-logo{color:rgba(255,255,255,0.9);font-size:14pt;font-weight:700;letter-spacing:-0.3px}
.cover-top-logo span{color:#f59e0b}
.cover-top-right{display:flex;gap:10px;align-items:center}
.tag{background:rgba(255,255,255,0.1);color:rgba(255,255,255,0.7);
  font-size:7.5pt;padding:4px 11px;border-radius:20px;font-weight:500}
.tag-acc{background:rgba(245,158,11,0.2);border:1px solid rgba(245,158,11,0.4);color:#f59e0b}

/* main content area */
.cover-main{padding:0 60px;z-index:1;position:relative}
.cover-kicker{
  color:rgba(255,255,255,0.5);font-size:8pt;font-weight:600;
  letter-spacing:2.5px;text-transform:uppercase;margin-bottom:18px
}
.cover-title{color:#fff;font-size:40pt;font-weight:700;line-height:1.1;margin-bottom:10px;letter-spacing:-1px}
.cover-title em{color:#f59e0b;font-style:normal}
.cover-subtitle{color:rgba(255,255,255,0.65);font-size:13pt;font-weight:300;margin-bottom:42px}
.cover-rule{width:56px;height:3px;background:#f59e0b;border-radius:2px;margin-bottom:38px}

/* metadata grid */
.cover-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:48px}
.cover-card{
  background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);
  border-radius:10px;padding:16px 18px
}
.cover-card-label{color:rgba(255,255,255,0.4);font-size:7pt;font-weight:600;
  letter-spacing:1.5px;text-transform:uppercase;margin-bottom:5px}
.cover-card-value{color:rgba(255,255,255,0.9);font-size:9.5pt;font-weight:500}

/* status row */
.cover-status{display:flex;gap:12px}
.status-item{display:flex;align-items:center;gap:7px;color:rgba(255,255,255,0.6);font-size:8.5pt}
.status-dot{width:7px;height:7px;border-radius:50%;background:#10b981;box-shadow:0 0 6px #10b981}
.status-dot-y{background:#f59e0b;box-shadow:0 0 6px #f59e0b}

/* PAGE HEADER */
.ph{background:var(--bd);color:rgba(255,255,255,0.5);font-size:7.5pt;
  letter-spacing:1.5px;text-transform:uppercase;padding:9px 58px;
  display:flex;justify-content:space-between;align-items:center}
.ph em{color:#f59e0b;font-style:normal}
.ph-dot{width:5px;height:5px;border-radius:50%;background:#f59e0b;display:inline-block;margin:0 4px}

/* CONTENT */
.content{padding:42px 58px;max-width:210mm}
p{margin-bottom:11px}
strong{color:var(--bd)}
code{font-family:'JetBrains Mono',monospace;background:#f1f5f9;color:#0f172a;
  padding:1px 5px;border-radius:4px;font-size:8.5pt}

/* HEADINGS */
h2{font-size:15pt;font-weight:700;color:var(--bd);margin-top:36px;margin-bottom:13px;
  padding-bottom:9px;border-bottom:2px solid var(--bl);
  display:flex;align-items:center;gap:10px;page-break-after:avoid}
.sn{background:var(--bm);color:#fff;font-size:8.5pt;font-weight:700;
  padding:2px 10px;border-radius:11px;letter-spacing:.3px;white-space:nowrap}
h3{font-size:11pt;font-weight:600;color:var(--bm);margin-top:22px;margin-bottom:9px;page-break-after:avoid}

/* INTRO BOX */
.intro{background:var(--bp);border-left:4px solid var(--bl);border-radius:0 10px 10px 0;
  padding:14px 18px;margin-bottom:20px;font-size:9.5pt;color:var(--bm)}
.intro strong{color:var(--bd)}

/* ALERT BOXES */
.alert{border-radius:8px;padding:13px 17px;margin:16px 0;font-size:9.5pt;
  display:flex;align-items:flex-start;gap:12px;page-break-inside:avoid}
.alert-icon{font-size:14pt;line-height:1;flex-shrink:0;padding-top:1px}
.alert-body{}
.alert-title{font-weight:700;margin-bottom:3px;font-size:9.5pt}
.alert-tip{background:#f0fdf4;border:1px solid #bbf7d0;color:#065f46}
.alert-tip .alert-title{color:#065f46}
.alert-note{background:#eff6ff;border:1px solid #bfdbfe;color:#1e40af}
.alert-note .alert-title{color:#1e40af}
.alert-warn{background:#fffbeb;border:1px solid #fde68a;color:#92400e}
.alert-warn .alert-title{color:#b45309}

/* DATA TABLES */
.dtable-wrap{margin:16px 0;border-radius:10px;overflow:hidden;
  border:1px solid var(--br);page-break-inside:avoid}
.dtable-title{background:linear-gradient(90deg,var(--bd),var(--bm));
  color:#fff;padding:9px 16px;font-size:9pt;font-weight:600;
  display:flex;justify-content:space-between;align-items:center}
.dtable-badge{background:rgba(255,255,255,0.18);font-size:7.5pt;
  padding:2px 8px;border-radius:8px;font-weight:500}
table{width:100%;border-collapse:collapse;font-size:9pt}
thead th{background:#1e3a5f;color:#fff;padding:9px 14px;text-align:left;font-weight:600;font-size:8.5pt}
tbody td{padding:8px 14px;border-bottom:1px solid var(--br);color:var(--tx);vertical-align:top}
tbody tr:nth-child(even) td{background:#f8fafc}
tbody tr:last-child td{border-bottom:none}
.val{color:var(--ok);font-weight:600}
.danger-val{color:var(--danger);font-weight:600}
.days-0{background:#fee2e2 !important}
.days-1{background:#fef9c3 !important}

/* GRAPH IMAGE */
.graph-wrap{border:1px solid var(--br);border-radius:10px;overflow:hidden;margin:18px 0}
.graph-wrap img{width:100%;display:block}
.graph-cap{background:#f8fafc;border-top:1px solid var(--br);padding:8px 14px;
  font-size:8pt;color:var(--mu);text-align:center;font-style:italic}

/* KPI SUMMARY CARDS */
.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:20px 0}
.kpi{background:linear-gradient(135deg,#f8fafc,#fff);border:1px solid var(--br);
  border-radius:10px;padding:14px 16px;text-align:center}
.kpi-val{font-size:18pt;font-weight:700;color:var(--bd);line-height:1}
.kpi-label{font-size:7.5pt;color:var(--mu);margin-top:4px;font-weight:500;text-transform:uppercase;letter-spacing:.5px}
.kpi-sub{font-size:8pt;color:var(--ok);font-weight:600;margin-top:2px}

/* FOOTER */
hr{border:none;border-top:1px solid var(--br);margin:26px 0}
.pf{margin-top:44px;padding-top:14px;border-top:1px solid var(--br);
  display:flex;justify-content:space-between;font-size:8pt;color:var(--mu)}
</style>
</head>
<body>

<!-- ═══════════════════════════════ COVER ═══════════════════════════════ -->
<div class="cover">
  <div class="cover-bg-circle1"></div>
  <div class="cover-bg-circle2"></div>
  <div class="cover-bg-circle3"></div>

  <div class="cover-top">
    <div class="cover-top-logo"><span>Radar</span>PNCP</div>
    <div class="cover-top-right">
      <span class="tag">eEDB-016</span>
      <span class="tag tag-acc">Etapa 3 &mdash; PoC Final</span>
    </div>
  </div>

  <div class="cover-main">
    <div class="cover-kicker">Relatório Técnico de Execução &mdash; Julho 2026</div>
    <div class="cover-title">Rede de<br/>Contratacao<br/><em>Publica</em></div>
    <p class="cover-subtitle">Mapeamento em Grafo com Neo4j &mdash; Dados Reais do PNCP na AWS</p>
    <div class="cover-rule"></div>

    <div class="cover-grid">
      <div class="cover-card">
        <div class="cover-card-label">Instituicao</div>
        <div class="cover-card-value">Escola Politecnica da USP</div>
      </div>
      <div class="cover-card">
        <div class="cover-card-label">Disciplina</div>
        <div class="cover-card-value">Repositorios de Dados e NoSQL (eEDB-016)</div>
      </div>
      <div class="cover-card">
        <div class="cover-card-label">Tecnologia NoSQL</div>
        <div class="cover-card-value">Neo4j 5 + Cypher &mdash; AWS EC2/RDS</div>
      </div>
      <div class="cover-card">
        <div class="cover-card-label">Dominio</div>
        <div class="cover-card-value">Auditoria de Contratos Publicos (PNCP)</div>
      </div>
    </div>

    <div class="cover-status">
      <div class="status-item"><div class="status-dot"></div> Grafo: ONLINE (AWS EC2)</div>
      <div class="status-item"><div class="status-dot"></div> RDS PostgreSQL: ATIVO</div>
      <div class="status-item"><div class="status-dot-y"></div> 200 Contratos Carregados</div>
    </div>
  </div>
</div>

<!-- ═══════════════════════════════ HEADER BAR ═══════════════════════════════ -->
<div class="ph">
  <span>RadarPNCP &mdash; Relatório Técnico de Execução</span>
  <span><span class="ph-dot"></span> eEDB-016 &middot; Escola Politecnica da USP &middot; <em>2026</em></span>
</div>

<div class="content">

<!-- INTRO -->
<div class="intro">
  <strong>Contexto de Execução:</strong> Este relatório documenta os resultados das 7 consultas analíticas (Q1-Q7) executadas diretamente no cluster Neo4j implantado na AWS EC2, consumindo dados extraídos do PostgreSQL (Gold Layer no RDS) e enriquecidos com endereços processados no Data Lake via AWS Athena (CSV da Receita Federal armazenado no S3).
</div>

<!-- INFRA SPECS -->
<h2><span class="sn">INFRA</span> Ambiente de Execução &mdash; AWS (us-east-1)</h2>
<table>
  <thead><tr><th>Recurso</th><th>Tipo / Specs</th><th>Endpoint / Detalhe</th></tr></thead>
  <tbody>
    <tr><td><strong>EC2 &mdash; Neo4j</strong></td><td><code>t3.medium</code> &mdash; <strong>4 GB RAM</strong>, 2 vCPU<br/>Ubuntu 22.04 LTS &mdash; EBS gp3 20 GB / 3000 IOPS</td><td><code>i-03d3f044e8ede0bca</code><br/>IP: <code>100.59.221.217</code> &mdash; AZ: us-east-1b</td></tr>
    <tr><td><strong>RDS &mdash; Gold Layer</strong></td><td><code>db.t3.micro</code> &mdash; 1 GB RAM<br/>PostgreSQL <code>18.3</code> &mdash; 20 GB gp2</td><td><code>radarpncp-gold-db.crlngyuimjw7<br/>.us-east-1.rds.amazonaws.com:5432</code></td></tr>
    <tr><td><strong>S3 &mdash; Data Lake</strong></td><td>2 buckets &mdash; ~4,8 GB<br/>Dados brutos Receita Federal (EMPRECSV)</td><td><code>radarpncp-hub-dados-a2e68685</code></td></tr>
    <tr><td><strong>Neo4j Browser</strong></td><td>Docker &mdash; Bolt :7687 &mdash; HTTP :7474</td><td><code>http://100.59.221.217:7474</code><br/>User: neo4j | Senha: radarpncp123</td></tr>
    <tr><td><strong>Custo Estimado</strong></td><td>EC2 + RDS + EBS + S3 + EIP</td><td>~<strong>$50/mês</strong> (USD, us-east-1)</td></tr>
  </tbody>
</table>

<!-- KPI ROW -->
<div class="kpi-row">
  <div class="kpi">
    <div class="kpi-val">200</div>
    <div class="kpi-label">Contratos</div>
    <div class="kpi-sub">Base PNCP</div>
  </div>
  <div class="kpi">
    <div class="kpi-val">45</div>
    <div class="kpi-label">Orgaos</div>
    <div class="kpi-sub">Conectados</div>
  </div>
  <div class="kpi">
    <div class="kpi-val">7</div>
    <div class="kpi-label">Queries</div>
    <div class="kpi-sub">Cypher / Neo4j</div>
  </div>
  <div class="kpi">
    <div class="kpi-val">6</div>
    <div class="kpi-label">Alertas</div>
    <div class="kpi-sub">Fracionamento</div>
  </div>
</div>


<!-- GRAPH -->
<h2><span class="sn">GRAFO</span> Rede de Contratos &mdash; Neo4j Browser (AWS)</h2>
<p>A renderizacao abaixo foi capturada diretamente da interface do Neo4j Browser rodando na instância AWS EC2, com dados reais do PNCP mapeados como nos (órgãos, fornecedores, contratos) e arestas (CONTRATOU, FORNECEU, MESMO_ENDERECO).</p>

<div class="graph-wrap">
  <img src="screenshots/neo4j_graph_visualization_1783524735421.png" alt="Grafo Neo4j"/>
  <div class="graph-cap">Figura: Visualizacao da rede de contratos publicos no Neo4j Browser &mdash; Instancia AWS EC2 &middot; Julho 2026</div>
</div>

<!-- Q1 -->
<h2><span class="sn">Q1</span> Top Contratos por Valor &mdash; Por Órgão</h2>
<p><strong>Órgão Analisado:</strong> <code>MINISTERIO DA GESTAO E DA INOVACAO EM SERVICOS PUBLICOS</code><br/>
Esta query identifica os maiores contratos (em volume financeiro) firmados pelo órgão selecionado.</p>

<div class="dtable-wrap">
  <div class="dtable-title">Resultado da Query Q1 <span class="dtable-badge">1 registro</span></div>
  <table>
    <thead><tr><th>Órgão</th><th>N&ordm; Contrato</th><th>Data Assinatura</th><th>Valor Global (R$)</th></tr></thead>
    <tbody>
      <tr>
        <td>MINISTERIO DA GESTAO E DA INOVACAO EM SERVICOS PUBLICOS</td>
        <td><code>00065</code></td>
        <td>12/12/2025</td>
        <td class="val">R$ 3.862.241.222,22</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- Q2 -->
<h2><span class="sn">Q2</span> Total Contratado por Fornecedor</h2>
<p>Total histórico recebido pelos fornecedores que atenderam o órgão analisado na Q1.</p>

<div class="dtable-wrap">
  <div class="dtable-title">Resultado da Query Q2 <span class="dtable-badge">1 registro</span></div>
  <table>
    <thead><tr><th>Fornecedor</th><th>Qtd. Contratos</th><th>Valor Total (R$)</th></tr></thead>
    <tbody>
      <tr>
        <td>SERVICO FEDERAL DE PROCESSAMENTO DE DADOS (SERPRO)</td>
        <td>1</td>
        <td class="val">R$ 3.862.241.222,22</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- Q3 -->
<h2><span class="sn">Q3</span> Concentração de Atendimento (Fornecedores Multi-Órgão)</h2>
<p>Identifica fornecedores com capilaridade extrema no governo, fornecendo para multiplos órgãos simultaneamente.</p>

<div class="dtable-wrap">
  <div class="dtable-title">Resultado da Query Q3 <span class="dtable-badge">7 registros</span></div>
  <table>
    <thead><tr><th>Fornecedor</th><th>Qtd. de Orgaos Atendidos</th></tr></thead>
    <tbody>
      <tr><td>SERVICO FEDERAL DE PROCESSAMENTO DE DADOS (SERPRO)</td><td class="val">45 órgãos</td></tr>
      <tr><td>PRIME CONSULTORIA E ASSESSORIA EMPRESARIAL LTDA</td><td class="val">35 órgãos</td></tr>
      <tr><td>CAIXA ECONOMICA FEDERAL - CEF</td><td class="val">35 órgãos</td></tr>
      <tr><td>BANCO DO BRASIL SA</td><td class="val">25 órgãos</td></tr>
      <tr><td>TELEFONICA BRASIL S.A.</td><td>5 órgãos</td></tr>
      <tr><td>MAXIFROTA SERVICOS DE MANUTENCAO DE FROTA LTDA</td><td>5 órgãos</td></tr>
      <tr><td>CRISTALIA PRODUTOS QUIMICOS FARMACEUTICOS LTDA</td><td>3 órgãos</td></tr>
    </tbody>
  </table>
</div>

<div class="alert alert-tip">
  <div class="alert-icon">&#128161;</div>
  <div class="alert-body">
    <div class="alert-title">Insight Analitico</div>
    Empresas estatais (SERPRO, CEF, BB) e grandes provedores de frota/tecnologia (Prime, Telefonica) dominam o atendimento descentralizado em dezenas de órgãos na amostra. Este padrao e esperado para estatais, mas merece atencao em empresas privadas com grau de conexao superior a 20 órgãos distintos.
  </div>
</div>

<!-- Q4/Q5 -->
<h2><span class="sn">Q4/Q5</span> Identificacao de Cartel / Monopolio Fisico</h2>
<p>As queries Q4 e Q5 cruzam o endereço matriz/filial (obtido da Receita Federal via Data Lake/Athena) para encontrar fornecedores diferentes operando no <strong>mesmo endereço físico</strong> e prestando serviços para o mesmo órgão.</p>

<div class="alert alert-note">
  <div class="alert-icon">&#128203;</div>
  <div class="alert-body">
    <div class="alert-title">Resultado na Amostra</div>
    Não foram identificadas empresas distintas dividindo o mesmo endereço operando no mesmo órgão na amostra de 200 contratos. A restrição do limite amostral mitigou o aparecimento de fraudes deste tipo nesta execução específica. Em uma base completa (milhares de contratos), a probabilidade de colisao é significativamente maior.
  </div>
</div>

<!-- Q6 -->
<h2><span class="sn">Q6</span> Volumes Totais por Modalidade</h2>
<p><strong>Modalidade Analisada:</strong> <code>Inexigibilidade de Licitacao</code> &mdash; Lista os fornecedores que mais faturaram globalmente dentro desta modalidade de contratacao.</p>

<div class="dtable-wrap">
  <div class="dtable-title">Resultado da Query Q6 <span class="dtable-badge">5 registros</span></div>
  <table>
    <thead><tr><th>Fornecedor</th><th>Valor Total na Modalidade (R$)</th></tr></thead>
    <tbody>
      <tr><td>SERVICO FEDERAL DE PROCESSAMENTO DE DADOS (SERPRO)</td><td class="val">R$ 8.478.844.194,75</td></tr>
      <tr><td>CAIXA ECONOMICA FEDERAL - CEF</td><td class="val">R$ 4.108.106.600,86</td></tr>
      <tr><td>BANCO DO BRASIL SA</td><td class="val">R$ 2.629.355.332,56</td></tr>
      <tr><td>PRIME CONSULTORIA E ASSESSORIA EMPRESARIAL LTDA</td><td>R$ 2.194.324.881,62</td></tr>
      <tr><td>MAXIFROTA SERVICOS DE MANUTENCAO DE FROTA LTDA</td><td>R$ 1.636.850.313,04</td></tr>
    </tbody>
  </table>
</div>

<!-- Q7 -->
<h2><span class="sn">Q7</span> Fracionamento de Despesa (Contratos Sucessivos &lt; 30 dias)</h2>
<p>Alerta para contratos emitidos pelo mesmo órgão, para o mesmo fornecedor, com intervalo menor ou igual a 30 dias entre assinaturas &mdash; possível burla de limite licitatório.</p>

<div class="dtable-wrap">
  <div class="dtable-title">Resultado da Query Q7 &mdash; Alertas de Fracionamento <span class="dtable-badge">6 alertas</span></div>
  <table>
    <thead><tr><th>Órgão</th><th>Fornecedor</th><th>Contrato A</th><th>Contrato B</th><th>Intervalo</th></tr></thead>
    <tbody>
      <tr class="days-0">
        <td>TRIBUNAL DE CONTAS DO ESTADO DO PARANA</td>
        <td>TELEFONICA BRASIL S.A.</td>
        <td><code>799</code></td><td><code>26</code></td>
        <td class="danger-val">0 dias</td>
      </tr>
      <tr class="days-0">
        <td>INSTITUTO CHICO MENDES (ICMBIO)</td>
        <td>MAXIFROTA SERVICOS DE FROTA</td>
        <td><code>3</code></td><td><code>00003</code></td>
        <td class="danger-val">0 dias</td>
      </tr>
      <tr class="days-1">
        <td>MINISTERIO DAS CIDADES</td>
        <td>CAIXA ECONOMICA FEDERAL</td>
        <td><code>00016</code></td><td><code>00008</code></td>
        <td class="danger-val">1 dia</td>
      </tr>
      <tr class="days-1">
        <td>MINISTERIO DAS CIDADES</td>
        <td>CAIXA ECONOMICA FEDERAL</td>
        <td><code>00016</code></td><td><code>00002</code></td>
        <td class="danger-val">1 dia</td>
      </tr>
      <tr>
        <td>MINISTERIO DA JUSTICA E SEG. PUB.</td>
        <td>SERPRO</td>
        <td><code>00001</code></td><td><code>00022</code></td>
        <td>9 dias</td>
      </tr>
      <tr>
        <td>MINISTERIO DA FAZENDA</td>
        <td>SERPRO</td>
        <td><code>00009</code></td><td><code>00001</code></td>
        <td>26 dias</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="alert alert-warn">
  <div class="alert-icon">&#9888;</div>
  <div class="alert-body">
    <div class="alert-title">Alerta de Fracionamento Identificado</div>
    Multiplos contratos assinados num intervalo de <strong>0 ou 1 dia</strong> foram identificados. E recomendavel que à auditoria verifique se o objeto dos contratos foi fragmentado artificialmente para evitar modalidades licitatorias mais rigorosas (ex.: Pregao Eletronico vs. Dispensa/Inexigibilidade).
  </div>
</div>

<hr/>
<div class="pf">
  <span>RadarPNCP &middot; Escola Politecnica da USP &middot; eEDB-016 &middot; 2026</span>
  <span>Relatório Técnico &mdash; Gerado via Chrome headless &middot; Julho 2026</span>
</div>

</div><!-- /content -->
</body>
</html>"""

HTML_F.write_text(HTML, encoding='utf-8')
print(f"HTML written: {HTML_F}")

cmd = [
    CHROME,
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--disable-extensions",
    "--disable-dev-shm-usage",
    f"--print-to-pdf={PDF_F}",
    "--print-to-pdf-no-header",
    "--no-pdf-header-footer",
    str(HTML_F),
]

print("Generating PDF via Chrome headless...")
import subprocess
result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
if PDF_F.exists() and PDF_F.stat().st_size > 10000:
    size_kb = PDF_F.stat().st_size // 1024
    print(f"PDF generated OK: {PDF_F} ({size_kb} KB)")
else:
    print("STDOUT:", result.stdout[:400])
    print("STDERR:", result.stderr[:400])
    print("Exit:", result.returncode)
