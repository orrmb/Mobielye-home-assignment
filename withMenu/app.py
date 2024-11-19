import requests
import os


TOKEN = os.environ['GITLABTOKEN']
roles_name = {"10": "Guest", "20": "Reporter",  "30": "Developer", "40": "Maintainer", "50": "Owner"}


def menu():
    print('\nPlease choose one from the option:')
    print('1) Grant/change role permission for user in repo/group.')
    print('2) Show issues/mr in a specific year.')
    print('3) Exit')
    user_choose = input('Enter your choose: ')
    if user_choose == '1':
        return user_per()
    elif user_choose == '2':
        return issues_mr()
    elif user_choose == '3':
        exit()
    else:
        print('Pay attention that you enter one form the option...\n')
        menu()


def valid_user(user_exists):
    user_data = user_exists.json()
    if len(user_data) == 0:
        print("Username not found, please try again.")
        return user_per()
    else:
        user_id = user_data[0]['id']
        return user_id


def valid_group_repo(repo_group):
    if '/' in repo_group:
        split_url = repo_group.split('/')
        check_project = requests.get("https://gitlab.com/api/v4/projects/{}%2F{}".format(split_url[0], split_url[1]),
                                         headers={'PRIVATE-TOKEN': TOKEN})
        if check_project.status_code == 200:
            pass
        else:
            print('The project was not found try again...')
            user_per()
    else:
        check_group = requests.get("https://gitlab.com/api/v4/groups/{}".format(repo_group),
                                     headers={'PRIVATE-TOKEN': TOKEN})
        if check_group.status_code == 200:
            pass
        else:
            print('The group was not found try again...')
            user_per()


def valid_gr_user(id_user,repo_group):
    if '/' in repo_group:
        split_url = repo_group.split('/')
        check_user_gr = requests.get("https://gitlab.com/api/v4/projects/{}%2F{}/members/{}"
                                         .format(split_url[0], split_url[1], id_user),
                                         headers={'PRIVATE-TOKEN': TOKEN})
        if check_user_gr.status_code == 200:
            pass
        else:
            print('The user is not part of the project')
            user_per()
    else:
        check_user_gr = requests.get("https://gitlab.com/api/v4/groups/{}/members/{}"
                                         .format(repo_group,id_user),
                                         headers={'PRIVATE-TOKEN': TOKEN})
        if check_user_gr.status_code == 200:
            pass
        else:
            print('The user is not part of the group')
            user_per()


def user_per():
    username = input('Enter username: ')
    user_exists = requests.get("https://gitlab.com/api/v4/users?username={}".format(username))
    id_user = valid_user(user_exists)
    repo_group = input('Enter repo/group, if repo enter with his namespace: ')
    valid_group_repo(repo_group)
    valid_gr_user(id_user, repo_group)
    print("Enter role (choose the number of the access level e.g Developer is '30'):\n"
                     '1) Guest - (10)\n'
                     '2) Reporter - (20)\n'
                     '3) Developer - (30)\n'
                     '4) Maintainer - (40)\n'
                     '5) Owner - (50)\n')
    role_id = input("Your choose: ")
    prompt_change = input('Pay attention the role for the username {} will going to change to {} are you sure (y/n)? '.format(username, roles_name[role_id]))
    if prompt_change in ['y', 'Y', 'yes', 'YES']:
        if '/' in repo_group:
            split_url = repo_group.split('/')
            requests.put("https://gitlab.com/api/v4/projects/{}%2F{}/members/{}?access_level={}"
                         .format(split_url[0], split_url[1], id_user, role_id), headers={'PRIVATE-TOKEN': TOKEN})
            print('The username {} is now {} in {}. '.format(username, roles_name[role_id], repo_group))
            menu()
        else:
            requests.put("https://gitlab.com/api/v4/groups/{}/members/{}?access_level={}"
                         .format(repo_group, id_user, role_id), headers={'PRIVATE-TOKEN': TOKEN})
            print('The username {} is now {} in {}. '.format(username, roles_name[role_id], repo_group))
            menu()


def issues_mr():
    iss_mr = input('Enter what do you want to see issues/ mr: ')
    if iss_mr == 'issues':
        endpoint = 'issues'
    elif iss_mr == 'mr':
        endpoint = 'merge_requests'
    else:
        print('Error please enter issues/mr')
        issues_mr()

    year = int(input('Enter the year that you want to see the (4 digits) {}: '.format(iss_mr)))
    if len(str(year)) != 4:
        print('Please year with 4 digits please')
        issues_mr()

    params = {
        'created_after': f'{year}-01-01T00:00:00Z',  # Start of the year
        'created_before': f'{year}-12-31T23:59:59Z',  # End of the year
        'per_page': 100}  # Fetch 100 items per request
    response = requests.get("https://gitlab.com/api/v4/{}".format(endpoint), headers={'PRIVATE-TOKEN': TOKEN},
                            params=params)
    if response.status_code == 200:
        data = response.json()
        if endpoint == 'issues':
            for issues in data:
                print('-----')
                print('Merge ID: {}'.format(issues['id']))
                print('Project ID: {}'.format(issues['project_id']))
                print('Title: {}'.format(issues['title']))
                print('description: {}'.format(issues['description']))
                print('state: {}'.format(issues['state']))
                print('author: {}'.format(issues['author']['username']))
                print('-----')
            menu()
        elif endpoint == 'merge_requests':
            for mr in data:
                print('-----')
                print('Merge ID: {}'.format(mr['id']))
                print('Project ID: {}'.format(mr['project_id']))
                print('Title: {}'.format(mr['title']))
                print('description: {}'.format(mr['description']))
                print('state: {}'.format(mr['state']))
                print('Target branch: {}'.format(mr['target_branch']))
                print('Source branch: {}'.format(mr['source_branch']))
                print('author: {}'.format(mr['author']['username']))
                print('-----')
            menu()
    else:
        print('There is no {} in this year, please try again'.format(endpoint))
        issues_mr()


if __name__ == "__main__":
    menu()
