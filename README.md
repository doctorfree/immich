# Immich Photo/Video Library Management

This repository contains initial [Immich](https://immich.app) photo and video
library management configuration and administration scripts.

Included here are the [backup-immich-pg](backup-immich-pg) script to backup the
`Immich` database and perform a `Borg` backup of the `Immich` library and the
[create-external-albums](create-external-albums) script to create albums from
an `Immich` external library which acts as a front-end for the `Python` script
[immich_auto_album.py](immich_auto_album.py).

See the [Immich documentation](https://immich.app/docs/overview/introduction)
for complete instructions on setup, install, administration, and use of
[Immich](https://immich.app).

## Contents

* `backup-immich-pg`: Backup Immich database and perform Borg backup of Immich library
* `cf_tunnel`: Run a Cloudflare tunnel to access Immich from outside local network
* `create-external-albums`: Create albums from an Immich external library
* `docker-compose.yml`: Docker compose file for this Immich instance
* `env-example`: Example `.env` for this Immich instance
* `hwaccel.yml`: Hardware acceleration example for Intel architecture machines
* `hwaccel-examples/hwaccel.ml.yml`: Hardware machine learning acceleration example
* `hwaccel-examples/hwaccel.transcoding.yml`: Hardware transcoding acceleration example
* `immich_auto_album.py`: Python script used by `create-external-albums`
* `start`: Convenience script to start the Immich server
* `stop`: Convenience script to stop the Immich server
* `upgrade`: Convenience script to upgrade the Immich server
* `update/get-docker-compose`: Convenience script to download the latest compose and env files

## Setup

### Environment file

Copy the `env-example` file to `.env` and edit to set your Immich database password:

```
DB_PASSWORD=<Your-Immich-Database-Password>
```

The example `env-example` has an external library path configured:

```
EXTERNAL_PATH=/u/Videos
```

This is used in conjunction with settings in `docker-compose.yml`:

```
    - ${EXTERNAL_PATH}:/usr/src/app/external
```

Either remove these external library settings or create an external library
at `/u/Videos` on the same system as `Immich`.

### Cloudflare tunnel

To run a Cloudflare tunnel, edit `cf_tunnel` and add the Cloudflare tunnel token:

```
    run --token <your-cloudflare-tunnel-token>
```
