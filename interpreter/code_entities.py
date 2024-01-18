from typing import Any, Callable
from re import search, findall
from tools import adapt_condition, adapt_expression, __bitwise_not__, printify, replace_ignore_quotes, read_only_read_write
from data_structures import aliases, LazyArray, LazyArrayInternal, Dictionary, DictionaryInternal, CustomStructure
from default_values import default_values
from limits import limits

class Instruction:

    def __init__(self, text: str, read_only: list[dict[str, Any]] = [{}], read_write: dict[str, Any] = {}) -> None:
        self.read_only: list[dict[str, Any]] = read_only
        self.read_write: dict[str, Any] = read_write
        self.INSTRUCTIONS: dict[str, Callable[[], None]] = {
            "input": self.input,
            "output": self.output,
            "assign": self.assign,
            "create": self.create,
            "delete": self.delete,
            "run": self.run
        }
        limits.change_limit_by_name("instructions", -1)
        instruction: str = text[:text.find(" ")]
        if instruction.lower() in self.INSTRUCTIONS:
            self.instruction: str = instruction.lower()
            self.content: tuple[str, Any] = (text[text.find(" ") + 1:].strip(), "")
        elif instruction.lower() in default_values or (instruction in read_only_read_write(self.read_only, self.read_write) and callable(read_only_read_write(self.read_only, self.read_write)[instruction]) and isinstance(read_only_read_write(self.read_only, self.read_write)[instruction](), CustomStructure)):
            self.instruction: str = "create"
            self.content: tuple[str, Any] = (text, "")
        elif text.find("<-") != -1:
            self.instruction: str = "assign"
            self.content: tuple[str, Any] = (text[:text.find("<-")].strip(), text[text.find("<-") + 2:].strip())
        elif text.find("->") != -1:
            self.instruction: str = "assign"
            self.content: tuple[str, Any] = (text[text.find("->") + 2:].strip(), text[:text.find("->")].strip())
        elif text.find(":=") != -1:
            self.instruction: str = "assign"
            self.content: tuple[str, Any] = (text[:text.find(":=")].strip(), text[text.find(":=") + 2:].strip())
        elif text.find("=") != -1:
            self.instruction: str = "assign"
            self.content: tuple[str, Any] = (text[:text.find("=")].strip(), text[text.find("=") + 1:].strip())
        else:
            self.instruction: str = "run"
            self.content: tuple[str, Any] = (text.strip(), "")

    def input(self) -> None:
        text: str
        if "__stdin__" in self.read_only[0]:
            try:
                while True:
                    text = self.read_only[0]["__stdin__"].pop()
                    if text != "":
                        break
            except:
                raise Exception("Not all inputs are given")
        else:
            try:
                while True:
                    text = input()
                    if text != "":
                        break
            except:
                raise Exception("Not all inputs are given")
        text = text.strip()
        value: Any = None
        try:
            value = int(text)
        except:
            try:
                value = float(text)
            except:
                if text in ["true", "false"]:
                    value = (text == "true")
                elif text == "none":
                    value = None
                elif text[0] == "[" and text[-1] == "]":
                    value = LazyArrayInternal(text[1:-1])
                elif text[0] == "{" and text[-1] == "}":
                    value = DictionaryInternal(text[1:-1])
                else:
                    value = text
        self.content = (self.content[0], value)
        self.assign(value_not_string=True)

    def output(self) -> None:
        if "__stdout__" in self.read_only[0]:
            self.read_only[0]["__stdout__"].append(printify(self.content[0], read_only_read_write(self.read_only, self.read_write)))
        else:
            print(printify(self.content[0], read_only_read_write(self.read_only, self.read_write)))

    def assign(self, value_not_string: bool = False) -> None:
        variable_structure: Any = self.read_write
        variable_indexes: list[Any] = [self.content[0] if self.content[0].find("[") == -1 else self.content[0][:self.content[0].find("[")]]
        if self.content[0].find("[") != -1:
            bracket_diff: int = 0
            current_index: str = ""
            for i in range(self.content[0].find("["), len(self.content[0])):
                if self.content[0][i] == "[":
                    bracket_diff += 1
                if self.content[0][i] == "]":
                    bracket_diff -= 1
                    if bracket_diff == 0:
                        variable_indexes.append(current_index)
                        current_index = ""
                if (bracket_diff >= 1 and self.content[0][i] != "[") or bracket_diff > 1:
                    current_index += self.content[0][i]
            if current_index != "":
                variable_indexes.append(current_index)
        index: Any
        for i in range(0, len(variable_indexes) - 1):
            if i > 0:
                index = eval(adapt_expression(variable_indexes[i]), read_only_read_write(self.read_only, self.read_write))
            else:
                index = variable_indexes[i]
            if variable_structure[index] is None:
                try:
                    next_index: Any = eval(adapt_expression(variable_indexes[i + 1]), read_only_read_write(self.read_only, self.read_write))
                    if int(next_index) == next_index and next_index >= 0:
                        variable_structure[index] = LazyArray([])
                    else:
                        variable_structure[index] = Dictionary({})
                except:
                    variable_structure[index] = Dictionary({})
            variable_structure = variable_structure[index]
        if len(variable_indexes) > 1:
            index = eval(adapt_expression(variable_indexes[-1]), read_only_read_write(self.read_only, self.read_write))
        else:
            index = variable_indexes[-1]
        if index in variable_structure:
            limits.change_limit_by_name("variables", 1)
            limits.change_limit_by_value(variable_structure[index], 1)
        value: Any
        if value_not_string:
            value = self.content[1]
        else:
            value = eval(adapt_expression(self.content[1]), read_only_read_write(self.read_only, self.read_write))
        limits.change_limit_by_name("variables", -1)
        limits.change_limit_by_value(value, -1)
        variable_structure[index] = value

    def create(self) -> None:
        data_type: str = self.content[0][:self.content[0].find(" ")].strip()
        if self.content[0][self.content[0].find(" ") + 1:].strip() not in self.read_write:
            limits.change_limit_by_name("variables", -1)
        else:
            limits.change_limit_by_value(self.read_write[self.content[0][self.content[0].find(" ") + 1:].strip()], 1)
        if data_type.lower() in default_values:
            self.read_write[self.content[0][self.content[0].find(" ") + 1:].strip()] = default_values[data_type.lower()]
            limits.change_limit_by_value(default_values[data_type.lower()], -1)
        elif data_type in read_only_read_write(self.read_only, self.read_write) and callable(read_only_read_write(self.read_only, self.read_write)[data_type]) and isinstance(read_only_read_write(self.read_only, self.read_write)[data_type](), CustomStructure):
            self.read_write[self.content[0][self.content[0].find(" ") + 1:].strip()] = read_only_read_write(self.read_only, self.read_write)[data_type]()
            limits.change_limit_by_value(read_only_read_write(self.read_only, self.read_write)[data_type](), -1)
        else:
            raise Exception("Invalid data type")

    def delete(self) -> None:
        limits.change_limit_by_name("variables", 1)
        limits.change_limit_by_value(self.read_write[self.content[0]], 1)
        del self.read_write[self.content[0]]

    def run(self) -> None:
        eval(adapt_expression(self.content[0]), read_only_read_write(self.read_only, self.read_write))

    def execute(self) -> None:
        self.INSTRUCTIONS[self.instruction]()

    def __str__(self) -> str:
        return f"{'{'} command: {self.instruction}, content: {self.content} {'}'}"

