import pickle, logging
import argparse
import hashlib

# Corrupt block number variable
CORRUPT_BLOCK_NUMBER = -1

# Checksum error constant for handling corrupt blocks
CHECKSUM_ERROR = -1

# For locks: RSM_UNLOCKED=0 , RSM_LOCKED=1 
RSM_UNLOCKED = bytearray(b'\x00') * 1
RSM_LOCKED = bytearray(b'\x01') * 1

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
  rpc_paths = ('/RPC2',)
  
# BLOCK LAYER
class DiskBlocks():
  def __init__(self, total_num_blocks, block_size):
    self.block = []                                            
    # Initialize raw blocks 
    for i in range (0, total_num_blocks):
      putdata = bytearray(block_size)
      self.block.insert(i,putdata)
      
    # Dict to store checksums for each block
    self.checksums = {}

  # CalcChecksum: calculates and stores a checksum for a provided block
  def CalcCheckSum(self, data):
    m = hashlib.md5()
    m.update(data.data)
    return m.hexdigest()  

if __name__ == "__main__":

  # Construct the argument parser
  ap = argparse.ArgumentParser()

  ap.add_argument('-nb', '--total_num_blocks', type=int, help='an integer value')
  ap.add_argument('-bs', '--block_size', type=int, help='an integer value')
  ap.add_argument('-port', '--port', type=int, help='an integer value')
  ap.add_argument('-sid', '--sid', type=int, help='an integer value')
  ap.add_argument('-cblk', '--cblk', type=int, help='an integer value')
  args = ap.parse_args()

  if args.total_num_blocks:
    TOTAL_NUM_BLOCKS = args.total_num_blocks
  else:
    print('Must specify total number of blocks') 
    quit()

  if args.block_size:
    BLOCK_SIZE = args.block_size
  else:
    print('Must specify block size')
    quit()

  if args.port:
    PORT = args.port
  else:
    print('Must specify port number')
    quit()
    
  if args.sid >= 0:
    SERVER_ID = args.sid
  else:
    print('Must specify server id')
    quit()
    
  if args.cblk:
    CORRUPT_BLOCK_NUMBER = args.cblk
    print('Corrupt block' + str(CORRUPT_BLOCK_NUMBER))

  # parameter used to emulate decay in a specific block
  # if args.cblk:

  # initialize blocks
  RawBlocks = DiskBlocks(TOTAL_NUM_BLOCKS, BLOCK_SIZE)

  # Create server
  server = SimpleXMLRPCServer(("127.0.0.1", PORT), requestHandler=RequestHandler) 

  def Get(block_number):
    # Read data from a block
    result = RawBlocks.block[block_number]
    # If the stored checksum does not match the computed checksum, return an error
    if block_number == CORRUPT_BLOCK_NUMBER:
      return CHECKSUM_ERROR
    return result

  server.register_function(Get)

  def Put(block_number, data):
    # Store data
    RawBlocks.block[block_number] = data
    # Compute and store a checksum for the data
    RawBlocks.checksums[block_number] = RawBlocks.CalcCheckSum(RawBlocks.block[block_number])
    # print('The checksum for block# ' + str(block_number) + ' is ' + str(RawBlocks.checksums[block_number]))
    return 0

  server.register_function(Put)

  def RSM(block_number):
    result = RawBlocks.block[block_number]
    # RawBlocks.block[block_number] = RSM_LOCKED
    RawBlocks.block[block_number] = bytearray(RSM_LOCKED.ljust(BLOCK_SIZE,b'\x01'))
    return result

  server.register_function(RSM)

  # Run the server's main loop
  print ("Running block server with nb=" + str(TOTAL_NUM_BLOCKS) + ", bs=" + str(BLOCK_SIZE) + " on port " + str(PORT))
  server.serve_forever()

