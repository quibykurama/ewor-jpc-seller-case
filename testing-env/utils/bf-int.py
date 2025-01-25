import sys
import os
import requests
import json
import re
import csv
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor

def run_brainfuck(brainfuck_code):
    tape = [0] * 30000
    pointer = 0
    code_pointer = 0
    output = []
    code_len = len(brainfuck_code)
    bracket_map = {}
    stack = []

    for i, command in enumerate(brainfuck_code):
        if command == '[':
            stack.append(i)
        elif command == ']':
            start = stack.pop()
            bracket_map[start] = i
            bracket_map[i] = start

    while code_pointer < code_len:
        command = brainfuck_code[code_pointer]
        if command == '>':
            pointer += 1
        elif command == '<':
            pointer -= 1
        elif command == '+':
            tape[pointer] = (tape[pointer] + 1) % 256
        elif command == '-':
            tape[pointer] = (tape[pointer] - 1) % 256
        elif command == '.':
            output.append(chr(tape[pointer]))
        elif command == ',':
            tape[pointer] = 0
        elif command == '[' and tape[pointer] == 0:
            code_pointer = bracket_map[code_pointer]
        elif command == ']' and tape[pointer] != 0:
            code_pointer = bracket_map[code_pointer]
        code_pointer += 1

    return ''.join(output)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 bf-int.py <brainfuck_file>")
        return

    input_file = sys.argv[1]

    with open(input_file, "r", encoding="utf-8") as file:
        brainfuck_code = file.read()

    decoded_script = run_brainfuck(brainfuck_code)

    # Debug: Print the decoded script
    print("\nDecoded Python Script:")
    print(decoded_script)

    # Try to execute the decoded script
    try:
        exec(
            decoded_script,
            {
                "__builtins__": __builtins__,
                "__name__": "__main__",
                "requests": requests,
                "BeautifulSoup": BeautifulSoup,
                "scrapy": scrapy,
                "CrawlerProcess": CrawlerProcess,
                "LinkExtractor": LinkExtractor,
                "pandas": pd,
                "numpy": np,
                "os": os,
                "json": json,
                "re": re,
                "csv": csv,
            },
        )
    except Exception as e:
        print(f"Error during execution: {e}")

if __name__ == "__main__":
    main()
