from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException
from database import cursor
from crud import get_players,get_player
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

async def attack_player(request):
    return JSONResponse([])

routes = [
    Route('/api/players',players),
    Route('/api/player',player),
    Route('/api/player/{name}',attack_player)
]

app = Starlette(debug=True, routes=routes)