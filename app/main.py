from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException
from database import cursor
from crud import get_players,get_player,create_player
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
        if not player:
            raise HTTPException(status_code=404,detail="Player with that name already exists")

    return JSONResponse(player)

routes = [
    Route('/api/players',players),
    Route('/api/player',player),
    Route('/api/createplayer',create_players,methods=['POST'])
]

app = Starlette(debug=True, routes=routes)