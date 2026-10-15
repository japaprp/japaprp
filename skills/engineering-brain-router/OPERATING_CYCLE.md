# Engineering Brain — ciclo operacional

Este documento transforma o roteador em um protocolo repetível de execução. Ele complementa o roteador; não substitui as skills de domínio.

## Ciclo de trabalho

### 1. Intake e classificação

Registre mentalmente ou no template de execução:
- objetivo e resultado observável esperado;
- repositório, branch, ambiente e stack confirmados;
- restrições explícitas: orçamento, prazo, compatibilidade, privacidade;
- risco: baixo, médio ou alto;
- limites de autorização e ações que exigem confirmação.

Se uma informação ausente mudar uma decisão irreversível ou de alto impacto, pergunte antes. Para incerteza reversível, declare a suposição e continue.

### 2. Plano mínimo e critérios de aceitação

Antes de editar:
1. inspecione instruções locais, estado/diff, entrypoints e testes relacionados;
2. selecione uma skill principal e somente complementares necessárias;
3. escreva de 1 a 5 passos, proporcionais ao escopo;
4. defina como cada critério será verificado;
5. identifique rollback ou proteção para mudanças de alto risco.

Não crie plano extenso para correção trivial. Não trate uma lista de tarefas como evidência de execução.

### 3. Execução controlada

- Trabalhe em pequenos incrementos que possam ser revisados.
- Preserve alterações preexistentes do usuário e contratos públicos.
- Prefira leitura antes de escrita e comandos não destrutivos antes dos destrutivos.
- Não leia nem carregue o catálogo inteiro; busque apenas o contexto necessário.
- Não introduza serviços pagos, dependências ou mudanças de infraestrutura sem justificar custo e obter autorização adequada.
- Pare e peça confirmação quando o próximo passo exceder a autorização recebida.

### 4. Verificação por camadas

Execute somente verificações disponíveis e relevantes, nesta ordem típica:
1. **Integridade:** diff, arquivos tocados, formato e ausência de segredos acidentais.
2. **Foco:** teste, lint, typecheck ou reprodução diretamente relacionados à mudança.
3. **Regressão:** testes de fluxos adjacentes e contratos afetados.
4. **Integração/produção:** apenas quando o ambiente, as credenciais e a autorização permitirem; preferir staging e dados sintéticos.
5. **Resultado externo:** confirmar via log, URL, estado persistido, resposta ou artefato real.

Marque cada critério como `PASS`, `FAIL`, `BLOCKED` ou `NOT RUN`. Um teste não executado nunca é `PASS`. Um build verde não prova sozinho que o comportamento de negócio está correto.

### 5. Revisão e entrega

Antes de concluir:
- confira o diff final e os arquivos modificados;
- confirme que os critérios de aceitação têm evidências proporcionais;
- reveja segurança, dados, compatibilidade, custos e rollback conforme o risco;
- informe o que foi feito, o que foi testado e o que não pôde ser comprovado;
- forneça o menor próximo passo se algo estiver bloqueado.

### 6. Aprendizado baseado em evidência

Após a verificação, registre somente o necessário:
- sintoma/objetivo e contexto técnico não sensível;
- hipótese inicial e evidência que a confirmou ou refutou;
- causa-raiz, quando conhecida;
- testes que detectaram ou deixaram escapar o problema;
- mudança feita e resultado observado;
- oportunidade de melhoria e confiança na conclusão.

Classifique a lição:
- **Caso isolado:** corrigir o projeto, sem alterar skill geral.
- **Lacuna de procedimento:** propor melhoria na skill de domínio existente.
- **Erro de roteamento:** ajustar regras/evals do roteador.
- **Falha repetível de validação:** adicionar teste automatizado ou caso de avaliação.
- **Evidência insuficiente:** melhorar observabilidade ou critério de aceitação, sem inventar uma causa.

Uma única falha não justifica automaticamente uma nova skill. Procure sobreposição antes de criar conteúdo novo. Registre o resultado observado antes de propor a alteração.

### 7. Aprovação e evolução

- Aprender não significa autoeditar-se em silêncio.
- Propostas que mudem skills, políticas, permissões, workflows, credenciais ou produção devem aparecer em diff revisável.
- Para mudanças com risco, peça aprovação antes de aplicá-las.
- Após atualizar o roteador, execute os smoke tests possíveis e registre os resultados reais.
- Nunca chame casos esperados de benchmark; benchmark exige execução observada, data, ambiente e resultados.

## Contrato mínimo de evidência

Uma conclusão deve permitir responder:
1. Qual era o objetivo?
2. O que mudou?
3. Qual comando/teste/observação foi executado?
4. Qual foi o resultado?
5. O que continua sem comprovação?

Use [o template de execução](../templates/ENGINEERING_RUN.md) para tarefas complexas, incidentes ou mudanças que merecem rastreabilidade. Não é obrigatório preencher o template para uma alteração de texto simples.
