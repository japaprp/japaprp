---
name: mobile-flutter-engineering
description: Projetar, implementar e validar aplicativos móveis, com foco em Flutter/Dart, arquitetura por features, estado, integração de APIs, acessibilidade e releases.
---

# Mobile & Flutter Engineering

Use para apps Flutter ou tarefas móveis nativas/multiplataforma. Identifique a plataforma, versão do SDK, arquitetura, gerenciamento de estado e convenções reais antes de escolher padrões. Não aplique Flutter a projetos nativos ou React Native.

## Arquitetura proporcional
1. Inspecione pubspec.yaml, estrutura de pastas, rotas, DI, gerenciamento de estado, clientes HTTP, modelos e testes existentes.
2. Preserve a arquitetura do projeto. Em Feature-First/Clean Architecture, mantenha dependências apontando para dentro e separe apresentação, casos de uso e infraestrutura apenas quando isso agregar clareza/testabilidade.
3. Evite abstrações e camadas novas para telas simples; não reescreva features não relacionadas.
4. Mantenha widgets focados, estado previsível e lógica de negócio fora de widgets quando a complexidade justificar.
5. Defina estados de loading, sucesso, vazio, erro, retry e sessão expirada para fluxos assíncronos.

## Dados, rede e segurança
- Trate timeouts, offline, perda de conexão, respostas inválidas, rate limits e indisponibilidade do backend.
- Não coloque segredos em app cliente: chaves embutidas podem ser extraídas. Credenciais privilegiadas e regras de autorização ficam no servidor.
- Use armazenamento seguro do sistema para tokens/sessões quando aplicável; evite persistir dados privados sem necessidade.
- Proteja contra múltiplos envios, respostas fora de ordem e atualizações após descarte do widget.
- Para cache/offline, defina política de expiração, sincronização, conflitos e dados que podem permanecer no dispositivo.
- Considere acessibilidade, escala de texto, teclado, contraste, áreas de toque, localização e formatos regionais.

## Testes e qualidade
1. Use testes unitários para regras e repositórios; widget tests para comportamento de UI; integration tests para jornadas críticas.
2. Teste estados de erro e retry, navegação, permissões do dispositivo, sessão expirada e diferentes tamanhos/orientações quando relevantes.
3. Gere mocks/fakes determinísticos e não dependa de serviços externos reais em testes comuns.
4. Execute formatter, analyzer e testes disponíveis conforme o projeto; não alegue sucesso se não foram executados.
5. Verifique desempenho e uso de memória em dispositivo/perfil real antes de alegar otimização.

## Build e publicação
- Confirme package/bundle ID, ambiente, configuração de assinatura, permissões, versão e canais de distribuição antes de release.
- Separe debug, staging e produção; não embuta credenciais ou endpoints secretos.
- Prefira distribuição gradual e plano de rollback quando a plataforma permitir.
- Não publique, altere certificados, assine artefatos ou envie uma versão à loja sem autorização explícita.

## Entrega
Liste arquivos/feature afetados, decisões de arquitetura, comandos e testes executados, plataformas não testadas e riscos de release. Preserve padrões existentes e mantenha o diff focado.
