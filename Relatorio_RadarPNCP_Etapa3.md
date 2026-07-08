# 📊 Relatório RadarPNCP (Etapa 3) - Dados Reais
> Executado no cluster AWS Neo4j com base extraída do PostgreSQL (Gold) e endereços da Receita Federal via Data Lake (S3/Athena).

## 🕸️ Grafo Interativo Gerado

Eu entrei no seu Neo4j remotamente agora há pouco e rodei a query do grafo.
Aqui está a prova visual de que os dados do PNCP estão conectados através da inteligência em grafos!

![Grafo Renderizado](./neo4j_graph.png)

### 📹 Vídeo do Acesso
*(Vídeo do processo ocultado na versão PDF)*

---

## Q1: Top 10 Contratos por Valor (Por Órgão)
**Órgão Analisado:** `MINISTERIO DA GESTAO E DA INOVACAO EM SERVICOS PUBLICOS`
Esta query identifica os maiores contratos (em volume financeiro) firmados pelo órgão selecionado.

| Órgão | Nº Contrato | Data Assinatura | Valor Global (R$) |
| :--- | :--- | :--- | :--- |
| MINISTERIO DA GESTAO E DA INOVACAO EM SERVICOS PUBLICOS | 00065 | 12/12/2025 | 3.862.241.222,22 |

---

## Q2: Total Contratado por Fornecedor (Mesmo Órgão de Q1)
Total histórico recebido pelos fornecedores que atenderam o órgão analisado.

| Fornecedor | Qtd. Contratos | Valor Total (R$) |
| :--- | :--- | :--- |
| SERVICO FEDERAL DE PROCESSAMENTO DE DADOS (SERPRO) | 1 | 3.862.241.222,22 |

---

## Q3: Concentração de Atendimento (Fornecedores Multi-Órgão)
Identifica fornecedores que detêm capilaridade extrema no governo, fornecendo para múltiplos órgãos simultaneamente.

| Fornecedor | Qtd. de Órgãos Diferentes Atendidos |
| :--- | :--- |
| SERVICO FEDERAL DE PROCESSAMENTO DE DADOS (SERPRO) | 45 órgãos |
| PRIME CONSULTORIA E ASSESSORIA EMPRESARIAL LTDA | 35 órgãos |
| CAIXA ECONOMICA FEDERAL - CEF | 35 órgãos |
| BANCO DO BRASIL SA | 25 órgãos |
| TELEFONICA BRASIL S.A. | 5 órgãos |
| MAXIFROTA SERVIÇOS DE MANUTENÇÃO DE FROTA LTDA | 5 órgãos |
| CRISTALIA PRODUTOS QUIMICOS FARMACEUTICOS LTDA | 3 órgãos |

> [!TIP]
> **Insights:** Empresas estatais (SERPRO, CEF, BB) e grandes provedores de frota/tecnologia (Prime, Telefônica) dominam o atendimento descentralizado em dezenas de órgãos na amostra analisada.

---

## Q4 e Q5: Identificação de Cartel / Monopólio Físico (Mesmo Endereço)
As queries Q4 e Q5 cruzam o endereço matriz/filial (obtido da Receita Federal via Data Lake/Athena) para encontrar fornecedores diferentes operando no **mesmo endereço físico** e prestando serviços para o mesmo órgão.

> [!NOTE]
> **Resultado na amostra de 200 contratos:** Não foram identificadas empresas distintas dividindo o mesmo endereço operando no mesmo órgão. *(A restrição do limite amostral mitigou o aparecimento de fraudes deste tipo nesta execução específica).*

---

## Q6: Volumes Totais por Modalidade
**Modalidade Analisada:** `Inexigibilidade de Licitação` (Dinâmica)
Lista os fornecedores que mais faturaram globalmente dentro de uma mesma modalidade de contratação.

| Fornecedor | Valor Total na Modalidade (R$) |
| :--- | :--- |
| SERVICO FEDERAL DE PROCESSAMENTO DE DADOS (SERPRO) | 8.478.844.194,75 |
| CAIXA ECONOMICA FEDERAL - CEF | 4.108.106.600,86 |
| BANCO DO BRASIL SA | 2.629.355.332,56 |
| PRIME CONSULTORIA E ASSESSORIA EMPRESARIAL LTDA | 2.194.324.881,62 |
| MAXIFROTA SERVIÇOS DE MANUTENÇÃO DE FROTA LTDA | 1.636.850.313,04 |

---

## Q7: Fracionamento de Despesa (Contratos Sucessivos < 30 dias)
Alerta para contratos emitidos pelo mesmo órgão, para o mesmo fornecedor, com um intervalo menor ou igual a 30 dias entre assinaturas (possível burla de limite licitatório).

| Órgão | Fornecedor | Contrato A | Contrato B | Dias de Intervalo |
| :--- | :--- | :--- | :--- | :--- |
| TRIBUNAL DE CONTAS DO ESTADO DO PARANA | TELEFONICA BRASIL S.A. | 799 | 26 | 0 dias |
| INSTITUTO CHICO MENDES (ICMBIO) | MAXIFROTA SERVIÇOS DE FROTA | 3 | 00003 | 0 dias |
| MINISTÉRIO DAS CIDADES | CAIXA ECONOMICA FEDERAL | 00016 | 00008 | 1 dia |
| MINISTÉRIO DAS CIDADES | CAIXA ECONOMICA FEDERAL | 00016 | 00002 | 1 dia |
| MINISTÉRIO DA JUSTICA E SEG. PUB. | SERPRO | 00001 | 00022 | 9 dias |
| MINISTÉRIO DA FAZENDA | SERPRO | 00009 | 00001 | 26 dias |

> [!WARNING]
> **Alerta de Fracionamento:** Múltiplos contratos assinados num intervalo de `0` ou `1` dias identificados! É recomendável que à auditoria verifique se o objeto dos contratos foi fragmentado artificialmente para evitar concorrência mais rigorosa.
