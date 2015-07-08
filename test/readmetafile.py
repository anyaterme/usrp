import numpy as np
import sys
import pmt
from gnuradio.blocks import parse_file_metadata as pfm

f = open ("./metafile.dat", "r")
data = f.read()
f.close()
header = pmt.deserialize_str(data)
mydict = pfm.parse_header(header)
print mydict
dataFile = np.fromfile('./metafile.dat', np.float32)
print dataFile



#


#dataFile = np.fromfile('./metafile.dat', np.float32)
#print dir(dataFile)
