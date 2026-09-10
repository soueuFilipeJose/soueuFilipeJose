# Seu perfil, fora de época

O README está pronto. Você não precisa instalar Python, Node, extensões ou configurar Actions para usá-lo.

## Colocar no GitHub

1. Entre na conta **soueuFilipeJose**. Crie ou abra o repositório público com o nome exato **soueuFilipeJose**.
2. Extraia o ZIP no computador. Abra a pasta `Perfil_GitHub_Punk`.
3. No repositório, use **Add file → Upload files**. Envie o arquivo `README.md` e a pasta `assets` com todo o conteúdo. Eles devem ficar diretamente na raiz do repositório, sem uma pasta `Perfil_GitHub_Punk` em volta.
4. Confirme o commit e abra seu perfil. O README aparece automaticamente quando o repositório é público e tem o mesmo nome de usuário.

Se já houver um README no repositório, guarde uma cópia antes de substituí-lo. Não envie apenas o ZIP: o GitHub precisa dos arquivos extraídos.

Você também pode enviar o pacote inteiro extraído. Só `README.md` e `assets/` são necessários para a exibição; os demais arquivos servem para edição.

Regras do perfil: [documentação oficial do GitHub](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme).

## O que vem no pacote

| Arquivo ou pasta | Para que serve |
| --- | --- |
| `README.md` | Perfil pronto para publicar. |
| `assets/quarto-punk.png` | Banner original, sem seu nome. |
| `assets/avatar-punk.png` | Avatar opcional e ilustração do Lado B, sem seu nome. |
| `assets/*.svg` | Título, navegação, seção e rodapé desenhados para este perfil. |
| `perfil.json` | Textos, usuário, links e projetos editáveis em um lugar. |
| `templates/README.template.md` | Estrutura usada pelo montador opcional. |
| `scripts/montar.py` | Monta o README com Python 3.9 ou superior, sem dependências. |
| `design/` | Direção visual, prompts e versões SVG com texto editável. |
| `preview/` | Prévias estáticas da composição em fundos claro/escuro e largura de celular. |

## Mudar os textos

O caminho mais rápido é editar o próprio `README.md` no GitHub. O texto de apresentação é uma sugestão; ajuste-o para soar como você.

Para centralizar a edição, altere `perfil.json` e execute:

```bash
python scripts/montar.py
```

No Windows, você também pode usar `py scripts/montar.py`. No macOS/Linux, `python3 scripts/montar.py`.

O comando substitui o README usando o JSON e o template. Se editar o README diretamente, não rode o montador depois sem passar suas mudanças para esses arquivos. O montador não publica nada: envie o README atualizado ao GitHub.

Para conferir se o README e a configuração correspondem:

```bash
python scripts/montar.py --check
```

## Incluir projetos e contatos

Em `perfil.json`, a lista `projetos` aceita objetos com `titulo`, `texto` e `url`. A lista `contatos` aceita `titulo` e `url`. Use links reais `https://...` ou `mailto:...`. Depois rode o montador e envie o README atualizado.

Essas listas começam vazias e suas seções só aparecem quando você adiciona itens. Os dois botões existentes abrem seus repositórios e favoritos; não dependem de nomes de projetos. Não foram incluídos números de contribuição, linguagens ou níveis de domínio não confirmados.

Se seu usuário mudar, altere `usuario` no JSON e monte novamente. Renomeie também o repositório de perfil.

## Usar o avatar

Para trocar a foto de perfil, envie `assets/avatar-punk.png` nas configurações do seu perfil e ajuste o recorte. A imagem é opcional; publicar o README não muda seu avatar.

## Personalizar os elementos gráficos

Os SVGs finais têm letras convertidas em curvas, preservando a aparência sem instalar fontes. Em `design/svg-editaveis/`, estão as versões com texto. Abra-as em um editor vetorial, altere e exporte como SVG simples para substituir o arquivo correspondente em `assets/`.

Preserve o `viewBox`, não adicione imagens externas ou scripts e mantenha o nome do arquivo. As fontes de desenho são DejaVu Sans Bold e DejaVu Sans Mono.

## Como a apresentação funciona

O perfil usa Markdown, imagens locais, links e um bloco expansível `details`. As imagens mantêm a mesma paleta nos temas claro e escuro; o texto acompanha o tema do GitHub.

O GitHub remove estilos inline e scripts do README. Por isso a identidade visual está nos SVGs e nas ilustrações, e não depende de CSS, JavaScript, iframes ou serviços de badges. Veja o [processamento oficial do Markdown](https://github.com/github/markup) e as [seções expansíveis](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections).

As imagens usam caminhos relativos, conforme a [orientação do GitHub](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#images). Mantenha `assets/` ao lado do README.

As imagens da pasta `preview/` são prévias estáticas locais do conteúdo do README; a moldura, os espaçamentos e a tipografia do GitHub podem variar. A inspeção verificou a integridade dos arquivos, os caminhos das imagens e a composição visual. A interação do Lado B não foi testada em navegador nesta entrega. O pacote não foi publicado em sua conta.
