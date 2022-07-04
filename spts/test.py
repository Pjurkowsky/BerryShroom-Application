import struct
payload2 = struct.pack(">BiB", 0x01, 123, 0xC8)
payload2 = struct.unpack(">BiB", payload2)
print(payload2)
