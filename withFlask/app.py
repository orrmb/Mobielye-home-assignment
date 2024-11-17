from flask import Flask, Response, request, jsonify
import os
import gitlab

app = Flask(__name__)

roles_name = {"10": "Guest", "20": "Reporter",  "30": "Developer", "40": "Maintainer", "50": "Owner"}
# gl = gitlab.Gitlab(url='https://gitlab.com', private_token=TOKEN)

@app.route("/")
def introduction():
    message = '''
    Run the following command to grant/change role permission for user in GitLab repo/group:

    If you run locally, run this:
    example for group--->>
    curl -X POST http://localhost:8080/chrole -H 'Content-Type: application/json' -d '{"username":"dany","group":"test-group", "role": "Guest"}'
    
    example for repo --->>
    curl -X POST http://localhost:8080/chrole -H 'Content-Type: application/json' -d '{"username":"dany","repo":"namespace/repo", "role": "Guest"}'

    If you run on host machine, run this:
    example for group --->>
    curl -X POST http://<IP ADDRESS>:8080/chrole -H 'Content-Type: application/json' -d '{"username":"dany","group":"test-group", "role": "Guest"}'

    example for repo --->>
    curl -X POST http://<IP ADDRESS>:8080/chrole -H 'Content-Type: application/json' -d '{"username":"dany","repo":"namespace/repo", "role": "Guest"}'

    Available roles: 
    1) Guest
    2) Reporter
    3) Developer
    4) Maintainer
    5) Owner

------------------------------------------------------------------------------------------------------------------------------------------------------------------

    Run the following command to present the issues/merge request from some year, run this:

    If you run locally, run this:
    example for issues --->>
    curl -X POST http://localhost:8080/mr_issues -H 'Content-Type: application/json' -d '{"kind":"issues","year":"2024"}'
    
    example for merge request --->>
    curl -X POST http://localhost:8080/mr_issues -H 'Content-Type: application/json' -d '{"kind":"mr","year":"2024"}'

    If you run on host machine, run this:
    example for issues --->>
    curl -X POST http://<IP ADDRESS>:8080/mr_issues -H 'Content-Type: application/json' -d '{"kind":"issues","year":"2024"}'

    example for merge request --->>
    curl -X POST http://<IP ADDRESS>:8080/mr_issues -H 'Content-Type: application/json' -d '{"kind":"mr","year":"2024"}'


    '''
    return Response(message, content_type='text/plain')

@app.route('/chrole', methods=['POST'])
def change_role_group_repo():
    data = request.get_json()

    username = data.get('username')
    group = data.get('group')
    repo = data.get('repo')
    role = data.get('role')

    if username or role or (repo or group) == 'None' :
        return jsonify({"error": "username, group/repo and role are required"}), 400
    
    return_message=f'''
    username: {username},
    group   : {group},
    repo    : {repo},
    role    : {role}
'''
    if group != 'None':
        pass

    else:

    return jsonify(return_message),200
    

@app.route('/mr_issues', methods=['POST'])
def get_mr_issues():
    data = request.get_json()
    mr_issues = data.get('kind')
    year = data.get('year')
    params = {
        'created_after': f'{year}-01-01T00:00:00Z',  # Start of the year
        'created_before': f'{year}-12-31T23:59:59Z',  # End of the year
        'per_page': 100}
    pass
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
