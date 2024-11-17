import json
import requests


def valid_user(user_exists):
    user_data = user_exists.json()
    if len(user_data) == 0:
        print("Username not found, please try again.")
        return user_per()
    else:
        user_id = user_data[0]['id']


def user_per():
    username = input('Enter username: ')
    try:
        requests.get("https://gitlab.com/api/v4/users?username={}".format(username))
    except:
        print('The uuser')


TOKEN = 'glpat-uKnMSftzai1mySyh9x_m'


if __name__ == "__main__":
    user_per()