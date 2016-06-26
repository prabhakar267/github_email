# github_email

[![PyPI version](https://badge.fury.io/py/github_email.svg)](https://badge.fury.io/py/github_email)
[![License](http://img.shields.io/:license-mit-blue.svg)](http://doge.mit-license.org)

Get a list of email IDs of any valid GitHub user from one function call **even if there are no public emails** for that user

It checks for all the public commits of the user and if the name of the author of commit is same as the name of user, it fetches that email ID.

## Installation
### Using pip
```pip
pip install github_email
```
### Using Git
```
git clone https://github.com/prabhakar267/github_email.git
cd github_email
python setup.py install
```

## Usage

```python
import github_email

# get JSON response for user
response = github_email.get(<username>, <max_limit>)

if response['success']:
    # prints a list of emails retrieved from public commits of user 
    print response['email']
else:
    # prints the error message related to any error that occured
    print response['message']
    
```

## Example
![github_email](screenshots/Screenshot from 2016-06-26 06:41:23.png?raw=true)

## Inspiration
[**github-email**](https://github.com/paulirish/github-email) by `paulirish`
I wanted to write a module, so as to use this in other projects
