import argparse
from game_client import Game_client

parser = argparse.ArgumentParser()

parser.add_argument("command",nargs="?")
parser.add_argument("--player_id",type=int,required=True)
parser.add_argument("--target_id",type=int)
parser.add_argument("--token",type=str)

args = parser.parse_args()

command = args.command
player_id = args.player_id
target_id = args.target_id
token = args.token

player = Game_client(player_id)

if command == "login":
    data = player.login()
    print(data)
elif command == "logout":
    data = player.logout()
    print(data)
elif command == "attack":
    data = player.attack(token,target_id)
    print(data)