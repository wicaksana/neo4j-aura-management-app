# Neo4j Aura Instance Management Demo

A Python app to interact with Aura API:
* Take Snapshots On-demand
* Restore an on-demand Snapshot
* Roll out new instances
* Delete specific instances
* Upsize existing Instances
* Downsize existing instances

## Dev

```shell
flask run
```

```shell
npm run dev
```

You need to authenticate first:
```shell
python app.py authenticate \
--user <username> \
--password <password>

```

Create an instance:
```shell
python app.py create \
--name arif-test \
--version 5 \
--region us-central1 \
--memory 2GB \
--type professional-db \
--tenant_id 208c09d0-12ed-5992-9171-e33d49e370e5 \
--cloud_provider gcp
```

Resize an instance:
```shell
python app.py resize \
--instance_id 57f58e24 \
--new_memory 4GB 
```

Create an on-demand snapshot:
```shell
python app.py create_snapshot \
--instance_id 57f58e24
```

Restore an on-demand snapshot:
```shell
python app.py restore_snapshot \
--instance_id 57f58e24 \
--snapshot_id 987a3941-a8cd-4778-993a-7fd5c7d48b2f
```

Delete an instance:
```shell
python app.py delete \
--instance_id 57f58e24
```