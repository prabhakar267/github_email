# -*- coding: utf-8 -*-
# @Author: prabhakar
# @Date:   2016-06-23 00:22:41
# @Last Modified by:   Prabhakar Gupta
# @Last Modified time: 2016-06-25 18:47:44

import requests
import sys
import json

from constants import ERROR_DICT, GITHUB_URL


def get_json_response(url):
    response = requests.get(url)
    return json.loads(response.text)


def add_email(email_set, email, max_len):
    if len(email_set) >= max_len:
        break_flag = True
    else:
        email_set = email_set | set([email])
        break_flag = False

    return email_set, break_flag


def main():
    user_email = set([])
    try:
        user = sys.argv[1]

        if len(sys.argv) > 1:
            max_email = int(sys.argv[2])
        else:
            max_email = 5
        
        users_profile_url = GITHUB_URL + "users/{0}".format(user)
        response = get_json_response(users_profile_url)

        # some error encountered
        if 'message' in response:
            return response['message']

        user_name = response['name']

        users_repository_url = GITHUB_URL + "users/{0}/repos?type=owner&sort=updated".format(user)
        response = get_json_response(users_repository_url)
        
        break_flag = False
        for repo in response:
            if not repo['fork']:
                users_repository_name = repo['full_name']
                repos_commit_url = GITHUB_URL + "repos/{0}/commits".format(users_repository_name)
                commit_reponse = get_json_response(repos_commit_url)
                
                possible_positions = ['committer', 'author']

                for commit in commit_reponse:
                    for i in possible_positions:
                        if (commit['commit'][i]['name'] == user_name):
                            user_email, break_flag = add_email(user_email, commit['commit'][i]['email'], max_email)

                    if break_flag:
                        break

            if break_flag:
                break

        return user_email

    except IndexError:
        return u'Not Found'

    except ValueError:
        return u'ValueError'

    except requests.exceptions.ConnectionError:
        return u'ConnectionError'


if __name__ == "__main__":
    email_response = main()
    
    if type(email_response) == set:
        response = {
            'success' : True,
            'email': list(email_response)
        }
    else:
        if email_response in ERROR_DICT.keys():
            message = ERROR_DICT[email_response]
        else:
            message = email_response

        response = {
            'success' : False,
            'message' : message,
        }

    print response
