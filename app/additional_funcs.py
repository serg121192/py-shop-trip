from datetime import datetime
from decimal import Decimal, ROUND_DOWN

from app.car import Car
from app.customer import Customer
from app.shop import Shop


def create_instances(customers: dict, shops: dict) -> tuple[
    list[Customer],
    list[Shop]
]:
    return (
        [
            Customer(
                customer["name"],
                customer["product_cart"],
                customer["location"],
                customer["money"],
                Car(
                    customer["car"]["brand"],
                    customer["car"]["fuel_consumption"]
                )
            ) for customer in customers
        ],
        [
            Shop(
                shop["name"],
                shop["location"],
                shop["products"]
            ) for shop in shops
        ]
    )


def calculate_distance_to_shop(
        customer_loc: list[int],
        shop_loc: list[int]
) -> float:
    return (
        round(
            ((shop_loc[0] - customer_loc[0]) ** 2
             + (shop_loc[1] - customer_loc[1]) ** 2)
            ** 0.5, 2)
    )


def shop_receipt(
        customers_cart: dict,
        shop_price: dict
) -> float:
    return sum(
        [
            customers_cart[key] * shop_price[key]
            for key in customers_cart
        ]
    )


def total_trip_cost(
        fuel_price: float,
        customers: list[Customer],
        shops: list[Shop]
) -> None:
    for customer in customers:
        for shop in shops:
            distance = calculate_distance_to_shop(
                customer.location,
                shop.location
            )
            receipt_cost = shop_receipt(
                customer.products_cart,
                shop.products
            )
            total_price = Decimal(
                receipt_cost
                + (distance * 2 * customer.car.fuel_consumption / 100)
                * fuel_price
            )

            cost = float(total_price.quantize(
                Decimal("0.01"),
                rounding=ROUND_DOWN
            ))
            customer.trips_costs[f"{shop.name}"] = cost


def customer_can_go_to_shop(customer: Customer) -> str:
    print(f"{customer.name} has {customer.money} dollars")
    for shop in customer.trips_costs:
        print(f"{customer.name}'s trip to the {shop} "
              f"costs {customer.trips_costs[shop]}")
    customers_minimal_trip_cost = min(customer.trips_costs.values())
    if customers_minimal_trip_cost <= customer.money:
        shop_name = list(customer.trips_costs.keys())[
            list(customer.trips_costs.values()).index(
                min(customer.trips_costs.values()))]
        print(f"{customer.name} rides to {shop_name}\n")
        return shop_name
    print(f"{customer.name} doesn't have enough money "
          f"to make a purchase in any shop\n")


def print_shop_receipt(
        customer: Customer,
        shops: list[Shop],
        shop_name: str
) -> None:
    product_names = ["milk", "bread", "butter"]
    for shop in shops:
        if shop.name == shop_name:
            receipt_lines = [
                f'Date: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n',
                f'Thanks, {customer.name}, for your purchase!\n'
            ]
            receipt_lines.append("You have bought:\n")
            for product in product_names:
                quantity = customer.products_cart.get(product, 0)
                price = shop.products.get(product, 0)
                total = quantity * price
                receipt_lines.append(
                    f'{quantity} {product}s for {total} dollars\n'
                )
            total_cost = shop_receipt(customer.products_cart, shop.products)
            receipt_lines.append(
                f'Total cost is {total_cost} dollars\n'
            )
            receipt_lines.append("See you again!\n")
            print("".join(receipt_lines))


def taking_back_home(customer: Customer, total_price: float) -> None:
    customer.money -= total_price
    print(f"{customer.name} rides home\n"
          f"{customer.name} now has {round(customer.money, 2)} dollars\n")
