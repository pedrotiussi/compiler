from Lexical.analyzer import Lexical_Analysis
from Syntatical.analyzer import Syntatical_Analysis
import sys

def run_compiler(test_file: str):

    file = open(test_file, 'r', encoding = 'utf-8')

    lexical = Lexical_Analysis(file)
    lexical.run()

    if lexical.lexicalError:
        file.close()
        exit()

    lexical = Lexical_Analysis(file)
    syntatical = Syntatical_Analysis(lexical)
    syntatical.parse()

    file.close()


if __name__ == '__main__':
    try:
        test_file = sys.argv[1]
    except:
        test_file = 'test_code.txt'

    run_compiler(test_file)