# Conselho Central — checklist de automação segura e recursos gratuitos

> Documento inicial de planejamento. Não autoriza alterações em produção, deploys, merges, pagamentos, publicação de mídia nem mudanças de permissões. Confirmar evidências e autorização antes de cada ação de risco.

## Objetivo

Reduzir trabalho manual e tempo de conclusão usando ferramentas gratuitas ou cotas gratuitas, com execução leve para o Galaxy Book Go, contexto seletivo, checkpoints recuperáveis, automação verificável e separação rígida entre projetos.

## Regras globais obrigatórias

- [ ] Trabalhar em branch dedicada; nunca editar `main` diretamente.
- [ ] Identificar e confirmar projeto, repositório, branch, ambiente e objetivo antes de agir.
- [ ] Separar contexto global, passaporte de cada projeto e checkpoint de cada execução.
- [ ] Preferir APIs oficiais, conectores autorizados e automação por eventos; evitar cliques de interface quando uma API segura e suportada existir.
- [ ] Não automatizar login por extração de cookies, sessão, senha salva ou token de navegador.
- [ ] Nunca imprimir, registrar, incluir em commits ou checkpoints senhas, tokens, cookies, chaves privadas ou valores secretos.
- [ ] Usar o menor escopo de permissão possível; preferir tokens temporários, OAuth autorizado e credenciais de curta duração quando suportados.
- [ ] Não desativar MFA, proteções de conta, validações, permissões ou políticas para facilitar automação.
- [ ] Não usar automação de interface para contornar cotas, limites de uso, CAPTCHA ou controles de acesso.
- [ ] Nenhum deploy, merge, cobrança, publicação externa, exclusão de dados ou alteração de produção sem autorização explícita.
- [ ] Toda afirmação de sucesso deve apontar para evidência observada; teste não executado = NOT RUN.
- [ ] Preservar alterações preexistentes do usuário e fornecer diff/rollback para mudanças relevantes.

## Memória, checkpoints e continuidade

- [ ] Criar checkpoint curto ao fim de cada etapa: projeto, branch/commit, objetivo, alterações, testes, bloqueios e próximo passo.
- [ ] Salvar checkpoints em arquivos versionados sem segredos; manter o estado ativo pequeno.
- [ ] Separar fatos confirmados, hipóteses, decisões aprovadas e itens ainda não verificados.
- [ ] Resumir tarefas antigas concluídas e arquivar detalhes que ainda possam servir para auditoria.
- [ ] Limpar duplicatas e dados temporários somente após verificar que não são necessários e que há cópia recuperável quando aplicável.
- [ ] Usar modo de simulação/dry-run antes de qualquer limpeza automática.
- [ ] Não apagar regras de segurança, decisões arquiteturais ainda vigentes, evidências de testes críticos ou requisitos do projeto.
- [ ] Ao retomar, confirmar branch e estado atual do repositório antes de reaplicar alterações; não confiar apenas no checkpoint.
- [ ] Tratar limites/cotas de ferramentas como bloqueio legítimo: salvar o estado e retomar quando autorizado, sem tentar contorná-los.

## Credenciais, login e APIs

- [ ] Inventariar somente nomes de variáveis, serviços, escopos e estado de presença; nunca coletar valores secretos para relatório.
- [ ] Para GitHub, avaliar GitHub App ou token fine-grained restrito ao repositório e às permissões necessárias.
- [ ] Para GitHub Actions, usar secrets protegidos e/ou OIDC quando suportado; não expor segredos em argumentos, saída, artefatos ou logs.
- [ ] Para Discord, usar bot oficial e/ou OAuth2 com escopos mínimos; não automatizar conta de usuário como self-bot.
- [ ] Para Google Sheets, escolher OAuth ou identidade de serviço conforme o cenário e compartilhar somente a planilha necessária.
- [ ] Separar credenciais de desenvolvimento, staging e produção.
- [ ] Validar credenciais com uma chamada de leitura ou health check que não revele o valor.
- [ ] Documentar nome esperado, finalidade, origem, escopo, ambiente e procedimento de rotação — nunca o valor.
- [ ] Verificar rate limits, termos de uso, quotas gratuitas e necessidade de consentimento antes de integrar.
- [ ] Nunca presumir que uma skill ou um conector possui permissão de leitura/escrita; testar acesso mínimo e registrar resultado.

