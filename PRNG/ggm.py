SEED_SIZE = 8
GENERATOR = 223
MODULUS = 36389


def FUNCTION_L(x): return x*3


def function_H(first_half, second_half):
    mod_exp = bin(pow(GENERATOR, int(first_half, 2), MODULUS)
                  ).replace('0b', '').zfill(SEED_SIZE)
    hard_core_bit = 0
    for i in range(len(first_half)):
        hard_core_bit = (hard_core_bit ^ (
            int(first_half[i]) & int(second_half[i]))) % 2
    return mod_exp + second_half + str(hard_core_bit)


def function_G(initial_seed):
    binary_string = initial_seed
    # import pdb; pdb.set_trace()
    result = ''
    for i in range(FUNCTION_L(SEED_SIZE)):
        first_half = binary_string[:int(len(binary_string)/2)]
        second_half = binary_string[int(len(binary_string)/2):]
        binary_string = function_H(first_half, second_half)
        result += binary_string[-1]
        binary_string = binary_string[:-1]
    return result


def PRNG(seed):
    init_seed = str(seed)
    # import pdb; pdb.set_trace()
    if len(init_seed) > SEED_SIZE:
        print('Inital seed too long!')
        return None
    output = function_G(init_seed)
    return output
