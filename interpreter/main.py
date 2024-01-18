from code_entities import Code
from sys import argv
from json import loads

if __name__ == "__main__":
    code: str = ""
    if len(argv) < 1:
        raise Exception("Missing code file")
    with open(argv[1], "r") as code_file:
        code = code_file.read()
    limits_config: dict[str, int | None] = {}
    if len(argv) > 2:
        with open(argv[2], "r") as limits_file:
            if argv[2].endswith(".json"):
                limits_config = loads(limits_file.read())
            else:
                text: str = limits_file.read()
                for line in text.split("\n"):
                    if line == "":
                        continue
                    key_value = line.split(":")
                    if len(key_value) != 2:
                        raise Exception("Invalid limits syntax")
                    limits_config[key_value[0].strip()] = None if key_value[1].strip() == "null" else int(key_value[1].strip())
    Code(code, limits_config).run()
