# Immich Photo/Video Library Management

This repository contains initial [Immich](https://immich.app) photo and video
library management configuration and administration scripts. Included here are
the [backup-immich-pg](backup-immich-pg) script to backup the `Immich`
database and perform a `Borg` backup of the `Immich` library and the
[create-external-albums](create-external-albums) script to create albums from
an `Immich` external library.

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
* `hwaccel-examples/hwaccel.ml.yml`: Hardware acceleration example
* `hwaccel-examples/hwaccel.transcoding.yml`: Hardware transcoding acceleration example
* `immich_auto_album.py`: Python script used by `create-external-albums`
* `start`: Convenience script to start the Immich server
* `stop`: Convenience script to stop the Immich server
* `upgrade`: Convenience script to upgrade the Immich server

## Setup

### Environment file

Copy the `env-example` file to `.env` and edit to set your Immich database password:

```
DB_PASSWORD=<Your-Immich-Database-Password>
```

### Cloudflare tunnel

To run a Cloudflare tunnel, edit `cf_tunnel` and add the Cloudflare tunnel token:

```
    run --token <your-cloudflare-tunnel-token>
```
