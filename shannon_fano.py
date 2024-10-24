# shanon_fano.py

def shannon_fano_encoder(symbols):
    # Sort symbols by their frequencies
    sorted_symbols = sorted(symbols.items(), key=lambda x: x[1], reverse=True)
    
    # Base case, return if there's only one symbol
    if len(sorted_symbols) == 1:
        return {sorted_symbols[0][0]: '0'}
    
    # Recursive function to divide symbols into two parts
    def split_list(symbols):
        total_sum = sum([pair[1] for pair in symbols])
        acc = 0
        for i in range(len(symbols)):
            acc += symbols[i][1]
            if acc >= total_sum / 2:
                return symbols[:i + 1], symbols[i + 1:]
    
    # Recursively assign bits to symbols
    def assign_bits(symbols, prefix=''):
        if len(symbols) == 1:
            return {symbols[0][0]: prefix}
        left, right = split_list(symbols)
        encoding = {}
        encoding.update(assign_bits(left, prefix + '0'))
        encoding.update(assign_bits(right, prefix + '1'))
        return encoding

    return assign_bits(sorted_symbols)

def shannon_fano_decoder(encoded_msg, encoding_table):
    reversed_table = {v: k for k, v in encoding_table.items()}
    current_code = ""
    decoded_message = ""
    
    for bit in encoded_msg:
        current_code += bit
        if current_code in reversed_table:
            decoded_message += reversed_table[current_code]
            current_code = ""
    
    return decoded_message

def get_symbol_frequencies(message):
    frequencies = {}
    for char in message:
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1
    return frequencies
