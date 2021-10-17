from analyzers.lexical.analyzer import LexicalAnalyzer
from analyzers.syntatic.analyzer import SyntaticAnalyzer
import sys

def run_compiler(test_file: str):

    file = open(test_file, 'r', encoding = 'utf-8')

    lexical = LexicalAnalyzer(file)
    lexical.run()

    if lexical.lexicalError:
        file.close()
        exit()

    lexical = LexicalAnalyzer(file)
    syntatical = SyntaticAnalyzer(lexical)
    syntatical.parse()

    file.close()


if __name__ == '__main__':
    try:
        test_file = sys.argv[1]
    except:
        test_file = 'test_code.txt'

    run_compiler(test_file)