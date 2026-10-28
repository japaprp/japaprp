"""Small deterministic router for content tasks; no network or account actions."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Route:
    primary: str
    optional: tuple[str, ...]
    reason: str


def route_content(*, platform: str, intent: str) -> Route:
    """Choose the minimum local workflow for an explicitly stated task."""
    p = (platform or "").strip().lower()
    i = (intent or "").strip().lower()

    if not i:
        raise ValueError("intent is required")

    primary = "content-commerce-distribution"
    optional = []

    if any(term in i for term in ("benchmark", "viral", "concorrente", "mediana", "analisar reels", "análise de reels")):
        if p in {"instagram", "instagram reels", "reels"}:
            optional.append("ig-viral")
        elif p in {"tiktok", "youtube shorts", "kwai"}:
            optional.append("virality")
    elif any(term in i for term in ("pontuar hook", "pontuação do hook", "avaliar gancho", "hook score")):
        optional.append("virality")
    elif p in {"instagram", "instagram reels", "reels"}:
        if any(term in i for term in ("legenda", "caption")):
            optional.append("ig-caption")
        if any(term in i for term in ("roteiro", "reel", "reels", "gancho", "hook")):
            optional.append("ig-reel")
        if any(term in i for term in ("perfil", "bio")):
            optional.append("ig-profile")
        if any(term in i for term in ("auditoria", "auditar", "audit")):
            optional.append("ig-audit")

    # Never route publishing to a skill that can publish. Human approval remains required.
    if any(term in i for term in ("publicar", "agendar", "postar automaticamente", "enviar mensagem em massa")):
        return Route(primary, tuple(dict.fromkeys(optional)), "draft/review only; publishing requires separate explicit authorization")
    return Route(primary, tuple(dict.fromkeys(optional)), "general content workflow first; add only platform-specific analysis when intent requires it")
