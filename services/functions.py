import string

def generate_letter_labels(n):
    letters = string.ascii_lowercase
    result = []
    i = 0
    while len(result) < n:
        prefix = ''
        q = i
        while True:
            q, r = divmod(q, 26)
            prefix = letters[r] + prefix
            if q == 0:
                break
        result.append(prefix)
        i += 1
    return result