class Condition:

    def __init__(self, conditions_text: list[str], if_blocks_text: list[str], else_block_text: str = "", read_only: list[dict[str, Any]] = [{}], read_write: dict[str, Any] = {}) -> None:
        self.read_only: list[dict[str, Any]] = read_only
        self.read_write: dict[str, Any] = read_write
        self.conditions: list[str] = [ct[ct.lower().find("if") + 2:] for ct in conditions_text]
        self.if_blocks: list[Block] = [Block(bt, self.read_only, self.read_write) for bt in if_blocks_text]
        if else_block_text != "":
            self.else_block: Block | None = Block(else_block_text, self.read_only, self.read_write)
        else:
            self.else_block: Block | None = None
        limits.change_limit_by_name("if_statements", -1)
        limits.change_limit_by_name("condition_statements", -1)

    def execute(self) -> Any | None:
        for i in range(0, len(self.conditions)):
            if eval(self.conditions[i], read_only_read_write(self.read_only, self.read_write)):
                return self.if_blocks[i].execute()
        else: 
            if self.else_block != None:
                return self.else_block.execute()

    def __str__(self) -> str:
        return f"{'{'} conditions: {self.conditions}, if_blocks: {self.if_blocks}, else_block: {self.else_block} {'}'}"

class Match:

    def __init__(self, match_text: str, cases_text: list[str], cases_blocks_text: list[str], otherwise_block_text: str = "", read_only: list[dict[str, Any]] = [{}], read_write: dict[str, Any] = {}) -> None:
        self.read_only: list[dict[str, Any]] = read_only
        self.read_write: dict[str, Any] = read_write
        self.cases: list[str] = [adapt_condition(f"({match_text[match_text.lower().find('match') + 5:]}) = ({ct[ct.lower().find('case') + 4:]})") for ct in cases_text]
        self.case_blocks: list[Block] = [Block(bt, self.read_only, self.read_write) for bt in cases_blocks_text]
        if otherwise_block_text != "":
            self.otherwise_block: Block | None = Block(otherwise_block_text, self.read_only, self.read_write)
        else:
            self.otherwise_block: Block | None = None
        limits.change_limit_by_name("match_statements", -1)
        limits.change_limit_by_name("condition_statements", -1)

    def execute(self) -> Any | None:
        for i in range(0, len(self.cases)):
            if eval(self.cases[i], read_only_read_write(self.read_only, self.read_write)):
                return self.case_blocks[i + 1].execute()
        else: 
            if self.otherwise_block != None:
                return self.otherwise_block.execute()

    def __str__(self) -> str:
        return f"{'{'} cases: {self.cases}, case_blocks: {self.case_blocks}, otherwise_block: {self.otherwise_block} {'}'}"

