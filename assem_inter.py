import sys
import json

class Assembler:
    def __init__(self):
        self.instructions = {
            "LOAD_CONSTANT": 13,
            "LOAD_MEMORY": 4,
            "STORE_TO_MEMORY": 2,
            "SQRT": 9
        }

    def assemble(self, source_code):
        machine_code = []
        log = []

        for line_no, line in enumerate(source_code.splitlines(), 1):
            line = line.strip()
            if not line or line.startswith(";"):  # Пропуск пустых строк и комментариев
                continue

            parts = line.split()
            command = parts[0]

            if command not in self.instructions:
                raise ValueError(f"Unknown instruction '{command}' on line {line_no}")

            opcode = self.instructions[command]
            if command == "LOAD_CONSTANT":
                if len(parts) != 3:
                    raise ValueError(f"Invalid number of arguments for command: {line}")
                _, value, address = parts
                value = int(value)
                address = int(address)

                # Проверка допустимых значений
                if not (0 <= value < (1 << 30)):
                    raise ValueError(f"Invalid value: {value}")
                if not (0 <= address < (1 << 37)):
                    raise ValueError(f"Invalid address: {address}")

                # Кодирование команды
                encoded = (opcode << 42) | (value << 7) | address
                machine_code.append(encoded)
                log.append({"line": line_no, "instruction": line, "binary": f"{encoded:012X}"})

            elif command == "LOAD_MEMORY":
                if len(parts) != 3:
                    raise ValueError(f"Invalid number of arguments for command: {line}")
                _, reg, address = parts
                reg = int(reg)
                address = int(address)

                # Проверка допустимых значений
                if not (0 <= reg < 32):
                    raise ValueError(f"Invalid register number: {reg}")
                if not (0 <= address < (1 << 42)):
                    raise ValueError(f"Invalid address: {address}")

                # Кодирование команды
                encoded = (opcode << 42) | (reg << 37) | address
                machine_code.append(encoded)
                log.append({"line": line_no, "instruction": line, "binary": f"{encoded:012X}"})

            elif command == "STORE_TO_MEMORY":
                if len(parts) != 3:
                    raise ValueError(f"Invalid number of arguments for command: {line}")
                _, reg, address = parts
                reg = int(reg)
                address = int(address)

                # Проверка допустимых значений
                if not (0 <= reg < 32):
                    raise ValueError(f"Invalid register number: {reg}")
                if not (0 <= address < (1 << 42)):
                    raise ValueError(f"Invalid address: {address}")

                # Кодирование команды
                encoded = (opcode << 42) | (reg << 37) | address
                machine_code.append(encoded)
                log.append({"line": line_no, "instruction": line, "binary": f"{encoded:012X}"})

            elif command == "SQRT":
                if len(parts) != 3:
                    raise ValueError(f"Invalid number of arguments for command: {line}")
                _, reg, address = parts
                reg = int(reg)
                address = int(address)

                # Проверка допустимых значений
                if not (0 <= reg < 32):
                    raise ValueError(f"Invalid register number: {reg}")
                if not (0 <= address < (1 << 17)):
                    raise ValueError(f"Invalid address: {address}")

                # Кодирование команды
                encoded = (opcode << 42) | (reg << 37) | address
                machine_code.append(encoded)
                log.append({"line": line_no, "instruction": line, "binary": f"{encoded:012X}"})

            else:
                raise ValueError(f"Unhandled instruction '{command}' on line {line_no}")

        return machine_code, log

class Interpretator:
    def __init__(self):
        self.registers = [0] * 32  # Регистры
        self.memory = [0] * 256  # Память (256 ячеек)
        self.log = []  # Лог выполнения команд

    def execute(self, machine_code):
        for index, instruction in enumerate(machine_code):
            opcode = (instruction >> 42) & 0xFF
            if opcode == 13:  # LOAD_CONSTANT
                value = (instruction >> 7) & 0x3FFFFFFF
                address = instruction & 0x7F
                self.registers[address] = value
                self.memory[address] = value  # Записываем значение в память
                self.log.append(f"[{index}] LOAD_CONSTANT: Loaded constant {value} into register {address} and memory[{address}].")

            elif opcode == 4:  # LOAD_MEMORY
                reg = (instruction >> 37) & 0x1F
                address = instruction & 0x3FFFFFFFFFF
                if address < 0 or address >= len(self.memory):
                    raise RuntimeError(f"LOAD_MEMORY failed: Invalid address {address}.")
                value = self.memory[address]
                self.registers[reg] = value
                self.log.append(f"[{index}] LOAD_MEMORY: Loaded value {value} from memory[{address}] into register {reg}.")

            elif opcode == 2:  # STORE_TO_MEMORY
                reg = (instruction >> 37) & 0x1F
                address = instruction & 0x3FFFFFFFFFF
                if address < 0 or address >= len(self.memory):
                    raise RuntimeError(f"STORE_TO_MEMORY failed: Invalid address {address}.")
                value = self.registers[reg]
                self.memory[address] = value
                self.log.append(f"[{index}] STORE_TO_MEMORY: Stored value {value} from register {reg} to memory[{address}].")

            elif opcode == 9:  # SQRT
                reg = (instruction >> 37) & 0x1F
                address = instruction & 0x1FFFF
                value = self.registers[reg]
                result = int(value ** 0.5)
                self.registers[reg] = result
                self.memory[address] = result  # Записываем результат в память
                self.log.append(f"[{index}] SQRT: Computed sqrt({value}) = {result} and stored in register {reg} and memory[{address}].")

            else:
                raise RuntimeError(f"Unknown opcode {opcode} at index {index}.")

    def get_memory_dump(self):
        """Возвращает содержимое памяти в виде словаря."""
        return {f"address_{i}": value for i, value in enumerate(self.memory)}

def main():
    if len(sys.argv) != 6:
        print("Usage: python script.py <input_file> <output_bin> <log_file> <result_json> <memory_range>")
        sys.exit(1)

    input_file, binary_file, log_file, result_file, memory_range = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    memory_range = int(memory_range)

    with open(input_file, "r") as f:
        source_code = f.read()

    assembler = Assembler()
    machine_code, log = assembler.assemble(source_code)

    # Запись бинарного файла
    with open(binary_file, "wb") as f:
        for instruction in machine_code:
            f.write(instruction.to_bytes(6, byteorder='big'))
    print(f"Binary file saved to {binary_file}")

    # Запись файла лога
    with open(log_file, "w") as f:
        json.dump(log, f, indent=4)
    print(f"Log file saved to {log_file}")

    # Выполнение машинного кода
    vm = Interpretator()
    try:
        vm.execute(machine_code)
        # Сохранение памяти в result.json
        memory_dump = vm.get_memory_dump()
        with open(result_file, "w") as f:
            json.dump(memory_dump, f, indent=4)
        print(f"Memory dump saved to {result_file}")

    except RuntimeError as e:
        print(f"Runtime error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
