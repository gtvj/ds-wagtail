import urllib


def skos_id_from_text(text: str) -> str:
    """
    Function to help with generation of SKOS identifiers for model instances
    that represent categories from TNA's official SKOS spec (assembled by
    Matt Hilliard).
    """
    return text.strip().replace("  ", " ").replace(" ", "_")


def urlunparse(scheme="", netloc="", path="", params="", query="", fragment=""):
    return urllib.parse.urlunparse((scheme, netloc, path, params, query, fragment))
