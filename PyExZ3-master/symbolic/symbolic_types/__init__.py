# Copyright: see copyright.txt

from .symbolic_int import SymbolicInteger as SymInt
from .symbolic_int import SymbolicObject as SymObj
from .symbolic_dict import SymbolicDict as SymD
from .symbolic_str import SymbolicStr as SymS
from .symbolic_bool import SymbolicBool as SymB
from .symbolic_float import SymbolicFloat as SymF
from .symbolic_type import SymbolicType as SymType
from .symbolic_range import SymbolicRange as SymR

SymObj.wrap = lambda conc, sym : SymbolicInteger("se",conc,sym)
SymbolicInteger = SymInt
SymbolicDict = SymD
SymbolicStr = SymS
SymbolicBool = SymB
SymbolicFloat = SymF
SymbolicType = SymType
SymbolicRange = SymR

def getSymbolic(v):
	exported = [(bool,SymbolicBool),(int,SymbolicInteger),(float,SymbolicFloat),(dict,SymbolicDict),(str,SymbolicStr), (range,SymbolicRange)]
	for (t,s) in exported:
		if isinstance(v,t):
			return s
	return None



