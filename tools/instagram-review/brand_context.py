"""Strict brand-context selector. Unknown/missing brand fails closed."""
BRANDS = {
    "casa_pratica_ofc": {
        "display_name": "Casa Prática OFC",
        "allowed_context": "affiliate home products; factual product benefits; verified affiliate links; manual human-reviewed posts",
    },
    "instancia_renascer_belvedere": {
        "display_name": "Instância Renascer Belvedere",
        "allowed_context": "organization identity, its own website and Instagram, its own approved communications",
    },
}


def select_brand_context(brand_id: str) -> dict:
    key = (brand_id or "").strip().lower()
    if key not in BRANDS:
        raise ValueError("unknown brand; refusing to infer or mix brand context")
    # Return a copy so downstream callers cannot mutate the canonical profile.
    return {"brand_id": key, **BRANDS[key].copy()}
