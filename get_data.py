import requests
import pandas as pd
import json 
import logging

# Set up logging configuration
logging.basicConfig(
    filename="script_log.txt",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Create a StreamHandler and set its log level to INFO
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and set it to the console handler
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logging.getLogger().addHandler(console_handler)


###custom table



def write_json(df, json_file):
    xdiz = df.to_dict()
    with open(json_file, "w") as file:
        json.dump(xdiz, file, indent=2)
    logging.info("Data written to JSON file: %s", json_file)


def get_api_data(endpoint):
    logging.info(f"Getting data from {endpoint}")
    try:
        response = requests.get(endpoint)
        response.raise_for_status()  # Check for any errors in the response
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error during API call:", e)
        return None
### brawlers, star powers and gadgets

#api request
import datetime
import os
new_week_download = datetime.datetime.fromtimestamp(os.path.getmtime("src/data/brawler_list.json")) < datetime.datetime.now().replace(microsecond=0) +datetime.timedelta(days=-7)

brawlers_info = get_api_data("https://api.brawlapi.com/v1/brawlers")
x = brawlers_info["list"]
n_brawlers = len(x)
actual_brawlers = len(pd.read_json("src/data/brawler_list.json"))
refresh_brawlers = n_brawlers > actual_brawlers
if refresh_brawlers or new_week_download:
    nomi = []
    ids = []
    gadget = []
    star_powers = []
    item = x[0]
    # get data from json
    for item in x:
        nomi.append(item['name'])
        ids.append(item['id'])
        gadgets = ', '.join([gadget['name'] for gadget in item['gadgets']])
        gadget.append(gadgets)
        star_powers.append(', '.join([star_power['name'] for star_power in item['starPowers']]))
    brawlers_info = pd.DataFrame({
        'name': nomi,
        'id': ids,
        'gadget': gadget,
        'starPowers': star_powers
    })
    brawlers_info = brawlers_info.set_index("name")
    write_json(brawlers_info, "src/data/brawler_list.json")

    #api request function for single brawler by id


    #write tables for gadgets and star powers
    brawlers_info = brawlers_info.reset_index()
    starpowers=[]
    gadgets=[]
    names_g = []
    names_sp = []
    for i in range(len(brawlers_info)):
        nome = brawlers_info.name[i]
        id = str(brawlers_info.id[i])
        url = "https://api.brawlapi.com/v1/brawlers" + "/" + id
        temp = get_api_data(url)
        starpowers.append(temp["starPowers"])
        for j in range(len(temp["starPowers"])):
            names_sp.append(nome)
        for j in range(len(temp["gadgets"])):
            names_g.append(nome)
        gadgets.append(temp["gadgets"])
    starpowers_list = [item for sublist in starpowers for item in sublist]
    starpowers_df = pd.DataFrame(starpowers_list)
    starpowers_df["brawler"] = names_sp
    gadgets_list = [item for sublist in gadgets for item in sublist]
    gadgets_df = pd.DataFrame(gadgets_list)
    gadgets_df = gadgets_df.set_index("name")

    gadgets_df["brawler"] = names_g
    write_json(gadgets_df, "src/data/gadgets_list.json")

    starpowers_df = starpowers_df.set_index("name")
    starpowers_df = starpowers_df.set_index("name")
    write_json(starpowers_df, "src/data/starpowers_list.json")

### maps

#api request
maps_info = get_api_data("https://api.brawlapi.com/v1/maps")["list"]
x = maps_info
nomi = []
ids = []
active = []
mod = []
imageUrl = []

# get data from json
for item in x:
    nomi.append(item['name'])
    ids.append(item['id'])
    active.append(item["disabled"])
    mod.append(item["gameMode"]["name"])
    imageUrl.append(item["imageUrl"])
maps_info = pd.DataFrame({
    'name': nomi,
    'id': ids,
    'active': active,
    'mod':mod,
    'imageUrl': imageUrl
})
maps_info["active"] = ~maps_info["active"]
maps_info=maps_info[maps_info.active]
maps_info0 = maps_info.copy()
maps_info = maps_info.set_index("name")
write_json(maps_info, "src/data/full_maps_list.json")


maps_info = maps_info0.sort_values(by=["mod","name"])
maps_info = maps_info.pivot_table(
    index="mod",
    values="name",
    aggfunc=list
)
write_json(maps_info, "src/data/mods_maps_list.json")