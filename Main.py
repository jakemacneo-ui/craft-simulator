import tkinter as tk
import random
import json
import os

# =====================
# DATA
# =====================

save_file = "save.json"

inventory = {
    "wood": 0,
    "stone": 0,
    "iron": 0,
    "diamond": 0,
    "plank": 0,
    "stick": 0,
    "sword": 0
}

player = {
    "xp": 0,
    "level": 1,
    "tool_level": 1
}

codes = {
    "CRAFT2026": {"wood": 10, "stone": 5},
    "FREEIRON": {"iron": 5},
    "OPSTART": {"diamond": 3}
}

used_codes = set()

# =====================
# SAVE / LOAD
# =====================

def save_game():
    data = {
        "inventory": inventory,
        "player": player,
        "used_codes": list(used_codes)
    }
    with open(save_file, "w") as f:
        json.dump(data, f)

def load_game():
    global inventory, player, used_codes
    if os.path.exists(save_file):
        with open(save_file, "r") as f:
            data = json.load(f)
            inventory.update(data["inventory"])
            player.update(data["player"])
            used_codes = set(data["used_codes"])

# =====================
# GAME LOGIC
# =====================

def update_display():
    inv_text = "\n".join([f"{k}: {v}" for k, v in inventory.items()])
    stats_text = f"Level: {player['level']} | XP: {player['xp']} | Tool: {player['tool_level']}"
    inventory_label.config(text=inv_text)
    stats_label.config(text=stats_text)

def add_xp(amount):
    player["xp"] += amount
    if player["xp"] >= player["level"] * 10:
        player["xp"] = 0
        player["level"] += 1
        player["tool_level"] += 1

def gather():
    wood = random.randint(1, 3) * player["tool_level"]
    stone = random.randint(0, 2) * player["tool_level"]
    iron = random.randint(0, 1) * player["tool_level"]

    if random.random() < 0.1:
        inventory["diamond"] += 1

    inventory["wood"] += wood
    inventory["stone"] += stone
    inventory["iron"] += iron

    add_xp(5)
    update_display()

def craft(item):
    recipes = {
        "plank": {"wood": 2},
        "stick": {"plank": 2},
        "sword": {"stick": 1, "iron": 2}
    }

    if item not in recipes:
        return

    for req, amt in recipes[item].items():
        if inventory[req] < amt:
            return

    for req, amt in recipes[item].items():
        inventory[req] -= amt

    inventory[item] += 1
    add_xp(3)
    update_display()

def redeem():
    code = code_entry.get().upper()
    if code in used_codes:
        return

    if code in codes:
        for item, amt in codes[code].items():
            inventory[item] += amt
        used_codes.add(code)

    update_display()

# =====================
# UI
# =====================

root = tk.Tk()
root.title("Craft Simulator")
root.geometry("400x500")

title = tk.Label(root, text="🛠️ Craft Simulator", font=("Arial", 16))
title.pack()

inventory_label = tk.Label(root, text="", justify="left")
inventory_label.pack()

stats_label = tk.Label(root, text="")
stats_label.pack()

tk.Button(root, text="Gather", command=gather).pack(pady=5)

tk.Button(root, text="Craft Plank", command=lambda: craft("plank")).pack()
tk.Button(root, text="Craft Stick", command=lambda: craft("stick")).pack()
tk.Button(root, text="Craft Sword", command=lambda: craft("sword")).pack()

code_entry = tk.Entry(root)
code_entry.pack()

tk.Button(root, text="Redeem Code", command=redeem).pack(pady=5)

tk.Button(root, text="Save Game", command=save_game).pack()

# Load + start
load_game()
update_display()

root.mainloop()
