import requests
import time

# CONFIGURAÇÕES
TOKEN = "SEU_GITHUB_TOKEN_AQUI"  # Gere em: https://github.com/settings/tokens
USERNAME = "walbarellos"
HEADERS = {"Authorization": f"token {TOKEN}"}

def get_list(endpoint):
    users = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{USERNAME}/{endpoint}?per_page=100&page={page}"
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            print(f"⚠️ Erro {r.status_code} ao buscar {endpoint}")
            break
        data = r.json()
        if not data:
            break
        users.extend([u["login"] for u in data])
        page += 1
    return set(users)

def main():
    followers = get_list("followers")
    following = get_list("following")

    nao_reciprocos = following - followers
    print(f"👤 Você segue {len(following)} pessoas.")
    print(f"🚫 {len(nao_reciprocos)} não te seguem de volta:\n")

    for u in sorted(nao_reciprocos):
        print("-", u)

    confirmar = input("\n❓ Deseja dar unfollow em todos esses usuários? (s/n) ")
    if confirmar.lower() == "s":
        for u in nao_reciprocos:
            url = f"https://api.github.com/user/following/{u}"
            r = requests.delete(url, headers=HEADERS)
            if r.status_code == 204:
                print(f"❌ Deixou de seguir {u}")
            else:
                print(f"⚠️ Erro ao deixar de seguir {u}: {r.status_code}")
            time.sleep(1)  # Evita rate-limit

if __name__ == "__main__":
    main()
