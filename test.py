import numpy as np
import hashlib

numServers = 5

# RAID5 PROTOTYPING
### RAID5
## Convert a virtual block to a physical block and server
def VirtualToPhysicalData(virtual_block_number):

    parityServer, parityBlock = VirtualToPhysicalParity(virtual_block_number)

    server_ID = virtual_block_number % (numServers-1) 
    physical_block_number = virtual_block_number // (numServers-1)

    if server_ID >= parityServer:
        server_ID += 1
    return server_ID, physical_block_number

def VirtualToPhysicalParity(virtual_block_number):
    physical_block_number = virtual_block_number // (numServers-1)
    server_ID = (numServers - 1) - (physical_block_number % (numServers))
    
    return server_ID, physical_block_number 

print('DATA')
for i in range(0, 30):
    server, block = VirtualToPhysicalData(i)
    print('VB = ' + str(i) + ' Server = ' + str(server) + ' PB = ' + str(block))

print('PARITY')


# for i in range(0, 20):
#     parityServer, parityBlock = VirtualToPhysicalParity(i)
#     print('VB = ' + str(i) + ' Server = ' + str(parityServer) + ' PB = ' + str(parityBlock))









# data = bytearray([1,2,3,4,5])
# hash = hashlib.md5(data).hexdigest()
# print(hash)


# server = 3
# numServers = 4
# servers = [bytearray([0,0,0,0,0]), bytearray([1,2,3,4,5]), bytearray([5,4,3,2,1]), bytearray([8,8,8,8,8])]
# parity = bytearray([0,0,0,0,0])
# recovered = bytearray([0,0,0,0,0])
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

# for i in range(0, numServers):
#     parity = bytearray(np.bitwise_xor(parity, servers[i][0]))
#     # print(str(parity))

# for i in range(0, numServers):
#     if i != server:
#         recovered = bytearray(np.bitwise_xor(recovered, servers[i][0]))

    # print(str(i))
    # print(str(parity))

    # print(str(recovered))

# print('Parity ' + str(parity[0]))
# recovered = bytearray(np.bitwise_xor(recovered, parity))
# print('Recovered ' + str(server) + ': ' + str(recovered))