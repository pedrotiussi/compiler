from analyzers.syntatic.states import *
from analyzers.scope.analyzer import *
from analyzers.scope.rules import *
from analyzers.type.type_classes import *
from analyzers.type.constants import *
from analyzers.semantic.global_variables import *


class SemanticAnalyzer():

    def __init__(self, lexical, rule, output_path):
        self.lexical = lexical
        self.rule = rule
        self.output_path = output_path
        self.generated_code = open(self.output_path, "a+")
        self.p = None

    def analyze(self):
        global t,f
        global IDD_,IDU_,ID_,T_,LI_,LI0_,LI1_,TRU_,FALS_,STR_,CHR_,NUM_,DC_,DC0_,DC1_,LP_,LP0_,LP1_,E_,E0_,E1_,L_,L0_,L1_,R_,R0_,R1_,Y_,Y0_,Y1_,F_,F0_,F1_,LV_,LV0_,LV1_,MC_,LE_,LE0_,LE1_,MT_,ME_,MW_
        global nFuncs
        global curFunction
        global constPool
        global SymbolTable
        
        global name
        global n
        global rLabel
        global hasErr 
        global semantic_stack 

        if self.rule == IDD_RULE:
            name = self.lexical.secondary_Token
            try:
                self.p= search(name)
            except:
                pass
            if self.p!= None:
                Error(self.lexical, ERR_REDCL)
            else:
                self.p= define(name)
            self.p.e_kind = NO_KIND_DEF_
            IDD_.t_nont = IDD
            IDD_._ = ID(self.p,name)
            semantic_stack.append(IDD_)

        elif self.rule == IDU_RULE:
            name = self.lexical.secondary_Token
            self.p= find(name)
            if self.p== None:
                Error(self.lexical, ERR_NO_DECL)
                self.p= define(name)
            IDU_.t_nont = IDU
            IDU_._ = ID(self.p,name)
            semantic_stack.append(IDU_)

        elif self.rule == ID_RULE:
            name = self.lexical.secondary_Token
            ID_.t_nont=ID
            ID_._=ID(None,name)
            semantic_stack.append(ID_)

        elif self.rule == T_IDU_RULE:
            IDU_ = semantic_stack.pop()
            self.p= IDU_._.object
            if IS_TYPE_KIND(self.p.e_kind) or self.p.e_kind==UNIVERSAL_:
                T_ = t_attrib(T,self.p._.n_size,T(self.p))
            else:
                T_ = t_attrib(T,0,T(universal_))
                Error(self.lexical, ERR_TYPE_EXPECTED)
            semantic_stack.append(T_)

        elif self.rule == T_INTEGER_RULE:
            T_ = t_attrib(T,1,T(int_))
            semantic_stack.append(T_)

        elif self.rule == T_CHAR_RULE:
            T_ = t_attrib(T,1,T(char_))
            semantic_stack.append(T_)

        elif self.rule == T_BOOL_RULE:
            T_ = t_attrib(T,1,T(bool_))
            semantic_stack.append(T_)

        elif self.rule == T_STRING_RULE:
            T_ = t_attrib(T,1,T(string_))
            semantic_stack.append(T_)

        elif self.rule == LI_IDD_RULE:
            IDD_ = semantic_stack.pop()
            LI_ = t_attrib(LI,None,LI(IDD_._.object))
            semantic_stack.append(LI_)
        
        elif self.rule == LI_COMMA_RULE:
            IDD_ = semantic_stack.pop()
            LI1_ = semantic_stack.pop()
            LI0_ = t_attrib(LI,None,LI(LI1_._.list))
            semantic_stack.append(LI0_)
        
        elif self.rule == DV_VAR_RULE:
            T_ = semantic_stack.pop()
            t = T_._.type
            LI_ = semantic_stack.pop()
            self.p= LI_._.list
            n = curFunction._.n_vars
            while self.p!= None and self.p.e_kind == NO_KIND_DEF_:
                self.p.e_kind = VAR_
                self.p._ = Var(t,n,T_.n_size)
                n+=T_.n_size
                self.p= self.p.pNext
            curFunction._.n_vars=n

        elif self.rule == TRUE_RULE:
            TRU_ = t_attrib(TRU, None, TRU(bool_))
            semantic_stack.append(TRU_)

        elif self.rule == FALSE_RULE:
            FALS_ = t_attrib(FALS,None,FALS(bool_))
            semantic_stack.append(FALS_)

        elif self.rule == CHR_RULE:
            CHR_ = t_attrib(CHR,None,CHR(char_, self.lexical.get_cte(self.lexical.secondary_token)))
            semantic_stack.append(CHR_)
        
        elif self.rule == STR_RULE:
            STR_ = t_attrib(STR,None,STR(string_, self.lexical.get_cte(self.lexical.secondary_Token), self.lexical.secondary_token))
            semantic_stack.append(STR_)
        
        elif self.rule == NUM_RULE:
            NUM_ = t_attrib(NUM,None,NUM(int_, self.lexical.get_cte(self.lexical.secondary_Token), self.lexical.secondary_Token))
            semantic_stack.append(NUM_)

        elif self.rule == DT_ARRAY_RULE:
            T_ = semantic_stack.pop()
            NUM_ = semantic_stack.pop()
            IDD_ = semantic_stack.pop()
            self.p= IDD_._.object
            n = NUM_._.val
            t = T_._.type
            self.p.e_kind = ARRAY_TYPE_
            self.p._ = Array(t,n,n*T_.n_size)

        elif self.rule == DT_ALIAS_RULE:
            T_ = semantic_stack.pop()
            IDD_ = semantic_stack.pop()
            self.p= IDD_._.object
            t = T_._.type
            self.p.e_kind = ALIAS_TYPE_
            self.p._ = Alias(t,T_.n_size)

        elif self.rule == DC_LI_RULE:
            T_ = semantic_stack.pop()
            LI_ = semantic_stack.pop()
            self.p= LI_._.list
            t = T_._.type
            n = 0
            while self.p!= None and self.p.e_kind == NO_KIND_DEF_:
                self.p.e_kind = FIELD_
                self.p._ = Field(t,n,T_.n_size)
                n = n+T_.n_size
                self.p= self.p.pNext
            DC_ = t_attrib(DC,n,DC(LI_._.list))
            semantic_stack.append(DC_)
        
        elif self.rule == DC_DC_RULE:
            T_ = semantic_stack.pop()
            LI_ = semantic_stack.pop()
            DC1_ = semantic_stack.pop()
            self.p= LI_._.list
            t = T_._.type
            n = DC1_.n_size
            while self.p!= None and self.p.e_kind == NO_KIND_DEF_:
                self.p.e_kind = FIELD_
                self.p._ = Field(t,n,T_.n_size)
                n = n+T_.n_size
                self.p= self.p.pNext
            DC0_ = t_attrib(DC,n,DC(DC1_._.list))
            semantic_stack.append(DC0_)
        
        elif self.rule == NB_RULE:
            NewBlock()

        elif self.rule == DT_STRUCT_RULE:
            DC_ = semantic_stack.pop()
            IDD_ = semantic_stack.pop()
            self.p= IDD_._.object
            self.p.e_kind = STRUCT_TYPE_
            self.p._ = Struct(DC_._.list,DC_.n_size)
            EndBlock()

        elif self.rule == LP_IDD_RULE:
            T_ = semantic_stack.pop()
            IDD_ = semantic_stack.pop()
            self.p= IDD_._.object
            self.p.e_kind = PARAM_
            self.p._ = Param(t,0,T_.n_size)
            LP_ = t_attrib(LP,T_.n_size,LP(self.p))
            semantic_stack.append(LP_)
        
        elif self.rule == LP_LP_RULE:
            T_ = semantic_stack.pop()
            IDD_ = semantic_stack.pop()
            LP1_ = semantic_stack.pop()
            self.p = IDD_._.object
            t = T_._.type
            n = LP1_.n_size
            self.p.e_kind = PARAM_
            self.p._ = Param(t,n,T_.n_size)
            LP0_ = t_attrib(LP,n+T_.n_size,LP(LP1_._.list))
        
        elif self.rule == NF_RULE:
            IDD_ = semantic_stack[-1]
            f = IDD_._.object
            f.e_kind = FUNCTION_
            f._ = Function(None,None,nFuncs,0,0)
            nFuncs+=1
            NewBlock()

        elif self.rule == MF_RULE:
            T_ = semantic_stack.pop()
            LP_ = semantic_stack.pop()
            IDD_ = semantic_stack.pop()
            f = IDD_._.object
            f.e_kind = FUNCTION_
            f._ = Function(T_._.type,LP_._.list,f._.n_index,LP_.n_size,LP_.n_size)
            curFunction = f
            self.generated_code.write(f"BEGIN_FUNC {f._.n_index} {f._.n_params}\n")

        elif self.rule == DF_RULE:
            EndBlock()
            self.generated_code.write("END_FUNC\n")

        elif self.rule == U_IF_RULE:
            MT_ = semantic_stack.pop()
            E_ = semantic_stack.pop()
            t = E_._.type
            if not CheckTypes(t,bool_):
                Error(self.lexical, ERR_BOOL_TYPE_EXPECTED)
                self.generated_code.write(f"L{MT_._.label}\n")
            
        elif self.rule == U_IF_ELSE_U_RULE:
            ME_ = semantic_stack.pop()
            MT_ = semantic_stack.pop()
            E_ = semantic_stack.pop()
            t = E_._.type
            if not CheckTypes(t,bool_):
                Error(self.lexical, ERR_BOOL_TYPE_EXPECTED)
            self.generated_code.write(f"L{ME_._.label}\n")

        elif self.rule == M_IF_ELSE_M_RULE:
            ME_ = semantic_stack.pop()
            MT_ = semantic_stack.pop()
            E_ = semantic_stack.pop()
            t = E_._.type
            if not CheckTypes(t,bool_):
                Error(self.lexical, ERR_BOOL_TYPE_EXPECTED)
            self.generated_code.write(f"L{ME_._.label}\n")

        elif self.rule == M_WHILE_RULE:
            MT_ = semantic_stack.pop()
            E_ = semantic_stack.pop()
            MW_ = semantic_stack.pop()
            t = E_._.type
            if not CheckTypes(t,bool_):
                Error(self.lexical, ERR_BOOL_TYPE_EXPECTED)
            self.generated_code.write(f"\tJMP_BW L'0'\nL{MT_._.label}n")        

        elif self.rule == M_DO_WHILE_RULE:
            E_ = semantic_stack.pop()
            MW_ = semantic_stack.pop()
            t = E_._.type
            if not CheckTypes(t,bool_):
                Error(self.lexical, ERR_BOOL_TYPE_EXPECTED)
            self.generated_code.write(f"\tNOT\n\tTJMP_BW L{MW_._.label}\n")  

        elif self.rule == E_AND_RULE:
            L_ = semantic_stack.pop()
            E1_ = semantic_stack.pop()
            if not CheckTypes(E1_._.type,bool_):
                Error(self.lexical, ERR_BOOL_TYPE_EXPECTED)
            if not CheckTypes(L_._.type,bool_):
                Error(self.lexical, ERR_BOOL_TYPE_EXPECTED)
            E0_ = t_attrib(E,None,E(bool_))
            semantic_stack.append(E0_)
            self.generated_code.write(f"\tAND\n")
        
        elif self.rule == E_OR_RULE:
            L_ = semantic_stack.pop()
            E1_ = semantic_stack.pop()
            if not CheckTypes(E1_._.type,bool_):
                Error(self.lexical, ERR_BOOL_TYPE_EXPECTED)
            if not CheckTypes(L_._.type,bool_):
                Error(self.lexical, ERR_BOOL_TYPE_EXPECTED)
            E0_ = t_attrib(E,None,E(bool_))
            semantic_stack.append(E0_)
            self.generated_code.write(f"\tOR\n")

        elif self.rule == E_L_RULE:
            L_ = semantic_stack.pop()
            E_ = t_attrib(E,None,E(L_._.type))
            semantic_stack.append(E_)
        
        elif self.rule == L_LESS_THAN_RULE:
            R_ = semantic_stack.pop()
            L1_ = semantic_stack.pop()
            if not CheckTypes(L1_._.type,R_._.type):
                Error(self.lexical, ERR_TYPE_MISMATCH)
            L0_ = t_attrib(L,None,L(bool_))
            semantic_stack.append(L0_)
            self.generated_code.write(f"\tLT\n")

        elif self.rule == L_GREATER_THAN_RULE:
            R_ = semantic_stack.pop()
            L1_ = semantic_stack.pop()
            if not CheckTypes(L1_._.type,R_._.type):
                Error(self.lexical, ERR_TYPE_MISMATCH)
            L0_ = t_attrib(L,None,bool_)
            semantic_stack.append(L0_)
            self.generated_code.write(f"\tGT\n")

        elif self.rule == L_LESS_EQUAL_RULE:
            R_ = semantic_stack.pop()
            L1_ = semantic_stack.pop()
            if not CheckTypes(L1_._.type,R_._.type):
                Error(self.lexical, ERR_TYPE_MISMATCH)
            L0_ = t_attrib(L,None,bool_)
            semantic_stack.append(L0_)
            self.generated_code.write(f"\tLE\n")

        elif self.rule == L_GREATER_EQUAL_RULE:
            R_ = semantic_stack.pop()
            L1_ = semantic_stack.pop()
            if not CheckTypes(L1_._.type,R_._.type):
                Error(self.lexical, ERR_TYPE_MISMATCH)
            L0_ = t_attrib(L,None,bool_)
            semantic_stack.append(L0_)
            self.generated_code.write(f"\tGE\n")

        elif self.rule == L_EQUAL_EQUAL_RULE:
            R_ = semantic_stack.pop()
            L1_ = semantic_stack.pop()
            if not CheckTypes(L1_._.type,R_._.type):
                Error(self.lexical, ERR_TYPE_MISMATCH)
            L0_ = t_attrib(L,None,bool_)
            semantic_stack.append(L0_)
            self.generated_code.write("\tEQ\n")

        elif self.rule == L_NOT_EQUAL_RULE:
            R_ = semantic_stack.pop()
            L1_ = semantic_stack.pop()
            if not CheckTypes(L1_._.type,R_._.type):
                Error(self.lexical, ERR_TYPE_MISMATCH)
            L0_ = t_attrib(L,None,bool_)
            semantic_stack.append(L0_)
            self.generated_code.write("\tNE\n")

        elif self.rule == L_R_RULE:
            R_ = semantic_stack.pop()
            L_ = t_attrib(L,None,L(R_._.type))
            semantic_stack.append(L_)
        
        elif self.rule == R_PLUS_RULE:
            Y_ = semantic_stack.pop()
            R1_ = semantic_stack.pop()
            if not CheckTypes(R1_._.type,Y_._.type):
                Error(self.lexical, ERR_TYPE_MISMATCH)
            if not CheckTypes(R1_._.type,int_) and not CheckTypes(R1_._.type,string_):
                Error(self.lexical, ERR_INVALID_TYPE)
            R0_ = t_attrib(R,None,R(R1_._.type))
            semantic_stack.append(R0_)
            self.generated_code.write("\tADD\n")

        elif self.rule == R_MINUS_RULE:
            Y_ = semantic_stack.pop()
            R1_ = semantic_stack.pop()
            if not CheckTypes(R1_._.type,Y_._.type):
                Error(self.lexical, ERR_TYPE_MISMATCH)
            if not CheckTypes(R1_._.type,int_):
                Error(self.lexical, ERR_INVALID_TYPE)
            R0_ = t_attrib(R,None,R(R1_._.type))
            semantic_stack.append(R0_)
            self.generated_code.write("\tSUB\n")

        elif self.rule == R_Y_RULE:
            Y_ = semantic_stack.pop()
            R_ = t_attrib(R,None,R(Y_._.type))
            semantic_stack.append(R_)
        
        elif self.rule == Y_TIMES_RULE:
            F_ = semantic_stack.pop()
            Y1_ = semantic_stack.pop()
            if not CheckTypes(Y1_._.type,F_._.type):
                Error(self.lexical, ERR_TYPE_MISMATCH)
            if not CheckTypes(Y1_._.type,int_):
                Error(self.lexical, ERR_INVALID_TYPE)
            Y0_ = t_attrib(Y,None,Y(Y1_._.type))
            semantic_stack.append(Y0_)
            self.generated_code.write("\tMUL\n")

        elif self.rule == Y_DIVIDE_RULE:
            F_ = semantic_stack.pop()
            Y1_ = semantic_stack.pop()
            if not CheckTypes(Y1_._.type,F_._.type):
                Error(self.lexical, ERR_TYPE_MISMATCH)
            if not CheckTypes(Y1_._.type,int_):
                Error(self.lexical, ERR_INVALID_TYPE)
            Y0_ = t_attrib(Y,None,Y(Y1_._.type))
            semantic_stack.append(Y0_)
            self.generated_code.write("\tDIV\n")

        elif self.rule == Y_F_RULE:
            F_ = semantic_stack.pop()
            Y_ = t_attrib(Y,None,Y(F_._.type))
            semantic_stack.append(Y_)
        
        elif self.rule == F_LV_RULE:
            LV_ = semantic_stack.pop()
            n = 0
            F_ = t_attrib(F,None,F(LV_._.type))
            semantic_stack.append(F_)
            self.generated_code.write(f"\tDE_REF {n}\n")
        
        elif self.rule == F_LEFT_PLUS_PLUS_RULE:
            LV_ = semantic_stack.pop()
            t = LV_._.type
            if not CheckTypes(t,int_):
                Error(self.lexical, ERR_INVALID_TYPE)
            F_ = t_attrib(F,None,F(int_))
            self.generated_code.write(f"\tDUP\n\tDUP\n\tDE_REF 1\n")
            self.generated_code.write(f"\tINC\n\tSTORE REF 1\n\tDE_REF 1\n")

        elif self.rule == F_LEFT_MINUS_MINUS_RULE:
            LV_ = semantic_stack.pop()
            t = LV_._.type
            if not CheckTypes(t,int_):
                Error(self.lexical, ERR_INVALID_TYPE)
            F_ = t_attrib(F,None,F(LV_._.type))
            semantic_stack.append(F_)
            self.generated_code.write(f"\tDUP\n\tDUP\n\tDE_REF 1\n")
            self.generated_code.write(f"\tDEC\n\tSTORE_REF 1\n\tDE_REF 1\n")

        elif self.rule ==F_RIGHT_PLUS_PLUS_RULE:
            LV_ = semantic_stack.pop()
            t = LV_._.type
            if not CheckTypes(t,int_):
                Error(self.lexical, ERR_INVALID_TYPE)
            F_ = t_attrib(F,None,F(LV_._.type))
            semantic_stack.append(F_)
            self.generated_code.write(f"\tDUP\n\tDUP\n\tDE_REF 1\n")
            self.generated_code.write(f"\tINC\n\tSTORE_REF 1\n\tDE_REF 1\n")
            self.generated_code.write(f"\tDEC\n")

        elif self.rule == F_RIGHT_MINUS_MINUS_RULE:
            LV_ = semantic_stack.pop()
            t = LV_._.type
            if not CheckTypes(t,int_):
                Error(self.lexical, ERR_INVALID_TYPE)
            F_ = t_attrib(F,None,F(t))
            semantic_stack.append(F_)
            self.generated_code.write(f"\tDUP\n\tDUP\n\tDE_REF 1\n")
            self.generated_code.write(f"\tDEC\n\tSTORE_REF 1\n\tDE_REF 1\n")
            self.generated_code.write(f"\tINC\n")

        elif self.rule == F_PARENTHESIS_E_RULE:
            E_ = semantic_stack.pop()
            F_ = t_attrib(F,None,F(E_._.type))
            semantic_stack.append(F_)

        elif self.rule == F_MINUS_F_RULE:
            F1_ = semantic_stack.pop()
            t = F1_._.type
            if not CheckTypes(t,int_):
                Error(self.lexical, ERR_INVALID_TYPE)
            F0_ = t_attrib(F,None,F(t))
            semantic_stack.append(F0_)
            self.generated_code.write(f"\tNEG\n")

        elif self.rule == F_NOT_F_RULE:
            F1_ = semantic_stack.pop()
            t = F1_._.type
            if not CheckTypes(t,bool_):
                Error(self.lexical, ERR_INVALID_TYPE)
            F0_ = t_attrib(F,None,F(t))
            semantic_stack.append(F0_)
            self.generated_code.write(f"\tNOT\n")

        elif self.rule == F_TRUE_RULE:
            TRU_ = semantic_stack.pop()
            F_ = t_attrib(F,None,F(bool_))
            semantic_stack.append(F_)
            self.generated_code.write(f"\tLOAD_TRUE\n")

        elif self.rule == F_FALSE_RULE:
            FALS_ = semantic_stack.pop()
            F_ = t_attrib(F,None,F(bool_))
            semantic_stack.append(F_)
            self.generated_code.write(f"\tLOAD_FALSE\n")

        elif self.rule == F_CHR_RULE:
            CHR_ = semantic_stack.pop()
            F_ = t_attrib(F,None,F(char_))
            semantic_stack.append(F_)
            n = self.lexical.secondary_Token
            self.generated_code.write(f"\tLOAD_CONST {constPool}\n")
            constPool+=1

        elif self.rule == F_STR_RULE:
            STR_ = semantic_stack.pop()
            F_ = t_attrib(F,None,F(string_))
            semantic_stack.append(F_)
            n = self.lexical.secondary_Token
            self.generated_code.write(f"\tLOAD_CONST {constPool}\n")
            constPool+=1

        elif self.rule == F_NUM_RULE:
            NUM_ = semantic_stack.pop()
            F_ = t_attrib(F,None,F(int_))
            semantic_stack.append(F_)
            n = self.lexical.secondary_Token
            self.generated_code.write(f"\tLOAD_CONST {constPool}\n")
            constPool+=1

        elif self.rule == LV_DOT_RULE:
            ID_ = semantic_stack.pop()
            LV1_ = semantic_stack.pop()
            t = LV1_._.type
            if t.e_kind != STRUCT_TYPE_:
                if t.e_kind != UNIVERSAL_:
                    Error(self.lexical, ERR_KIND_NOT_STRUCT)
                LV0_ = t_attrib(LV,None,LV(universal_))
            else:
                self.p = t._.p_fields
                while self.p != None:
                    if self.p.aName == ID_._.name:
                        break
                    self.p = self.p.pNext
                if self.p == None:
                    Error(self.lexical, ERR_FIELD_NOT_DECL)
                    LV0_ = t_attrib(LV,None,LV(universal_))
                else:
                    LV0_ = t_attrib(LV,None,LV(self.p._.p_type))
                    LV0_._.type._ = Type(None,self.p._.n_size)
            semantic_stack.append(LV0_)
            self.generated_code.write(f"\tADD {self.p._.n_index}\n")

        elif self.rule == LV_SQUARE_RULE:
            E_ = semantic_stack.pop()
            LV1_ = semantic_stack.pop()
            t = LV1_._.type
            if CheckTypes(t,string_):
                LV0_ = t_attrib(LV,None,LV(char_))
            elif t.e_kind!=ARRAY_TYPE_:
                if t.e_kind != UNIVERSAL_:
                    Error(self.lexical, ERR_KIND_NOT_ARRAY)
                LV0_ = t_attrib(LV,None,LV(universal_))
            else:
                LV0_ = t_attrib(LV,None,LV(t._.p_elem_type))
                n = t._.p_elem_type._.n_size
                self.generated_code.write(f"\tMUL {n}\n")
                self.generated_code.write("\tADD\n")
            if not CheckTypes(E_._.type,int_):
                Error(self.lexical, ERR_INVALID_INDEX_TYPE)
            semantic_stack.append(LV0_)

        elif self.rule == LV_IDU_RULE:
            IDU_ = semantic_stack.pop()
            self.p = IDU_._.object
            if self.p.e_kind != VAR_ and self.p.e_kind!=PARAM_:
                if self.p.e_kind != UNIVERSAL_:
                    Error(self.lexical, ERR_KIND_NOT_VAR)
                LV_ = t_attrib(LV,None,LV(universal_))
            else:
                LV_ = t_attrib(LV,None,LV(self.p._.p_type))
                LV_._.type._ = Type(None,self.p._.n_size)
                self.generated_code.write(f"\tLOAD_REF {self.p._.n_index}\n")
            semantic_stack.append(LV_)
            
        elif self.rule == MC_RULE:
            IDU_ = semantic_stack[-1]
            f = IDU_._.object
            if f.e_kind != FUNCTION_:
                MC_ = t_attrib(MC,None,MC(universal_,None,True))
            else:
                MC_ = t_attrib(MC,None,MC(f._.p_ret_type,f._.p_params,False))
            semantic_stack.append(MC_)
        
        elif self.rule == LE_E_RULE:
            E_ = semantic_stack.pop()
            MC_ = semantic_stack[-1]
            LE_ = t_attrib(LE,None,LE(None,None,MC_._.err,1))
            if not MC_._.err:
                p=MC_._.param 
                if p == None:
                    Error(self.lexical, ERR_TOO_MANY_ARG)
                    LE_._.err = True
                else:
                    if not CheckTypes(self.p._.tipo,E_._.type):
                        Error(self.lexical, ERR_PARAM_TYPE)
                    LE_._.param = self.p.pNext   
                    LE_._.n = n + 1
            semantic_stack.append(LE_)
        
        elif self.rule == LE_LE_RULE:
            E_ = semantic_stack.pop()
            LE1_ = semantic_stack.pop()
            LE0_ = t_attrib(LE,None,LE(None,None,L1_._.err,LE1_._.n))
            if not LE1_._.err:
                p = LE1_._.param
                if p == None:
                    Error(self.lexical, ERR_TOO_MANY_ARG)
                    LE0_._.err = True
                else:
                    if not CheckTypes(self.p._.tipo,E_._.type):
                        Error(self.lexical, ERR_PARAM_TYPE)
                    LE0_._.param = self.p.pNext
                    LE0_._.n = n+1
            semantic_stack.append(LE0_)
        
        elif self.rule == F_IDU_MC_RULE:
            LE_ = semantic_stack.pop()
            MC_ = semantic_stack.pop()
            IDU_ = semantic_stack.pop()
            f = IDU_._.object
            F_ = t_attrib(F,None,F(MC_._.type))
            if not LE_._.err:
                if LE_._.n-1 < f._n_params and LE_._.n != 0:
                    Error(self.lexical, ERR_TOO_FEW_ARGS)
                elif LE_._.n-1 > f._.n_params:
                    Error(self.lexical, ERR_TOO_MANY_ARG)
            semantic_stack.append(F_)
            self.generated_code.write(f"\tCALL {f._.n_index}\n")

        elif self.rule == MT_RULE:
            rLabel = newLabel()
            MT_ = t_attrib(MT,None,MT(rLabel))
            semantic_stack.append(MT_)
            self.generated_code.write(f"\tTJMP_FW L{rLabel}\n")

        elif self.rule == ME_RULE:
            MT_ = semantic_stack[-1]
            rLabel = newLabel()
            ME_._.label = rLabel
            ME_.t_nont = ME
            semantic_stack.append(ME_)
            self.generated_code.write(f"\tTJMP_FW L{rLabel}\n")
            self.generated_code.write(f"L{MT_._.label}\n")

        elif self.rule == MW_RULE:
            rLabel = newLabel()
            MW_ = semantic_stack.pop()
            MW_._.label = rLabel
            semantic_stack.append(MW_)
            self.generated_code.write(f"L{rLabel}\n")

        elif self.rule ==M_BREAK_RULE:
            MT_ = semantic_stack[-1]

        elif self.rule == M_CONTINUE_RULE:
            pass
        
        elif self.rule == M_E_SEMICOLON:
            E_ = semantic_stack.pop()
            LV_ = semantic_stack.pop()
            if not CheckTypes(LV_._.type,E_._.type):
                Error(self.lexical, ERR_TYPE_MISMATCH)
            t = LV_._.type
            E0_._ = F(E_._.type)
            semantic_stack.append(E0_)
            if t._ == None or t._.n_size == None:
                self.generated_code.write(f"\tSTORE_REF 1\n")
            else:
                self.generated_code.write(f"\tSTORE_REF {t._.n_size}\n")

        self.generated_code.close()
