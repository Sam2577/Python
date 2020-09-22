

##num = 900
##numset = set(range(2, num))
##
##half = int(num / 2)
##for i in range(2, half - 1):
##    for j in range(2, half - 1):
##        number = j * i
##        if number in numset:
##            numset.remove(number)

    
def is_prime(num):
    half = num // 2
    for i in range(2, half + 1):
        if not num % i:
            return False
    return True

print([i for i in range(2,100) if is_prime(i)])
