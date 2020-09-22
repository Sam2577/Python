
def remove_spaces(string):
    head = string[0]
    tail = string[1:]
    if string is None: return None
    if type(string)() is not str(): raise TypeError()
    if len(string) < 1: return str()
    if head == " ": return remove_spaces(tail)
    return head + remove_spaces(tail)

def reverse(string):
    head = string[0]
    tail = string[1:]
    if len(string) < 1: return str()
    return reverse(tail) + head

def palindrome(given_string):
    if given_string is None: return False
    string = remove_spaces(given_string)
    reverse_string = reverse(string)
    if string == reverse_string: return True
    return False


print(palindrome("sammas"))
print(palindrome("racecar"))
