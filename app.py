import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from services.cache import TTLCache
from services.github_client import (
    USERNAME,
    list_followers, list_following, enrich_users, delete_follow
)
from services.audit import write_unfollow_log

load_dotenv()

DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"
CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS", "600"))

app = Flask(__name__)
cache = TTLCache(ttl_seconds=CACHE_TTL)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data")
def api_data():
    """
    Retorna:
      - following_only: usuários que você segue e NÃO te seguem
      - mutuals: seguem-se mutuamente
      - not_followed_back_by_you: te seguem e você NÃO segue (opcional p/ ação)
    Todos enriquecidos com metadados.
    """
    key = "dataset_v1"
    cached = cache.get(key)
    if cached:
        return jsonify(cached)

    followers = list_followers(USERNAME)
    following = list_following(USERNAME)

    following_only = sorted(list(following - followers))
    mutuals = sorted(list(following & followers))
    not_followed_back_by_you = sorted(list(followers - following))

    # Enriquecer (apenas onde importa mais: following_only e mutuals; o terceiro é útil p/ decisões)
    enriched_following_only = enrich_users(following_only)
    enriched_mutuals = enrich_users(mutuals[:150])  # otimização: subsample, pode ajustar via UI
    enriched_nfby = enrich_users(not_followed_back_by_you[:150])

    payload = {
        "username": USERNAME,
        "dry_run": DRY_RUN,
        "counts": {
            "following": len(following),
            "followers": len(followers),
            "following_only": len(following_only),
            "mutuals": len(mutuals),
            "not_followed_back_by_you": len(not_followed_back_by_you),
        },
        "following_only": enriched_following_only,
        "mutuals": enriched_mutuals,
        "not_followed_back_by_you": enriched_nfby,
    }
    cache.set(key, payload)
    return jsonify(payload)

@app.route("/api/unfollow", methods=["POST"])
def api_unfollow():
    """
    Executa unfollow nos logins enviados.
    Respeita DRY_RUN; sempre registra log de auditoria.
    """
    data = request.get_json(force=True) or {}
    users = data.get("logins", [])
    results = []

    for login in users:
        if DRY_RUN:
            results.append({"login": login, "status": "dry-run"})
        else:
            ok, code = delete_follow(login)
            results.append({"login": login, "status": "ok" if ok else f"error:{code}"})

    log_path = write_unfollow_log(USERNAME, results, DRY_RUN)
    return jsonify({"ok": True, "dry_run": DRY_RUN, "log_path": log_path, "results": results})

if __name__ == "__main__":
    app.run(debug=True)
