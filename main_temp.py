# -*- coding: utf-8 -*-
# @Author: prabhakar
# @Date:   2016-06-23 00:22:41
# @Last Modified by:   Prabhakar Gupta
# @Last Modified time: 2016-06-24 21:39:03

import requests
import sys
import json

GITHUB_URL = "https://api.github.com/"

def get_json_response(url):
    response = requests.get(url)
    return json.loads(response.text)


def main():
    user_email = set([])
    user = sys.argv[1]

    users_profile_url = GITHUB_URL + "users/{0}".format(user)
    response = get_json_response(users_profile_url)
    print response
    user_name = response['name']

    users_repository_url = GITHUB_URL + "users/{0}/repos?type=owner&sort=updated".format(user)
    response = get_json_response(users_repository_url)
    
    for repo in response:
        if not repo['fork']:
            users_repository_name = repo['full_name']
            repos_commit_url = GITHUB_URL + "repos/{0}/commits".format(users_repository_name)
            commit_reponse = get_json_response(repos_commit_url)
            
            break_flag = False
            for commit in commit_reponse:
                if (commit['commit']['committer']['name'] == user_name):
                    if len(user_email) >= 2:
                        break_flag = True
                        break
                    else:
                        new_email = set([commit['commit']['committer']['email']])
                        user_email = user_email | new_email

                if (commit['commit']['author']['name'] == user_name):
                    if len(user_email) >= 2:
                        break_flag = True
                        break
                    else:
                        new_email = set([commit['commit']['author']['email']])
                        user_email = user_email | new_email

            if break_flag:
                break

    print user_email

            # print repos_commit_url
            # break


        # print i['full_name']
    # print user_name

    # import ipdb; ipdb.set_trace()
    # print json.dumps(response, indent=4, sort_keys=True)
    # response_line_list = response.content.splitlines()

    
if __name__ == "__main__":
    main()

# https://api.github.com/users/prabhakar267
# https://api.github.com/users/prabhakar267/repos?type=owner&sort=updated
# https://api.github.com/repos/prabhakar267/github-classifier/commits

# https://gist.github.com/sindresorhus/4512621