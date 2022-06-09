from app.database import cursor

with cursor() as cur:
    cur.execute("INSERT INTO players(name, proffesion, hp, attack_points) VALUES ('Master','Mage', 50, 15)")
    cur.execute("INSERT INTO players(name, proffesion, hp, attack_points) VALUES ('Blaster','Paladin', 40, 25)")
    cur.execute("INSERT INTO players(name, proffesion, hp, attack_points) VALUES ('Caster','Soldier', 30, 30)")
    cur.execute("INSERT INTO players(name, proffesion, hp, attack_points) VALUES ('Daster','Archer', 20, 40)")