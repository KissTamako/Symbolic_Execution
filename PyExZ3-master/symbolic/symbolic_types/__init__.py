# Copyright: see copyright.txt

from .symbolic_int import SymbolicInteger as SymInt
from .symbolic_int import SymbolicObject as SymObj
from .symbolic_dict import SymbolicDict as SymD
from .symbolic_str import SymbolicStr as SymS
from .symbolic_type import SymbolicType as SymType
from .symbolic_range import SymbolicRange as SymR
from .symbolic_list import SymbolicList as SymL
from .symbolic_float import SymbolicFloat as SymF

SymObj.wrap = lambda conc, sym : SymbolicInteger("se",conc,sym)
SymbolicInteger = SymInt
SymbolicDict = SymD
SymbolicStr = SymS
SymbolicType = SymType
SymbolicRange = SymR
SymbolicList = SymL
SymbolicFloat = SymF

def getSymbolic(v):
	exported = [
        (int,SymbolicInteger),
        (dict,SymbolicDict),
        (str,SymbolicStr),
        (range,SymbolicRange),
        (list,SymbolicList),
        (float,SymbolicFloat)
    ]
	for (t,s) in exported:
		if isinstance(v,t):
			return s
	return None



