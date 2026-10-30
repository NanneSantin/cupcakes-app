"""Regras de validação reaproveitadas pelos controllers."""

import re

EMAIL_VALIDO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validar_nome(nome):
    """Nome com pelo menos 3 letras e que não seja um e-mail."""
    if len(nome) < 3 or "@" in nome or not re.search(r"[A-Za-zÀ-ÿ]{2,}", nome):
        return "Informe seu nome (não use o e-mail no lugar do nome)."
    return None


def validar_endereco(endereco):
    """Endereço mínimo: nome da rua, número e bairro/cidade.
    Ex.: "Rua das Flores, 100 - Centro, Curitiba"."""
    tem_rua = re.search(r"[A-Za-zÀ-ÿ]{3,}", endereco)
    tem_numero = re.search(r"\d", endereco)
    partes = [p for p in re.split(r"[,\-]", endereco) if p.strip()]
    if len(endereco) < 10 or not tem_rua or not tem_numero or len(partes) < 3:
        return (
            "Informe um endereço completo: rua, número e bairro/cidade "
            "(ex.: Rua das Flores, 100 - Centro, Curitiba)."
        )
    return None


def ler_quantidade_valida(texto):
    """Converte a quantidade digitada em número inteiro maior que zero.
    Retorna None se for inválida (vazia, texto, zero ou negativa)."""
    try:
        quantidade = int(str(texto).strip())
    except (TypeError, ValueError):
        return None
    return quantidade if quantidade >= 1 else None
