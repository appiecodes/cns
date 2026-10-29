def rol(x, n):
    return ((x << n) | (x >> (8 - n))) & 0xff

def better_hash(msg):
    state = bytearray(msg.encode())

    for rnd in range(8):

        for i in range(len(state)):
            state[i] ^= (rnd * 41 + i * 17) & 0xff
            state[i] = rol(state[i], (rnd + i) & 7)


        for i in range(1, len(state)):
            state[i] ^= state[i - 1]

        state = state[1:] + state[:1]

    return state.hex()



HASH = "5f070b54361613bca31a123e95321cff154ba64f549bb34fdc7688f10efb569aed4ccbd6ba"

def reverse_rol(x, n):
    return ((x >> n) | (x << (8 - n))) & 0xff

def reverse_better_hash(target_hash):
    state = bytearray.fromhex(target_hash)

    # Undo rounds in reverse order: 7 to 0
    for rnd in reversed(range(8)):

        # Undo the byte-array rotation
        state = state[-1:] + state[:-1]

        # Undo neighboring XOR, right to left
        for i in range(len(state) - 1, 0, -1):
            state[i] ^= state[i - 1]

        # Undo bit rotation, then XOR mask
        for i in range(len(state)):
            n = (rnd + i) & 7
            state[i] = reverse_rol(state[i], n)
            state[i] ^= (rnd * 41 + i * 17) & 0xff

    return state.decode()

print(reverse_better_hash(HASH))
