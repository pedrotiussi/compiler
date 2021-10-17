class Var:
    def __init__(self, p_type = None, n_index = None, n_size = None):
        self.p_type = p_type
        self.n_index = n_index
        self.n_size = n_size

class Param:
    def __init__(self, p_type = None, n_index = None, n_size = None):
        self.p_type = p_type
        self.n_index = n_index
        self.n_size = n_size

class Field:
    def __init__(self, p_type = None, n_index = None, n_size = None):
        self.p_type = p_type
        self.n_index = n_index
        self.n_size = n_size

class Function:
    def __init__(self, p_ret_type = None, p_params = None, n_index = None, n_params = None, n_vars = None):
        self.p_ret_type = p_ret_type
        self.p_params = p_params
        self.n_index = n_index
        self.n_params = n_params
        self.n_vars = n_vars       

class Array:
    def __init__(self, p_elem_type = None, n_num_elems = None, n_size = None):
        self.p_elem_type = p_elem_type
        self.n_num_elems = n_num_elems
        self.n_size = n_size

class Struct:
    def __init__(self, p_fields = None, n_size = None):
        self.p_fields = p_fields
        self.n_size = n_size

class Alias:
    def __init__(self, p_base_type = None, n_size = None):
        self.p_base_type = p_base_type
        self.n_size = n_size

class Type:
    def __init__(self, p_base_type = None, n_size = None):
        self.p_base_type = p_base_type
        self.n_size = None

class object:
    def __init__(self, n_name = None, p_next = None, e_kind = None, _ = None):
        self.n_name = n_name
        self.pNext = p_next
        self.e_kind = e_kind
        self._ = None

class ID:
    def __init__(self, object = None, name = None):
        self.object = object
        self.name=name

class T:
    def __init__(self, type = None):
        self.type = type

class E:
    def __init__(self, type = None):
        self.type = type

class L:
    def __init__(self, type = None):
        self.type = type

class R:
    def __init__(self, type = None):
        self.type = type

class Y:
    def __init__(self, type = None):
        self.type = type

class F:
    def __init__(self, type = None):
        self.type = type

class LV:
    def __init__(self, type = None):
        self.type = type

class MC:
    def __init__(self, type = None, param = None, err = None):
        self.type = type
        self.param = param
        self.err = err

class MT:
    def __init__(self, label = None):
        self.label = label   

class ME:
    def __init__(self, label = None):
        self.label = label

class MW:
    def __init__(self, label = None):
        self.label = label

class MA:
    def __init__(self, label = None):
        self.label = label

class LE:
    def __init__(self, type = None, param = None, err = None, n = None):
        self.type = type
        self.param = param
        self.err = err
        self.n = n

class LI:
    def __init__(self, list = None):
        self.list = list

class DC:
    def __init__(self, list = None):
        self.list = list

class LP:
    def __init__(self, list = None):
        self.list = list

class TRU:
    def __init__(self, type = None):
        self.type = type
        self.val = True

class FALS:
    def __init__(self, type = None):
        self.type = type
        self.val = False

class CHR:
    def __init__(self, type = None,pos = None, val = None):
        self.type = type
        self.pos = pos
        self.val = val    

class STR:
    def __init__(self, type = None, val = None, pos = None):
        self.type = type
        self.pos = pos
        self.val = val

class NUM:
    def __init__(self, type = None, val = None, pos = None):
        self.type = type
        self.pos = pos
        self.val = val

class t_attrib:
    def __init__(self, t_nont = None, n_size = None, _ = None):
        self.t_nont = t_nont
        self.n_size = n_size
        self._ = _