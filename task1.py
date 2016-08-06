import sys
import os.path
try:
    from lxml import etree
except ImportError:
    print("lxml must be installed")
    sys.exit()
 
total = len(sys.argv)
cmdargs = str(sys.argv)
if total < 2:
    print("too few args")
    print("Usage: %s path_to_xml" % sys.argv[0])
    sys.exit()
    

path = str(sys.argv[1])
if not os.path.isfile(path):
    print("file not exist")
    sys.exit()

try:
    tree = etree.parse(path)
except etree.XMLSyntaxError:
    print("file not valid")
    sys.exit();
    
count = tree.xpath("count(//@value2)")
summ = tree.xpath("sum(//@value2)")

if count > 0:
    print(summ/count)
else:
    print(0)