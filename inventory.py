import json
import os

inventory_file = 'user_inventory.json'
user_inventory = {}

def load_inventory():
    global user_inventory
    if os.path.exists(inventory_file):
        with open(inventory_file, 'r') as f:
            user_inventory = json.load(f)
    else:
        user_inventory = {}

def save_inventory():
    with open(inventory_file, 'w') as f:
        json.dump(user_inventory, f, indent=4)

load_inventory()

def get_user_inventory(user_id):
    return user_inventory.get(user_id, [])

def add_to_inventory(user_id, item):
    if user_id not in user_inventory:
        user_inventory[user_id] = []
    user_inventory[user_id].append(item)
    save_inventory()

def remove_3_star_items(user_id):
    if user_id in user_inventory:
        user_inventory[user_id] = [item for item in user_inventory[user_id] if item[2] != "3-star"]
        save_inventory()

def create_inventory_embed(username, pages, current_page):
    inventory_list = pages[current_page]
    embed = discord.Embed(title=f"{username}'s Inventory (Page {current_page+1}/{len(pages)})", color=0x00ff00)
    for item in inventory_list:
        embed.add_field(name=item[0], value=f"Stars: {item[1]}, Rarity: {item[2]}", inline=False)
    return embed
