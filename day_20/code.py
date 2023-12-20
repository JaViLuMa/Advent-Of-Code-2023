import math
from copy import deepcopy
from collections import deque


BUTTON_PRESSES = 1000
BUTTON_PRESSES_FOR_RX = 5000


def populate_modules_memory(modules):
    for name, module in modules.items():
        for destination in module["destinations"]:
            if destination in modules and modules[destination]["type"] == "&":
                modules[destination]["memory"][name] = "low"


def get_product_of_low_and_high_pulses(modules):
    low_pulses = 0
    high_pulses = 0

    for _ in range(BUTTON_PRESSES):
        low_pulses += 1

        modules_queue = deque(
            [
                ("broadcaster", destination, "low")
                for destination in modules["broadcaster"]["destinations"]
            ]
        )

        while modules_queue:
            start, destination, pulse = modules_queue.popleft()

            if pulse == "low":
                low_pulses += 1
            else:
                high_pulses += 1

            if destination in modules:
                module = modules[destination]

                if module["type"] == "%":
                    if pulse == "low":
                        module["memory"] = "on" if module["memory"] == "off" else "off"

                        for destination_module in module["destinations"]:
                            modules_queue.append(
                                (
                                    destination,
                                    destination_module,
                                    "high" if module["memory"] == "on" else "low",
                                )
                            )
                else:
                    module["memory"][start] = pulse

                    new_pulse = (
                        "low"
                        if all(x == "high" for x in module["memory"].values())
                        else "high"
                    )

                    for destination_module in module["destinations"]:
                        modules_queue.append(
                            (destination, destination_module, new_pulse)
                        )

    return low_pulses * high_pulses


def get_minimal_button_presses_to_deliver_low_pulse_to_rx(modules):
    conjuction_module_cycles = {}

    for cycle in range(1, BUTTON_PRESSES_FOR_RX):
        modules_queue = deque(
            [
                ("broadcaster", destination, "low")
                for destination in modules["broadcaster"]["destinations"]
            ]
        )

        while modules_queue:
            start, destination, pulse = modules_queue.popleft()

            if destination in modules:
                module = modules[destination]

                if module["type"] == "%":
                    if pulse == "low":
                        module["memory"] = "on" if module["memory"] == "off" else "off"

                        for destination_module in module["destinations"]:
                            modules_queue.append(
                                (
                                    destination,
                                    destination_module,
                                    "high" if module["memory"] == "on" else "low",
                                )
                            )
                else:
                    module["memory"][start] = pulse

                    new_pulse = (
                        "low"
                        if all(x == "high" for x in module["memory"].values())
                        else "high"
                    )

                    if (
                        new_pulse == "high"
                        and destination not in conjuction_module_cycles
                    ):
                        conjuction_module_cycles[destination] = cycle

                    for destination_module in module["destinations"]:
                        modules_queue.append(
                            (destination, destination_module, new_pulse)
                        )

    return math.prod(conjuction_module_cycles.values())


modules = {}

for line in open("input.txt").read().splitlines():
    module_with_symbol, destination_modules_string = line.split(" -> ")

    if "%" in module_with_symbol or "&" in module_with_symbol:
        symbol, module = module_with_symbol[0], module_with_symbol[1:]

        modules[module] = {
            "type": symbol,
            "destinations": destination_modules_string.split(", "),
            "memory": "off" if symbol == "%" else {},
        }
    else:
        modules[module_with_symbol] = {
            "type": "broadcaster",
            "destinations": destination_modules_string.split(", "),
            "memory": "off",
        }

populate_modules_memory(modules)

modules_copy = deepcopy(modules)

product_of_low_and_high_pulses = get_product_of_low_and_high_pulses(modules)

minimal_button_presses_to_deliver_low_pulse_to_rx = (
    get_minimal_button_presses_to_deliver_low_pulse_to_rx(modules_copy)
)

print(
    f"Part 1: {product_of_low_and_high_pulses} | Part 2: {minimal_button_presses_to_deliver_low_pulse_to_rx}"
)
