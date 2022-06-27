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

def attack_user(db,attack_points,target,base_hp):
    target['hp'] -= attack_points
    if target['hp'] <= 0:
        target['hp'] = base_hp
        target['deaths'] += 1
        target['status'] = "offline"

    db.execute("UPDATE players SET hp=?, deaths=?, status=? WHERE rowid=?",(target['hp'],target['deaths'],target['status'],target['id']))
    return target

    # try:
    #     user_rows = db.execute("SELECT attack_points,kills FROM players WHERE rowid=?",[user_id]).fetchone() 
    #     attack_points = user_rows[0]
    #     kills = user_rows[1]
    # except TypeError:
    #     return None
    # try:
    #     target_rows = db.execute("SELECT hp,deaths FROM players WHERE rowid=?",[target_id]).fetchone()
    #     target_hp = target_rows[0]
    #     target_deaths = target_rows[1]
    # except TypeError:
    #     return None
    # if target_hp <= 0:
    #     return target_hp

    # new_hp = target_hp - attack_points
    # if new_hp <= 0:
    #     target_deaths += 1
    #     kills += 1
    # db.execute("UPDATE players SET hp=?, deaths=? WHERE rowid=?",(new_hp,target_deaths,target_id))
    # db.execute("UPDATE players SET kills=? WHERE rowid=?",(kills,user_id))
    # return attack_points, target_hp, new_hp,target_deaths