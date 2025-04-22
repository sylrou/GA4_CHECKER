# --- query_classifier.py ---
# --- Dictionnaire enrichi pour classification de paramètres d'URL ---
# --- Ce dictionnaire est à enrichir et sera compute pour améliorer la time complexity ---

import re

QUERY_PARAM_CATEGORIES = {
    "marketing": {
        "gclid", "fbclid", "msclkid", "ttclid", "dclid",
        "yclid", "pk_campaign", "pk_kwd", "ref", "referrer",
        "source", "affid", "affiliate", "cid"
    },

    "ecommerce": {
        "product_id", "category", "variant", "coupon", "discount",
        "order_id", "orderid", "cart_id", "item_id", "sku", "quantity", "price"
    },

    "search": {
        "q", "query", "search", "s", "k", "keyword", "term"
    },

    "navigation": {
        "page", "tab", "step", "section", "view", "mode", "filter", "sort", "lang", "locale"
    },

    "critical": {
        "user_id", "userid", "session_id", "sessionid", "auth", "token",
        "email", "mail", "name", "firstname", "lastname", "username", "login",
        "lat", "lng", "latitude", "longitude", "phone", "zipcode", "country", "city",
        "token"
    },

    "technical": {
    # Standard
    "debug", "preview", "test", "cache_buster", "cb", "timestamp", "ts",
    "rand", "nonce", "v", "version", "bust",

    # WordPress
    "preview_id", "preview_nonce", "p", "page_id", "post_type", "post",
    "attachment_id", "m", "cat", "tag", "author", "feed", "comments_popup",

    # Shopify
    "variant", "view", "section_id", "page", "sort_by", "constraint",
    "customer_posted", "form_type", "utf8", "return_url", "design_theme_id",
    "shop", "checkout_url", "key", "step",

    # PrestaShop
    "id_product", "id_category", "id_lang", "id_currency", "controller",
    "fc", "orderby", "orderway", "n", "search_query", "submit_search",
    "back", "token"
    },

    "experiment": {
        "abtest", "exp", "experiment", "variation", "var", "testgroup"
    }
}

# --- Mise à plat du dictionnaire au-dessus pour réduire la time/complexity lors du compute ---
PARAM_TO_CATEGORY = {
    param.lower(): category
    for category, params in QUERY_PARAM_CATEGORIES.items()
    for param in params
}

# --- Mise à plat du dictionnaire au-dessus pour réduire la time/complexity lors du compute ---
def classify_query_param(param_name: str) -> str:
    """
    Retourne la catégorie d'un paramètre d'URL en fonction de son nom.
    Exemple : 'utm_source' → 'tracking'
    """
    r1 = r'(token|mail|email|session|auth)'
    r2 = r'(^utm_|^at_|^pk_|clid$|campaign|source)'

    if re.search(r1, param_name.lower()):
        return 'critical'
    elif re.search(r2, param_name.lower()):
        return 'marketing'
    else:
        return PARAM_TO_CATEGORY.get(param_name.lower(), "other")
