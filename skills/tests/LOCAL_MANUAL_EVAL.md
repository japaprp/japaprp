# Execução local das avaliações comportamentais (sem API)

O conjunto router-eval-cases.json define cenários esperados, não um benchmark executado. Use este procedimento para observar o comportamento real do agente configurado no Codex / VS Code.

## Requisitos

- Python 3.10+ (somente biblioteca padrão).
- Catálogo de skills disponível no workspace e configurado para o agente.
- Nenhuma chave de API é necessária para o script. O script não chama modelos nem faz requisições de rede.

## Executar

Na raiz do repositório:

```bash
python scripts/run_router_eval.py --list
python scripts/run_router_eval.py --agent "Codex / VS Code" --catalog-revision "$(git rev-parse HEAD)"
```

Para executar um único caso ou um subconjunto:

```bash
python scripts/run_router_eval.py --case route-cross-tenant-auth
python scripts/run_router_eval.py --case route-cross-tenant-auth --case route-duplicate-crud
```

## Procedimento por caso

1. Copie o prompt mostrado pelo script e execute-o no agente-alvo com o catálogo de skills ativo.
2. Observe a skill acionada no trace/contexto do agente. Não adivinhe: se não for possível observar, registre not-observable.
3. Cole a resposta real no terminal e termine a entrada com uma linha separada contendo END_RESPONSE. Digite SKIP como primeira linha se não executou o caso.
4. Julgue cada critério de aceitação e cada comportamento proibido com base na resposta e nas evidências disponíveis. unknown é preferível a uma suposição.
5. O script grava o resultado após cada caso, inclusive se a execução for interrompida com Ctrl+C.

## Estados

- PASS: resposta observada, roteamento correto quando uma skill é exigida, todos os critérios de aceitação atendidos e nenhum comportamento proibido observado.
- FAIL: critério não atendido, comportamento proibido observado ou skill primária divergente da esperada.
- BLOCKED: evidência insuficiente, skill não observável ou alguma checagem marcada unknown.
- NOT_RUN: caso pulado sem resposta avaliada.

O caso de correção simples tem expected_primary_skill null; ele não exige uma skill específica. A opção none é válida se nenhuma skill foi necessária.

## Privacidade e integridade

- Resultados são salvos fora do repositório em ~/.engineering-brain/evals/ para evitar commits acidentais de respostas potencialmente sensíveis.
- Não cole credenciais, tokens, chaves, dados pessoais ou conteúdo confidencial no relatório.
- A saída é evidência registrada pelo avaliador, não uma certificação independente. Para achados importantes, inclua um trace, teste reproduzível ou referência concreta em evidence_notes.
- Não altere o roteador ou as skills durante a execução de uma rodada. Registre os resultados primeiro; depois faça a menor mudança justificada e reexecute os casos afetados.
- Este teste é manual e não tem custo de API; não mede automaticamente o raciocínio do modelo e não deve ser descrito como benchmark estatístico.
