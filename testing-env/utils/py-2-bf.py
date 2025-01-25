import sys
import os  # To handle file extension manipulation

def convert_to_brainfuck(byte_script):
    brainfuck_code = []
    for byte in byte_script:
        brainfuck_code.append('+' * byte)
        brainfuck_code.append('.')
        brainfuck_code.append('[-]')
    return ''.join(brainfuck_code)

def save_brainfuck_script(brainfuck_code, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(brainfuck_code)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 python-to-brainfuck.py <input_python_file>")
        return

    input_file = sys.argv[1]
    output_file = os.path.join(os.getcwd(), os.path.splitext(input_file)[0] + ".bf")
    #output_file = os.path.splitext(input_file)[0] + ".bf"  # Automatically set output filename

    with open(input_file, "r", encoding="utf-8") as file:
        script_content = file.read()

    script_bytes = script_content.encode("utf-8")
    brainfuck_code = convert_to_brainfuck(script_bytes)

    save_brainfuck_script(brainfuck_code, output_file)
    print(f"Brainfuck script saved to {output_file}")

if __name__ == "__main__":
    main()