## Planilhas e dados tabulares

- [ ] Reutilizar `skills/spreadsheet-data-engineering/SKILL.md` para CSV/XLSX/Google Sheets.
- [ ] Inspecionar cabeçalhos, tipos, nulos, duplicatas, fórmulas, datas, moeda, codificação e regras de negócio antes de transformar.
- [ ] Preservar o original; produzir cópia/saída nova por padrão.
- [ ] Definir chave de unicidade e regras de reconciliação antes de remover duplicatas.
- [ ] Validar totais, contagens, fórmulas, linhas rejeitadas e integridade entre origem e saída.
- [ ] Proteger dados pessoais e evitar conteúdo de planilhas nos logs.
- [ ] Prevenir formula injection em CSV exportado.
- [ ] Automatizar importação/exportação apenas por conectores e permissões autorizados.

## Imagem, vídeo e áudio — capacidade compartilhada

- [ ] Antes de escolher ferramenta, confirmar o resultado: gerar imagem, editar imagem, criar vídeo, gravar, transmitir, cortar clipes, legendar ou publicar.
- [ ] Preferir ferramentas open-source e processamento local leve quando compatível com o Galaxy Book Go; mover tarefas pesadas para CI/cloud somente se a cota gratuita e o armazenamento forem suficientes.
- [ ] Avaliar FFmpeg para corte, conversão, compressão, normalização de áudio e geração de thumbnails.
- [ ] Avaliar OBS Studio para gravação/transmissão quando o dispositivo e a rede suportarem.
- [ ] Reutilizar as skills de vídeo existentes e verificar versões/licenças antes de adicionar dependências.
- [ ] Não adicionar serviços de IA com custo por chamada sem orçamento, cota e fallback explícitos.
- [ ] Validar direitos de uso de imagens, músicas, fontes e clipes; registrar a origem/licença dos assets.
- [ ] Validar arquivo final, codec, resolução, duração, áudio, legendas e tamanho antes de considerar a tarefa concluída.
- [ ] Nunca publicar nem enviar mídia a terceiros sem autorização.

## Perifa Pro — vídeo de peladas e campeonatos

- [ ] Tratar gravação de partidas, upload, organização por campeonato/equipe/jogo, clipes e compartilhamento como capacidades a avaliar, não como funcionalidades já implementadas.
- [ ] Definir primeiro o fluxo de captura (celular/câmera), upload, armazenamento, processamento, visualização e compartilhamento.
- [ ] Estimar custo de armazenamento, banda e processamento antes de escolher hospedagem; vídeo pode exceder cotas gratuitas rapidamente.
- [ ] Planejar uploads retomáveis, limites de tamanho/duração, compressão, thumbnails, processamento assíncrono e limpeza de temporários.
- [ ] Avaliar geração de melhores momentos por marcação manual no MVP; avaliar detecção automática por áudio/movimento/visão computacional somente após teste de qualidade e custo.
- [ ] Permitir marcação temporal de gol, defesa, falta e jogada para facilitar cortes sem IA pesada.
- [ ] Projetar permissões para vídeos privados, links compartilhados, exclusão, moderação e denúncia.
- [ ] Considerar consentimento, privacidade e direitos de imagem das pessoas gravadas, especialmente menores; limitar exposição e retenção.
- [ ] Testar em vídeos curtos e dados de teste antes de processar partidas completas.
- [ ] Medir tempo de processamento, tamanho de saída, falhas, custo/cota e qualidade dos clipes.

## Arquitetura de automação e avaliação

- [ ] Manter o roteador existente e carregar somente as skills pertinentes ao projeto/tarefa.
- [ ] Paralelizar análises independentes de leitura; coordenar alterações de escrita para evitar conflitos.
- [ ] Usar GitHub Actions para lint, validações, testes determinísticos e avaliações leves dentro das cotas gratuitas.
- [ ] Usar fixtures sintéticas e não segredos/dados reais em CI.
- [ ] Adicionar avaliações para classificação do projeto, seleção de skills, preservação de limites e recuperação de checkpoints.
- [ ] Registrar resultados observados e regressões; não tratar cenários esperados como benchmarks executados.
- [ ] Adotar automação de interface apenas como último recurso para um fluxo autorizado que não tenha API viável; exigir confirmação para ações irreversíveis.

