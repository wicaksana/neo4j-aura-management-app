import argparse
import requests
import os
import sys
from urllib.parse import urljoin

base_uri = 'https://api.neo4j.io/'
token_filename = '.token'


def authenticate(user, password):
    """
    Authenticate against Neo4j Aura API.
    Reference: https://neo4j.com/docs/aura/platform/api/authentication/#_creating_credentials
    :param user: client ID
    :param password: client secret
    """
    uri = urljoin(base_uri, 'oauth/token')
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'client_credentials'}
    auth = (user, password)

    r = requests.post(uri, headers=headers, data=data, auth=auth)
    if r.status_code == 200:
        with open(token_filename, 'w') as tf:
            tf.write(r.json()['access_token'])
        print('Successfully authenticated.')
    else:
        print(f'[!] Cannot authenticate: Error code {r.status_code} - {r.json()}')


def check_token_file_existence():
    return os.path.exists(token_filename) and os.path.getsize(token_filename) > 0


def get_token():
    """
    Read token from .token file.
    :return: token
    """
    with open(token_filename) as tf:
        token = tf.readline()
    return token


def create_instance(name, version, region, memory, instance_type, tenant_id, cloud_provider):
    """
    Creates an Aura instance.
    Reference: https://neo4j.com/docs/aura/platform/api/specification/#/instances/post-instances
    :param name: instance name
    :param version: Neo4j version
    :param region: Cloud region
    :param memory: Memory size
    :param instance_type: Instance type
    :param tenant_id: Aura tenant ID
    :param cloud_provider: Cloud provider of choice
    """
    if check_token_file_existence():
        token = get_token()
        data = {
            'version': version,
            'region': region,
            'memory': memory,
            'name': name,
            'type': instance_type,
            'tenant_id': tenant_id,
            'cloud_provider': cloud_provider
        }
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        uri = urljoin(base_uri, 'v1/instances')
        print(f'API endpoint: {uri}')
        print('Creating the instance...')
        r = requests.post(uri, headers=headers, json=data)
        if r.status_code == 202:
            print(f'Instance is being created: {r.json()}')
        else:
            print(f'[!] Something is wrong: Error code: {r.status_code} - {r.json()}')
    else:
        print('[!] Aura token is not found. Please authenticate first.')


def resize_instance(instance_id, new_memory):
    """
    Resize an instance.
    Reference: https://neo4j.com/docs/aura/platform/api/specification/#/instances/patch-instance-id
    :param instance_id:
    :param new_memory:
    """
    uri = urljoin(base_uri, f'v1/instances/{instance_id}')
    if check_token_file_existence():
        token = get_token()
        data = {'memory': new_memory}
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        r = requests.patch(uri, headers=headers, json=data)
        if r.status_code == 202:
            print(f'Instance is being resized: {r.json()}')
        else:
            print(f'[!] Something is wrong: Error code: {r.status_code} - {r.json()}')
    else:
        print('[!] Aura token is not found. Please authenticate first.')


def create_snapshot(instance_id):
    """
    Create an on-demand snapshot from an Aura instance.
    Reference: https://neo4j.com/docs/aura/platform/api/specification/#/instances/post-snapshots
    :param instance_id: Instance ID
    """
    uri = urljoin(base_uri, f'v1/instances/{instance_id}/snapshots')
    if check_token_file_existence():
        token = get_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        r = requests.post(uri, headers=headers)
        if r.status_code == 202:
            print(f'Snapshot is being taken: {r.json()}')
        else:
            print(f'[!] Something is wrong: Error code: {r.status_code} - {r.json()}')
    else:
        print('[!] Aura token is not found. Please authenticate first.')


def restore_snapshot(instance_id, snapshot_id):
    """
    Restore a snapshot of an instance.
    Reference: https://neo4j.com/docs/aura/platform/api/specification/#/instances/post-restore-snapshot
    :param instance_id: instance id
    :param snapshot_id: snapshot id
    """
    uri = urljoin(base_uri, f'v1/instances/{instance_id}/snapshots/{snapshot_id}/restore')
    if check_token_file_existence():
        token = get_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        r = requests.post(uri, headers=headers)
        if r.status_code == 202:
            print(f'Snapshot is being restored: {r.json()}')
        else:
            print(f'[!] Something is wrong: Error code: {r.status_code} - {r.json()}')
    else:
        print('[!] Aura token is not found. Please authenticate first.')


def delete_instance(instance_id):
    """
    Delete an instance.
    Reference: https://neo4j.com/docs/aura/platform/api/specification/#/instances/delete-instance-id
    :param instance_id: instance ID
    """
    uri = urljoin(base_uri, f'v1/instances/{instance_id}')
    if check_token_file_existence():
        token = get_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        r = requests.delete(uri, headers=headers)
        if r.status_code == 202:
            print(f'Instance is being deleted: {r.json()}')
        else:
            print(f'[!] Something is wrong: Error code: {r.status_code} - {r.json()}')
    else:
        print('[!] Aura token is not found. Please authenticate first.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command')

    # First step: authenticate
    authentication = subparser.add_parser(name='authenticate', help='Authenticate to Neo4j Aura API')
    authentication.add_argument('--user', help='Username', required=True, type=str)
    authentication.add_argument('--password', help='Password', required=True, type=str)

    # Create an instance
    create = subparser.add_parser(name='create', help='Create an Aura instance.')
    create.add_argument('--name', help='Instance name', required=True)
    create.add_argument('--version', help='Neo4j version', required=True)
    create.add_argument('--region', help='Cloud region', required=True)
    create.add_argument('--memory', help='Memory size', required=True)
    create.add_argument('--type', help='Instance type', required=True)
    create.add_argument('--tenant_id', help='Tenant ID', required=True)
    create.add_argument('--cloud_provider', help='Cloud provider', required=True)

    # Resize an instance
    resize = subparser.add_parser(name='resize', help='Resize an Aura instance.')
    resize.add_argument('--instance_id', help='Instance ID', required=True)
    resize.add_argument('--new_memory', help='New memory size', required=True)

    # create snapshot
    create_s = subparser.add_parser(name='create_snapshot', help='Create an on-demand snapshot from an Aura instance')
    create_s.add_argument('--instance_id', help='Instance ID', required=True)

    # restore snapshot
    restore_s = subparser.add_parser(name='restore_snapshot', help='Restore an on-demand snapshot of an Aura instance')
    restore_s.add_argument('--instance_id', help='Instance ID', required=True)
    restore_s.add_argument('--snapshot_id', help='Snapshot ID', required=True)

    # Delete an instance
    delete = subparser.add_parser(name='delete', help='delete instance')
    delete.add_argument('--instance_id')

    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    if args.command == 'authenticate':
        authenticate(args.user.strip(), args.password.strip())
    elif args.command == 'create':
        create_instance(args.name, args.version, args.region, args.memory, args.type, args.tenant_id, args.cloud_provider)
    elif args.command == 'resize':
        resize_instance(args.instance_id, args.new_memory)
    elif args.command == 'create_snapshot':
        create_snapshot(args.instance_id)
    elif args.command == 'restore_snapshot':
        restore_snapshot(args.instance_id, args.snapshot_id)
    elif args.command == 'delete':
        delete_instance(args.instance_id)


