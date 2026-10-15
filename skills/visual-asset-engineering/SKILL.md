---
name: visual-asset-engineering
description: Preparar, gerar, editar, organizar e otimizar imagens e assets visuais para web, aplicativos, portfólios e conteúdo.
---

# Visual Asset Engineering

## Escopo
Cobre pipeline e integração de assets visuais — não substitui direção de arte geral, geração de imagem por uma ferramenta dedicada nem motion/vídeo.

## Fluxo
1. Determine o destino e a função do asset: hero, avatar, ícone, thumbnail, captura de tela, mockup, ilustração, imagem de produto ou recurso de app.
2. Descubra dimensões, proporção, densidade, fundo/transparência, formato, limites de tamanho, direitos de uso e requisitos de acessibilidade.
3. Inspecione os assets existentes e preserve a identidade visual aprovada. Não substitua imagens do usuário nem altere a direção de arte sem solicitação.
4. Se for necessário gerar ou editar uma imagem, confirme que a ferramenta de imagem está disponível; a skill não é, por si só, um gerador.
5. Para web, escolha formatos adequados (por exemplo, AVIF/WebP com fallback quando necessário, SVG para vetores confiáveis e PNG quando transparência sem perdas for importante). Verifique suporte e pipeline real.
6. Gere variantes responsivas e dimensões adequadas; evite enviar imagens enormes para miniaturas ou usar CSS para disfarçar proporções incorretas.
7. Use nomes de arquivo descritivos e estáveis, caminhos coerentes e alt text que comunique a função da imagem. Imagens decorativas devem ter alternativa acessível apropriada.
8. Considere compressão, lazy loading fora da área inicial, dimensões explícitas para reduzir layout shift, cache e impacto no carregamento.
9. Para SVGs externos ou enviados por usuários, trate conteúdo como não confiável; sanitize antes de inline/renderizar e não permita scripts ou referências perigosas.
10. Respeite licenças, atribuições e privacidade. Não remova marcas d'água nem apresente assets licenciados como próprios.
11. Valide visualmente em tamanhos relevantes, tema claro/escuro e telas responsivas; confirme os caminhos e que o build inclui os arquivos.

## Evitar
- Não inventar capturas de tela, logotipos, funcionalidades ou resultados de produto.
- Não gerar assets redundantes quando os existentes atendem ao pedido.
- Não declarar ganho de performance sem medir o tamanho ou o carregamento.
- Não colocar segredos ou dados pessoais em imagens, metadados ou nomes de arquivo.

## Entrega
Liste assets criados/alterados, formatos e dimensões confirmados, uso no projeto, checagens feitas e limitações restantes.
