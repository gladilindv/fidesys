import sys

class Zero(): # a class that is zero (Python2)
    def __nonzero__(self): 
        return False

class Len0(): # a class with zero length
    def __len__(self):
        return 0
    
class NEqual(): # a class that is not equal to everything
    def __ne__(self, other):
        return False
    
class Bool(): # a class that is False (Python3)
    def __bool__(self):
        return False;


x = [None, False, 0, 0.0, 0j, (), [], {}, set(), '', float('NaN'), float('inf'), Zero(), Len0(), NEqual(), Bool()]

print ('{:_^20} {:_<15} {:_<20} {:_<20} {:_<15}'.format('TYPE', 'VALUE', 'Is Bool', 'Is Not None', 'Is Not Eq'))

for item in x:
   
    ok1 = False
    if item:
        ok1 = True
        
    ok2 = False    
    if item is not None:
        ok2 = True
    
    ok3 = False
    if item != None:
        ok3 = True
    
    
    if not ok1: ok1 = '-'
    if not ok2: ok2 = '-'
    if not ok3: ok3 = '-'
    s = map(lambda x: str(x).ljust(20), [type(item), item, ok1, ok2, ok3])
    if sys.version_info[0] < 3:
        if 'instance' in str(type(item)):
            s = map(lambda x: str(x).ljust(20), [type(item), str(item)[10:14], ok1, ok2, ok3])
    else:
        if 'main' in str(type(item)):
            s = map(lambda x: str(x).ljust(20), [str(type(item))[:15], str(item)[10:14], ok1, ok2, ok3])    
        
    s = "".join(s)
    
    print(s)