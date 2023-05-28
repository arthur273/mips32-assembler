def create_file(file_path, file_contents):
    try:
        with open(file_path, 'w') as file:
            file.write(file_contents)
        return True
    except IOError:
        return False

path = "/text.mif"

def main():
    file_path = input("Enter the path to the file: ")

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"File not found: {file_path}")

    asm = assembler(64, instructions, registers, pseudoinstructions, layouts, 4)
    asm.first_pass(lines)
    asm.second_pass(lines)
    asm.machine_code()
    
    contents = ''
    for item in asm.final:
        contents += item + '\n'
    path = 'text.mif'
    input("Press to save files")
    if create_file(path, contents):
        print("File created successfully.")
    else:
        print("Error creating the file.")

main()


