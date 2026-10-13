---
name: vercel-react-performance
description: Aplicar práticas de desempenho para React e Next.js: waterfalls, data fetching, bundles, renderização e server actions. Use somente em projetos React/Next.js.
---

# React & Next.js Performance

**Referência pública:** [vercel-labs/agent-skills — react-best-practices](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices). Consulte a versão oficial para regras e exemplos detalhados; esta skill é um guia de seleção e execução.

## Gatilho
Use somente quando o projeto realmente usar React ou Next.js. Não aplique padrões React a PHP puro, Flutter ou HTML simples.

## Prioridade de investigação
1. Eliminar waterfalls de rede e chamadas sequenciais que poderiam ser paralelas.
2. Evitar carregar código pesado no caminho inicial; analisar bundle e imports antes de adicionar bibliotecas.
3. Buscar dados na camada apropriada e evitar requests duplicados ou serialização excessiva.
4. Proteger cada mutação server-side com autenticação e autorização no próprio endpoint/action; layout e middleware não substituem verificação da operação.
5. Evitar renders desnecessários apenas quando medição ou análise do fluxo justificar a otimização.
6. Considerar streaming, cache e deduplicação conforme framework e semântica dos dados.
7. Otimizar listas e DOM grandes; não usar memoização indiscriminadamente.
8. Medir antes/depois com profiler, bundle analyzer, traces ou Web Vitals.

## Método econômico
- Inspecione package.json, rotas e componentes do caminho afetado.
- Busque o símbolo ou request problemático antes de abrir arquivos amplos.
- Forme uma hipótese e use profiler/teste específico.
- Faça diff pequeno e valide funcionalidade, segurança e desempenho.
- Não introduza cache sem definir invalidação, escopo por usuário e consistência.

## Entrega
Indique gargalo comprovado, evidência, arquivos afetados, mudança, testes e métrica antes/depois. Se não houver medição, declare que a melhoria é esperada, não comprovada.