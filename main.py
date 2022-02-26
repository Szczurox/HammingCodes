import math
from functools import reduce
from random import randint


# Generates hamming code
def generate_hamming(msgBits, s, r):
  hammingCodeLength = s + r
  # Hamming code list
  hammingCode = [0 for i in range(hammingCodeLength)]
  # Find position of redundant bits
  for i in range(r):
    hammingCode[pow(2, i) - 1] = -1
  
  j = 0
  # Place message bits where there are no redundant bits
  for i, v in enumerate(hammingCode):
    if v == 0:
      hammingCode[i] = msgBits[j]
      j += 1
    
  for i, v in enumerate(hammingCode):
    # Continue if current bit is not redundant
    if v != -1:
      continue
    
    x = int(math.log(i + 1, 2))
    one_count = 0

    # Count ones
    for j in range(v + 2, hammingCodeLength + 1):
      if j & (1 << x):
        if hammingCode[j - 1] == 1:
          one_count += 1
    
    # Set redundant bit to 0 if number of ones % 2 is equal to 0 else set it to 1
    hammingCode[i] = int(bool(one_count % 2))

  # Return hamming code with a one bonus bit at the beginning 
  # This bit is useful for noise error handling
  return [0] + hammingCode


def find_hamming(msgBits):
  # Message bits size
  size = len(msgBits)
  # Number of redundant bits
  rBits = 1
  # Find number of redundant bits
  while pow(2, rBits) < size + rBits + 1:
    rBits += 1
  # Generate hamming code
  hammingCode = generate_hamming(msgBits, size, rBits)
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
  print(f"\nHamming code recieved: {' '.join([str(elem) for elem in hammingCode])}")
  # Find error if there is any
  error = checkHamming(hammingCode)
  # Correct bit
  hammingCode[error] = int(not hammingCode[error])
  # Number of redundant bits
  rBits = 1
  # Find number of redundant bits
  while pow(2, rBits) < len(hammingCode):
    rBits += 1
  for i in range(rBits):
    hammingCode.pop(pow(2, i))
  msgBitsStr = ' '.join([str(elem) for elem in hammingCode[1::]])

  # Print out data
  if error:
    print(f"Error found at: {error}")
    print(f"Fixed received message bits: {msgBitsStr}\n")
  else: 
    print("No error found")
    print(f"Message bits received: {msgBitsStr}\n")


def main():
  # Get message bits
  msgBits = list(input("Message bits: ").replace(" ", ""))
  # Message bits
  msgBits = list(map(int, msgBits))
  # Generate hamming code
  hammingCode = find_hamming(msgBits)
  # Print out data
  print(f"\nMessage bits: {' '.join([str(elem) for elem in msgBits])}")
  print(f"Hamming code: {' '.join([str(elem) for elem in hammingCode])}")
  # Send data with random noise to receiver
  receiver(noise(hammingCode))


if __name__ == "__main__":
  main()