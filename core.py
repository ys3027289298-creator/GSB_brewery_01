"""酿酒厂核心逻辑：原料、发酵、批次、质检和陈化。"""

import json

OVER_TEMP_THRESHOLD = 30
HOLIDAY_BONUS = 10
FIXED_DATE = "2026-09-29"


def new_game():
    return {
        "batches": {},
        "tanks": {"K1": None, "K2": None},
        "stock": 100,
        "date": FIXED_DATE,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    if not text or not text.strip():
        return new_game()
    state = json.loads(text)
    if not isinstance(state, dict):
        raise ValueError("存档格式错误")
    state.setdefault("batches", {})
    state.setdefault("tanks", {"K1": None, "K2": None})
    state.setdefault("stock", 0)
    state.setdefault("date", FIXED_DATE)
    return state


def new_batch(state, batch_id):
    if not batch_id or batch_id in state["batches"]:
        return False
    state["batches"][batch_id] = {
        "ingredients": [],
        "amount": 0,
        "stage": 0,
        "locked": False,
        "paused": False,
        "temp": 20,
        "defect": False,
        "holiday_applied": False,
    }
    return True


def add_ingredient(state, batch_id, ingredient, amount):
    batch = state["batches"].get(batch_id)
    if batch is None or batch["locked"]:
        return False
    if not ingredient or amount <= 0 or amount > state["stock"]:
        return False
    if ingredient in batch["ingredients"]:
        return False
    batch["ingredients"].append(ingredient)
    batch["amount"] += amount
    state["stock"] -= amount
    return True


def ferment(state, batch_id, minutes):
    batch = state["batches"].get(batch_id)
    if batch is None or batch["paused"] or minutes <= 0:
        return False
    batch["stage"] += minutes
    return True


def check_temp(state, batch_id):
    batch = state["batches"].get(batch_id)
    if batch is None:
        return "unknown"
    if batch["temp"] >= OVER_TEMP_THRESHOLD:
        return "over"
    return "ok"


def inspect(state, batch_id):
    batch = state["batches"].get(batch_id)
    if batch is None:
        return False
    if batch["defect"]:
        state["stock"] += batch["amount"]
        batch["amount"] = 0
        return False
    return True


def assign_tank(state, batch_id, tank_id):
    if batch_id not in state["batches"] or tank_id not in state["tanks"]:
        return False
    occupant = state["tanks"][tank_id]
    if occupant is not None:
        return occupant == batch_id
    state["tanks"][tank_id] = batch_id
    return True


def cancel_order(state, batch_id):
    for tank_id, occupant in state["tanks"].items():
        if occupant == batch_id:
            state["tanks"][tank_id] = None
    return state["batches"].pop(batch_id, None) is not None


def holiday_event(state, batch_id):
    batch = state["batches"].get(batch_id)
    if batch is None or batch["holiday_applied"]:
        return False
    batch["stage"] += HOLIDAY_BONUS
    batch["holiday_applied"] = True
    return True


def main():
    state = new_game()
    print("酿酒厂 - 命令: batch/add/ferment/temp/inspect/tank/cancel/holiday/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw:
            print("空命令")
            continue
        parts = raw.split()
        cmd, args = parts[0], parts[1:]
        if cmd == "quit":
            break
        try:
            if cmd == "batch" and len(args) == 1:
                print("ok" if new_batch(state, args[0]) else "error")
            elif cmd == "add" and len(args) == 3:
                print("ok" if add_ingredient(state, args[0], args[1], int(args[2])) else "error")
            elif cmd == "ferment" and len(args) == 2:
                print("ok" if ferment(state, args[0], int(args[1])) else "error")
            elif cmd == "temp" and len(args) == 1:
                print(check_temp(state, args[0]))
            elif cmd == "inspect" and len(args) == 1:
                print("ok" if inspect(state, args[0]) else "error")
            elif cmd == "tank" and len(args) == 2:
                print("ok" if assign_tank(state, args[0], args[1]) else "error")
            elif cmd == "cancel" and len(args) == 1:
                print("ok" if cancel_order(state, args[0]) else "error")
            elif cmd == "holiday" and len(args) == 1:
                print("ok" if holiday_event(state, args[0]) else "error")
            else:
                print("未知命令")
        except ValueError:
            print("参数错误")


if __name__ == "__main__":
    main()
