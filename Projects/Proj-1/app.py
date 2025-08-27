import streamlit as st
import json
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).parent
INVENTORY_FILE = BASE_DIR / "inventory.json"
LOG_FILE = BASE_DIR / "logs.txt"


def read_inventory():
    if not INVENTORY_FILE.exists():
        return {}
    try:
        return json.loads(INVENTORY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def write_inventory(data):
    INVENTORY_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def append_log(message: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")


def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def flatten_items(inv):
    # returns list of tuples (compound_key, dept, item_key, item_dict)
    out = []
    for dept_key, items in inv.items():
        for item_key, item in items.items():
            compound = f"{dept_key}/{item_key}"
            out.append((compound, dept_key, item_key, item))
    return out


def main():
    st.title("Inventory Management — Streamlit")

    inventory = read_inventory()

    st.sidebar.header("Buy an item")
    user_name = st.sidebar.text_input("Your name")

    # Build select options
    flat = flatten_items(inventory)
    if flat:
        option_labels = [f"{c} — {itm['name']} (${itm['price']}) — {itm['count']} in stock" for c, _, _, itm in flat]
        idx = st.sidebar.selectbox("Select item", list(range(len(option_labels))), format_func=lambda i: option_labels[i])
        quantity = st.sidebar.number_input("Quantity", min_value=1, value=1)
        if st.sidebar.button("Buy"):
            compound, dept, item_key, item = flat[idx]
            purchase_time = now_str()
            if item.get("count", 0) >= quantity:
                item["count"] = item.get("count", 0) - quantity
                total = item.get("price", 0) * quantity
                write_inventory(inventory)
                log = f"{purchase_time} - {user_name or 'Unknown'} bought {quantity} {item['name']} for ${total}"
                append_log(log)
                st.success(f"Purchase successful — Total: ${total}")
            else:
                log = f"{purchase_time} - {user_name or 'Unknown'} tried to buy {quantity} {item['name']} but not enough stock"
                append_log(log)
                st.error("Not enough stock")
    else:
        st.sidebar.info("No items available in inventory.")

    st.header("Departments & Items")
    if not inventory:
        st.info("Inventory is empty or missing `inventory.json` in this folder.")
        return

    for dept_key, items in inventory.items():
        with st.expander(dept_key.title(), expanded=False):
            for item_key, item in items.items():
                cols = st.columns([3, 1, 1])
                cols[0].write(f"**{item.get('name')}**\n\n{item.get('description','')}" if item.get('description') else f"**{item.get('name')}**")
                cols[1].write(f"Price: ${item.get('price')}")
                cols[2].write(f"Stock: {item.get('count')}")


if __name__ == "__main__":
    main()
