---
name: computer-vision-video-intelligence
description: Projetar e avaliar sistemas de visão computacional para detecção e rastreamento de pessoas/objetos, reconhecimento facial sob autorização, leitura de placas veiculares (ANPR/LPR), OCR e análise de vídeo/câmeras, com privacidade, segurança e governança desde o desenho.
---

# Computer Vision & Video Intelligence

## Objetivo e limites

Projetar, avaliar e integrar capacidades de visão computacional em aplicações autorizadas. Cobrir imagens estáticas, fluxos de câmera e vídeo gravado, com foco em detecção, classificação, rastreamento, OCR, leitura de placas e biometria facial.

Não presumir que "identificar pessoa" significa reconhecer sua identidade. Separar sempre:
- **Detecção:** localizar uma pessoa, veículo ou objeto em um frame.
- **Classificação:** atribuir uma classe (pessoa, carro, moto, animal, equipamento etc.).
- **Rastreamento:** associar detecções entre frames sem afirmar identidade civil.
- **OCR/LPR/ANPR:** localizar e transcrever caracteres de placas; uma leitura não prova propriedade, identidade do condutor ou infração.
- **Reconhecimento facial/biométrico:** comparar características faciais para verificar ou identificar uma pessoa. É uma categoria de risco elevado e não deve ser ativada por padrão.

## Fluxo de decisão

1. Defina finalidade, cenário, operador, titular dos dados, local da câmera, origem das imagens, escala, latência e resultado esperado.
2. Verifique se a finalidade pode ser atendida por detecção, contagem ou rastreamento sem identificação biométrica. Prefira a alternativa menos invasiva.
3. Identifique dados pessoais e biométricos, pessoas vulneráveis, expectativa de privacidade, contexto público/privado e possibilidade de monitoramento sistemático.
4. Faça avaliação jurídica e de impacto antes de coletar/rotular imagens ou ativar reconhecimento facial/LPR em operação real.
5. Consulte primeiro o catálogo local de skills e repositórios de referência. Reutilize componentes já aprovados; não clone/importa coleções inteiras nem acrescente dependência sem necessidade.
6. Compare candidatos técnicos por qualidade no cenário real, licença, manutenção, dependências, hardware, latência, segurança, documentação, custo e capacidade de operar localmente.
7. Prototipe com dados sintéticos, públicos licenciados ou amostras autorizadas e minimizadas. Nunca enviar imagens reais para serviços externos sem aprovação e base jurídica.
8. Avalie erros, viés, falsos positivos/negativos, desempenho por condições de captura e impacto sobre pessoas. Defina revisão humana e mecanismo de contestação quando aplicável.
9. Só integrar após threat model, revisão de privacidade, autorização, testes e plano de retenção/eliminação.

## Capacidades técnicas

### Detecção e rastreamento
- Detecção de pessoas, veículos, animais e objetos por frame.
- Contagem e zonas/linhas virtuais, com cuidado para não converter presença em inferência de comportamento.
- Tracking multiobjeto com identificadores temporários e limitados ao evento/sessão.
- Detecção de eventos apenas quando a definição for objetiva, validada e proporcional à finalidade.

### Placas veiculares (LPR/ANPR)
- Pipeline: detectar veículo → localizar placa → corrigir perspectiva/qualidade → OCR → normalizar caracteres → estimar confiança → revisão humana quando necessário.
- Registrar frame/tempo, confiança e versão do modelo; separar resultado automático de confirmação humana.
- Considerar ângulo, iluminação, movimento, chuva, sujeira, placas parcialmente ocultas, padrões de jurisdição e falsos matches.
- Não inferir proprietário, condutor, endereço ou histórico sem fonte e autorização independentes.

### Pessoas e reconhecimento facial
- Priorizar detecção, contagem e tracking não identificável.
- Reconhecimento facial exige avaliação específica de necessidade, proporcionalidade, base legal, transparência, segurança, retenção, direitos dos titulares e alternativas menos intrusivas.
- Não criar listas de vigilância, identificação em massa, inferência de atributos sensíveis ou monitoramento clandestino.
- Não usar similaridade facial como prova conclusiva. Exigir limiar validado, medição de falsos matches, revisão humana qualificada e procedimento de contestação.
- Não usar biometria para decisões adversas automatizadas sem análise jurídica e salvaguardas apropriadas.

### Objetos e análise de vídeo
- Definir taxonomia de classes e condições de captura; não confundir detecção com entendimento semântico.
- Medir precisão/recall, mAP quando aplicável, latência, FPS, consumo de memória/energia e robustez.
- Em vídeo contínuo, aplicar processamento na borda quando viável, limitar resolução/zonas e evitar armazenar frames desnecessários.

## Governança, privacidade e segurança

