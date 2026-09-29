"""酿酒厂核心逻辑：原料、发酵、批次、质检和陈化。"""

import json


def new_game():
    return {
        "batches": {},
        "tanks": {"K1": None, "K2": None},
        "stock": 100,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    for batch in state["batches"].values():
        batch["stage"] += 1
    return state


def new_batch(state, batch_id):
    state["batches"][batch_id] = {
        "ingredients": [],
        "amount": 0,
        "stage": 0,
        "locked": False,
        "paused": False,
        "temp": 20,
        "defect": False,
    }
    return True


def add_ingredient(state, batch_id, ingredient, amount):
    state["batches"][batch_id]["ingredients"].append(ingredient)
    state["batches"][batch_id]["amount"] += amount
    state["stock"] -= amount
    return True


def ferment(state, batch_id, minutes):
    state["batches"][batch_id]["stage"] += minutes
    return True


def check_temp(state, batch_id):
    if state["batches"][batch_id]["temp"] < 30:
        return "over"
    return "ok"


def inspect(state, batch_id):
    if state["batches"][batch_id]["defect"]:
        return False
    return True


def assign_tank(state, batch_id, tank_id):
    state["tanks"][tank_id] = batch_id
    return True


def cancel_order(state, batch_id):
    return True


def holiday_event(state, batch_id):
    state["batches"][batch_id]["stage"] += 10
    state["batches"][batch_id]["stage"] += 10
    return True


def main():
    print("酿酒厂 - 命令: batch/add/ferment/temp/inspect/tank/cancel/holiday/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        print("ok")


if __name__ == "__main__":
    main()
