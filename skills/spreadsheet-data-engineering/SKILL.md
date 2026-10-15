---
name: spreadsheet-data-engineering
description: Criar, auditar, transformar e automatizar planilhas e arquivos tabulares com integridade, rastreabilidade e validação.
---

# Spreadsheet & Tabular Data Engineering

## Objetivo
Resolver tarefas com Excel, CSV, TSV e formatos tabulares sem confundir planilhas com banco de dados nem alterar silenciosamente os dados de origem.

## Fluxo
1. Identifique o arquivo, formato, volume, objetivo, colunas, regras de negócio e formato de saída esperado.
2. Inspecione uma amostra e o esquema antes de transformar: cabeçalhos, tipos, nulos, duplicatas, codificação, delimitador, datas, moeda, separador decimal e fórmulas.
3. Preserve o original. Gere uma cópia/novo arquivo por padrão; sobrescreva somente quando explicitamente solicitado.
4. Escolha a ferramenta disponível adequada ao formato e volume. Não presuma que bibliotecas, Excel instalado ou conectores estejam disponíveis.
5. Defina validações antes da transformação: contagem de linhas, unicidade, totais, faixas, chaves, fórmulas e regras cruzadas.
6. Para CSV, confirme UTF-8/codificação, delimitador, aspas, quebras de linha e tratamento de células que começam com =, +, - ou @ quando o arquivo será aberto em planilhas (risco de formula injection).
7. Em fórmulas, verifique referências, intervalos, erros e compatibilidade da versão. Não alegue recálculo de fórmulas se a ferramenta não calculou os resultados.
8. Em dados financeiros, confirme unidade monetária, arredondamento, precisão decimal, sinal e reconciliação de totais.
9. Em dados pessoais ou sensíveis, minimize campos, não exponha amostras no log e use somente destinos autorizados.
10. Compare entrada e saída e informe linhas processadas, linhas rejeitadas, validações realizadas e limitações.

## Práticas de qualidade
- Evite converter identificadores em números; preserve zeros à esquerda e valores como códigos postais.
- Normalize datas/timezones explicitamente e não infira datas ambíguas sem declarar a regra.
- Não remova duplicatas sem definir a chave e a regra de sobrevivência.
- Prefira transformações reproduzíveis e scripts reutilizáveis para tarefas recorrentes.
- Para grandes volumes, avalie memória e processamento incremental.
- Não envie planilhas, e-mails ou arquivos a terceiros sem autorização.

## Entrega
Informe arquivo de saída confirmado, mudanças realizadas, resumo de validações e quaisquer perdas, linhas excluídas ou suposições. Nunca invente uma validação ou um arquivo gerado.
