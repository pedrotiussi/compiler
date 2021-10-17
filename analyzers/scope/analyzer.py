from analyzers.lexical.analyzer import *
from analyzers.scope.rules import *
from analyzers.scope.classes import *
from analyzers.scope.types import *

int_ = object(-1, None, SCALAR_TYPE_, Type(None,1))
char_ = object(-1, None, SCALAR_TYPE_, Type(None,1))
bool_ = object(-1, None, SCALAR_TYPE_, Type(None,1))
string_ = object(-1, None, SCALAR_TYPE_, Type(None,1))
universal_ = object(-1, None, SCALAR_TYPE_, Type(None,1))

global SymbolTable
SymbolTable = []
global SymbolTableLast
SymbolTableLast = []
global nCurrentLevel
nCurrentLevel = 0
global label_no
label_no = 0
global nFuncs
nFuncs = 0
global constPool
constPool = 0
global curFunction
curFunction = object()


def IS_TYPE_KIND(e_kind):
    return (e_kind == ARRAY_TYPE_ or e_kind == STRUCT_TYPE_ or e_kind == ALIAS_TYPE_ or e_kind == SCALAR_TYPE_)

def search(a_name):
    global SymbolTable
    obj = SymbolTable[nCurrentLevel]
    while obj != None:
        if obj.n_name == a_name:
            break
        else:
            obj = obj.pNext
    return obj

def find(a_name):
    global SymbolTable
    obj = None
    for i in range(nCurrentLevel+1):
        obj = SymbolTable[i]
        while obj != None:
            if obj.n_name == a_name:
                break
            else:
                obj = obj.pNext
        if obj != None:
            break
    return obj

def define(a_name):
    global SymbolTable
    global SymbolTableLast

    obj = object(a_name,None)

    try:
        SymbolTable[nCurrentLevel]
    except:
        SymbolTable.append(None)
    try:
        SymbolTableLast[nCurrentLevel]
    except:
        SymbolTableLast.append(None)

    if SymbolTable[nCurrentLevel] == None:
        SymbolTable[nCurrentLevel] = obj
        SymbolTableLast[nCurrentLevel] = obj

    else:
        aux = SymbolTable[nCurrentLevel]
        while True:
            if aux.pNext == None:
                aux.pNext = obj
                SymbolTableLast[nCurrentLevel] = obj
                break
            else:
                aux = aux.pNext
    return obj

def new_label():
    global label_no

    label_no += 1
    return label_no - 1

def new_block():
    global nCurrentLevel
    global SymbolTable
    global SymbolTableLast

    nCurrentLevel += 1
    SymbolTable.append(None)
    SymbolTableLast.append(None)
    return nCurrentLevel

def end_block():
    global nCurrentLevel
    nCurrentLevel -= 1
    return nCurrentLevel

def error(lexical, code):
    has_Err = True
    print(f"Line: {lexical.line} - ")
    if code == ERR_NO_DECL:
        print("Variable not declared")
    elif code == ERR_REDCL:
        print("Variable already declared")
    elif code == ERR_TYPE_EXPECTED:
        print("Type not declared")
    elif code == ERR_BOOL_TYPE_EXPECTED:
        print("Expected Type boolean")
    elif code == ERR_INVALID_TYPE:
        print("Invalid Type for this operation")
    elif code == ERR_TYPE_MISMATCH:
        print("Invalid Type for this operation")
    elif code == ERR_KIND_NOT_STRUCT:
        print("Only Struct Types are allowed for this operation")
    elif code == ERR_FIELD_NOT_DECL:
        print("Field not declared")
    elif code == ERR_KIND_NOT_ARRAY:
        print("Only Array Types are allowed for this operation")
    elif code == ERR_INVALID_INDEX_TYPE:
        print("Invalid Index for Array")
    elif code == ERR_KIND_NOT_VAR:
        print("Only Var Types are allowed for this operation")
    elif code == ERR_KIND_NOT_FUNCTION:
        print("Only Function Types are allowed for this operation")
    elif code == ERR_TOO_FEW_ARGS:
        print("Number of parameters less than the specified value")
    elif code == ERR_TOO_MANY_ARG:
        print("Number of parameters greater than the specified value")
    elif code == ERR_PARAM_TYPE:
        print("Invalid Specified Type")
    elif code == ERR_RETURN_TYPE_MISMATCH:
        print("Return Type not compatible with the specified function return Type")

def check_types(t1,t2):
    if t1 == t2:
        return True
    elif t1 == universal_ or t2 == universal_:
        return True
    elif t1.e_kind == UNIVERSAL_ or t2.e_kind == UNIVERSAL_:
        return True
    elif t1.e_kind == ALIAS_TYPE_ and t2.e_kind != ALIAS_TYPE_:
        return check_types(t1._.p_base_type,t2)
    elif t1.e_kind != ALIAS_TYPE_ and t2.e_kind == ALIAS_TYPE_:
        return check_types(t1,t2._.p_base_type)
    elif t1.e_kind == t2.e_kind:
        if t1.e_kind == ALIAS_TYPE_:
            return check_types(t1._.p_base_type,t2._.p_base_type)
        elif t1.e_kind == ARRAY_TYPE_:
            if t1._.n_num_elems == t2._.n_num_elems:
                return check_types(t1._.p_elem_type,t2._.p_elem_type)
        elif t1.e_kind == STRUCT_TYPE_:
            f1 = t1._.p_fields
            f2 = t2._.p_fields
            while f1 != None and f2 != None:
                if not check_types(f1._.p_type,f2._.p_type):
                    return False
            return (f1 == None and f2 == None)
    else:
        return False