## Ordem de implementação sugerida

1. [ ] Validar o inventário atual de skills, workflows, templates e avaliações.
2. [ ] Definir esquema mínimo de checkpoint e política de retenção/arquivamento.
3. [ ] Adicionar testes para retomada, separação de projetos e ausência de segredos.
4. [ ] Melhorar o roteador para detectar credenciais, planilhas, APIs, imagem/vídeo e nível de risco.
5. [ ] Expandir GitHub Actions com verificações leves e sem credenciais.
6. [ ] Criar adaptadores por serviço somente quando houver caso de uso, permissão autorizada e alternativa gratuita confirmada.
7. [ ] Projetar o MVP de vídeo do Perifa Pro separadamente, começando por marcação manual de momentos e testes de upload/armazenamento.
8. [ ] Medir resultados, revisar custos e aprovar mudanças por PR antes de integrar.

## Critérios de aceite

- [ ] Nenhum segredo aparece em arquivos, logs, checkpoints ou artefatos de teste.
- [ ] Nenhuma mudança foi aplicada à branch principal ou à produção sem autorização.
- [ ] A retomada identifica corretamente projeto, branch, commit, testes e próximo passo.
- [ ] A limpeza tem dry-run, relatório do que seria removido e proteção contra perda de estado essencial.
- [ ] Os testes reportam PASS/FAIL/BLOCKED/NOT RUN com evidência real.
- [ ] Dependências, serviços e APIs têm licença, custo/cota, limitações e alternativa documentados.
- [ ] Cada projeto mantém seu próprio passaporte e suas próprias credenciais/ambientes.


## Engenharia reversa autorizada e reaproveitamento de código aberto

### Regra de entrada

- [ ] Só iniciar engenharia reversa depois de registrar o alvo, o objetivo técnico, a autorização/base legítima e o ambiente de teste.
- [ ] Priorizar primeiro código-fonte, documentação, changelog, issues, testes, formatos públicos e APIs oficiais; usar análise de binários ou tráfego quando isso for necessário e permitido.
- [ ] Não usar estas técnicas para roubar credenciais, extrair sessões/cookies, contornar licenças ou DRM, burlar autenticação/pagamento, explorar terceiros ou acessar dados sem autorização.
- [ ] Não reutilizar código de terceiros sem conferir licença, atribuições, avisos, obrigações de distribuição e compatibilidade com o projeto.
- [ ] Registrar evidência reproduzível: versão/commit da ferramenta, comandos relevantes sem segredos, hashes de artefatos de teste, observações e limitações.
- [ ] Tratar tráfego capturado, binários e arquivos desconhecidos como dados não confiáveis; usar sandbox, fixtures sintéticas e dados minimizados.
- [ ] Nunca guardar payloads com tokens, cookies, dados pessoais ou segredos em issues, commits, logs ou checkpoints; sanitizar antes de compartilhar.

### Catálogo inicial de ferramentas open source a avaliar

