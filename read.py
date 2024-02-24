def ishex(s):
    try:
        n = int(s,16)
        return True
    except ValueError:
        return False

file = open("micro-s.lst", "r")
count = 0
current_addr = 0
data = bytearray(2048)

for line in file.readlines():
    count += 1
    line = line.strip()
    if not line:
        continue
    if line.startswith("#"):
        continue
    s = line.split(" ")
    print(line)
    if not ishex(s[0]):
        raise Exception(f"address not hex in line {count}")
    addr = int(s[0],16)
    if current_addr==0:
        current_addr = addr
    if current_addr != addr:
        raise Exception(f"address do no match in line {count}")
    for x in s[1:]:
        if len(x)!=2 and len(x)!=4:
            raise Exception(f"error in line {count}")
        if not ishex(x):
            raise Exception(f"data not hex in line {count}")
        if len(x)==2:
            data[current_addr-0xf000] = int(x,16)
        else:
            data[current_addr-0xf000+0] = int(x[2:],16)
            data[current_addr-0xf000+1] = int(x[:2],16)
        current_addr+= len(x)//2
        

file.close()

with open("micro-s.bin", "wb") as binary_file:
    binary_file.write(data)