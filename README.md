# Neo4j Aura Instance Management 

A Python script to interact with Aura API for:
* Creating a new instance
* Deleting a specific instance
* Resizing an existing instance
* Taking an on-demand snapshot
* Restoring an on-demand Snapshot
* Load dummy data

# How to

You need to authenticate first. Please read this [documentation](https://neo4j.com/docs/aura/platform/api/authentication/#_creating_credentials) 
in order to generate the credentials. Upon successful authentication, the following command will generate a file named 
`.token` to store the token that will be used for other commands:
```shell
python app.py authenticate \
--user <username> \
--password <password>

```

Create an instance (example). Refer to this [documentation](https://neo4j.com/docs/aura/platform/api/specification/#/instances/post-instances)
for the correct argument values:
```shell
python app.py create \
--name arif-test \
--version 5 \
--region us-central1 \
--memory 2GB \
--type professional-db \
--tenant_id <tenant_id> \
--cloud_provider gcp
```

Resize an instance (example: from 2GB to 4GB instance). Refer to this [documentation](https://neo4j.com/docs/aura/platform/api/specification/#/instances/patch-instance-id)
for the correct argument values:
```shell
python app.py resize \
--instance_id 57f58e24 \
--new_memory 4GB 
```

Create an on-demand snapshot (example). Refer to this [documentation](https://neo4j.com/docs/aura/platform/api/specification/#/instances/post-snapshots)
for the correct argument values:
```shell
python app.py create_snapshot \
--instance_id 57f58e24
```

Restore an on-demand snapshot (example). Refer to this [documentation](https://neo4j.com/docs/aura/platform/api/specification/#/instances/post-restore-snapshot)
for the correct argument values:
```shell
python app.py restore_snapshot \
--instance_id 57f58e24 \
--snapshot_id 987a3941-a8cd-4778-993a-7fd5c7d48b2f
```

Delete an instance (example). Refer to this [documentation](https://neo4j.com/docs/aura/platform/api/specification/#/instances/delete-instance-id):
```shell
python app.py delete \
--instance_id 57f58e24
```

Load dummy data (example):
```shell
python app.py load_dummy \
--uri neo4j+s://blabla.databases.neo4j.io \
--user neo4j \
--password <password>
```