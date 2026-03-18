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

recipes = {
    "plank": {"wood": 2},
    "stick": {"plank": 2},
    "sword": {"stick": 1, "iron": 2}
}

codes = {
    "CRAFT2026": {"wood": 10, "stone": 5},
    "FREEIRON": {"iron": 5},
    "OPSTART": {"diamond": 3}
}

used_codes = set()

achievements = {
    "First Gather": False,
    "Crafter": False,
    "First Sword": False,
    "Diamond Finder": False
}

# =====================
# SAVE / LOAD
# =====================

def save_game():
    data = {
        "inventory": inventory,
        "player": player,
        "used_codes": list(used_codes),
        "achievements": achievements
    }
    with open(save_file, "w") as f:
        json.dump(data, f)
    print("💾 Game saved!")

def load_game():
    global inventory, player, used_codes, achievements

    if not os.path.exists(save_file):
        return

    with open(save_file, "r") as f:
        data = json.load(f)

    inventory = data["inventory"]
    player = data["player"]
    used_codes = set(data["used_codes"])
    achievements = data["achievements"]

    print("📂 Save loaded!")

# =====================
# XP SYSTEM
# =====================

def add_xp(amount):
    player["xp"] += amount
    if player["xp"] >= player["level"] * 10:
        player["xp"] = 0
        player["level"] += 1
        player["tool_level"] += 1
        print(f"🎉 LEVEL UP! You are now level {player['level']}!")
        print("🪓 Your tools are stronger!")

# =====================
# GAME FUNCTIONS
# =====================

def show_inventory():
    print("\n📦 INVENTORY")
    print("-----------------")
    for item, amount in inventory.items():
        print(f"{item.capitalize()}: {amount}")

    print(f"\n⭐ Level: {player['level']} | XP: {player['xp']}")
    print(f"🪓 Tool Level: {player['tool_level']}")

def gather():
    print("\n🌲 Gathering...")

    multiplier = player["tool_level"]

    wood = random.randint(1, 3) * multiplier
    stone = random.randint(0, 2) * multiplier
    iron = random.randint(0, 1) * multiplier

    # Rare drop
    diamond = 0
    if random.random() < 0.1:
        diamond = 1
        inventory["diamond"] += 1
        achievements["Diamond Finder"] = True
        print("💎 You found a DIAMOND!")

    inventory["wood"] += wood
    inventory["stone"] += stone
    inventory["iron"] += iron

    print(f"You got: {wood} wood, {stone} stone, {iron} iron")

    add_xp(5)
    achievements["First Gather"] = True

def craft():
    print("\n🛠️ CRAFTING")
    print("-----------------")

    for item, req in recipes.items():
        print(f"{item} -> {req}")

    choice = input("\nCraft what? ").lower()

    if choice not in recipes:
        print("❌ Invalid item!")
        return

    requirements = recipes[choice]

    for item, amount in requirements.items():
        if inventory[item] < amount:
            print("❌ Not enough resources!")
            return

    for item, amount in requirements.items():
        inventory[item] -= amount

    inventory[choice] += 1
    print(f"✅ Crafted {choice}!")

    add_xp(3)
    achievements["Crafter"] = True

    if choice == "sword":
        achievements["First Sword"] = True

def redeem_code():
    code = input("\n🎁 Enter code: ").upper()

    if code in used_codes:
        print("❌ Already used!")
        return

    if code in codes:
        for item, amount in codes[code].items():
            inventory[item] += amount
        used_codes.add(code)
        print("✅ Code redeemed!")
    else:
        print("❌ Invalid code!")

def show_achievements():
    print("\n🏆 ACHIEVEMENTS")
    print("-----------------")
    for name, done in achievements.items():
        status = "✅" if done else "❌"
        print(f"{name}: {status}")

# =====================
# MAIN LOOP
# =====================

def main():
    load_game()

    while True:
        print("\n========================")
        print("   🛠️ CRAFT SIMULATOR")
        print("========================")
        print("1. Gather")
        print("2. Craft")
        print("3. Inventory")
        print("4. Codes")
        print("5. Achievements")
        print("6. Save Game")
        print("7. Exit")

        choice = input("\n> ")

        if choice == "1":
            gather()
        elif choice == "2":
            craft()
        elif choice == "3":
            show_inventory()
        elif choice == "4":
            redeem_code()
        elif choice == "5":
            show_achievements()
        elif choice == "6":
            save_game()
        elif choice == "7":
            save_game()
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
