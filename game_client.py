import requests

class Game_client():
    def __init__(self,id):
        self.id = id
    def login(self):
        response = requests.get(f'http://127.0.0.1:8000/api/player/{self.id}/online')
        try:
            return response.json()
        except requests.JSONDecodeError:
            return response.text
        
    def logout(self):
        response = requests.get(f'http://127.0.0.1:8000/api/player/{self.id}/offline').json()
        return response
    def attack(self,token, target_id):
        response = requests.post(f'http://127.0.0.1:8000/api/player/{self.id}/attack', headers={"Authorization": token}, json={"target_user": target_id})
        try:
            return response.json()
        except requests.JSONDecodeError:
            return response.text