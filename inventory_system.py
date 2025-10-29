"""
Inventory Management System

Provides basic inventory operations:
- Add and remove items
- Save/load inventory data to JSON
- Check for low-stock items
"""

import json
from datetime import datetime
from typing import List, Dict


def add_item(stock: Dict[str, int], item: str, qty: int, logs: List[str] | None = None) -> None:
    """
    Add quantity of a given item to the stock.

    Args:
        stock (dict): Current inventory dictionary.
        item (str): Item name.
        qty (int): Quantity to add (must be integer).
        logs (list, optional): List to record log messages.
    """
    if not isinstance(item, str) or not isinstance(qty, int):
        print(f"Invalid item or quantity: {item}, {qty}")
        return

    if logs is None:
        logs = []

    stock[item] = stock.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(stock: Dict[str, int], item: str, qty: int) -> None:
    """
    Remove quantity of an item from the stock.
    Deletes the item if quantity drops to zero or below.

    Args:
        stock (dict): Current inventory dictionary.
        item (str): Item name.
        qty (int): Quantity to remove.
    """
    if not isinstance(item, str) or not isinstance(qty, int):
        print(f"Invalid item or quantity: {item}, {qty}")
        return

    try:
        stock[item] -= qty
        if stock[item] <= 0:
            del stock[item]
    except KeyError:
        print(f"Warning: Tried to remove '{item}' which does not exist.")


def get_qty(stock: Dict[str, int], item: str) -> int:
    """
    Retrieve current quantity for a given item.

    Args:
        stock (dict): Current inventory dictionary.
        item (str): Item name.

    Returns:
        int: Quantity available, or 0 if not found.
    """
    return stock.get(item, 0)


def load_data(file: str = "inventory.json") -> Dict[str, int]:
    """
    Load inventory data from a JSON file.

    Args:
        file (str): File path to load from.

    Returns:
        dict: Loaded inventory data (empty if file not found or invalid).
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"Loaded inventory data from {file}")
        return data
    except FileNotFoundError:
        print(f"No existing inventory file found: {file}. Starting fresh.")
        return {}
    except json.JSONDecodeError:
        print(f"Error reading JSON file: {file}. Using empty stock data.")
        return {}


def save_data(stock: Dict[str, int], file: str = "inventory.json") -> None:
    """
    Save current inventory data to a JSON file.

    Args:
        stock (dict): Current inventory dictionary.
        file (str): File path to save to.
    """
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock, f, indent=4)
        print(f"Inventory data saved to {file}")
    except OSError as e:
        print(f"Error saving inventory data: {e}")


def print_data(stock: Dict[str, int]) -> None:
    """Print all current inventory items and their quantities."""
    print("\n=== Items Report ===")
    for item, qty in stock.items():
        print(f"{item} -> {qty}")
    print("====================\n")


def check_low_items(stock: Dict[str, int], threshold: int = 5) -> List[str]:
    """
    Return a list of items with quantity below the threshold.

    Args:
        stock (dict): Current inventory dictionary.
        threshold (int): Minimum safe stock level.

    Returns:
        list[str]: Items with low stock.
    """
    return [item for item, qty in stock.items() if qty < threshold]


def main() -> None:
    """Main function demonstrating example inventory operations."""
    stock = load_data()

    add_item(stock, "apple", 10)
    add_item(stock, "banana", 2)
    add_item(stock, "orange", 0)

    remove_item(stock, "apple", 3)
    remove_item(stock, "pear", 1)  # non-existent item

    print(f"Apple stock: {get_qty(stock, 'apple')}")
    print("Low items:", check_low_items(stock))

    save_data(stock)
    print_data(stock)


if __name__ == "__main__":
    main()
