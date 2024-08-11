import random

def random_trace_id():
    hex_digits = "0123456789abcdef"
    trace_id = ''.join(random.choice(hex_digits) for _ in range(16))
    return trace_id

# Example usage
print(random_trace_id())
