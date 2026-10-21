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
