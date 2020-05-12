import protocolstream

bs = protocolstream.BinaryStreamWriter()
bs.WriteInt32(1024)
print(bs.m_data)

bs.ReadInt32(bs.m_data)

bs.WriteInt32(0)
print(bs.m_data)
cde = bs.ReadInt32(bs.m_data[4:8])
print(cde)