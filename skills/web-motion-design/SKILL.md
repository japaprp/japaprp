---
name: web-motion-design
description: Planejar, implementar e auditar motion design para interfaces web: hero animations, scroll storytelling, microinterações, transições, SVG/Lottie e performance acessível. Use quando a tarefa é animar a interface real, não renderizar um filme.
---

# Web Motion Design

## Objetivo

Criar movimento intencional, refinado e responsivo em interfaces web, reforçando hierarquia, feedback e narrativa sem comprometer legibilidade, acessibilidade ou desempenho. Trabalhe com a stack já instalada; não adicione bibliotecas sem benefício claro.

## Escolha de técnica

1. Inspecione a stack, os componentes existentes, os estilos, o roteamento e as dependências antes de escolher uma técnica.
2. Prefira CSS para transições simples; use a biblioteca já presente (Motion/Framer Motion, GSAP ou outra) quando ela resolver uma necessidade real.
3. Use GSAP/ScrollTrigger para timelines ou experiências de scroll complexas; Motion para estados, gestos e transições React; SVG/CSS para traços, máscaras e ícones; Lottie somente quando houver um asset apropriado.
4. Não misture motores de animação sem necessidade nem instale vários pacotes para o mesmo efeito.
5. Consulte a documentação oficial da versão instalada antes de usar APIs ou plugins.

## Processo de design

1. Defina o propósito de cada animação: orientar atenção, mostrar relação espacial, confirmar uma ação ou sustentar uma narrativa.
2. Crie uma pequena especificação de motion: gatilho, duração, easing, distância/escala, sequência, comportamento em mobile e alternativa com movimento reduzido.
3. Para hero e storytelling, organize a sequência em beats: entrada, foco principal, demonstração, transição e CTA. Use scroll-pinning apenas se melhorar a compreensão e não bloquear a navegação.
4. Para microinterações, cubra estados normal, hover, pressed, focus, loading, success, error e disabled quando aplicável.
5. Preserve layout e conteúdo aprovados. Não reposicione seções, CTAs ou componentes fora do escopo sem autorização explícita.
6. Faça movimento expressivo e sóbrio: evite parallax excessivo, animações contínuas decorativas, blur pesado, zooms aleatórios e padrões genéricos de template.

## Performance e acessibilidade

- Prefira animar `transform` e `opacity`; meça antes de otimizar outras propriedades.
- Evite leitura/escrita de layout em loops, observers duplicados e listeners sem cleanup.
- Respeite `prefers-reduced-motion`; reduza ou remova deslocamentos grandes sem eliminar feedback essencial.
- Não dependa apenas de hover; garanta toque, teclado, foco visível e alternativa sem movimento.
- Evite scroll-jacking e preserve rolagem natural, navegação por teclado e âncoras.
- Valide viewport móvel, orientação, conteúdo longo, carregamento lento e estados de erro.
- Para canvas/WebGL ou efeitos intensivos, forneça fallback estático quando necessário.

## Validação obrigatória

1. Execute lint/build/testes disponíveis e registre os comandos reais.
2. Se houver browser ou screenshots, confira desktop e mobile, início/meio/fim das animações, overflow, foco, scroll e layout.
3. Verifique `prefers-reduced-motion` e ausência de erros de console quando as ferramentas estiverem disponíveis.
4. Não alegue FPS, acessibilidade total ou inspeção visual sem medições/evidência.
5. Entregue um resumo dos arquivos, técnica escolhida, validações e limitações.

## Referências públicas

Estas são referências para consulta, não dependências obrigatórias nem instrução para copiar código integralmente:

- iart-ai/web-animation-skills (MIT): https://github.com/iart-ai/web-animation-skills
- Motion: https://motion.dev/docs
- GSAP: https://gsap.com/docs/
- LottieFiles: https://github.com/LottieFiles
