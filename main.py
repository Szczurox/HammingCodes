import math
from functools import reduce
from random import randint

# Generates hamming code
def generateHamming(msgBits: list, s: int, r: int):
  # Hamming code list length range
  hammingLR = range(s+r)
  # Hamming code list
  hammingCode: list = [0 for i in hammingLR]
  # Find position of redundant bits
  for i in range(r):
    hammingCode[pow(2, i) - 1] = -1
  
  j: int = 0
  # Place message bits where there are no redundant bits
  for i in hammingLR:
    if hammingCode[i] == 0:
      hammingCode[i] = msgBits[j]
      j += 1
  for i in hammingLR:
    # Continue if current bit is not redundant
    if hammingCode[i] != -1:
      continue
    
    x: int = int(math.log(i+1, 2))
    one_count: int = 0

    # Count ones
    for j in range(i + 2, s+r+1):
      if j & (1 << x):
        if hammingCode[j - 1] == 1:
          one_count += 1
    
    # Set redundant bit to 0 if number of ones % 2 is equal to 0 else set it to 1
    hammingCode[i] = int(bool(one_count % 2))

  # Return hamming code with a one bonus bit at the beginning 
  # This bit is useful for noise error handling
  return [0] + hammingCode


def findHamming(msgBits: list):
  # Message bits size
  size: int = len(msgBits)
  # Number of redundant bits
  rBits: int = 1
  # Find number of redundant bits
  while pow(2, rBits) < (size + rBits + 1):
    rBits += 1
  # Generate hamming code
  hammingCode: list = generateHamming(msgBits, size, rBits)
  # Return hamming code
  return hammingCode

# Checks for error in hamming code
def checkHamming(bits):
  return reduce(lambda x, y: x ^ y, [i for i, bit in enumerate(bits) if bit])

# Random noise
def noise(message):
  if randint(0,1):
    rn = randint(0, len(message)-1)
    message[rn] = int(not message[rn])
  return message


def receiver(hammingCode):
  print("\nHamming code recieved: " + ' '.join([str(elem) for elem in hammingCode]))
  # Find error if there is any
  error: int = checkHamming(hammingCode)
  # Correct bit
  hammingCode[error] = int(not hammingCode[error])

  # Getting the message
  size: int = len(hammingCode)
  # Number of redundant bits
  rBits: int = 1
  # Find number of redundant bits
  while pow(2, rBits) < (size):
    rBits += 1
  for i in range(rBits):
    hammingCode[pow(2, i)] = -1
  # Message bits
  msgBits = list(filter(lambda a: a != -1, hammingCode))
  msgBitsStr = ' '.join([str(elem) for elem in msgBits[1::]]) + "\n"

  # Print out data
  if error:
    print("Error found at: " + str(error))
    print("Fixed received message bits: " + msgBitsStr)
  else: 
    print("No error found")
    print("Message bits received: " + msgBitsStr)


def main():
  bits = input("Message bits: ")
  # Message bits
  msgBits: list = list(map(int, list(bits)))
  # Generate hammign code
  hammingCode = findHamming(msgBits)
  # Print out data
  print("\nMessage bits: " + ' '.join([str(elem) for elem in msgBits]))
  print("Hamming code: " + ' '.join([str(elem) for elem in hammingCode]))
  # Send data with random noise to receiver
  receiver(noise(hammingCode))


if __name__ == "__main__":
  main()