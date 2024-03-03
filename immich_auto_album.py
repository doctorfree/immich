import requests
import os
import argparse
from collections import defaultdict


# I have photos in subfolders like : 
# /mnt/media/Photos/2023-08 Holidays
# /mnt/media/Photos/2023-06 Birthday
# /mnt/media/Photos/2022-12 Christmas
# This script will create 3 albums
# 2023-08 Holidays, 2023-06 Birthday, 2022-12 Christmas
# And populate them with the photos inside
# The script can be run multiple times to update, new albums will be created,
# or new photos added in existing subfolder will be added to corresponding album 

parser = argparse.ArgumentParser(description="Create Immich Albums from an external library path based on the top level folders", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("root_path", help="The external libarary's root path in Immich")
parser.add_argument("api_url", help="The root API URL of immich, e.g. https://immich.mydomain.com/api/")
parser.add_argument("api_key", help="The Immich API Key to use")
parser.add_argument("-u", "--unattended", action="store_true", help="Do not ask for user confirmation after identifying albums. Set this flag to run script as a cronjob.")
parser.add_argument("-c", "--chunk-size", default=2000, type=int, help="Maximum number of assets to add to an album with a single API call")
parser.add_argument("-C", "--fetch-chunk-size", default=5000, type=int, help="Maximum number of assets to fetch with a single API call")
args = vars(parser.parse_args())

root_path = args["root_path"]
root_url = args["api_url"]
api_key = args["api_key"]
number_of_images_per_request = args["chunk_size"]
number_of_assets_to_fetch_per_request = args["fetch_chunk_size"]
unattended = args["unattended"]

# Yield successive n-sized 
# chunks from l. 
def divide_chunks(l, n): 
      
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 
  

requests_kwargs = {
    'headers' : {
        'x-api-key': api_key,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
}
if root_path[-1] != '/':
    root_path = root_path + '/'
if root_url[-1] != '/':
    root_url = root_url + '/'


print("  1. Requesting all assets")
assets = []
# Initial API call, let's fetch our first chunk
r = requests.get(root_url+'asset?take='+str(number_of_assets_to_fetch_per_request), **requests_kwargs)
assert r.status_code == 200
assets = assets + r.json()

# If we got a full chunk size back, let's perfrom subsequent calls until we get less than a full chunk size
skip = 0
while len(r.json()) == number_of_assets_to_fetch_per_request:
    skip += number_of_assets_to_fetch_per_request
    r = requests.get(root_url+'asset?take='+str(number_of_assets_to_fetch_per_request)+'&skip='+str(skip), **requests_kwargs)
    if skip == number_of_assets_to_fetch_per_request and assets == r.json():
        print("Non-chunked Immich API detected, stopping fetching assets since we already got all in our first call")
        break
    assert r.status_code == 200
    assets = assets + r.json()
print(len(assets), "photos found")

print("  2. Sorting assets to corresponding albums using folder name")
album_to_assets = defaultdict(list)
for asset in assets:
    asset_path = asset['originalPath']
    if root_path not in asset_path:
        continue
    album_name = asset_path.replace(root_path, '').split('/')[0]
    # Check that the extracted album name is not actually a file name in root_path
    if not asset_path.endswith(album_name):
        album_to_assets[album_name].append(asset['id'])

album_to_assets = {k:v for k, v in sorted(album_to_assets.items(), key=(lambda item: item[0]))}

print(len(album_to_assets), "albums identified")
print(list(album_to_assets.keys()))
if not unattended:
    print("Press Enter to continue, Ctrl+C to abort")
    input()

album_to_id = {}

print("  3. Listing existing albums on immich")
r = requests.get(root_url+'album', **requests_kwargs)
assert r.status_code == 200
albums = r.json()
album_to_id = {album['albumName']:album['id'] for album in albums }
print(len(albums), "existing albums identified")

print("  4. Creating albums if needed")
cpt = 0
for album in album_to_assets:
    if album in album_to_id:
        continue
    data = {
        'albumName': album,
        'description': album
    }
    r = requests.post(root_url+'album', json=data, **requests_kwargs)
    assert r.status_code in [200, 201]
    album_to_id[album] = r.json()['id']
    print(album, 'album added!')
    cpt += 1
print(cpt, "albums created")

print("  5. Adding assets to albums")
# Note: immich manage duplicates without problem, 
# so we can each time ad all assets to same album, no photo will be duplicated 
for album, assets in album_to_assets.items():
    id = album_to_id[album]
    
    assets_chunked = list(divide_chunks(assets, number_of_images_per_request))
    for assets_chunk in assets_chunked:
        data = {'ids':assets_chunk}
        r = requests.put(root_url+f'album/{id}/assets', json=data, **requests_kwargs)
        if r.status_code not in [200, 201]:
            print(album)
            print(r.json())
            print(data)
            continue
        assert r.status_code in [200, 201]
        response = r.json()

        cpt = 0
        for res in response:
            if not res['success']:
                if  res['error'] != 'duplicate':
                    print("Warning, error in adding an asset to an album:", res['error'])
            else:
                cpt += 1
        if cpt > 0:
            print(f"{str(cpt).zfill(3)} new assets added to {album}")

print("Done!")
