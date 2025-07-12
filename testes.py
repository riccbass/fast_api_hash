import requests

token = input("Digite o token: ")

headers = {
    "Authorization": f"Bearer {token}"
}

requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(requisicao)
print(requisicao.json())