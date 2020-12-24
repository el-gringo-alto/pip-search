# pip search
Get information about packages from PyPI. This was inspired from [a project suggestion by u/appinv in the r/Python project ideas megathread](https://www.reddit.com/r/Python/comments/kh5hrt/monday_megathread_project_ideas/ggkfezx?utm_source=share&utm_medium=web2x&context=3) with a little hint of my own boredom to back it up.

## Installation
```
cd pip-search
pip install -r requirements.txt
```

## Usage
```python
import pipsearch

# initialize the PyPI class
pypi = pipsearch.PyPI()

# get a specific package
package = pypi.search('requests')

# output the package data
print(package.name) # requests
print(package.pip_command) # pip install requests
print(package.summary) # Python HTTP for Humans.

# get a random package
package = pypi.random()
```

## TODO
* Add more information to return about the packages
    * Add Github repository data
* Add more search queries to get more packages
* Add command-line arguments
