import requests
from flask import Flask, jsonify
from flask_cors import CORS
from urllib.parse import urljoin

app = Flask(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImFKbWhtUTlYeExsQmFLdHNuZnJIcCJ9.eyJ1c3IiOiI0ZmY0YmVhYy02ZTIxLTVhZjYtOGEwMC00ZDEzMjVkZTk4MzMiLCJpc3MiOiJodHRwczovL2F1cmEtYXBpLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJDZzJBNUtLOGxYdHdXVExqeUo0NGtFTjFJOURUZnByVkBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9jb25zb2xlLm5lbzRqLmlvIiwiaWF0IjoxNzEwNDAxMzgzLCJleHAiOjE3MTA0MDQ5ODMsImF6cCI6IkNnMkE1S0s4bFh0d1dUTGp5SjQ0a0VOMUk5RFRmcHJWIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIn0.FuPihnbSlWhaDKCi6Dr_X51eBeWJHADKeoXXJY1K7t8Rd81N9GpY4OmAUQOSAvx_F0PQ4AdH4PFHNPZJvIjrs9xXLh03wD6w7yOErxeAh_NM2pZUOWdW3X0RUQ5vftl6DLL40tN-RkCuZIzUIWCgMZa7reT2IL6ap-fkHUTeyNIQY_WPT909sJWjC6H31_R5B_aiwlzu1YIHuhQV2sojXIbJehlmSPd5okx0j9e0JviOQ3pFwmIB_ppfTr4OQK0OjwN1ktKnNrJx9Vx6LAcFxW301E_ywQrAFpN5s8tmO7sw77Ine1E3JYkb4aeefLpKSkEkclqP8CF6l8J8gfqMcg'
base_uri = 'https://api.neo4j.io/v1/'
tenant_id = '208c09d0-12ed-5992-9171-e33d49e370e5'


@app.route('/')
def hello():
    return 'Hello world!'


@app.route('/instances', methods=['GET'])
def get_instances():
    """
    Gets all instances.
    Returned value from Aura API:
    {'data': [{'cloud_provider': 'gcp',
   'id': '<instance-id>',
   'name': 'neo4j_vertexai',
   'tenant_id': '<tenant-id>'}, .....]}
    :return:
    """
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get(urljoin(base_uri, 'instances'), headers=headers)
    return r.json()


@app.route('/instances', methods=['POST'])
def create_instance():
    """
    Creates a new instance.
    Returned value from Aura API:
    {'data': {'cloud_provider': 'gcp',
          'connection_url': 'neo4j+s://<url>',
          'id': '<instance-id>',
          'name': 'arif-test',
          'password': '<password>',
          'region': 'us-central1',
          'tenant_id': '<tenant-id>',
          'type': '<type>',
          'username': 'neo4j'}}
    :return:
    """
    data = {
        'version': '5',
        'region': 'us-central1',
        'memory': '2GB',
        'name': 'arif-test',
        'type': 'professional-db',
        'tenant_id': tenant_id,
        'cloud_provider': 'gcp'
    }
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    r = requests.post(urljoin(base_uri, 'instances'), headers=headers, json=data)
    return r.json()


@app.route('/instances/<instance_id>', methods=['PATCH'])
def resize_instance(instance_id):
    """
    Resizes an existing instance.
    :param instance_id:
    :return:
    """
    instance_id = 'c2d29a65'
    data = {
        'memory': '16GB'
    }
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    r = requests.patch(urljoin(base_uri, f'instances/{instance_id}'), headers=headers, json=data)
    return r.json()


# * Delete specific instances
@app.route('/instances/<instance_id>', methods=['DELETE'])
def delete_instance(instance_id):
    return jsonify(instance_id)


# Take Snapshots On-demand
@app.route('/instances/<instance_id>/snapshots', methods=['POST'])
def get_snapshot(instance_id):
    return jsonify(instance_id)

# Delete Snapshots On-demand


if __name__ == '__main__':
    # TODO scrape some data from Neo4j Aura API specifications (instance type, supported types, etc.)
    app.run()