class Loop:

    def __init__(self, condition: str, block: str, read_only: list[dict[str, Any]] = [{}], read_write: dict[str, Any] = {}) -> None:
        self.read_only: list[dict[str, Any]] = read_only
        self.read_write: dict[str, Any] = read_write
        limits.change_limit_by_name("loop_statements", -1)
        if "while" in condition.lower():
            limits.change_limit_by_name("while_loop_statements", -1)
            self.type: str = "while"
            self.condition: str = condition[condition.lower().find("while") + 5:]
        elif "until" in condition.lower():
            limits.change_limit_by_name("until_loop_statements", -1)
            self.type: str = "until"
            self.condition: str = condition[condition.lower().find("until") + 5:]
        elif "from" in condition.lower() and "to" in condition.lower():
            limits.change_limit_by_name("for_loop_statements", -1)
            self.type = "for"
            self.start_instruction: Instruction = Instruction(f"{condition[condition.lower().find('loop') + 4:condition.lower().find('to')]}".replace("from", "="), self.read_only, self.read_write)
            self.iter_instruction: Instruction = Instruction(f"{condition[condition.lower().find('loop') + 4:condition.lower().find('from') - 1]} = {condition[condition.lower().find('loop') + 4:condition.lower().find('from') - 1]} + 1", self.read_only, self.read_write)
            self.end_instruction: Instruction = Instruction(f"delete {condition[condition.lower().find('loop') + 4:condition.lower().find('from') - 1]}", self.read_only, self.read_write)
            self.condition: str = f"{condition[condition.lower().find('loop') + 4:condition.lower().find('from')]} <= {condition[condition.lower().find('to') + 2:]}"
        else:
            limits.change_limit_by_name("while_loop_statements", -1)
            self.type: str = "while"
            self.condition: str = condition[condition.lower().find("loop") + 4:]
        self.block: Block = Block(block, self.read_only, self.read_write)

    def execute(self) -> None:
        if self.type == "while":
            while eval(self.condition, read_only_read_write(self.read_only, self.read_write)):
                try:
                    self.block.execute()
                except Exception as exc:
                    if str(exc) == "Unexpected break":
                        break
                    elif str(exc) != "Unexpected continue":
                        raise Exception(str(exc))
        elif self.type == "until":
            while not eval(self.condition, read_only_read_write(self.read_only, self.read_write)):
                try:
                    self.block.execute()
                except Exception as exc:
                    if str(exc) == "Unexpected break":
                        break
                    elif str(exc) != "Unexpected continue":
                        raise Exception(str(exc))
        elif self.type == "for":
            self.start_instruction.execute()
            while eval(self.condition, read_only_read_write(self.read_only, self.read_write)):
                try:
                    self.block.execute()
                except Exception as exc:
                    if str(exc) == "Unexpected break":
                        break
                    elif str(exc) != "Unexpected continue":
                        raise Exception(str(exc))
                self.iter_instruction.execute()
            self.end_instruction.execute()

    def __str__(self) -> str:
        if self.type == "for":
            return f"{'{'} type: {self.type} condition: {self.condition}, start_instruction: {self.start_instruction}, iter_instruction: {self.iter_instruction}, end_instruction: {self.end_instruction} block: {self.block} {'}'}"
        else:
            return f"{'{'} type: {self.type} condition: {self.condition}, block: {self.block} {'}'}"

