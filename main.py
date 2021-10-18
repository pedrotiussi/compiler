import sys
import os
from analyzers.lexical.lexical_analyzer import LexicalAnalyzer
from analyzers.syntatic.syntatic_analyzer import SyntaticAnalyzer


def run_compiler(input_file_path: str):

    lexical = LexicalAnalyzer(input_file_path)
    lexical.run()
    if lexical.lexicalError:
        exit()
    syntatical = SyntaticAnalyzer(lexical)
    syntatical.parse()


if __name__ == '__main__':
    try:
        test_file = sys.argv[1]
    except:
        test_file = os.path.join('input', 'test_code.txt')

    run_compiler(test_file)