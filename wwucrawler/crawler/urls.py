import re


def get_domain(url: str) -> str:
    return re.split(r"/", url, 3)[2]


def get_domain_subdomain(url: str) -> tuple[str, str]:
    full_domain = get_domain(url)
    segmented = full_domain.split(".")
    domain = ".".join(segmented[len(segmented) - 2 :])
    subdomain = segmented[len(segmented) - 3] if len(segmented) > 2 else None
    return domain, subdomain


def strip_query(url: str) -> str:
    return url.split("?")[0]
