# -*- coding: utf-8 -*-
# @Author: prabhakar
# @Date:   2016-06-23 00:22:41
# @Last Modified by:   Prabhakar Gupta
# @Last Modified time: 2016-12-25 20:36:29

import requests
import json

GITHUB_URL = "https://api.github.com/"

"""
Function to get JSON response from a URL
:params:
    url     string
:return:
            JSON
"""
def __get_json_response(url):
    response = requests.get(url)
    return json.loads(response.text)

"""
Function to add email to a set of emails and set a loop break flag

:params:
    email_set       set         set of all the emails for the user
    email           string      new email to be added
    max_len         integer     maximum number of emails to be extracted
:return:
    email_set       set         set of all the emails for the user
    break_flag      boolean     if max_limit is reached, break_flag is set to True
"""
def __add_email(email_set, email, max_len):
    email_set = email_set | set([email])
    break_flag = (len(email_set) >= max_len)

    return email_set, break_flag

"""
Function to get user emails using GitHub APIs

:params:
    user        string      a valid GitHub username
    max_limit   integer     maximum number of email ID to be fetched
:return:
    user_email  set         a set of all emails extracted
    message     string      if any error occurs, this holds the respective error message
"""
def __get_github_emails(user, max_limit):
    user_email = set([])
    break_flag = False
    try:
        users_profile_url = GITHUB_URL + "users/{0}".format(user)
        response = __get_json_response(users_profile_url)

        # some error encountered
        if 'message' in response:
            if response['message'] == 'Not Found':
                return u'You need to enter a valid GitHub Username'
            else:
                return response['message']


        user_name = response['name']

        # if user has a public email, add that to the set of emails
        if response['email']:
            user_email, break_flag = __add_email(user_email, response['email'], max_limit)

        if not break_flag:
            users_repository_url = GITHUB_URL + "users/{0}/repos?type=owner&sort=updated".format(user)
            response = __get_json_response(users_repository_url)

            for repo in response:
                if not repo['fork']:
                    users_repository_name = repo['full_name']
                    repos_commit_url = GITHUB_URL + "repos/{0}/commits".format(users_repository_name)
                    commit_reponse = __get_json_response(repos_commit_url)
                    
                    possible_positions = ['committer', 'author']

                    for commit in commit_reponse:
                        for i in possible_positions:
                            if commit['commit'][i]['name'] == user_name:
                                email_string = commit['commit'][i]['email']
                                if "noreply" not in email_string:
                                    user_email, break_flag = __add_email(user_email, email_string, max_limit)

                        if break_flag:
                            break

                if break_flag:
                    break

        if len(user_email) > 0:
            return user_email
        else:
            return u'No emails found'

    except requests.exceptions.ConnectionError:
        return u'Proper internet connection not found'

"""
Function to get the emails associated to a username on GitHub

:params:
    username    string      a valid GitHub username
    num         integer     maximum number of email ID to be fetched, default 1
:return:
    response    JSON response
        success     boolean     flag to determine other key in JSON
        email       list        if 'success' is True, list of all the emails fetched
        message     string      if 'success' is False, returns the error message
"""
def get(username, num=1):
    github_email_response = __get_github_emails(username, num)
    
    if type(github_email_response) == set:
        response = {
            'success' : True,
            'email': list(github_email_response)
        }
    else:
        response = {
            'success' : False,
            'message' : github_email_response,
        }

    return response
