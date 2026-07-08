"""
Converte README.md em PDF com estilo profissional.
Usa: markdown + xhtml2pdf
"""
import markdown
import os
from pathlib import Path

README_PATH = Path("README.md")
OUTPUT_PDF  = Path("README_RadarPNCP.pdf")

# Lê o Markdown
md_text = README_PATH.read_text(encoding="utf-8")

# Converte Markdown → HTML
body_html = markdown.markdown(
    md_text,
    extensions=["fenced_code", "tables", "codehilite", "toc"]
)

# Template HTML completo com CSS bonito
html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8"/>
  <style>
    @page {{
      size: A4;
      margin: 2cm 2.2cm 2cm 2.2cm;
    }}
    body {{
      font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
      font-size: 10.5pt;
      line-height: 1.65;
      color: #222;
    }}
    h1 {{ font-size: 20pt; color: #1a237e; border-bottom: 2px solid #1a237e; padding-bottom: 6px; margin-top: 0; }}
    h2 {{ font-size: 14pt; color: #283593; border-bottom: 1px solid #c5cae9; padding-bottom: 4px; margin-top: 24px; }}
    h3 {{ font-size: 11.5pt; color: #37474f; margin-top: 16px; }}
    h4 {{ font-size: 10.5pt; color: #546e7a; }}
    a  {{ color: #1565c0; }}
    pre {{
      background: #f5f5f5;
      border: 1px solid #ddd;
      border-left: 4px solid #1a237e;
      padding: 10px 14px;
      font-size: 8.5pt;
      font-family: "Courier New", monospace;
      white-space: pre-wrap;
      word-wrap: break-word;
      border-radius: 3px;
    }}
    code {{
      background: #f0f0f0;
      padding: 1px 4px;
      border-radius: 2px;
      font-size: 9pt;
      font-family: "Courier New", monospace;
    }}
    blockquote {{
      border-left: 4px solid #42a5f5;
      margin: 0;
      padding: 6px 14px;
      background: #e3f2fd;
      color: #1a237e;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 9.5pt;
      margin: 12px 0;
    }}
    th {{
      background: #1a237e;
      color: white;
      padding: 6px 10px;
      text-align: left;
    }}
    td {{
      border: 1px solid #ddd;
      padding: 5px 10px;
    }}
    tr:nth-child(even) td {{
      background: #f5f5f5;
    }}
    hr {{
      border: none;
      border-top: 1px solid #e0e0e0;
      margin: 18px 0;
    }}
    img {{
      max-width: 100%;
      border-radius: 4px;
      margin: 8px auto;
      display: block;
    }}
    p {{ margin: 8px 0; }}
    ul, ol {{ margin: 8px 0 8px 20px; }}
    li {{ margin-bottom: 3px; }}
    strong {{ color: #1a237e; }}
  </style>
</head>
<body>
{body_html}
</body>
</html>
"""

# Salva HTML temporário
html_path = Path("readme_temp.html")
html_path.write_text(html, encoding="utf-8")

# Tenta gerar PDF com xhtml2pdf
try:
    from xhtml2pdf import pisa
    with open(OUTPUT_PDF, "wb") as pdf_file:
        result = pisa.CreatePDF(html, dest=pdf_file, encoding="utf-8")
    if result.err:
        print(f"Erro ao gerar PDF: {result.err}")
    else:
        size_kb = OUTPUT_PDF.stat().st_size // 1024
        print(f"PDF gerado com sucesso: {OUTPUT_PDF} ({size_kb} KB)")
        html_path.unlink(missing_ok=True)
except ImportError:
    print("xhtml2pdf não encontrado. PDF não gerado.")
    print(f"HTML salvo em: {html_path}")
