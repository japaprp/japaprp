---
name: code-review-minimal-change
description: Revisar diffs e pull requests por defeitos relevantes e manter a implementação no menor escopo necessário, sem refatoração oportunista.
---

# Code Review & Minimal Change

Use para revisar um diff/PR, preparar uma revisão antes de merge ou implementar uma correção com risco de expansão de escopo. Esta skill complementa o roteador; não substitui segurança, testes ou conhecimento da stack.

## Revisão baseada em evidências

1. Determine o objetivo e os critérios de aceitação a partir da solicitação, issue e contexto do projeto.
2. Leia o diff completo e os trechos necessários ao redor; siga os fluxos afetados quando o contexto não bastar.
3. Priorize defeitos concretos: comportamento incorreto, exposição de dados, autorização ausente, corrupção/perda de dados, concorrência, quebra de contrato, falhas em caminhos críticos e regressões de desempenho.
4. Verifique testes ausentes para comportamentos importantes, limites, falhas e permissões; rode apenas comandos disponíveis e relevantes.
5. Não trate preferência de estilo como defeito quando formatter/linter ou convenções existentes já resolvem isso.
6. Não invente falhas para preencher uma quota. Se não encontrar problemas, diga qual escopo foi revisado e o que não foi testado.

## Severidade e formato dos achados

- **Bloqueador/Crítico:** exploração de segurança, perda/corrupção de dados, bypass de autorização ou falha grave no caminho principal.
- **Alto:** bug provável que afeta funcionalidade importante, compatibilidade ou integridade.
- **Médio/Baixo:** risco localizado, tratamento de erro incompleto, manutenção ou melhoria não bloqueadora.
- **Nit:** preferência cosmética ou alternativa sem impacto demonstrado; omita se não ajudar.

Para cada achado, informe:
- localização precisa (arquivo e linha, se disponível);
- cenário reproduzível e impacto;
- evidência que sustenta a conclusão;
- correção mínima sugerida;
- teste de regressão que comprovaria a correção.

Comece com resumo do escopo e dos riscos principais. Ordene os achados por severidade. Faça uma revisão consolidada em vez de enviar comentários fragmentados.

## Disciplina de mudança mínima

1. Declare o que precisa mudar e o que fica fora do escopo.
2. Corrija o caminho defeituoso sem reescrever módulos vizinhos nem fazer limpeza oportunista.
3. Cada alteração deve ter relação demonstrável com requisito, causa raiz, segurança ou teste necessário.
4. Não adicione abstrações, flags, dependências, comentários ou tratamento hipotético sem benefício comprovado.
5. Preserve contratos, estilo e alterações preexistentes do usuário.
6. Se descobrir um problema real fora do escopo, relate-o como follow-up separado; não o inclua silenciosamente.
7. Antes de concluir, revise o diff para alterações não relacionadas, efeitos colaterais e arquivos acidentalmente modificados.

## Limites e validação

- Não altere produção, dados reais, permissões, segredos ou infraestrutura sem autorização adequada.
- Não enfraqueça testes ou controles para fazer a revisão passar.
- Não afirme que um teste passou sem executar o comando e observar o resultado.
- Separe claramente defeitos confirmados, hipóteses e questões que precisam de contexto.
- A conclusão deve indicar achados, verificações executadas, testes não executados e riscos restantes.
