from urllib.parse import urlparse, parse_qsl
from collections import Counter

# --- Classe utilitaire (compute) : permet d'analyser une URL et d'en extraire des caractéristiques ---
class URLInspector:
    def __init__(self, url):
        self.url = url
        self.parsed = urlparse(url)
        self.query_params = parse_qsl(self.parsed.query, keep_blank_values=True)

    def is_https(self):
        return self.parsed.scheme == "https"

    def get_netloc(self):
        return self.parsed.netloc

    def get_duplicate_params(self):
        keys = [k for k, _ in self.query_params]
        return [k for k, v in Counter(keys).items() if v > 1]

    def get_param_keys(self):
        return [k for k, _ in self.query_params]

    def get_unique_param_keys(self):
        return set(k for k, _ in self.query_params)

    def get_fragment(self):
        return self.parsed.fragment

    def has_fragment(self):
        return bool(self.parsed.fragment)

    def is_url_too_long(self, limit=1000):
        return len(self.url) > limit

    def summary(self):
        return {
            "url": self.url,
            "https": self.is_https(),
            "hostname": self.get_netloc(),
            "param_count": len(self.query_params),
            "param_keys": self.get_param_keys(),
            "dup_params": self.get_duplicate_params(),
            "fragment": self.get_fragment(),
            "has_fragment": self.has_fragment(),
            "url_too_long": self.is_url_too_long()
        }
