from Lexical.analyzer import Lexical_Analysis
from Syntatical.analyzer import Syntatical_Analysis

file = open('codigo-teste-1.ssl', 'r', encoding = 'utf-8')

lexical = Lexical_Analysis(file)
lexical.run()

if lexical.lexicalError:
    file.close()
    exit()

lexical = Lexical_Analysis(file)
syntatical = Syntatical_Analysis(lexical)
syntatical.parse()

file.close()