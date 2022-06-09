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