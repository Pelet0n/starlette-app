from __future__ import barry_as_FLUFL
from sqlite3 import IntegrityError
from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException
from database import cursor
from crud import get_players,get_player,create_player,get_player_by_id
import json

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
    'mage': {"hp":50,"attack_points":15},
    'knight': {"hp":70,"attack_points":30}
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
    return JSONResponse(player)

async def status_offline(request):
    id = request.path_params['user_id']
    with cursor() as cur:
        cur.execute('UPDATE players SET status="offline" WHERE rowid=?',[id])
        player = get_player_by_id(cur,id)
        if not player:
            raise HTTPException(status_code=404,detail="Player not found")
        
        
    return JSONResponse(player)

routes = [
    Route('/api/players',players),
    Route('/api/player',player),
    Route('/api/createplayer',create_players,methods=['POST']),
    Route('/api/player/{user_id}/online',status_online),
    Route('/api/player/{user_id}/offline',status_offline)
]

app = Starlette(debug=True, routes=routes)