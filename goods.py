GOODS = {
    "1b431aa8-577d-436a-83bc-acd56395cef6": { "name": "block", "price": 80, "count": 0 },
    "1a76c063-dbb4-4192-b7fd-f9fb87cff3f9": { "name": "time", "price": 110, "count": 0 },
    "bc9d2297-1a9e-412b-9a62-d168dd3200c3": { "name": "limit_turbo", "price": 130, "count": 0 },
    "0f131b05-b239-4ae2-a0fd-b2f04a78f0d6": { "name": "x2_moneys", "price": 200, "count": 0 },
    "963c7d2d-c748-46a6-af0e-0d320c9f18dd": { "name": "mirror", "price": 500, "count": 0 },
    "8cada432-8898-4955-874b-0243b46aff15": { "name": "airdrop", "price": 750, "count": 0 },
    "d9923700-68f3-4aa4-970b-ced2f527ffcf": { "name": "trap", "price": 999, "count": 0 },
    "4fa48aeb-8d64-4403-993e-7907851c4a36": { "name": "atom_explosion", "price": 5000, "count": 0 }
}

def toJSON(goods_value):
    data = { "items": [] }
    for item_id, item_data in goods_value.items():
        item = {
            "id": item_id,
            "name": item_data["name"],
            "price": item_data["price"],
	    "count": item_data["count"]
                }
        data["items"].append(item)
    return data

def fromJSON(json_value):
    data = json_value["items"]

    result = dict()

    for item in data:
        id, name, price = item["id"], item["name"], item["price"]
        result[id] = {"name": name, "price": price}

    return result