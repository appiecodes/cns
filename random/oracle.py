n = 3233
e = 17
c = 855
r = 7

print("c_modified: ", r**e * c % n)
c_modified = 1637

m_modified = 861
print("response server: " , m_modified)

M = (m_modified * pow(r, -1, n)) % n
print("M: ", M)