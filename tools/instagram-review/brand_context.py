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


ALLOWED_FACT_FIELDS = {
    "casa_pratica_ofc": {"product_facts", "verified_affiliate_links", "approved_ctas"},
    "instancia_renascer_belvedere": {"organization_facts", "approved_announcements", "official_links"},
}


def select_brand_context(brand_id: str) -> dict:
    key = (brand_id or "").strip().lower()
    if key not in BRANDS:
        raise ValueError("unknown brand; refusing to infer or mix brand context")
    # Return a copy so downstream callers cannot mutate the canonical profile.
    return {"brand_id": key, **BRANDS[key].copy()}


def build_brand_payload(brand_id: str, facts: dict) -> dict:
    """Build a synthetic/content payload only from fields allowed for this brand."""
    context = select_brand_context(brand_id)
    allowed = ALLOWED_FACT_FIELDS[context["brand_id"]]
    unknown = set(facts) - allowed
    if unknown:
        raise ValueError(f"facts contain fields not allowed for brand {context['brand_id']}: {sorted(unknown)}")
    return {"brand": context, "facts": dict(facts)}
