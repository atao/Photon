import re
import requests
import random

from core.utils import verb, xml_parser
from core.colors import run, good
from plugins.wayback import time_machine


def zap(input_url, archive, domain, host, internal, robots, proxies, verf):
    response = ""
    """Extract links from robots.txt and sitemap.xml."""
    if archive:
        print(f"{run} Fetching URLs from archive.org")
        if False:
            archived_urls = time_machine(domain, "domain")
        else:
            archived_urls = time_machine(host, "host")
        print(f"{good} Retrieved {len(archived_urls) - 1} URLs from archive.org")
        for url in archived_urls:
            verb("Internal page", url)
            internal.add(url)
    # Makes request to robots.txt
    try:
        response = requests.get(
            input_url + "/robots.txt", proxies=random.choice(proxies), verify=verf
        ).text
    except requests.exceptions.SSLError as Error:
        response = requests.get(
            input_url + "/robots.txt", proxies=random.choice(proxies), verify=verf
        ).text
    # Making sure robots.txt isn't some fancy 404 page
    if "<body" not in response:
        # If you know it, you know it
        matches = re.findall(r"Allow: (.*)|Disallow: (.*)", response)
        if matches:
            # Iterating over the matches, match is a tuple here
            for match in matches:
                # One item in match will always be empty so will combine both
                # items
                match = "".join(match)
                # If the URL doesn't use a wildcard
                if "*" not in match:
                    url = input_url + match
                    # Add the URL to internal list for crawling
                    internal.add(url)
                    # Add the URL to robots list
                    robots.add(url)
            print(f"{good} URLs retrieved from robots.txt: {len(robots)}")
    # Makes request to sitemap.xml
    try:
        response = requests.get(
            input_url + "/sitemap.xml", proxies=random.choice(proxies), verify=verf
        ).text
    except requests.exceptions.SSLError as Error:
        response = requests.get(
            input_url + "/sitemap.xml", proxies=random.choice(proxies), verify=verf
        ).text
    # Making sure robots.txt isn't some fancy 404 page
    if "<body" not in response:
        matches = xml_parser(response)
        if matches:  # if there are any matches
            print(f"{good} URLs retrieved from sitemap.xml: {len(matches)}")
            for match in matches:
                verb("Internal page", match)
                # Cleaning up the URL and adding it to the internal list for
                # crawling
                internal.add(match)