class Function:

    def __init__(self, statement: str, block_text: str, read_only: list[dict[str, Any]] = [{}]) -> None:
        self.read_only: list[dict[str, Any]] = read_only
        statement_list: list[str] = findall(r"(\w+)", statement)
        self.name: str = statement_list[1]
        self.arguments: list[str] = statement_list[2:]
        self.block_text: str = block_text
        limits.change_limit_by_name("functions", -1)
        limits.change_limit_by_name("functions_and_procedures", -1)

    def execute(self, *args: list[Any]) -> Any | None:
        return Block(self.block_text, self.read_only, dict(zip(self.arguments, args))).execute()

class Procedure(Function):

    def __init__(self, statement: str, block_text: str, read_only: list[dict[str, Any]] = [{}]) -> None:
        super().__init__(statement, block_text, read_only)
        limits.change_limit_by_name("functions", 1)
        limits.change_limit_by_name("procedures", -1)

    def execute(self, *args: list[Any]) -> None:
        Block(self.block_text, self.read_only, dict(zip(self.arguments, args))).execute()

class Structure:

    def __init__(self, name: str, block: list[str], read_only: list[dict[str, Any]] = [{}], read_write: dict[str, Any] = {}) -> None:
        self.name: str = name
        self.block: list[block] = block
        self.read_only: list[dict[str, Any]] = read_only
        self.read_write: dict[str, Any] = read_write
        self.read_write[name] = lambda *args: CustomStructure([], [], *args)
        limits.change_limit_by_name("custom_structure_definitions", -1)
        
    def execute(self) -> None:
        attr_names: list[str] = []
        attr_values: list[Any] = []
        for line in self.block:
            data_type: str = line[:line.find(" ")]
            if line.find("<-") != -1:
                attr_names.append(line[:line.find("<-")].strip())
                attr_values.append(eval(adapt_expression(line[line.find("<-") + 2:].strip()), read_only_read_write(self.read_only, self.read_write)))
            elif line.find("->") != -1:
                attr_names.append(line[line.find("->") + 2:].strip())
                attr_values.append(eval(adapt_expression(line[:line.find("->")].strip()), read_only_read_write(self.read_only, self.read_write)))
            elif line.find(":=") != -1:
                attr_names.append(line[:line.find(":=")].strip())
                attr_values.append(eval(adapt_expression(line[line.find(":=") + 2:].strip()), read_only_read_write(self.read_only, self.read_write)))
            elif line.find("=") != -1:
                attr_names.append(line[:line.find("=")].strip())
                attr_values.append(eval(adapt_expression(line[line.find("=") + 1:].strip()), read_only_read_write(self.read_only, self.read_write)))
            elif data_type.lower() in default_values or (data_type in read_only_read_write(self.read_only, self.read_write) and callable(read_only_read_write(self.read_only, self.read_write)[data_type]) and isinstance(read_only_read_write(self.read_only, self.read_write)[data_type](), CustomStructure)):
                attr_names.append(line[line.find(" ") + 1:].strip())
                attr_values.append(default_values[data_type.lower()] if data_type.lower() in default_values else read_only_read_write(self.read_only, self.read_write)[data_type]())
            else:
                attr_names.append(line)
                attr_values.append(None)
        self.read_write[self.name] = lambda *args: CustomStructure(attr_names, attr_values, *args)

