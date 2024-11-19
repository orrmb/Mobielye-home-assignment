from flask import Flask, Response, request, jsonify
import os
import gitlab

app = Flask(__name__)

TOKEN = os.environ['GITLABTOKEN']

roles_name = {
    "Guest": 10,
    "Reporter": 20,
    "Developer": 30,
    "Maintainer": 40,
    "Owner": 50
}
gl = gitlab.Gitlab(url='https://gitlab.com', private_token=TOKEN)

@app.route("/")
def introduction():
    message = '''
    Run the following command to grant/change role permission for user in GitLab repo/group:

    If you run locally, run this:
    example for group--->>
    curl -X POST http://localhost:8080/chrole -H 'Content-Type: application/json' -d '{"username": "dany","group": "test-group", "role": "Guest"}'
    
    example for repo --->>
    curl -X POST http://localhost:8080/chrole -H 'Content-Type: application/json' -d '{"username": "dany","repo": "namespace/repo", "role": "Guest"}'

    If you run on host machine, run this:
    example for group --->>
    curl -X POST http://<IP ADDRESS>:8080/chrole -H 'Content-Type: application/json' -d '{"username": "dany", "group": "test-group", "role": "Guest"}'

    example for repo --->>
    curl -X POST http://<IP ADDRESS>:8080/chrole -H 'Content-Type: application/json' -d '{"username": "dany", "repo": "namespace/repo", "role": "Guest"}'

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
    curl -X POST http://localhost:8080/mr_issues -H 'Content-Type: application/json' -d '{"kind": "issues","year": "2024"}'
    
    example for merge request --->>
    curl -X POST http://localhost:8080/mr_issues -H 'Content-Type: application/json' -d '{"kind": "mr", "year": "2024"}'

    If you run on host machine, run this:
    example for issues --->>
    curl -X POST http://<IP ADDRESS>:8080/mr_issues -H 'Content-Type: application/json' -d '{"kind": "issues", "year":"2024"}'

    example for merge request --->>
    curl -X POST http://<IP ADDRESS>:8080/mr_issues -H 'Content-Type: application/json' -d '{"kind": "mr", "year": "2024"}'


    '''
    return Response(message, content_type='text/plain')

@app.route('/chrole', methods=['POST'])
def change_role_group_repo():
    data = request.get_json()

    username = data.get('username')
    group = data.get('group')
    repo = data.get('repo')
    role = data.get('role')

    if not username or not role or (not group and not repo):
        return jsonify({"error": "username, group/repo and role are required"}), 400
    
    if role not in roles_name:
        return jsonify({"error": f"Invalid role: {role}. Valid roles are {', '.join(roles_name.keys())}."}), 400
    
    access_level = roles_name[role]

    if group:
        try:
            #check if the group is exists
            respone_group = gl.groups.list(owned=True, search=group)[0]
            if not respone_group:
                return jsonify({"error": f"Group '{group}' not found."}), 404
            #check if the username is exists
            respone_user = gl.users.list(username='{}'.format(username))[0]
            if not respone_user:
                return jsonify({"error": f"User '{username}' not found."}), 404
            #check if the username is member in the group
            member = respone_group.members.get(respone_user.id)
            #change the role for the member
            member.access_level = access_level
            member.save()
            return jsonify({"message": f"Successfully updated role for {username} to {role} in group {group}."}), 200
        except:
            return jsonify('There is a problem, try again and check if the user is member of the group!'),400

    elif repo:
        try:
            #check if the repo is exists
            respone_repo = gl.projects.get(repo)
            if not respone_group:
                return jsonify({"error": f"Repository '{repo}' not found."}), 404
            #check if the username is exists
            respone_user = gl.users.list(username=username)[0]
            if not respone_user:
                return jsonify({"error": f"User '{username}' not found."}), 404
            #check if the user is part of the repo
            member = respone_repo.members_all.get(respone_user.id)
            #change the role for the user
            member.access_level = access_level
            return jsonify({"message": f"Successfully updated role for {username} to {role} in repo {repo}."}), 200
        except:
            return jsonify('There is a problem, try again and check if the user is member of the repo!'),400


@app.route('/mr_issues', methods=['POST'])
def get_mr_issues():
    data = request.get_json()
    mr_issues = data.get('kind')
    year = data.get('year')
    if not mr_issues or not year:
        return jsonify({"error": "Both 'kind' and 'year' are required"}), 400
    if mr_issues not in ["issues", "mr"]:
        return jsonify({"error": "'kind' must be either 'issues' or 'mr'"}), 400
    params = {
        'created_after': f'{year}-01-01T00:00:00Z',  # Start of the year
        'created_before': f'{year}-12-31T23:59:59Z',  # End of the year
        'per_page': 100}
    
    result = []
    try:
        if mr_issues == "issues":
            issues = gl.issues.list(**params)
            for issue in issues:
                issue_data = {
                    'title': issue.title,
                    'author': issue.author['name'],
                    'assignee': issue.assignee['name'] if issue.assignee else 'None',
                    'created_at': issue.created_at,
                    'state': issue.state,
                    'web_url': issue.web_url
                }
                result.append(issue_data)

        
        elif mr_issues == "mr":
            mrs = gl.mergerequests.list(**params)
            for mr in mrs:
                mr_data = {
                    'title': mr.title,
                    'author': mr.author['name'],
                    'assignee': mr.assignee['name'] if mr.assignee else 'None',
                    'created_at': mr.created_at,
                    'state': mr.state,
                    'web_url': mr.web_url
                }
                result.append(mr_data)

        return jsonify(result),200
    
    except Exception as e:
        return {"error": f"Error fetching {mr_issues}: {str(e)}"}, 500

    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
