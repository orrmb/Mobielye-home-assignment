import requests
import gitlab
import os

TOKEN = ''
roles_name = {"10": "Guest", "20": "Reporter",  "30": "Developer","40": "Maintainer", "50": "Owner"}

def menu():
    print('\nPlease choose one from the option:')
    print('1) Grant/change role permission for user in repo')
    print('2) issues/mr (mr= merge requests) created on the given year.')
    user_choose = input('Enter your choose: ')
    if user_choose == '1':
        return user_per()
    elif user_choose == '2':
        return issues_mr()
    else:
        print('Pay attention that you enter one form the option...\n')
        menu()


def user_per():
    print("hey,")
    repo_group = input('Enter repo/group: ')
    respone = requests.get("https://gitlab.com/api/v4/groups/{}/members".format(repo_group), headers={'PRIVATE-TOKEN': TOKEN})
    data = respone.json()
    username = input('Enter username: ')
    usernames = [user['username']for user in data]
    if username in usernames:
        respone_id = requests.get("https://gitlab.com/api/v4/users?username={}".format(username), headers={'PRIVATE-TOKEN': TOKEN})
        data = respone_id.json()
        user_id = data[0]['id']
        print(user_id)
        print("Enter role (choose the number of the access level e.g Developer is '30':\n"
                     '1) Guest - (10)\n'
                     '2) Reporter - (20)\n'
                     '3) Developer - (30)\n'
                     '4) Maintainer - (40)\n'
                     '5) Owner - (50)\n')
        role_id = input("Your choose: ")
        prompt_change = input('Pay attention the role for the username {} will going to change to {} are you sure (y/n)? '.format(username, roles_name[role_id]))
        if prompt_change in ['y', 'Y', 'yes', 'YES']:
            requests.put("https://gitlab.com/api/v4/groups/{}/members/{}?access_level={}".format(repo_group, user_id, role_id), headers={'PRIVATE-TOKEN': TOKEN})
            print('The username {} is now {} in {}. '.format(username, roles_name[role_id], repo_group))

        else:
            print('try again...')
            menu()
    else:
        print('Error, no username found in {}, please try again'.format_map(repo_group))
        menu()


def issues_mr(username):


    pass


if __name__ == "__main__":
    menu()