class Block:

    def __init__(self, text: str, read_only: list[dict[str, Any]] = [{}], read_write: dict[str, Any] = {}) -> None:
        self.read_only: list[dict[str, Any]] = read_only
        self.read_write: dict[str, Any] = read_write
        self.code: list[Instruction | Condition | Match | Loop] = []
        current_if_case_block: list[str] = []
        current_else_otherwise_block: list[str] = []
        if_case_conditions: list[str] = []
        if_case_blocks: list[str] = []
        current_statement: str = ""
        current_block: list[str] = []
        state: str = ""
        state_difference: int = 0
        text = text.replace("\r", "")
        text = replace_ignore_quotes(r"[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+then[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*\n", "\n", text)
        text = replace_ignore_quotes(r"[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+with[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*\n", "\n", text)
        text = replace_ignore_quotes(r"loop[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+for[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", "loop ", text)
        text = replace_ignore_quotes(r"//.*\n", "\n", text)
        counter: int = 0
        lines: list[str] = text.split("\n")
        line: str
        for line in lines:
            if search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*//", line.strip()):
                continue
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*end structure[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()) and state == "structure":
                self.code.append(Structure(current_statement, current_block, self.read_only, self.read_write))
                current_statement = ""
                current_block = []
                state = ""
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*structure[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", line.lower()) and state == "":
                state = "structure"
                current_statement = line[line.find("structure") + 9:].strip()
            elif state == "structure":
                current_block.append(line.strip())
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*end procedure[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()) and state == "procedure" and state_difference == 0:
                self.read_write[findall(r"(\w+)", current_statement)[1]] = Procedure(current_statement, "\n".join(current_block), self.read_only + [self.read_write]).execute
                current_statement = ""
                current_block = []
                state = ""
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*procedure[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", line.lower()) and state == "":
                state = "procedure"
                current_statement = adapt_condition(line)
            elif state == "procedure":
                if search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*end procedure[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()):
                    state_difference -= 1
                elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*procedure[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", line.lower()):
                    state_difference += 1
                current_block.append(line)
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*end function[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()) and state == "function" and state_difference == 0:
                self.read_write[findall(r"(\w+)", current_statement)[1]] = Function(current_statement, "\n".join(current_block), self.read_only + [self.read_write]).execute
                current_statement = ""
                current_block = []
                state = ""
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*function[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", line.lower()) and state == "":
                state = "function"
                current_statement = adapt_condition(line)
            elif state == "function":
                if search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*end function[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()):
                    state_difference -= 1
                elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*function[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", line.lower()):
                    state_difference += 1
                current_block.append(line)
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*end loop[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()) and state == "loop" and state_difference == 0:
                self.code.append(Loop(current_statement, "\n".join(current_block), self.read_only, self.read_write))
                current_statement = ""
                current_block = []
                state = ""
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*loop[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", line.lower()) and state == "":
                state = "loop"
                current_statement = adapt_condition(line)
            elif state == "loop":
                if search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*end loop[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()):
                    state_difference -= 1
                elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*loop[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", line.lower()):
                    state_difference += 1
                current_block.append(line)
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*end if[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()) and (state == "if" or state == "else") and state_difference == 0:
                if_case_blocks.append("\n".join(current_if_case_block))
                self.code.append(Condition(if_case_conditions, if_case_blocks, "\n".join(current_else_otherwise_block), self.read_only, self.read_write))
                if_case_conditions = []
                current_if_case_block = []
                current_else_otherwise_block = []
                if_case_blocks = []
                state = ""
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*else if[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", line.lower()) and (state == "if" or state == "else") and state_difference == 0:
                if state == "if":
                    if_case_blocks.append("\n".join(current_if_case_block))
                state = "if"
                current_if_case_block = []
                if_case_conditions.append(adapt_condition(line))
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*else[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()) and state == "if" and state_difference == 0:
                state = "else"
                if_case_blocks.append("\n".join(current_if_case_block))
                current_if_case_block = []
            elif state == "else":
                if search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*end if[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()):
                    state_difference -= 1
                elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*else[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()):
                    state_difference += 1
                current_else_otherwise_block.append(line)
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*if[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", line.lower()) and state == "":
                state = "if"
                if_case_conditions.append(adapt_condition(line))
            elif state == "if":
                if search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*end if[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()):
                    state_difference -= 1
                elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*if[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", line.lower()):
                    state_difference += 1
                current_if_case_block.append(line)
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*end match[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()) and (state == "case" or state == "otherwise") and state_difference == 0:
                if_case_blocks.append("\n".join(current_if_case_block))
                self.code.append(Match(current_statement, if_case_conditions, if_case_blocks, "\n".join(current_else_otherwise_block), self.read_only, self.read_write))
                if_case_conditions = []
                current_if_case_block = []
                current_else_otherwise_block = []
                if_case_blocks = []
                current_statement = ""
                state = ""
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*case[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", line.lower()) and (state == "case" or state == "otherwise") and state_difference == 0:
                if state == "case":
                    if_case_blocks.append("\n".join(current_if_case_block))
                state = "case"
                current_if_case_block = []
                if_case_conditions.append(line)
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*otherwise[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()) and state == "case" and state_difference == 0:
                state = "otherwise"
                if_case_blocks.append("\n".join(current_if_case_block))
                current_if_case_block = []
            elif state == "otherwise":
                if search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*end match[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()):
                    state_difference -= 1
                elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*otherwise[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()):
                    state_difference += 1
                current_else_otherwise_block.append(line)
            elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*match[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", line.lower()) and state == "":
                state = "case"
                current_statement = line
            elif state == "case":
                if search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*end match[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*$", line.lower()):
                    state_difference -= 1
                elif search(r"^[^a-zA-Z0-9\[\]{}()+\-*/_\"\']*case[^a-zA-Z0-9\[\]{}()+\-*/_\"\']+", line.lower()):
                    state_difference += 1
                current_if_case_block.append(line)
            elif line.strip() != "":
                self.code.append(Instruction(line.strip(), self.read_only, self.read_write))
            counter += 1
        if state != "":
            raise Exception(f"Some end {state if state != 'else' else 'if'} is missed")

    def execute(self) -> Any | None:
        for entity in self.code:
            if isinstance(entity, Instruction) and entity.content[0].lower() == "continue":
                raise Exception("Unexpected continue")
            elif isinstance(entity, Instruction) and entity.content[0].lower() == "break":
                raise Exception("Unexpected break")
            elif isinstance(entity, Instruction) and entity.content[0].lower() == "return":
                return None
            elif isinstance(entity, Instruction) and "return" in entity.content[0].lower():
                return eval(adapt_expression(entity.content[0][entity.content[0].lower().find("return") + 6:]), read_only_read_write(self.read_only, self.read_write))
            res: Any | None = entity.execute()
            if res is not None:
                return res

    def __str__(self) -> str:
        return f"{'{'} code: {self.code} {'}'}"

class Code:

    def __init__(self, code: str, limits_config: dict[str, int | None] = {}) -> None:
        limits.apply_config(limits_config)
        self.global_vars: dict[str, Any] = {
            "bitwise_not": __bitwise_not__,
        }
        self.global_vars.update(aliases)
        self.parsing_err: str = ""
        try:
            self.global_block: Block = Block(code, [self.global_vars], {})
        except Exception as exc:
            self.parsing_err = str(exc).replace(" (<string>, line 1)", "")

    def run(self) -> None:
        if self.parsing_err == "":
            try:
                self.global_block.execute()
            except Exception as exc:
                print(str(exc).replace(" (<string>, line 1)", ""))
        else:
            print(self.parsing_err)
    
    def __str__(self) -> str:
        return f"{'{'} global_vars: {self.global_vars}, global_blocks: {self.global_block} {'}'}"

class CodeInternal:

    def __init__(self, code: str, stdin: str, limits_config: dict[str, int | None]) -> None:
        limits.apply_config(limits_config)
        self.global_vars: dict[str, Any] = {
            "bitwise_not": __bitwise_not__,
            "__stdin__": stdin.replace("\r", "").split("\n")[::-1],
            "__stdout__": []
        }
        self.global_vars.update(aliases)
        self.parsing_err: str = ""
        try:
            self.global_block: Block = Block(code, [self.global_vars], {})
        except Exception as exc:
            self.parsing_err = str(exc).replace(" (<string>, line 1)", "")

    def run(self) -> str:
        if self.parsing_err == "":
            try:
                self.global_block.execute()
                return "\n".join(self.global_vars["__stdout__"])
            except Exception as exc:
                return str(exc).replace(" (<string>, line 1)", "")
        else:
            return self.parsing_err
    
    def __str__(self) -> str:
        return f"{'{'} global_vars: {self.global_vars}, global_blocks: {self.global_block} {'}'}"