#!/usr/bin/env python3
"""Atualiza o README usando perfil.json. Python 3.9+, sem dependências.

Uso, a partir da pasta do projeto:
    python scripts/montar.py
    python scripts/montar.py --check

Não acessa a internet, não publica arquivos e não altera as imagens.
"""

import argparse
import html
import json
import re
import sys
from pathlib import Path
from string import Template
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


def texto(value):
    """Escapa texto inserido dentro dos elementos HTML do template."""
    if not isinstance(value, str):
        raise ValueError("Os campos de texto precisam ser strings.")
    return html.escape(value, quote=True)


def markdown_texto(value):
    """Escapa texto comum nos trechos interpretados como Markdown."""
    return re.sub(r"([\\`*_{}\[\]#!|])", r"\\\1", texto(value))


def lista(config, key):
    value = config.get(key, [])
    if not isinstance(value, list):
        raise ValueError(f"O campo '{key}' precisa ser uma lista.")
    if any(not isinstance(item, dict) for item in value):
        raise ValueError(f"Cada item de '{key}' precisa ser um objeto.")
    return value


def link_url(value):
    if not isinstance(value, str):
        raise ValueError("O campo 'url' precisa ser um texto.")
    parsed = urlparse(value)
    if parsed.scheme not in {"https", "mailto"}:
        raise ValueError("Use uma URL https:// ou mailto: nos links.")
    if parsed.scheme == "https" and not parsed.netloc:
        raise ValueError("URL HTTPS sem domínio.")
    if parsed.scheme == "mailto" and "@" not in parsed.path:
        raise ValueError("Endereço de e-mail incompleto.")
    if any(c.isspace() for c in value):
        raise ValueError("Não use espaços ou quebras de linha na URL.")
    return html.escape(value, quote=True)


def montar(config):
    if not isinstance(config, dict):
        raise ValueError("perfil.json precisa conter um objeto JSON.")
    usuario = config.get("usuario", "")
    if not isinstance(usuario, str) or not re.fullmatch(
        r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", usuario
    ) or "--" in usuario:
        raise ValueError("Confira o nome de usuário do GitHub em 'usuario'.")

    bancada = []
    for item in lista(config, "bancada"):
        bancada.append(f"### {markdown_texto(item['titulo'])}\n\n{markdown_texto(item['texto'])}")

    projetos = []
    for item in lista(config, "projetos"):
        title, url = texto(item["titulo"]), link_url(item["url"])
        description = texto(item.get("texto", ""))
        projetos.append(f'<li><a href="{url}"><strong>{title}</strong></a>'
                        + (f" — {description}" if description else "") + "</li>")
    projetos_html = ""
    if projetos:
        projetos_html = "<h3>Em destaque</h3>\n\n<ul>\n" + "\n".join(projetos) + "\n</ul>"

    contatos = []
    for item in lista(config, "contatos"):
        contatos.append(f'<a href="{link_url(item["url"])}">{texto(item["titulo"])}</a>')
    contatos_html = ""
    if contatos:
        contatos_html = '<p align="center">' + " &nbsp; / &nbsp; ".join(contatos) + "</p>"

    template = Template((ROOT / "templates/README.template.md").read_text(encoding="utf-8"))
    return template.substitute(
        usuario=usuario,
        frase=texto(config["frase"]),
        bio=texto(config["bio"]),
        bancada="\n\n".join(bancada),
        lado_b=markdown_texto(config["lado_b"]),
        nota=texto(config["nota"]),
        projetos=projetos_html,
        contatos=contatos_html,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="confere sem gravar arquivos")
    args = parser.parse_args()
    try:
        config = json.loads((ROOT / "perfil.json").read_text(encoding="utf-8"))
        result = montar(config)
        output = ROOT / "README.md"
        if args.check:
            if not output.exists() or output.read_text(encoding="utf-8") != result:
                print("README diferente da configuração. Rode: python scripts/montar.py")
                return 1
            print("README corresponde ao perfil.json e ao template.")
        else:
            temporary = output.with_suffix(".md.tmp")
            temporary.write_text(result, encoding="utf-8")
            temporary.replace(output)
            print(f"README atualizado: {output}")
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Não foi possível montar o README: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
