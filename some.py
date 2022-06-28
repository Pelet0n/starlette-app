import argparse
import requests


parser = argparse.ArgumentParser()

parser.add_argument("command",nargs="?")
parser.add_argument("--player_id",type=int,required=True)
parser.add_argument("--target_id",type=int,required=True)

args = parser.parse_args()

command = args.command
player_id = args.player_id
target_id = args.target_id

response = requests.post(f"http://127.0.0.1:8000/api/player/{player_id}/attack",json={
    "target_user": target_id
})
status_code = response.status_code
breakpoint()

if status_code == 404:
    print("zalogowano")
elif status_code == 200:
    data = response.json()
    print(data)