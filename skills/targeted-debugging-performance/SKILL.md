---
name: targeted-debugging-performance
description: Diagnosticar bugs, travamentos, lentidão, crashes e regressões com investigação orientada por evidência sem ler todos os arquivos.
---

# Targeted Debugging & Performance

## Regra central
Não leia todos os arquivos por padrão. Investigue por hipóteses e evidências, expandindo o escopo só quando o caminho de execução exigir.

## Fluxo
1. Capture sintoma, passos para reproduzir, frequência, ambiente, impacto e último estado funcional.
2. Leia primeiro logs/stack trace, erro do console, request que falha, status HTTP, diff recente e arquivo afetado.
3. Mapeie somente dependências chamadas pelo caminho: handler → serviço → repositório → integração.
4. Forme até três hipóteses verificáveis e ordene por probabilidade, impacto e custo de teste.
5. Faça observação/teste pequeno por hipótese. Não reescreva módulos inteiros para tentar.
6. Reproduza com entrada mínima, compare esperado e observado e registre evidência.
7. Corrija a causa raiz com diff pequeno, adicione regressão e rode testes focados.
8. Se faltar evidência, peça o log ou artefato específico em vez de escanear tudo.

## Travamentos
- Frontend: loops de renderização, efeitos incorretos, estado duplicado, listas pesadas, listeners não removidos, requests duplicados.
- Backend: chamadas bloqueantes, timeout ausente, pool esgotado, deadlock, query lenta, fila acumulada e retries sem limite.
- Memória: listeners/handles não liberados, cache sem limite e buffers mantidos em RAM.
- Rede: waterfall, timeout, retry storm, DNS/TLS e dependência indisponível.
- Mobile: thread principal bloqueada, rebuilds, lifecycle, streams não cancelados e I/O na UI thread.

## Medir antes de otimizar
Use profiler, métricas, traces ou benchmark da stack. Compare baseline e resultado; não declare melhoria sem medição. Considere p95/p99, taxa de erro, CPU, memória e bundle conforme aplicável.

Não apague dados/cache nem reinicie produção sem autorização. Entregue causa confirmada ou hipótese, evidência, arquivos/linhas, correção, testes, métrica antes/depois e risco restante.