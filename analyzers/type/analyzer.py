from analyzers.scope.rules import *
from analyzers.type.type_classes import *

int_ = object(-1, None, SCALAR_TYPE_, Type(None,1))
char_ = object(-1, None, SCALAR_TYPE_, Type(None,1))
bool_ = object(-1, None, SCALAR_TYPE_, Type(None,1))
string_ = object(-1, None, SCALAR_TYPE_, Type(None,1))
universal_ = object(-1, None, SCALAR_TYPE_, Type(None,1))

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