from utils import player_to_dict

def get_players(db):
    query = "Select rowid, name, proffesion, hp, attack_points,status,deaths,kills FROM players"
    results = []

    for player in db.execute(query):
        breakpoint()
        player_data = player_to_dict(*player)
        results.append(player_data)
    return results

def get_player(db,name):
    query = "Select rowid, name, proffesion, hp, attack_points,status,deaths,kills FROM players WHERE name=?"
    player_data = db.execute(query,[name]).fetchone()
    if not player_data:
        return None
    return player_to_dict(*player_data)

def create_player(db,name,proffesion,hp,attack_points):
    check_exist = db.execute("SELECT * FROM players WHERE name=?",[name]).fetchone()
    if check_exist:
        return None
    query = "INSERT INTO players(name,proffesion,hp,attack_points) VALUES(?,?,?,?)"
    db.execute(query,(name,proffesion,hp,attack_points))
    player_data = db.execute("SELECT rowid, name, proffesion,hp,attack_points,status,deaths,kills FROM players WHERE name=?",[name]).fetchone()

    return player_to_dict(*player_data)