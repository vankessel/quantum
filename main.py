import os
from bitstring import BitArray
import dimod

from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

FILENAME = 'results'
EXT = 'txt'
NUM_BYTES = 16

# solver = dimod.ExactSolver()
solver = EmbeddingComposite(DWaveSampler())

bytelist = []
params = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0}

print("Generating bytes:")
for _ in range(NUM_BYTES):
    # Send degenerate problem to QPU
    response = solver.sample_ising(params, {}, num_reads=1)

    # Get data and transform to bit tuple
    sample = next(response.data()).sample
    byte = tuple([0 if sample[x] == -1 else 1 for x in sorted(sample)])
    print(byte)

    bytelist.append(byte)

# Generate list of numbers
intlist = [BitArray(x).uint for x in bytelist]

print("\nRandom bytes:")
for num in intlist:
    print(num)

# Generate list of characters
charlist = [chr(x) for x in intlist]

print("\nRandom characters:")
print(''.join(charlist))

# Generate filename
idx = 0
filename = FILENAME + '_' + str(idx) + '.' + EXT
while(os.path.isfile(filename)):
    idx += 1
    filename = FILENAME + '_' + str(idx) + '.' + EXT

# Write result to file
print("\nWriting to {}".format(filename))
with open(filename, 'w') as f:
    for byte, num in tuple(zip(bytelist, intlist)):
        f.write(''.join([str(bit) for bit in byte]) + ' | {}\n'.format(num))
