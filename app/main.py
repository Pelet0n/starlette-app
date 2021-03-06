from sqlite3 import IntegrityError
from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException
from database import cursor
from crud import get_players,get_player,create_player,get_player_by_id,attack_user
from utils import create_jwt_token,check_jwt_token
import json
from jwt import exceptions

async def players(request):
    with cursor() as cur:
        results = get_players(cur)
    return JSONResponse(results)

async def player(request):
    with cursor() as cur:
        try:
            name = request.query_params['name']
        except KeyError:
            return JSONResponse([])
        results = get_player(cur,name)
        if not results:
            raise HTTPException(status_code=404,detail="Player not found")
    return JSONResponse(results)

PROFFESION = {
    'MAGE': {"hp":50,"attack_points":15},
    'KNIGHT': {"hp":70,"attack_points":30},
    'PALADIN': {"hp": 60, "attack_points": 40}
}

async def create_players(request):
    with cursor() as cur:
        data = await request.json()
        proffesion = data.get('proffesion')
        proffesion_data = PROFFESION.get(proffesion)
        data.update(proffesion_data)

        player = create_player(cur,**data)
        if player==None:
            raise HTTPException(status_code=404,detail="Player with that name already exists")

    return JSONResponse(player)

async def status_online(request):
    id = request.path_params['user_id']
    with cursor() as cur:   
        status = cur.execute('SELECT status FROM players WHERE rowid=?',[id]).fetchone()
        if not status:
            raise HTTPException(status_code=404,detail="Player not found")
        elif status[0] == 'online':
            raise HTTPException(status_code=404,detail="Player is online")
        cur.execute('UPDATE players SET status="online" WHERE rowid=?',[id])
        player = get_player_by_id(cur,id)
    token = create_jwt_token(player)

    return JSONResponse({'token':token, 'player':player})

async def status_offline(request):
    id = request.path_params['user_id']
    with cursor() as cur:
        cur.execute('UPDATE players SET status="offline" WHERE rowid=?',[id])
        player = get_player_by_id(cur,id)
        if not player:
            raise HTTPException(status_code=404,detail="Player not found")
        
        
    return JSONResponse(player)

async def attack_player(request):
    data = await request.json()
    target_id= data['target_user']
    if 'Authorization' not in request.headers:
        raise HTTPException(status_code=401,detail="Unauthorized")
    token = request.headers['Authorization']
    if not token:
        return JSONResponse("Missing token")
    
    id = request.path_params['user_id']
    with cursor() as cur:
        player = get_player_by_id(cur,id)
        target  = get_player_by_id(cur,target_id)

        if not player:
            raise HTTPException(status_code=404,detail="Player does not exist")
        if not target:
            raise HTTPException(status_code=404,detail="Target does not exist")

        if player['status'] == "offline":
            return JSONResponse("You are offline")

        player_payload = {
            "id": player['id'],
            "name": player['name'],
            "proffesion": player['proffesion']
        }

        
        try:
            payload = check_jwt_token(token)
        except exceptions.InvalidTokenError:
            raise HTTPException(status_code=404,detail="Invalid token")

        if payload != player_payload:
            raise HTTPException(status_code=401,detail="Player not authorized")
        if not target['status'] == 'online':
            raise HTTPException(status_code=404,detail="Target is offline")
        attack_points = player['attack_points']
        base_hp = PROFFESION.get(target['proffesion'].upper())['hp']
        attack_data = attack_user(cur,attack_points,target,base_hp)
        target.update(attack_data)
    return JSONResponse(target)

routes = [
    Route('/api/players',players),
    Route('/api/player',player),
    Route('/api/createplayer',create_players,methods=['POST']),
    Route('/api/player/{user_id}/online',status_online),
    Route('/api/player/{user_id}/offline',status_offline),
    Route('/api/player/{user_id}/attack',attack_player,methods=['POST'])
]

app = Starlette(debug=True, routes=routes)