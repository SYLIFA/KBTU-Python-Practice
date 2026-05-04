import json
import os

def load_settings():
    default = {"sound": True, "car_color": "blue", "difficulty": "Medium"}
    try:
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                data = json.load(f)
                # Проверка, что все ключи на месте
                for key in default:
                    if key not in data: data[key] = default[key]
                return data
    except:
        pass
    return default

def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)

def load_leaderboard():
    try:
        if os.path.exists("leaderboard.json"):
            with open("leaderboard.json", "r") as f:
                return json.load(f)
    except:
        pass
    return []

def save_score(name, score, distance):
    board = load_leaderboard()
    board.append({"name": name, "score": score, "distance": distance})
    board = sorted(board, key=lambda x: x['score'], reverse=True)[:10]
    with open("leaderboard.json", "w") as f:
        json.dump(board, f, indent=4)