| Necessidade | Candidato | Uso possível | Cautela |
|---|---|---|---|
| Entender chamadas HTTP/API e WebSockets | [mitmproxy](https://github.com/mitmproxy/mitmproxy) | Inspecionar, gravar e reproduzir tráfego de desenvolvimento autorizado; útil para depurar integrações próprias | Capturas podem conter tokens e dados pessoais; sanitizar e restringir a ambiente autorizado |
| Analisar binários e engenharia reversa nativa | [Ghidra](https://github.com/NationalSecurityAgency/ghidra) | Inspeção estática e análise de binários próprios ou autorizados | Requer conhecimento técnico; análise dinâmica deve ocorrer em ambiente isolado |
| Análise de binários e arquitetura | [radare2](https://github.com/radareorg/radare2) | Inspeção, desmontagem e análise de executáveis | Verificar suporte ao formato/arquitetura e validar conclusões |
| Inspecionar aplicações Android | [JADX](https://github.com/skylot/jadx) | Decompilar DEX/APK para leitura e pesquisa do código recuperável | Código decompilado pode ser incompleto; usar somente apps próprios ou autorizados |
| Inspecionar e reconstruir recursos de APK | [Apktool](https://github.com/iBotPeaches/Apktool) | Examinar recursos e estrutura de apps Android de teste | Não presumir que reconstruir APK concede direito de redistribuir ou modificar app de terceiros |
| Encontrar vulnerabilidades conhecidas em dependências | [OSV-Scanner](https://github.com/google/osv-scanner) | Verificar dependências e avisos de vulnerabilidade | Revisar resultados e atualizar em branch de teste; não atualizar produção automaticamente |
| Gerar inventário de componentes (SBOM) | [Syft](https://github.com/anchore/syft) | Mapear bibliotecas e pacotes presentes em projeto/imagem | Conferir falsos positivos e escopo do inventário |
| Analisar vulnerabilidades de componentes | [Grype](https://github.com/anchore/grype) | Cruzar SBOM/artefatos com bases de vulnerabilidade | Validar severidade, versão afetada e correção aplicável |
| Verificar licenças de dependências | [OSV-Scanner — licença](https://github.com/google/osv-scanner/blob/main/docs/license-scanning.md) | Criar inventário e identificar licenças que exigem revisão | Scanner não substitui revisão jurídica das obrigações |

Ferramentas acima são candidatas, não dependências aprovadas automaticamente. Antes de adotar qualquer uma, confirmar repositório oficial, licença vigente, releases, manutenção, requisitos, vulnerabilidades conhecidas, tamanho, compatibilidade com o ambiente e custo operacional.

### Fluxo operacional por projeto

1. [ ] Formular a pergunta concreta (por exemplo: “por que o cliente desconecta?”, “qual formato a API espera?” ou “qual componente causa a incompatibilidade?”).
2. [ ] Procurar código/documentação públicos e issues existentes antes de instrumentar um sistema.
3. [ ] Criar branch e fixture mínima reproduzível; manter o alvo de análise isolado.
4. [ ] Escolher a técnica menos invasiva: leitura do código → testes/logs sanitizados → análise estática → captura autorizada de tráfego → análise de binário, se necessária.
5. [ ] Separar observações, inferências e hipóteses; não tratar saída de ferramenta como prova conclusiva.
6. [ ] Criar teste de regressão que demonstre o comportamento antes de alterar a implementação.
7. [ ] Comparar a solução local com alternativas open source e APIs oficiais; preferir reutilizar componentes bem mantidos quando licença e arquitetura permitirem.
8. [ ] Fazer revisão de segurança/licença e teste em ambiente isolado antes de propor PR.
9. [ ] Registrar resultado e próxima decisão no passaporte/checkpoint daquele projeto, sem copiar segredos ou dados de outro projeto.

### Aplicação por tipo de projeto

- **Guerra Infinita:** priorizar leitura do código, logs sanitizados, testes determinísticos e análise autorizada de tráfego para entender autenticação, persistência, desconexões e concorrência. Nunca usar contas/dados de terceiros nem capturar tokens reais para fixtures.
- **ReservaRP/EventosRP:** estudar máquina de estados, webhooks documentados, idempotência, reconciliação e testes de concorrência; usar payloads sintéticos e não reproduzir pagamentos reais em testes.
- **Perifa Pro:** investigar codecs, formatos de vídeo, pipelines de upload e bibliotecas de edição; testar em clipes próprios/autorizados e estimar CPU, armazenamento e banda antes de adicionar processamento automático.
- **Portfolio e sites:** comparar padrões públicos de acessibilidade, animação e layout; reaproveitar bibliotecas somente após avaliar licença, peso e compatibilidade.
- **Planilhas/Portal RH/Casa Prática:** engenharia reversa de estrutura de arquivo e fluxo de dados deve preservar dados pessoais e links/identificadores privados; usar amostras sintéticas sempre que possível.

### Critério de decisão para incorporar um repositório

- [ ] A licença permite o uso pretendido e as obrigações estão documentadas.
- [ ] O repositório é oficial ou a origem e os mantenedores são confiáveis.
- [ ] Há atividade/releases ou justificativa clara para usar um projeto sem manutenção ativa.
- [ ] Dependências, vulnerabilidades, permissões e comportamento de rede foram revisados.
- [ ] A ferramenta resolve uma necessidade concreta e não duplica capacidade já disponível.
- [ ] O impacto em RAM/CPU, armazenamento, tempo de CI e cotas foi avaliado.
- [ ] Existe teste de aceitação e plano de remoção/rollback.
- [ ] A adoção fica limitada ao projeto que precisa dela, sem compartilhamento automático de credenciais ou dados.
