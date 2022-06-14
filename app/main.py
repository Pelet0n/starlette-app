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

PROFESSION = {
    'mage': {"hp":50,"attack":15},
    'knight': {"hp":50,"attack":15}
}

async def create_player(request):
    data = await request.json()
    profession = data.get('profession')
    profession_data = PROFESSION.get(profession)
    breakpoint()
    data['hp'] = profession_data['hp']
    data['attack'] = profession_data['attack']


    with cursor() as cur:
        player = create_player(cur,data)
    
    return JSONResponse(player)

routes = [
    Route('/api/players',players),
    Route('/api/player',player),
    Route('/api/createplayer',create_player,methods=['POST'])
]

app = Starlette(debug=True, routes=routes)