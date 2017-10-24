import os
import argparse
from bs4 import BeautifulSoup as soup
from requests import get

parser = argparse.ArgumentParser(description="Download all PDFs on the specified webpage.")
parser.add_argument('url', type=str, help="Webpage to download from")
parser.add_argument('dir', type=str, help="abs/rel path to save the files to")
parser.add_argument('-u', '--user', type=str, help="username for auth if needed")
parser.add_argument('-p', '--password', type=str, help="password for auth if needed")

args = parser.parse_args()
url = args.url
dir = args.dir
usr = args.user
password = args.password

# change working directory to specified dir.
os.chdir(dir)

client = get(url)

page_soup = soup(client.content, "html.parser")

# get all the tags with href attribute.
# ends up being just <a> tags with href attribute.
links = page_soup.find_all(href=True)
for link in links:
    href = link["href"]
    if "pdf" in href:
        # download the file.
        if "/" in href:
            name = href.rsplit('/', 1)[-1]
        else:
            name = href
        pdf = get('/'.join([url, href]))
        with open(name, 'wb') as file:
            file.write(pdf.content)
