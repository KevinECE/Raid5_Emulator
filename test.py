import numpy as np
# oldData = bytearray([1, 2, 3])
# newData = bytearray([1, 0, 2])
# dataXOR = bytes(oldData ^ newData for (oldData, newData) in zip(oldData, newData))
# print(str(dataXOR))
# dataXOR_bytearr = bytearray(dataXOR)  
# print(str(dataXOR_bytearr))



server = 3
numServers = 4
servers = [bytearray([0,0,0,0,0]), bytearray([1,2,3,4,5]), bytearray([5,4,3,2,1]), bytearray([8,8,8,8,8])]
parity = bytearray([0,0,0,0,0])
recovered = bytearray([0,0,0,0,0])
# for i in range(0, numServers):
#     for j in range(0, 5):
#             parity[j] ^= servers[i][j]

# for i in range(0, numServers):
#     for j in range(0, 5):
#         if i != server:
#             recovered[j] ^= servers[i][j]
               
# for i in range(0,5):
#     recovered[i] ^= parity[i]

# print('Recovered ' + str(server) + ': ' + str(recovered))

for i in range(0, numServers):
    parity = bytearray(np.bitwise_xor(parity, servers[i][0]))
    # print(str(parity))

for i in range(0, numServers):
    if i != server:
        recovered = bytearray(np.bitwise_xor(recovered, servers[i][0]))

    # print(str(i))
    # print(str(parity))

    # print(str(recovered))

# print('Parity ' + str(parity[0]))
recovered = bytearray(np.bitwise_xor(recovered, parity))
print('Recovered ' + str(server) + ': ' + str(recovered))