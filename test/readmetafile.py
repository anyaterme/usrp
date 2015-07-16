import numpy as np
import sys
import pmt
from gnuradio.blocks import parse_file_metadata as pfm

filename = "metafile.dat"
path = "./"
filepath = "%s%s" % (path, filename)

f = open ("%s.hdr" % filepath, "r")
data = f.read()
f.close()
header = pmt.deserialize_str(data)
mydict = pfm.parse_header(header)
print pfm.HEADER_LENGTH
print mydict
dataFile = np.fromfile(filepath, np.float32)
#


#dataFile = np.fromfile('./metafile.dat', np.float32)
#print dir(dataFile)
