---
name: game-development-engineering
description: Projetar, implementar, depurar e otimizar jogos, escolhendo a engine e os sistemas adequados ao projeto real.
---

# Game Development Engineering

## Primeiro, identifique o projeto
1. Determine se o pedido é desenvolvimento de um jogo, ferramenta interna, mod autorizado, análise de desempenho ou automação de um jogo existente.
2. Inspecione os arquivos do projeto e identifique engine, versão, linguagem, plataformas-alvo, pipeline de assets e sistema de build antes de recomendar APIs.
3. Se o projeto ainda não existe, esclareça o gênero, plataforma, escopo, experiência do time e orçamento antes de escolher Unity, Unreal, Godot ou outra tecnologia.
4. Não misture APIs ou padrões de engines diferentes. Consulte documentação correspondente à versão realmente usada.

## Engenharia de gameplay
- Separe estado de jogo, regras, apresentação, input, persistência e efeitos de áudio/visual conforme a arquitetura do projeto.
- Defina estados e transições explícitos; trate pausa, reinício, carregamento, falha e saída.
- Considere determinismo e fixed timestep quando física, replay, simulação ou multiplayer exigirem.
- Para multiplayer, planeje autoridade do servidor, validação de ações, latência, reconexão, sincronização e proteção contra clientes adulterados.
- Use pooling, batching, LOD, streaming e redução de alocações somente quando adequados e medidos.
- Projete controles, HUD, feedback, acessibilidade e navegação para o dispositivo-alvo.
- Planeje salvamento/versionamento de dados e migrações quando formatos persistidos mudarem.

## Assets, build e publicação
- Verifique escala, pivôs, rigs, animações, colisores, texturas, áudio, licenças e tamanho do pacote.
- Use perfis de build e profiling na plataforma-alvo; não declare FPS, consumo de memória ou estabilidade sem medição.
- Valide builds de desenvolvimento e distribuição, assinatura, permissões, compatibilidade e requisitos da loja antes de publicar.
- Não exponha chaves de serviço, segredos ou credenciais em builds de cliente. Segredos que exigem confidencialidade devem permanecer no servidor.
- Mantenha projeto, assets e configurações versionados de forma adequada, excluindo caches e artefatos regeneráveis quando aplicável.

## Segurança e limites
- Para economia, inventário, ranking e compras online, valide operações sensíveis no servidor e torne transações idempotentes.
- Use somente APIs, SDKs, mods e ferramentas autorizados. Não implemente roubo de conta, evasão de anti-cheat, exploração de vulnerabilidades, botting abusivo ou automação que viole regras do serviço.
- Em jogos de terceiros, diferencie análise informativa de interação automatizada; respeite termos, privacidade e controles de acesso.
- Não faça compras, publique builds ou altere serviços de produção sem autorização explícita.

## Verificação e entrega
- Execute testes unitários, testes de gameplay, build e profiling que o ambiente realmente suporte.
- Registre engine/versão, plataforma testada, comandos executados e resultados. Se não houver engine instalada ou dispositivo-alvo, declare a limitação e forneça o próximo teste reproduzível.
