from data_structures import aliases
default_values = {
    "number": 0,
    "boolean": False,
    "string": "",
    "none": None
}

for alias, structure in aliases.items():
    default_values[alias.lower()] = structure()