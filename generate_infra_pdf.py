"""
Gera Infra_RadarPNCP_AWS.pdf — Documentação de Infraestrutura
via Chrome headless com design premium.
"""
import subprocess
from pathlib import Path

BASE   = Path(__file__).parent.resolve()
HTML_F = BASE / "infra_premium.html"
PDF_F  = BASE / "Infra_RadarPNCP_AWS.pdf"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ARCH   = BASE / "beautiful_arch.png"

HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"/>
<title>RadarPNCP - Infraestrutura AWS</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<style>
:root{
  --bd:#020c2b;--bm:#0d2b6e;--bl:#2563eb;--bp:#eff6ff;
  --acc:#f59e0b;--acc2:#fbbf24;
  --tx:#1e293b;--mu:#64748b;--br:#e2e8f0;
  --cb:#0a0f1e;--ct:#94a3b8;--wh:#ffffff;
  --ok:#059669;--warn:#d97706;--danger:#dc2626;
  --green:#10b981;
}
*{box-sizing:border-box;margin:0;padding:0;overflow-wrap:break-word;word-break:break-word}
@page{size:A4;margin:0}
body{font-family:'Inter',sans-serif;font-size:10.5pt;line-height:1.7;color:var(--tx);background:#fff;overflow-x:hidden}

/* ── COVER ───────────────────────────────────── */
.cover{
  width:210mm;height:297mm;
  background:linear-gradient(160deg,#020c2b 0%,#0d1f4a 35%,#0a3272 65%,#1e40af 100%);
  position:relative;overflow:hidden;page-break-after:always;
  display:flex;flex-direction:column;justify-content:space-between;
}
/* Decorative circles */
.dc{position:absolute;border-radius:50%}
.dc1{width:500px;height:500px;top:-200px;right:-150px;background:radial-gradient(circle,rgba(37,99,235,.15),transparent 70%)}
.dc2{width:300px;height:300px;bottom:-100px;left:-80px;background:radial-gradient(circle,rgba(245,158,11,.1),transparent 70%)}
.dc3{width:200px;height:200px;top:50%;right:80px;background:radial-gradient(circle,rgba(255,255,255,.04),transparent 70%)}
/* Grid pattern */
.grid-overlay{
  position:absolute;inset:0;
  background-image:
    linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);
  background-size:40px 40px;
}
/* Top strip */
.c-top{
  position:relative;z-index:2;
  padding:22px 60px;
  border-bottom:1px solid rgba(255,255,255,.07);
  display:flex;justify-content:space-between;align-items:center;
}
.c-logo{color:#fff;font-size:15pt;font-weight:800;letter-spacing:-0.5px}
.c-logo em{color:var(--acc);font-style:normal}
.c-chip{background:rgba(245,158,11,.18);border:1px solid rgba(245,158,11,.4);
  color:var(--acc);font-size:7.5pt;font-weight:600;letter-spacing:1.5px;
  text-transform:uppercase;padding:5px 13px;border-radius:20px}
/* Main content */
.c-main{
  position:relative;z-index:2;
  padding:0 60px;flex:1;
  display:flex;flex-direction:column;justify-content:center;
}
.c-eyebrow{color:rgba(255,255,255,.4);font-size:8pt;font-weight:600;
  letter-spacing:2.5px;text-transform:uppercase;margin-bottom:14px}
.c-title{font-size:44pt;font-weight:800;color:#fff;line-height:1.0;
  letter-spacing:-2px;margin-bottom:8px}
.c-title em{
  background:linear-gradient(90deg,var(--acc),var(--acc2));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  font-style:normal}
.c-sub{color:rgba(255,255,255,.6);font-size:12pt;font-weight:300;
  margin-bottom:44px;max-width:450px;line-height:1.5}
.c-rule{width:48px;height:3px;background:linear-gradient(90deg,var(--acc),var(--acc2));
  border-radius:2px;margin-bottom:38px}
/* Stats row */
.c-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:0}
.c-stat{
  background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);
  border-radius:12px;padding:16px 18px;
}
.c-stat-val{font-size:20pt;font-weight:700;color:#fff;line-height:1;margin-bottom:4px}
.c-stat-val.green{color:var(--green)}
.c-stat-val.amber{color:var(--acc)}
.c-stat-label{font-size:7pt;color:rgba(255,255,255,.45);text-transform:uppercase;
  letter-spacing:1px;font-weight:600}
/* Bottom strip */
.c-bottom{
  position:relative;z-index:2;
  padding:18px 60px;
  border-top:1px solid rgba(255,255,255,.07);
  display:flex;justify-content:space-between;align-items:center;
}
.c-bottom-l{color:rgba(255,255,255,.4);font-size:8pt}
.c-bottom-r{display:flex;gap:8px}
.badge{background:rgba(255,255,255,.08);color:rgba(255,255,255,.65);
  font-size:7.5pt;padding:4px 10px;border-radius:20px;font-weight:500}

/* ── PAGE HEADER ─────────────────────────────── */
.ph{
  background:var(--bd);color:rgba(255,255,255,.5);
  font-size:7.5pt;letter-spacing:1.5px;text-transform:uppercase;
  padding:9px 58px;display:flex;justify-content:space-between;
}
.ph em{color:var(--acc);font-style:normal}

/* ── CONTENT ─────────────────────────────────── */
.content{padding:40px 58px;width:210mm;max-width:210mm;overflow:hidden}
p{margin-bottom:11px}
strong{color:var(--bd)}
a{color:var(--bl)}
code{font-family:'JetBrains Mono',monospace;background:#f1f5f9;color:#0f172a;
  padding:1px 5px;border-radius:4px;font-size:7.5pt;
  word-break:break-all;overflow-wrap:anywhere}

/* HEADINGS */
h2{font-size:14.5pt;font-weight:700;color:var(--bd);margin-top:36px;margin-bottom:12px;
  padding-bottom:9px;border-bottom:2px solid var(--bl);
  display:flex;align-items:center;gap:10px;page-break-after:avoid}
.sn{background:var(--bl);color:#fff;font-size:8pt;font-weight:700;
  padding:2px 9px;border-radius:10px}
h3{font-size:10.5pt;font-weight:600;color:var(--bm);margin-top:20px;
  margin-bottom:8px;page-break-after:avoid}

/* ARCH IMAGE */
.arch-img{width:100%;border-radius:10px;margin:16px 0;
  border:1px solid var(--br);box-shadow:0 4px 16px rgba(0,0,0,.06)}

/* TOPOLOGY BOX */
.topology{
  background:var(--cb);border-radius:10px;padding:14px 18px;margin:16px 0;
  font-family:'JetBrains Mono',monospace;font-size:7.5pt;line-height:1.8;
  color:#64748b;page-break-inside:avoid;
  overflow:hidden;white-space:pre-wrap;word-break:break-all;
  max-width:100%
}
.topology .svc{color:#67e8f9}
.topology .ip{color:#86efac}
.topology .res{color:#f9a8d4}
.topology .note{color:#475569}

/* KPI CARDS */
.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:18px 0}
.kpi{border:1px solid var(--br);border-radius:10px;padding:14px 15px;text-align:center;
  background:linear-gradient(135deg,#f8fafc,#fff)}
.kpi-val{font-size:17pt;font-weight:700;color:var(--bd);line-height:1}
.kpi-label{font-size:7.5pt;color:var(--mu);margin-top:4px;font-weight:500;
  text-transform:uppercase;letter-spacing:.5px}
.kpi-sub{font-size:8pt;color:var(--ok);font-weight:600;margin-top:2px}
.kpi.warn .kpi-val{color:var(--warn)}
.kpi.danger .kpi-val{color:var(--danger)}
.kpi.ok .kpi-val{color:var(--ok)}

/* SPEC TABLE */
.spec-wrap{border:1px solid var(--br);border-radius:10px;overflow:hidden;
  margin:14px 0;page-break-inside:avoid;width:100%}
.spec-header{background:linear-gradient(90deg,var(--bd),var(--bm));color:#fff;
  padding:9px 16px;font-size:9pt;font-weight:600;
  display:flex;justify-content:space-between;align-items:center}
.spec-badge{background:rgba(255,255,255,.18);font-size:7.5pt;
  padding:2px 8px;border-radius:8px;white-space:nowrap}
table{width:100%;border-collapse:collapse;font-size:8.5pt;
  table-layout:fixed;word-break:break-word}
thead th{background:#1e3a5f;color:#fff;padding:8px 12px;text-align:left;font-weight:600;
  word-break:normal}
tbody td{padding:6px 12px;border-bottom:1px solid var(--br);vertical-align:top;
  word-break:break-word;overflow-wrap:anywhere}
tbody tr:nth-child(even) td{background:#f8fafc}
tbody tr:last-child td{border-bottom:none}
td:first-child{color:var(--mu);font-weight:500;width:32%;white-space:nowrap}
td:last-child{color:var(--tx);font-weight:400}

/* STATUS PILL */
.pill{display:inline-flex;align-items:center;gap:5px;padding:2px 9px;
  border-radius:12px;font-size:8pt;font-weight:600}
.pill-green{background:#dcfce7;color:#065f46}
.pill-red{background:#fee2e2;color:#991b1b}
.pill-yellow{background:#fef9c3;color:#713f12}
.pill-dot{width:6px;height:6px;border-radius:50%}
.pill-green .pill-dot{background:#16a34a}
.pill-red .pill-dot{background:#dc2626}
.pill-yellow .pill-dot{background:#ca8a04}

/* ALERT BOXES */
.alert{border-radius:8px;padding:12px 16px;margin:14px 0;
  display:flex;align-items:flex-start;gap:11px;font-size:9.5pt;page-break-inside:avoid}
.ai{font-size:13pt;flex-shrink:0;padding-top:1px}
.ab .at{font-weight:700;margin-bottom:2px}
.alert-warn{background:#fffbeb;border:1px solid #fde68a;color:#92400e}
.alert-warn .at{color:#b45309}
.alert-ok{background:#f0fdf4;border:1px solid #bbf7d0;color:#065f46}
.alert-ok .at{color:#15803d}
.alert-info{background:#eff6ff;border:1px solid #bfdbfe;color:#1e40af}
.alert-info .at{color:#1d4ed8}

/* CODE BLOCK */
pre{background:var(--cb);color:var(--ct);border-radius:8px;padding:12px 16px;
  font-family:'JetBrains Mono',monospace;font-size:7.5pt;line-height:1.6;
  white-space:pre-wrap;word-break:break-all;overflow-wrap:anywhere;
  margin:12px 0;page-break-inside:avoid;max-width:100%;overflow:hidden}
pre .kw{color:#93c5fd}
pre .str{color:#86efac}
pre .cmt{color:#475569}

/* PORT TABLE */
.port-ok{color:var(--ok);font-weight:600}
.port-warn{color:var(--warn);font-weight:600}

/* COST ROW */
.cost-total td{background:#fef3c7 !important;font-weight:700;color:#92400e}

/* FOOTER */
hr{border:none;border-top:1px solid var(--br);margin:26px 0}
.pf{margin-top:44px;padding-top:13px;border-top:1px solid var(--br);
  display:flex;justify-content:space-between;font-size:8pt;color:var(--mu)}
</style>
</head>
<body>

<!-- ═══ COVER ═══════════════════════════════════════════════════════════ -->
<div class="cover">
  <div class="dc dc1"></div><div class="dc dc2"></div><div class="dc dc3"></div>
  <div class="grid-overlay"></div>

  <div class="c-top">
    <div class="c-logo"><em>Radar</em>PNCP</div>
    <div class="c-chip">Infraestrutura AWS &mdash; Julho 2026</div>
  </div>

  <div class="c-main">
    <div class="c-eyebrow">Documentacao Tecnica de Infraestrutura Cloud</div>
    <div class="c-title">AWS<br/><em>Infrastructure</em><br/>Report</div>
    <p class="c-sub">Especificacoes completas dos recursos provisionados na Amazon Web Services para o projeto RadarPNCP.</p>
    <div class="c-rule"></div>
    <div class="c-stats">
      <div class="c-stat">
        <div class="c-stat-val green">t3.medium</div>
        <div class="c-stat-label">EC2 Instance</div>
      </div>
      <div class="c-stat">
        <div class="c-stat-val">4 GB</div>
        <div class="c-stat-label">RAM Total</div>
      </div>
      <div class="c-stat">
        <div class="c-stat-val amber">4.8 GB</div>
        <div class="c-stat-label">Dados no S3</div>
      </div>
      <div class="c-stat">
        <div class="c-stat-val">~$50</div>
        <div class="c-stat-label">Custo/mes USD</div>
      </div>
    </div>
  </div>

  <div class="c-bottom">
    <span class="c-bottom-l">eEDB-016 &middot; Escola Politecnica da USP &middot; Account: 089445119491</span>
    <div class="c-bottom-r">
      <span class="badge">us-east-1</span>
      <span class="badge">Neo4j &middot; PostgreSQL &middot; S3</span>
    </div>
  </div>
</div>

<!-- ═══ HEADER BAR ═══════════════════════════════════════════════════════ -->
<div class="ph">
  <span>RadarPNCP &mdash; Infraestrutura AWS</span>
  <span>eEDB-016 &middot; Escola Politecnica da USP &middot; <em>Julho 2026</em></span>
</div>

<div class="content">

<!-- ARCH IMAGE -->
<h2><span class="sn">TOPOLOGIA</span> Arquitetura Geral</h2>
<img class="arch-img" src="beautiful_arch.png" alt="Arquitetura AWS"/>

<!-- TOPOLOGY ASCII -->
<div class="topology">
<span class="note">AWS Region: us-east-1 (N. Virginia) | Account: 089445119491</span><br/>
<span class="note">VPC: vpc-0da7d8e58d69c379c | CIDR: 172.31.0.0/16 | IGW: igw-0b8e038bbb3a06c0b</span><br/><br/>
<span class="svc">S3: radarpncp-hub-dados</span>         <span class="note">4.8 GB (Receita Federal CSVs)</span><br/>
<span class="svc">S3: radarpncp-athena-results</span>     <span class="note">Resultados Athena (reservado)</span><br/><br/>
&#x250C;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2510;<br/>
&#x2502; <span class="svc">EC2: RadarPNCP-Neo4j</span>  (<span class="res">t3.medium / 4GB</span>)           &#x2502;<br/>
&#x2502; IP: <span class="ip">100.59.221.217</span>  AZ: us-east-1b              &#x2502;<br/>
&#x2502; Docker &rarr; Neo4j 5 &nbsp; :7474 Browser &nbsp; :7687 Bolt &#x2502;<br/>
&#x2502; SG: neo4j_sg (22, 7474, 7687 abertas)           &#x2502;<br/>
&#x251C;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2524;<br/>
&#x2502; <span class="svc">RDS: radarpncp-gold-db</span> (<span class="res">db.t3.micro / 1GB</span>)         &#x2502;<br/>
&#x2502; PostgreSQL 18.3 &nbsp; AZ: us-east-1c &nbsp; :5432         &#x2502;<br/>
&#x2502; SG: default (5432 aberta publicamente)           &#x2502;<br/>
&#x2514;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2500;&#x2518;
</div>

<!-- KPIs -->
<div class="kpi-row">
  <div class="kpi ok"><div class="kpi-val">2 vCPU</div><div class="kpi-label">EC2 Compute</div><div class="kpi-sub">t3.medium</div></div>
  <div class="kpi ok"><div class="kpi-val">4 GB</div><div class="kpi-label">RAM EC2</div><div class="kpi-sub">Neo4j + OS</div></div>
  <div class="kpi"><div class="kpi-val">20 GB</div><div class="kpi-label">EBS gp3</div><div class="kpi-sub">3000 IOPS</div></div>
  <div class="kpi warn"><div class="kpi-val">~$50</div><div class="kpi-label">Custo/mes</div><div class="kpi-sub">USD estimado</div></div>
</div>

<!-- EC2 -->
<h2><span class="sn">EC2</span> Instancia RadarPNCP-Neo4j</h2>

<div class="spec-wrap">
  <div class="spec-header">Especificacoes da Instancia <span class="spec-badge">t3.medium &bull; RUNNING</span></div>
  <table>
    <tbody>
      <tr><td>Instance ID</td><td><code>i-03d3f044e8ede0bca</code></td></tr>
      <tr><td>Tipo / RAM / vCPUs</td><td><code>t3.medium</code> &mdash; <strong>4 GB RAM</strong>, 2 vCPUs (Burstable)</td></tr>
      <tr><td>Arquitetura</td><td>x86_64 &mdash; Linux/UNIX (Ubuntu 22.04 LTS)</td></tr>
      <tr><td>AMI</td><td><code>ami-0a02a779008fa3b99</code></td></tr>
      <tr><td>Estado</td><td><span class="pill pill-green"><span class="pill-dot"></span>running</span></td></tr>
      <tr><td>Iniciada em</td><td>08/07/2026 &agrave;s 14:32 UTC</td></tr>
      <tr><td>Regiao / AZ</td><td><code>us-east-1</code> / <code>us-east-1b</code></td></tr>
      <tr><td>IP Publico</td><td><code>100.59.221.217</code></td></tr>
      <tr><td>DNS Publico</td><td><code>ec2-100-59-221-217.compute-1.amazonaws.com</code></td></tr>
      <tr><td>IP Privado</td><td><code>172.31.9.197</code></td></tr>
      <tr><td>VPC / Subnet</td><td><code>vpc-0da7d8e58d69c379c</code> / <code>subnet-06b090d44ec12cae3</code> (172.31.0.0/20)</td></tr>
      <tr><td>Key Pair</td><td><code>vockey</code> (RSA)</td></tr>
      <tr><td>Security Group</td><td><code>sg-0807c93cf1fb07789</code> &mdash; neo4j_sg</td></tr>
    </tbody>
  </table>
</div>

<h3>Volume EBS</h3>
<div class="spec-wrap">
  <table>
    <tbody>
      <tr><td>Volume ID</td><td><code>vol-096ba68536bd5069e</code></td></tr>
      <tr><td>Tipo / Tamanho</td><td><code>gp3</code> &mdash; 20 GB</td></tr>
      <tr><td>IOPS / Throughput</td><td>3.000 IOPS &mdash; 125 MB/s (garantido)</td></tr>
      <tr><td>Device</td><td><code>/dev/sda1</code> (root)</td></tr>
    </tbody>
  </table>
</div>

<h3>Regras de Acesso &mdash; Security Group neo4j_sg</h3>
<div class="spec-wrap">
  <div class="spec-header">Inbound Rules <span class="spec-badge">sg-0807c93cf1fb07789</span></div>
  <table>
    <thead><tr><th>Porta</th><th>Protocolo</th><th>Origem</th><th>Servico</th></tr></thead>
    <tbody>
      <tr><td><code>22</code></td><td>TCP</td><td class="port-warn">0.0.0.0/0</td><td>SSH (acesso remoto)</td></tr>
      <tr><td><code>7474</code></td><td>TCP</td><td>0.0.0.0/0</td><td class="port-ok">Neo4j Browser (HTTP)</td></tr>
      <tr><td><code>7687</code></td><td>TCP</td><td>0.0.0.0/0</td><td class="port-ok">Neo4j Bolt Driver</td></tr>
    </tbody>
  </table>
</div>

<div class="alert alert-warn">
  <div class="ai">&#9888;</div>
  <div class="ab">
    <div class="at">SSH Aberto para Internet</div>
    A porta 22 esta exposta para 0.0.0.0/0. Em producao, substituir por AWS Systems Manager Session Manager (sem SSH publico) ou restringir ao IP corporativo especifico.
  </div>
</div>

<!-- RDS -->
<h2><span class="sn">RDS</span> PostgreSQL &mdash; Gold Layer</h2>

<div class="spec-wrap">
  <div class="spec-header">radarpncp-gold-db <span class="spec-badge">db.t3.micro &bull; AVAILABLE</span></div>
  <table>
    <tbody>
      <tr><td>Identifier</td><td><code>radarpncp-gold-db</code></td></tr>
      <tr><td>Classe / RAM</td><td><code>db.t3.micro</code> &mdash; 1 GB RAM, 2 vCPUs</td></tr>
      <tr><td>Engine</td><td>PostgreSQL <code>18.3</code></td></tr>
      <tr><td>Endpoint</td><td><code>radarpncp-gold-db.crlngyuimjw7.us-east-1.rds.amazonaws.com:5432</code></td></tr>
      <tr><td>Usuario Master</td><td><code>postgres</code></td></tr>
      <tr><td>Storage</td><td>20 GB &mdash; <code>gp2</code> (SSD)</td></tr>
      <tr><td>Encriptacao</td><td><span class="pill pill-red"><span class="pill-dot"></span>Nao</span></td></tr>
      <tr><td>Acesso Publico</td><td><span class="pill pill-yellow"><span class="pill-dot"></span>Sim (ambiente academico)</span></td></tr>
      <tr><td>AZ</td><td><code>us-east-1c</code></td></tr>
      <tr><td>Multi-AZ</td><td><span class="pill pill-red"><span class="pill-dot"></span>Nao</span></td></tr>
      <tr><td>Backup Retention</td><td>0 dias (sem backup automatico)</td></tr>
      <tr><td>Parameter Group</td><td><code>default.postgres18</code></td></tr>
      <tr><td>Security Group</td><td><code>sg-0bfd0d5393863161b</code> &mdash; default (porta 5432 aberta)</td></tr>
      <tr><td>Status</td><td><span class="pill pill-green"><span class="pill-dot"></span>available</span></td></tr>
    </tbody>
  </table>
</div>

<h3>Connection String Python</h3>
<pre><span class="kw">import</span> psycopg2

conn = psycopg2.connect(
    host=<span class="str">"radarpncp-gold-db.crlngyuimjw7.us-east-1.rds.amazonaws.com"</span>,
    port=5432,
    dbname=<span class="str">"postgres"</span>,
    user=<span class="str">"postgres"</span>,
    password=<span class="str">"&lt;senha_configurada&gt;"</span>
)</pre>

<!-- S3 -->
<h2><span class="sn">S3</span> Data Lake &mdash; Buckets</h2>

<div class="spec-wrap">
  <div class="spec-header">radarpncp-hub-dados-a2e68685 <span class="spec-badge">~4.8 GB</span></div>
  <table>
    <thead><tr><th>Arquivo</th><th>Tamanho</th><th>Modificado</th></tr></thead>
    <tbody>
      <tr><td><code>receita_federal/K3241.K03200Y0.D50510.EMPRECSV.csv</code></td><td>1,6 GB</td><td>08/07/2026 13:29</td></tr>
      <tr><td><code>receita_federal/K3241.K03200Y0.D60613.EMPRECSV.csv</code></td><td>2,1 GB</td><td>08/07/2026 14:20</td></tr>
      <tr><td><code>receita_federal/K3241.K03200Y1.D60613.EMPRECSV.csv</code></td><td>311 MB</td><td>08/07/2026 14:26</td></tr>
      <tr><td><code>receita_federal/K3241.K03200Y2.D60613.EMPRECSV.csv</code></td><td>328 MB</td><td>08/07/2026 14:27</td></tr>
      <tr><td><code>receita_federal/K3241.K03200Y3.D60613.EMPRECSV.csv</code></td><td>333 MB</td><td>08/07/2026 14:28</td></tr>
    </tbody>
  </table>
</div>

<div class="spec-wrap">
  <div class="spec-header">radarpncp-athena-results-a2e68685 <span class="spec-badge">Athena / Reservado</span></div>
  <table>
    <tbody>
      <tr><td>Uso</td><td>Resultados de queries Amazon Athena (reservado para expansao)</td></tr>
      <tr><td>Versioning</td><td>Desativado</td></tr>
      <tr><td>Criado em</td><td>08/07/2026 02:24 UTC</td></tr>
    </tbody>
  </table>
</div>

<!-- NETWORK -->
<h2><span class="sn">REDE</span> VPC, Subnets e Internet Gateway</h2>

<div class="spec-wrap">
  <div class="spec-header">Subnets Disponiveis <span class="spec-badge">vpc-0da7d8e58d69c379c</span></div>
  <table>
    <thead><tr><th>Subnet ID</th><th>CIDR</th><th>AZ</th><th>IPs Livres</th></tr></thead>
    <tbody>
      <tr><td><code>subnet-07c3894de41615ae9</code></td><td>172.31.32.0/20</td><td>us-east-1a</td><td>4.091</td></tr>
      <tr><td><code>subnet-06b090d44ec12cae3</code> &#9733;</td><td>172.31.0.0/20</td><td>us-east-1b</td><td>4.090</td></tr>
      <tr><td><code>subnet-09a8adb227bee398e</code></td><td>172.31.80.0/20</td><td>us-east-1c</td><td>4.090</td></tr>
      <tr><td><code>subnet-02fcf691b6fc8b482</code></td><td>172.31.16.0/20</td><td>us-east-1d</td><td>4.091</td></tr>
      <tr><td><code>subnet-06165d60348b47018</code></td><td>172.31.48.0/20</td><td>us-east-1e</td><td>4.091</td></tr>
      <tr><td><code>subnet-0ed00d3048f712014</code></td><td>172.31.64.0/20</td><td>us-east-1f</td><td>4.091</td></tr>
    </tbody>
  </table>
</div>
<p style="font-size:8.5pt;color:var(--mu)">&#9733; Subnet em uso pela EC2 RadarPNCP-Neo4j</p>

<div class="alert alert-info">
  <div class="ai">&#128204;</div>
  <div class="ab">
    <div class="at">Elastic IP Nao Associado</div>
    O EIP <code>34.197.181.255</code> (AllocationId: eipalloc-017e9ca6702d76a6d) esta alocado mas nao associado a nenhuma instancia, gerando cubranca de aproximadamente <strong>$3,60/mes</strong>. Liberar se nao for utilizado.
  </div>
</div>

<!-- IAM -->
<h2><span class="sn">IAM</span> Funcao de Execucao</h2>

<div class="spec-wrap">
  <div class="spec-header">LabRole <span class="spec-badge">Funcao Principal</span></div>
  <table>
    <tbody>
      <tr><td>ARN</td><td><code>arn:aws:iam::089445119491:role/LabRole</code></td></tr>
      <tr><td>Policies</td><td>AmazonSSMManagedInstanceCore &middot; AmazonEKSClusterPolicy &middot; AmazonEC2ContainerRegistryReadOnly &middot; VocLabPolicy1/2/3</td></tr>
      <tr><td>Key Pair</td><td><code>vockey</code> (RSA) &mdash; ID: key-00a13bc20484b26b9</td></tr>
    </tbody>
  </table>
</div>

<!-- COSTS -->
<h2><span class="sn">CUSTO</span> Estimativa Mensal</h2>

<div class="spec-wrap">
  <table>
    <thead><tr><th>Recurso</th><th>Tipo</th><th>USD/hora</th><th>USD/mes estimado</th></tr></thead>
    <tbody>
      <tr><td>EC2</td><td>t3.medium</td><td>$0,0416</td><td>~$30,00</td></tr>
      <tr><td>RDS</td><td>db.t3.micro</td><td>$0,0170</td><td>~$12,24</td></tr>
      <tr><td>EBS gp3</td><td>20 GB</td><td>&mdash;</td><td>~$1,60</td></tr>
      <tr><td>RDS Storage gp2</td><td>20 GB</td><td>&mdash;</td><td>~$2,30</td></tr>
      <tr><td>S3</td><td>~5 GB</td><td>&mdash;</td><td>~$0,12</td></tr>
      <tr><td>Elastic IP livre</td><td>eipalloc-017e9ca</td><td>$0,005</td><td>~$3,60</td></tr>
      <tr class="cost-total"><td><strong>Total estimado</strong></td><td></td><td></td><td><strong>~$49,86/mes</strong></td></tr>
    </tbody>
  </table>
</div>

<!-- SCALE -->
<h2><span class="sn">ESCALA</span> Recomendacoes para Producao</h2>

<div class="spec-wrap">
  <table>
    <thead><tr><th>Componente</th><th>Atual (Academico)</th><th>Producao Sugerida</th></tr></thead>
    <tbody>
      <tr><td>EC2 (Neo4j)</td><td>t3.medium &mdash; 4 GB</td><td>r5.xlarge &mdash; 32 GB</td></tr>
      <tr><td>RDS (Postgres)</td><td>db.t3.micro &mdash; 1 GB</td><td>db.r5.large &mdash; 16 GB</td></tr>
      <tr><td>EBS</td><td>20 GB gp3</td><td>500 GB gp3 + snapshots</td></tr>
      <tr><td>RDS Storage</td><td>20 GB gp2</td><td>200 GB gp3 + Multi-AZ</td></tr>
      <tr><td>Backup</td><td>Sem backup</td><td>7 dias retencao + PITR</td></tr>
      <tr><td>Encriptacao</td><td>Nao</td><td>KMS habilitado em tudo</td></tr>
      <tr><td>SSH Publico</td><td>0.0.0.0/0 aberto</td><td>Somente SSM Session Manager</td></tr>
      <tr><td>Custo estimado</td><td>~$50/mes</td><td>~$800/mes</td></tr>
    </tbody>
  </table>
</div>

<div class="alert alert-ok">
  <div class="ai">&#10003;</div>
  <div class="ab">
    <div class="at">Ambiente Academico &mdash; Boa Relacao Custo/Beneficio</div>
    Para a PoC com 200 contratos e as 7 consultas analiticas exigidas, a configuracao atual (t3.medium + db.t3.micro) e suficiente e economica. O Neo4j com 4 GB de RAM processa grafos com centenas de nos sem degradacao de performance mensuravel.
  </div>
</div>

<hr/>
<div class="pf">
  <span>RadarPNCP &middot; AWS Infrastructure Report &middot; eEDB-016 &middot; 2026</span>
  <span>Coletado via boto3 &middot; 08/07/2026 14:21 &middot; Account: 089445119491</span>
</div>

</div>
</body>
</html>"""

HTML_F.write_text(HTML, encoding='utf-8')
print(f"HTML: {HTML_F}")

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
result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
if PDF_F.exists() and PDF_F.stat().st_size > 10000:
    print(f"OK: {PDF_F} ({PDF_F.stat().st_size // 1024} KB)")
else:
    print("STDOUT:", result.stdout[:300])
    print("STDERR:", result.stderr[:300])
