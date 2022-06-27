import requests

def test_player(player):
    response = requests.get('http://127.0.0.1:8000/api/player?name=Hubert').json()
    
    assert player['id'] == response['id']
    assert player['name'] == response['name']
    assert player['proffesion'] == response['proffesion']
    assert player['status'] == response['status']
    assert player['kills'] == response['kills']
    assert player['deaths'] == response['deaths']
    assert player['attack_points'] == response['attack_points']