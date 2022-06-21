from sqlite3 import IntegrityError
from utils import player_to_dict

def get_players(db):
    query = "Select rowid, name, proffesion, hp, attack_points,status,deaths,kills FROM players"
    results = []

    for player in db.execute(query):
        player_data = player_to_dict(*player)
        results.append(player_data)
    return results

def get_player(db,name):
    query = "Select rowid, name, proffesion, hp, attack_points,status,deaths,kills FROM players WHERE name=?"
    player_data = db.execute(query,[name]).fetchone()
    if not player_data:
        return None
    return player_to_dict(*player_data)

def get_player_by_id(db,rowid):
    query = "Select rowid, name, proffesion, hp, attack_points,status,deaths,kills FROM players WHERE rowid=?"
    player_data = db.execute(query,[rowid]).fetchone()
    if not player_data:
        return None
    return player_to_dict(*player_data)

def create_player(db,name,proffesion,hp,attack_points):
    # check_exist = db.execute("SELECT * FROM players WHERE name=?",[name]).fetchone()
    # if check_exist:
    #     return None
    query = "INSERT INTO players(name,proffesion,hp,attack_points) VALUES(?,?,?,?)"
    try:
        player = db.execute(query,(name,proffesion,hp,attack_points))
    except IntegrityError:
        return None
    
    player_data = get_player_by_id(db,player.lastrowid)

    return player_data