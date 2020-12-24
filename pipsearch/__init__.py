import json
import pathlib
import random
import re
from time import sleep

import requests
from bs4 import BeautifulSoup, SoupStrainer



# add different params for the PyPI search to get different kinds of results
# this should allow us to get more packages when scraping
_pypi_params = {
    'relevance': {
        'q': '',
        'o': '',
        'c': ''
    }
}



def _get_soup(link, params={}, strainer=None):
    with requests.get(link, params=params) as req:
        if req.status_code < 400:
            return BeautifulSoup(req.text, 'lxml', parse_only=strainer)
        else:
            return None



class Package:
    """docstring for Package."""

    def __init__(self, name):
        self.name = name
        soup = _get_soup(f"https://pypi.org/project/{self.name}/", strainer=SoupStrainer(id='content'))
        # pathlib.Path(f"{self.name}.html").write_text(soup.prettify())
        if soup == None:
            print(f"{self.name} doesn't exist.")
            del self

        def _soup_text(**kwargs):
            return soup.find(**kwargs).get_text()

        self.pip_command = _soup_text(id='pip-command')
        self.summary = _soup_text(class_='package-description__summary')
        self.description = _soup_text(class_='project-description')



class PyPI:
    def __init__(self, build=False, packages_file='packages.json', pages_to_get=500):
        self.build = build
        self.packages_file = pathlib.Path(packages_file)
        # search results only go to 500 pages
        self.pages_to_get = pages_to_get
        if self.pages_to_get < 0 or self.pages_to_get > 500:
            raise ValueError(f"PyPI search results can only go up to 500 pages. Please specify a number between 0 and 500.")

        self.packages = []
        if self.build == True or not self.packages_file.exists():
            # search results only go to 500 pages
            for page in range(1, self.pages_to_get + 1):
                print(f"Getting page {page} of {self.pages_to_get}", end='\r')
                soup = _get_soup('https://pypi.org/search/', {'c': '', 'page': page}, SoupStrainer('a', class_='package-snippet'))
                # wait between each request so we don't put too much strain on PyPi's server
                sleep(1)

                for link in soup.find_all('a'):
                    # package names can only contain letters, numbers, underscores, and periods
                    name = re.findall('(?<=\/project\/)[A-Za-z0-9_\-\.]+', link.get('href'))[0]
                    if name not in self.packages:
                        self.packages.append(name)

            self.packages_file.write_text(json.dumps(self.packages))
            print(f"Packages file created at {self.packages_file} with {len(self.packages)} packages")
        else:
            self.packages = json.loads(self.packages_file.read_text())

    def random(self):
        package_name = random.choice(self.packages)
        return Package(package_name)

    def search(self, name):
        if (name not in self.packages and
            (package := Package(name)) is not None):
            self.packages.append(name)
            self.packages_file.write_text(json.dumps(self.packages))
            return package
