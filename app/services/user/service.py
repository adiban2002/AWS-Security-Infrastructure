users_db = {}

def create_user(user_id: str, name: str):
    users_db[user_id] = {"user_id": user_id, "name": name}
    return users_db[user_id]


def get_user(user_id: str):
    return users_db.get(user_id)