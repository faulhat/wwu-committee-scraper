import re


def get_domain(url):
    return re.split(r"/", url, 3)[2]


def get_domain_subdomain(url):
    full_domain = get_domain(url)
    segmented = full_domain.split(".")
    domain = ".".join(segmented[len(segmented) - 2 :])
    subdomain = segmented[len(segmented) - 3] if len(segmented) > 2 else None
    return domain, subdomain


# Get rid of the GET request query
#  Needed since some pages contain recursive links
def strip_query(url):
    return url.split("?")[0]
