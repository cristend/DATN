SEED_SIZE = 4
GENERATOR = 223
MODULUS = 36389


def FUNCTION_L(x): return x*3


def function_H(first_half, second_half):
    mod_exp = format(pow(GENERATOR, int(first_half, 2),
                         MODULUS), 'b').zfill(SEED_SIZE)
    hard_core_bit = 0
    for i in range(len(first_half)):
        hard_core_bit = (hard_core_bit ^ (
            int(first_half[i]) & int(second_half[i]))) % 2
    return mod_exp + second_half + str(hard_core_bit)


def function_G(initial_seed, output_size=None):
    binary_string = initial_seed
    result = ''
    output_size = (FUNCTION_L(SEED_SIZE)
                   if output_size is None else output_size)
    for i in range(output_size):
        first_half = binary_string[:int(len(binary_string)/2)]
        second_half = binary_string[int(len(binary_string)/2):]
        binary_string = function_H(first_half, second_half)
        result += binary_string[-1]
        binary_string = binary_string[:-1]
    return result


def PRNG(seed, output_size=None):
    init_seed = str(seed)
    if len(init_seed) > SEED_SIZE:
        print('Inital seed too long!')
        return None
    output = function_G(initial_seed=init_seed, output_size=output_size)
    return output


def G_L(self, X):
    prn = PRNG(seed=X)
    return prn[:int(len(prn)/3)]


def G_M(self, X):
    prn = PRNG(seed=X)
    return prn[int(len(prn)/3):int(len(prn)*2/3)]


def G_R(self, X):
    prn = PRNG(seed=X)
    return prn[int(len(prn)*2/3):]
