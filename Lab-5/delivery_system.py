"""Manage food delivery orders, menu configuration, and revenue."""

import json
from datetime import datetime

VALID_STATUSES = ['placed', 'cooking', 'out_for_delivery', 'delivered']
DEFAULT_MENU = {'pizza': 250, 'burger': 150, 'fries': 90, 'coke': 40}


class FoodDeliverySystem:
    """Store and manage food delivery orders."""

    def __init__(self):
        """Initialize the order system with an empty order list."""
        self.orders = {}
        self.next_id = 1
        self.menu = DEFAULT_MENU.copy()
        self.order_history = []

    def create_order(self, customer, items):
        """Create an order after validating the customer and menu items."""
        if not customer.strip():
            raise ValueError('Customer name cannot be empty.')
        if not items:
            raise ValueError('An order must contain at least one item.')
        unknown_items = [item for item in items if item not in self.menu]
        if unknown_items:
            raise ValueError(f'Unknown menu items: {unknown_items}')
        total = sum(self.menu[item] for item in items)
        order_id = self.next_id
        self.orders[order_id] = {
            'customer': customer,
            'items': items,
            'total': total,
            'status': 'placed',
        }
        self.order_history.append(order_id)
        self.next_id += 1
        return order_id

    def update_order_status(self, order_id, status):
        """Update an order only when its ID and status are valid."""
        if order_id not in self.orders:
            return False
        if status not in VALID_STATUSES:
            return False
        self.orders[order_id]['status'] = status
        return True

    def read_menu_config(self, file='menu.json'):
        """Load menu prices from JSON, or use the default menu."""
        try:
            with open(file, 'r', encoding='utf-8') as config_file:
                loaded_menu = json.load(config_file)
            if isinstance(loaded_menu, dict):
                self.menu = loaded_menu
            else:
                self.menu = DEFAULT_MENU.copy()
        except (FileNotFoundError, json.JSONDecodeError):
            self.menu = DEFAULT_MENU.copy()

    def daily_revenue(self):
        """Calculate revenue from orders marked as delivered."""
        return sum(
            order['total']
            for order in self.orders.values()
            if order['status'] == 'delivered'
        )

    def backup_orders(self, file='orders.json'):
        """Save all orders to a JSON backup file."""
        with open(file, 'w', encoding='utf-8') as backup_file:
            json.dump(self.orders, backup_file, indent=4)

    def restore_orders(self, file='orders.json'):
        """Restore orders from a JSON backup file."""
        try:
            with open(file, 'r', encoding='utf-8') as backup_file:
                saved_orders = json.load(backup_file)
            self.orders = {
                int(order_id): order
                for order_id, order in saved_orders.items()
            }
            self.next_id = max(self.orders, default=0) + 1
        except (FileNotFoundError, json.JSONDecodeError):
            self.orders = {}
            self.next_id = 1

    def print_queue(self):
        """Print the current order queue."""
        print(f'Order queue at {datetime.now()}')
        for order_id, order in self.orders.items():
            print(
                order_id,
                order['customer'],
                order['status'],
                order['total'],
            )


def main():
    """Run a short demonstration of the food delivery system."""
    system = FoodDeliverySystem()
    system.read_menu_config()
    first_order = system.create_order('Asha', ['pizza', 'coke'])
    second_order = system.create_order('Ravi', ['burger', 'fries'])
    system.update_order_status(first_order, 'delivered')
    system.update_order_status(second_order, 'teleported')
    print('Revenue today:', system.daily_revenue())
    system.backup_orders()
    system.restore_orders()
    system.print_queue()


if __name__ == '__main__':
    main()
