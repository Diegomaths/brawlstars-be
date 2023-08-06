#esposizione api

import json
import pandas as pd
import requests
import os
import shutil
from flask import Flask, jsonify, request
app = Flask(__name__)
def get_table():
    with open("src/data/brawl_data.json") as file:
        try:
            brawl_data = json.load(file)
            df = pd.DataFrame(brawl_data).T
        except:
            column_names = ["Brawler",
                "Modalita",
                "Mappa",
                "Gadget",
                "Abilita stellare",
                "Coppia"]
            df=pd.DataFrame(columns=column_names)
        return df


with open("src/data/gadgets_list.json") as file:
    gadgets_data = json.load(file)
with open("src/data/starpowers_list.json") as file:
    starpowers_data = json.load(file)
with open("src/data/full_maps_list.json") as file:
    full_maps_data = json.load(file)
with open("src/data/mods_maps_list.json") as file:
    mods_maps_data = json.load(file)


@app.route('/api/add_row', methods=['POST'])
def add_row():
    df = get_table()
    try:
        # Leggi il nuovo record JSON in input dalla richiesta POST
        new_row = request.get_json(force=True)
        # Converte il nuovo record in DataFrame
        new_row_df = pd.DataFrame(new_row, index=[0])
        # Aggiungi il nuovo record al DataFrame esistente
        new_df = pd.concat([df, new_row_df]).reset_index(drop=True).drop_duplicates()
        # Salva il DataFrame aggiornato in brawl_data.json
        if new_df.shape[0] >= 2:
            new_df.replace('', pd.NA, inplace=True)
            new_df = new_df.dropna(how='all').reset_index(drop=True)
        new_df.T.to_json("src/data/brawl_data.json", indent=2)
        master_file = os.path.join("src", "data", "brawl_data.json")
        base_dir = os.path.join("src","data", "users")
        user_file = os.path.join(base_dir, current_user, "brawl_data.json")
        shutil.copy(master_file, user_file)
        return jsonify({"message": "Added row"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": str(e)})

@app.route('/api/delete_row', methods=['POST'])
def delete_row():
    df = get_table()
    try:
        # Leggi il nuovo record JSON in input dalla richiesta POST
        to_drop = request.get_json(force=True)
        # Rimuovi
        df = df.drop(to_drop, axis=0).reset_index(drop=True)
        # Salva il DataFrame aggiornato in brawl_data.json
        df.T.to_json("src/data/brawl_data.json", indent=2)
        master_file = os.path.join("src", "data", "brawl_data.json")
        base_dir = os.path.join("src","data", "users")
        user_file = os.path.join(base_dir, current_user, "brawl_data.json")
        shutil.copy(master_file, user_file)
        return jsonify({"message": "Removed row"}), 200
    except Exception as e:
        return jsonify({"message": str(e)})

@app.route('/api/edit_row', methods=['POST'])
def edit_row():
    df = get_table()
    try:
        # Leggi il nuovo record JSON in input dalla richiesta POST
        req = request.get_json(force=True)
        to_edit = req["row"]
        new_value = req["new_value"]
        new_row = pd.DataFrame(new_value, index=[0]).reset_index(drop=True)

        # modifica
        df.loc[to_edit, :] = new_row

        # Salva il DataFrame aggiornato in brawl_data.json
        df.T.to_json("src/data/brawl_data.json", indent=2)
        master_file = os.path.join("src", "data", "brawl_data.json")
        base_dir = os.path.join("src","data", "users")
        user_file = os.path.join(base_dir, current_user, "brawl_data.json")
        shutil.copy(master_file, user_file)
        return jsonify({"message": "Modified row"}), 200
    except Exception as e:
        return jsonify({"message": str(e)})
    
@app.route("/api/gadgets_list")
def get_gadgets_list():
    return jsonify(gadgets_data)

@app.route("/api/starpowers_list")
def get_starpowers_list():
    return jsonify(starpowers_data)

@app.route("/api/full_maps_list")
def get_full_maps_list():
    return jsonify(full_maps_data)

@app.route("/api/mods_maps_list")
def get_mods_maps_list():
    return jsonify(mods_maps_data)


# dati per utente
@app.route('/api/get_user', methods=['POST'])
def get_user():
    try:
        # Leggi il nuovo record JSON in input dalla richiesta POST
        user = request.get_json(force=True)
        global current_user
        current_user = user
        base_dir = os.path.join("src","data", "users")

        users_list = [ f.path for f in os.scandir(base_dir) if f.is_dir() ]
        last_elements = [string.split("/")[-1] for string in users_list]
        result = f"User {user} data"
        master_file = os.path.join("src", "data", "brawl_data.json")
        if user in last_elements:
            user_file = os.path.join(base_dir, user, "brawl_data.json")
            shutil.copy(user_file, master_file)
            result += " successfully retrieved"
        else:
            new_dir = os.path.join(base_dir, user)
            os.makedirs(new_dir)
            user_file = os.path.join(new_dir, "brawl_data.json")
            empty_file = os.path.join("src", "data", "empty.json")
            shutil.copy(empty_file, user_file)
            shutil.copy(user_file, master_file)
            result += " successfully created"
        df = get_table()
        return jsonify({"message": result}), 200
    
    except Exception as e:
        print(e)
        return jsonify({"message": str(e)})




if __name__ == "__main__":
    app.run(debug=True)


# Brawl Data: http://127.0.0.1:5000/api/brawl_data
# Gadgets List: http://127.0.0.1:5000/api/gadgets_list
# Star Powers List: http://127.0.0.1:5000/api/starpowers_list
# Full Maps List: http://127.0.0.1:5000/api/full_maps_list
# Mods Maps List: http://127.0.0.1:5000/api/mods_maps_list