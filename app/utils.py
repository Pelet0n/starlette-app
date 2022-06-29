import jwt

SECRET = "secret_code"

def player_to_dict(rowid, name, proffesion, hp, attack_points,status,deaths,kills):
    return {
        "id": rowid,
        "name": name,
        "proffesion": proffesion,
        "hp": hp,
        "attack_points": attack_points,
        "status":status,
        "deaths": deaths,
        "kills": kills
    }

def create_jwt_token(player):
    
    payload = {
        "id": player["id"],
        "name": player["name"],
        "proffesion": player["proffesion"]
    }

    token = jwt.encode(payload, SECRET, algorithm="HS256")

    return token

def check_jwt_token(token):
    payload = jwt.decode(token,SECRET,algorithms=["HS256", ])
    return payload