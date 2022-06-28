import requests
import pytest
from app.database import cursor
from app.utils import player_to_dict


@pytest.fixture
def player():
    with cursor() as cur:
        data = cur.execute('SELECT rowid, name, proffesion, hp, attack_points,status,deaths,kills FROM players WHERE name="Hubert"').fetchone()
        return player_to_dict(*data)
    