- Aplicar legislação vigente do país/estado e regras setoriais do contexto. No Brasil, submeter dados pessoais e biométricos à revisão conforme LGPD e orientações vigentes da ANPD; confirmar texto, atualizações e aplicabilidade em fontes oficiais antes de decidir.
- Biometria facial vinculada a pessoa identificada ou identificável deve ser tratada como dado pessoal sensível. Documentar finalidade, hipótese legal aplicável, necessidade, proporcionalidade e avaliação de impacto; não presumir que consentimento seja a única ou sempre a adequada hipótese legal.
- Para cada câmera/canal, documentar controlador, operador, finalidade, local, campo de visão, aviso/transparência, acesso, compartilhamentos e retenção.
- Minimizar captura, resolução, área monitorada, campos armazenados e prazo de retenção. Evitar áudio se não for necessário.
- Definir política de retenção e descarte verificável; proteger backups, exports, logs, thumbnails e datasets de treinamento.
- Criptografar trânsito/repouso; usar controle de acesso por função, MFA quando disponível, trilhas de auditoria, rotação de credenciais e segregação por cliente/tenant.
- Nunca misturar imagens, embeddings, listas de referência, eventos, modelos ou credenciais entre tenants/projetos.
- Não usar imagens para treinar modelos ou finalidade secundária sem autorização e avaliação jurídica própria.
- Fazer DPIA/RIPD ou avaliação equivalente quando exigida ou indicada pelo risco; registrar riscos, mitigação, responsáveis e aprovação.
- Proibir acesso clandestino, bypass de câmera, reconhecimento fora do escopo, scraping de rostos/placas e consultas a bases não autorizadas.
- Incidentes com imagens/biometria exigem resposta, contenção, preservação de evidências e avaliação de notificação conforme a lei aplicável.

## Avaliação e critérios de aceite

Registrar por conjunto de teste e cenário:
- origem/licença/autorização dos dados, consentimento quando aplicável e critérios de anonimização;
- composição, tamanho, períodos, condições de iluminação/ângulo/distância e limitações;
- precision, recall, falsos positivos, falsos negativos e calibração de confiança;
- para biometria: FAR/FRR, FMR/FNMR, desempenho por grupos relevantes quando legal/eticamente permitido, limiar e protocolo de revisão;
- para LPR: taxa de leitura exata, taxa de placas não lidas, erros de caractere e desempenho por jurisdição/condição;
- latência ponta a ponta, FPS, disponibilidade, custo e comportamento offline;
- testes de segurança, acesso cruzado entre tenants, retenção, exclusão e auditabilidade.

Não declarar "acurácia" sem definir métrica, conjunto de teste e condições. Não aceitar benchmark do fornecedor como validação no ambiente real.

## Arquitetura de referência

Manter módulos desacoplados:
1. ingestão autorizada e validação de origem;
2. pré-processamento e mascaramento/minimização;
3. detector/classificador;
4. tracking;
5. OCR/LPR ou componente biométrico separado;
6. motor de regras/eventos;
7. revisão humana e contestação;
8. armazenamento com retenção e isolamento;
9. auditoria/monitoramento.

Preferir interfaces versionadas e adaptadores para trocar modelos sem acoplar o produto a um fornecedor. Não compartilhar banco ou storage entre aplicações; compartilhar somente código genérico revisado e contratos sem dados.

## Roteamento com outras skills

- engineering-brain-router: selecionar a menor combinação e aplicar o protocolo de lacunas.
- application-security-auth: autenticação, autorização, segregação de tenants, sessão e controle de acesso.
- ai-integration-evaluation: integração/avaliação de modelos, inferência e pipelines de IA.
- infrastructure-database-engineering: câmeras, edge, filas, storage, observabilidade e operação.
- api-engineering-contracts ou public-api-integration: contratos internos ou APIs de terceiros.
- testing-regression-quality: testes de qualidade, desempenho, segurança e regressão.
- repo-reverse-engineering: avaliar código-fonte e repositórios externos antes de reutilização.

Não carregar todas por padrão; escolher conforme a tarefa concreta.

## Estado e autorização

Esta skill é procedimento de referência, não prova de que modelos, câmeras, datasets, bibliotecas ou conectores estejam instalados/aprovados. Antes de cada adoção, verificar repositório oficial, licença, versão, manutenção, dependências, vulnerabilidades, compatibilidade e permissões. Não instalar, publicar, conectar câmeras reais, processar biometria real, alterar acesso ou gerar custos sem autorização específica.

## Relato

Classificar cada etapa como PASS, FAIL, BLOCKED ou NOT RUN. Separar evidência observada, hipótese e recomendação. Informar modelo/versão, dataset, métricas, cenário, limitações, licença e decisão de governança. Nunca declarar reconhecimento correto ou conformidade legal sem validação correspondente.
