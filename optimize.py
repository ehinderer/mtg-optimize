import requests
import time
import json
import pandas as pd

# Get redundant card list for library
library = pd.read_csv("library/10-5-2023.csv", header=0)
library_name_list = library["Name"].to_list()
library_quantity_list = library["Quantity"].to_list()
library_list = [[library_name_list[i] for j in range(library_quantity_list[i])] for i in range(len(library_name_list))]
library_list = [item for sublist in library_list for item in sublist]


def send_api_request(url, method='GET', headers=None, data=None, params=None):
    response = None
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, params=params)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data, params=params)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=data, params=params)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, params=params)
        # Check if the request was successful
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return None


def get_decks(curr_page=1, deckformat=3):
    base_url = "https://archidekt.com/api/decks/"
    params = {
        'page': curr_page,
        'deckFormat': deckformat
    }
    response_data = send_api_request(base_url, method='GET', params=params)
    if response_data:
        response = response_data["results"]
    else:
        response = {}
    return response


def get_cards(deck_id):
    base_url = "https://archidekt.com/api/decks/{}/".format(deck_id)
    params = {}
    response_data = send_api_request(base_url, method='GET', params=params)
    if response_data:
        response = response_data
    else:
        response = {}
    return response


def evaluate_deck(deck_data):
    deck_list = [item for sublist in [[card["card"]["oracleCard"]["name"] for _ in range(card["quantity"])] for card in deck_data["cards"]] for item in sublist]
    card_value_dict = {card["card"]["oracleCard"]["name"]: card["card"]["prices"]["ck"] for card in deck_data["cards"]}
    missing_cards = [item for item in deck_list if item not in library_list]
    missing_card_value = sum([card_value_dict[i] for i in missing_cards])
    print(missing_cards)
    print(missing_card_value)


if __name__ == "__main__":
    deck_import = []
    for i in range(10):
        data = get_decks(curr_page=i+1)
        deck_import.extend(data)
        time.sleep(2)
    for deck in deck_import:
        json_string = json.dumps(deck)
        with open("./decks/{}.json".format(deck["id"]), "w") as out_file:
            out_file.write(json_string)
"""
    deck_ids = [i["id"] for i in deck_import]
    for deck_id in deck_ids:
        data = get_cards(deck_id)
        evaluate_deck(data)
        time.sleep(2)
"""