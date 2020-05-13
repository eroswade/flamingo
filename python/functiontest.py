import protocolstream
import struct
# ret = protocolstream.write7BitEncoded(1025)
# print(ret)# \x81\x08
# print(protocolstream.write7BitEncoded(82))#R

d = 1
d = d.to_bytes(1,'big')
values = (d,92,91)
s = struct.Struct('cII') #  I4: unsigned int s: char* f:float p:char* c: char i: int
packed_data = s.pack(*values)
unpacked_data = s.unpack(packed_data)
print(packed_data)