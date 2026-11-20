# ADR-0001: Arquitetura de integração MCP do Conselho Central

- **Status:** Proposed
- **Data:** 2026-11-20
- **Projeto:** Conselho Central (`japaprp/japaprp`)
- **Branch de documentação:** `feat/central-project-capability-registries`
- **PR relacionado:** [#4 — Project and Capability Registries](https://github.com/japaprp/japaprp/pull/4)
- **Escopo:** decisão arquitetural e critérios para um piloto; não autoriza implementação, instalação, publicação ou deploy.

## 1. Contexto

O Conselho Central já possui uma camada de decisão baseada em skills, Engineering Brain Router e registros de projetos e capacidades. Esses registros são fontes de referência para seleção e governança; não constituem, por si só, um runtime MCP nem ativam ferramentas automaticamente.

A auditoria comparativa de 20/11/2026 examinou:

- [OpenRemote Core](https://github.com/openremote/core)
- [OpenRemote MCP Server (Python)](https://github.com/openremote/service-mcp-server)
- [OpenRemote MCP Client (Python)](https://github.com/openremote/service-mcp-client)
- [OpenRemote MCP Server (TypeScript)](https://github.com/openremote/mcp-server)

A implementação TypeScript inspecionada registra ferramentas e resources MCP em módulos separados, usa schemas Zod e conecta-se à REST API OpenRemote. A documentação do próprio repositório descreve o runtime como STDIO-only, Node.js 24, versão Beta 0.2.x, com OAuth 2.0 client credentials e usuário de serviço. Ela também documenta ferramentas de leitura e escrita, inclusive operações destrutivas. O projeto Python expõe uma abordagem diferente, com FastMCP e integração HTTP/serviços. O cliente Python usa uma camada de cliente MCP e integração com modelos.

Esses repositórios são referências técnicas, não dependências aprovadas do Conselho Central. OpenRemote é uma plataforma IoT e gestão de dispositivos; o Central é uma arquitetura de coordenação de agentes, ferramentas e projetos. Substituir o Central pelo OpenRemote criaria sobreposição de responsabilidades e não atende ao objetivo.

## 2. Problema

O Central ainda não tem uma integração MCP ponta a ponta comprovada no runtime dos agentes. É necessário definir como agentes descobrem e invocam ferramentas externas sem:

- conceder acesso geral ao ambiente ou a todos os projetos;
- confundir descoberta de ferramenta com autorização para executá-la;
- duplicar ferramentas Python e fluxos de análise que já existem;
- misturar arquivos, evidências, branches, credenciais ou dados entre projetos;
- permitir que conteúdo retornado por ferramentas externas se torne instrução privilegiada;
- executar escrita, exclusão, publicação ou ações pagas sem autorização específica;
- introduzir uma segunda plataforma de orquestração ou dependência IoT desnecessária.

## 3. Decisão proposta

Adotar MCP como **protocolo de interoperabilidade de ferramentas**, mantendo o Conselho Central como autoridade de decisão e governança.

A primeira capacidade a ser projetada e validada é um **MCP Client/adapter integrado ao runtime real dos agentes**, condicionado à identificação e inspeção desse runtime. Não se aprova neste ADR a criação imediata de um serviço Gateway independente: a função de política e mediação pode inicialmente ser implementada como uma fronteira lógica dentro do runtime existente. A separação em serviço próprio só será considerada se houver necessidade comprovada de escala, múltiplos runtimes ou isolamento operacional.

O fluxo de decisão deve ser:

1. O Router resolve o projeto e a tarefa.
2. O Central consulta os registros de projeto e capacidades como dados de referência.
3. Uma política do Central filtra os servidores e ferramentas permitidos para aquele projeto, agente e tarefa.
4. O cliente MCP descobre schemas e capacidades dos servidores autorizados.
5. A descoberta é cruzada com uma allowlist explícita; ferramenta descoberta não é automaticamente autorizada.
6. O cliente valida argumentos, limites, timeout e política de efeito colateral.
7. A ferramenta é invocada somente após as verificações aplicáveis.
8. O resultado é tratado como dado externo não confiável, validado e associado a evidências.
9. O Central registra a chamada e seu resultado, sem registrar segredos ou dados desnecessários.

## 4. Arquitetura lógica

```text
User request
    |
    v
Engineering Brain Router
    |
    +--> Project Registry / Capability Registry
    |
    v
Central policy decision
(project + agent + task + tool allowlist)
    |
    v
MCP Client / Adapter (inside verified agent runtime)
    |
    +--> MCP Server A (project-scoped)
    +--> MCP Server B (read-only)
    +--> Existing local tools via narrow adapters
    |
    v
Validated result + evidence + audit event
    |
    v
Central task state / next decision
```

O diagrama é conceitual. Não afirma que qualquer componente MCP já esteja instalado, conectado ou executando no Central.

### 4.1 Responsabilidades

| Camada | Responsabilidade | Não deve fazer |
|---|---|---|
| Router | Resolver intenção, projeto, fase e skill | Executar ferramentas externas por conta própria |
| Registries | Declarar projetos, capacidades, restrições e candidatos | Ativar ou instalar ferramentas automaticamente |
| Política Central | Autorizar servidor/ferramenta para contexto específico | Confiar apenas no nome ou descrição fornecida pelo servidor |
| MCP Client/Adapter | Descoberta, validação, chamada, timeout e normalização | Contornar política ou ampliar escopo |
| MCP Server | Expor ferramentas pequenas com schemas e autorização no servidor | Confiar apenas na autorização do cliente |
| Auditoria | Registrar identidade, projeto, ferramenta, correlação e resultado | Armazenar tokens, segredos ou payloads pessoais desnecessários |

## 5. Modelo de identidade, isolamento e autorização

A autorização deve ser aplicada em duas fronteiras: no cliente/política do Central e no servidor MCP sempre que este suportar autenticação e autorização próprias.

Cada chamada deve carregar um contexto verificável equivalente a:

- `project_id`
- `agent_id`
- `task_id` ou correlation ID
- `server_id`
- `tool_name`
- `permission_profile`
- `approval_reference`, quando aplicável

Esses campos são um contrato lógico proposto; o formato de transporte e propagação ainda precisa ser validado com o runtime escolhido.

Regras obrigatórias:

1. Identidade e credenciais separadas por projeto e servidor; nunca compartilhar tokens entre REA, Guerra Infinita, Casa Prática ou outros projetos.
2. Menor privilégio: conceder somente ferramentas e escopos necessários à tarefa.
3. Allowlist por projeto e perfil de agente. Uma ferramenta fora da allowlist deve ser negada mesmo que apareça em `tools/list`.
4. Negação por padrão para ferramentas sem classificação de risco, dono, finalidade ou política explícita.
5. Verificação de autorização no servidor para cada operação; validação no cliente não substitui autorização no servidor.
6. Nenhuma ferramenta recebe shell, filesystem amplo, acesso irrestrito ao GitHub ou credenciais globais por conveniência.
7. Respostas, descrições, resources e conteúdo retornado são dados não confiáveis; não podem alterar instruções de sistema, política, projeto ativo ou permissões.
8. Segredos ficam em mecanismo seguro de configuração/segredos, referenciados apenas por nome. Nunca em código, argumentos, logs ou documentos.

### 5.1 Perfis de permissão iniciais

| Perfil | Permissão | Política |
|---|---|---|
| `read_only` | Consultas e inspeção sem efeito colateral | Permitido no piloto após allowlist |
| `write_reviewed` | Escrita reversível e limitada | Desabilitado no piloto; aprovação por operação |
| `destructive` | Exclusão, reset, alteração irreversível | Bloqueado por padrão; exige autorização explícita específica e confirmação contextual |
| `external_effect` | Publicação, envio, deploy, compra, ação paga ou mudança compartilhada | Bloqueado sem autorização explícita específica |

## 6. Primeiro piloto: REA somente leitura

O primeiro piloto recomendado é o projeto de análise REA de Dark War: Survival, por permitir validar o protocolo sobre ferramentas e evidências já existentes sem conceder escrita no jogo, nos artefatos originais ou no projeto Guerra Infinita.

O piloto deve **adaptar ferramentas existentes**, não reconstruir seus algoritmos. Candidatas a ferramentas somente leitura, sujeitas a inventário e validação local:

- consultar manifestos e integridade de arquivos;
- consultar mapeamentos e registros já existentes;
- localizar TextAssets e referências já indexadas;
- pesquisar nomes, caminhos, hashes e relações nos resultados existentes;
- recuperar resultados de análises com referência ao artefato de origem.

Restrições do piloto:

- nenhuma escrita ou exclusão nos artefatos originais;
- nenhuma instalação de dependências ou serviço externo como parte deste ADR;
- nenhum acesso amplo ao armazenamento do telefone;
- nenhuma varredura completa de bundles sem hipótese e autorização de escopo;
- nenhuma transferência automática de artefatos originais para o repositório de Guerra Infinita;
- conexão entre REA e desenvolvimento somente por achados revisados e decisões de design documentadas.

A lista final de ferramentas depende de inventário do runtime e dos scripts realmente disponíveis. Não se declara que essas ferramentas já estejam expostas via MCP.

## 7. Estratégia de transporte e implementação

Não fixar agora um transporte único. A escolha depende do runtime dos agentes, ambiente de execução, isolamento de processos, conectividade e suporte real dos clientes disponíveis.

Critérios:

- **STDIO:** considerar para servidor local/subprocesso quando cliente e servidor compartilham ambiente e ciclo de vida.
- **HTTP transport:** considerar para servidor remoto quando autenticação, autorização, TLS, rede e ciclo de vida estiverem definidos e suportados pelo SDK/protocolo escolhido.
- Não assumir que o pacote OpenRemote TypeScript oferece transporte remoto: a documentação e o código inspecionados descrevem STDIO-only.
- Não assumir que uma implementação HTTP de outro repositório é intercambiável sem validar versão do protocolo, autenticação, streaming, timeouts e compatibilidade do cliente.

O primeiro marco é provar um MCP Client real no runtime do agente com um servidor de teste inofensivo e somente leitura. O servidor MCP próprio do Central é uma etapa posterior, não pré-requisito para consumir ferramentas externas.

## 8. Contrato de ferramentas

Cada ferramenta aprovada deve ter:

- nome estável e descrição operacional específica;
- schema de entrada tipado, limites e validação no servidor;
- indicação explícita de projeto, escopo, perfil de permissão e classificação de risco;
- resultado estruturado, tamanho máximo e referências de evidência;
- timeout, cancelamento e política de paginação;
- semântica de erro acionável, sem stack trace ou segredo;
- comportamento de idempotência declarado;
- distinção explícita entre leitura, escrita reversível e ação irreversível.

Ferramentas devem ser pequenas e coesas. Preferir operações de leitura específicas a uma ferramenta genérica como `execute_command`, `read_any_file` ou `call_any_api`.

## 9. Confiabilidade e observabilidade

Requisitos mínimos:

- timeout por chamada e limite de concorrência;
- cancelamento quando a tarefa ou sessão for encerrada;
- retries somente para falhas transitórias e operações comprovadamente idempotentes;
- nunca repetir automaticamente escrita ou efeito externo sem chave/idempotência e verificação do estado;
- paginação e limites de tamanho para evitar respostas excessivas;
- correlation ID de ponta a ponta;
- health check que diferencie processo ativo de dependência saudável;
- logs estruturados sem tokens, dados pessoais ou conteúdo sensível;
- registro de ferramenta, servidor, projeto, agente, duração, resultado e motivo de negação;
- degradação segura: indisponibilidade do MCP não deve conceder fallback mais amplo.

## 10. Segurança e ameaças consideradas

| Ameaça | Controle obrigatório |
|---|---|
| Tool discovery vira execução implícita | Allowlist e decisão explícita do Central |
| Confusão ou troca de projeto | Contexto de projeto imutável por tarefa e credenciais segregadas |
| Prompt injection em resultado externo | Tratar conteúdo como dado não confiável; nunca como instrução |
| Argumentos malformados ou excessivos | Schema e limites validados no cliente e servidor |
| Vazamento de credenciais | Secret store, redaction e proibição de segredos em logs |
| Ferramenta destrutiva acionada pelo modelo | Perfil bloqueado e aprovação humana específica |
| Replay/retry com efeito duplicado | Idempotência, correlation ID e reconciliação de estado |
| Servidor comprometido ou trocado | Identidade do servidor, origem aprovada, transporte autenticado e revisão de mudanças |
| Exfiltração entre projetos | Allowlist por projeto, testes negativos e isolamento de credenciais |
| Resposta gigantesca ou indisponibilidade | Limites, timeout, paginação, cancelamento e circuit breaker quando justificado |

## 11. Alternativas consideradas

### A. Instalar o OpenRemote Core como núcleo do Central — rejeitada

OpenRemote é uma plataforma IoT com gestão de assets, realms, regras e dispositivos. Ela não substitui o Router, os registries e a governança de agentes do Central. Adotá-la como núcleo adicionaria infraestrutura e responsabilidades fora do objetivo.

### B. Adotar integralmente o OpenRemote MCP Client — rejeitada por enquanto

A implementação examinada é um cliente/demonstração acoplado a escolhas próprias de framework e modelos. Não há evidência de que corresponda ao runtime real dos agentes do Central. Reutilizar conceitos é preferível a introduzir uma segunda camada de agente.

### C. Copiar integralmente um dos MCP Servers OpenRemote — rejeitada

Os servidores são específicos para a API e domínio OpenRemote. O servidor TypeScript contém ferramentas administrativas e destrutivas; o servidor Python também é adaptado ao domínio IoT. Não são servidores genéricos de ferramentas do Central.

### D. Criar imediatamente um MCP Gateway independente — adiada

Um serviço dedicado pode fazer sentido se houver múltiplos runtimes, necessidade de isolamento de processo, escala ou auditoria centralizada. Primeiro é necessário identificar o runtime e validar se uma fronteira lógica dentro do cliente existente resolve o problema com menos componentes.

### E. MCP Client/Adapter integrado ao runtime existente — preferida

É o caminho mais incremental. Permite validar descoberta, allowlist, autorização, schemas e auditoria sem instalar uma plataforma adicional ou expor prematuramente ferramentas do Central.

## 12. Licenças e adoção de código externo

Esta decisão recomenda **reutilização de padrões e conceitos**, não cópia de código.

Antes de incorporar qualquer código, pacote ou trecho externo, realizar revisão de licença do repositório e das dependências transitivas, obrigações de distribuição, compatibilidade com a licença do Central e obrigações de atribuição/compartilhamento. A auditoria documental atual não fecha essa revisão jurídica; portanto, nenhuma dependência ou trecho OpenRemote está aprovado para cópia.

## 13. Plano de implementação condicionado

| Etapa | Entrega | Critério de saída |
|---|---|---|
| 0. Descoberta do runtime | Identificar runtime/cliente dos agentes, versões, transporte, ambiente e limites | Evidência reproduzível; nenhuma suposição sobre MCP instalado |
| 1. Contrato e política | Tipos de identidade, allowlist, perfis e decisão de autorização | Revisão de segurança e contrato aprovado |
| 2. Cliente mínimo | MCP Client/Adapter com servidor de teste read-only | Listar, validar e chamar uma ferramenta inofensiva |
| 3. Piloto REA | Expor subconjunto de ferramentas existentes e somente leitura | Evidência rastreável, sem alteração de originais |
| 4. Endurecimento | Isolamento, negação, timeout, cancelamento, auditoria e recuperação | Suíte de segurança/confiabilidade aprovada |
| 5. Avaliar servidor próprio | Expor capacidades do Central somente se houver consumidor real | Caso de uso externo demonstrado e decisão separada |

Nenhuma etapa autoriza merge, deploy, publicação externa, alteração de segredos/permissões, instalação paga ou operação destrutiva. Essas ações exigem autorização específica.

## 14. Critérios de aceitação e testes

A implementação futura não poderá ser considerada concluída sem:

1. **Discovery:** cliente lista ferramentas do servidor de teste e interpreta schemas válidos.
2. **Allowlist:** ferramenta descoberta, mas não autorizada, é negada antes da chamada.
3. **Autenticação:** credencial ausente, expirada ou inválida falha de modo fechado.
4. **Isolamento:** agente REA não consegue invocar ferramenta ou acessar credencial de Guerra Infinita, Casa Prática ou outro projeto.
5. **Validação:** argumentos ausentes, tipos incorretos, tamanho excessivo e payload malformado são rejeitados.
6. **Read-only:** ferramentas de leitura não alteram estado; comprovar com fixture antes/depois.
7. **Aprovação:** escrita, exclusão e efeito externo permanecem bloqueados sem autorização específica.
8. **Prompt injection:** conteúdo de ferramenta com instruções maliciosas é tratado como dado e não altera política.
9. **Confiabilidade:** timeout, cancelamento, serviço indisponível, resposta vazia e falha transitória são testados.
10. **Idempotência:** retry não duplica efeitos; operações sem idempotência não são repetidas automaticamente.
11. **Auditoria:** chamada e negação produzem evento correlacionável sem segredo ou dado pessoal desnecessário.
12. **Comportamento do agente:** em sessão nova, o agente escolhe a ferramenta correta, usa schema e interpreta o resultado com evidências.

Cada validação deve ser reportada como `PASS`, `FAIL`, `BLOCKED` ou `NOT RUN`. Testes estruturais não substituem teste comportamental em sessão nova.

## 15. Estado atual e pendências

Na data deste ADR:

- **PASS:** auditoria documental e inspeção estática dos repositórios OpenRemote listados.
- **PASS:** branch de trabalho identificada como `feat/central-project-capability-registries`; PR #4 permanece Draft e aberto.
- **PASS:** instruções do Central e skill `mcp-tooling-engineering` revisadas.
- **NOT RUN:** identificação do runtime MCP efetivamente usado pelos agentes do Central.
- **NOT RUN:** cliente MCP conectado a um servidor real.
- **NOT RUN:** piloto REA.
- **NOT RUN:** testes de isolamento e segurança ponta a ponta.
- **BLOCKED:** aprovação de código/dependências externas, pendente de revisão de licença.
- **NOT RUN:** benchmark de latência, consumo de memória e custo.

A integração anterior denominada Central Bridge não deve ser considerada funcional sem nova evidência: o estado registrado anteriormente inclui falha HTTP 401 na autenticação. Este ADR não altera nem reativa essa ponte.

## 16. Fontes primárias

- [OpenRemote Core](https://github.com/openremote/core)
- [OpenRemote MCP Server — Python](https://github.com/openremote/service-mcp-server)
- [OpenRemote MCP Client — Python](https://github.com/openremote/service-mcp-client)
- [OpenRemote MCP Server — TypeScript](https://github.com/openremote/mcp-server)
- [OpenRemote TypeScript MCP server — server registration](https://github.com/openremote/mcp-server/blob/main/src/server.ts)
- [OpenRemote TypeScript MCP server — authentication](https://github.com/openremote/mcp-server/blob/main/src/auth.ts)
- [OpenRemote TypeScript MCP server — assets tools](https://github.com/openremote/mcp-server/blob/main/src/tools/assets.ts)
- [OpenRemote TypeScript MCP server — realms tools](https://github.com/openremote/mcp-server/blob/main/src/tools/realms.ts)
- [OpenRemote TypeScript MCP server — runtime and scope notes](https://github.com/openremote/mcp-server/blob/main/CLAUDE.md)
- [Conselho Central — Engineering Brain Router](https://github.com/japaprp/japaprp/blob/feat/central-project-capability-registries/skills/engineering-brain-router/SKILL.md)
- [Conselho Central — MCP Tooling Engineering](https://github.com/japaprp/japaprp/blob/feat/central-project-capability-registries/skills/mcp-tooling-engineering/SKILL.md)
- [Conselho Central — Project Registry](https://github.com/japaprp/japaprp/blob/feat/central-project-capability-registries/skills/registries/PROJECT_REGISTRY.json)
- [Conselho Central — Capability Registry](https://github.com/japaprp/japaprp/blob/feat/central-project-capability-registries/skills/registries/CAPABILITY_REGISTRY.json)

---

**Resumo da decisão:** MCP será uma camada controlada de interoperabilidade. O Router e a governança do Conselho Central permanecem soberanos. O primeiro passo de implementação, após aprovação técnica separada, será um cliente/adapter mínimo e read-only no runtime real dos agentes, validado inicialmente com ferramentas existentes do REA.