import sys, math


def is_prime(num):
    if num > 1:
        for i in range(2, ((num // 2) + 1)):
            if num % i == 0:
                return False
        return True
    return False


def get_final_list(given_list, num):
    newlist = list()
    tolerance = 0.0009
    for item in given_list:
        log = math.log(num, item)
        print(num, item, log)
        if abs(int(log) - float(log)) < tolerance:
            newlist.extend([item] * int(log))
        else:
            newlist.append(item)
    return newlist
    
def factors(num):
    for i in range(2, num + 1):
        if num % i == 0 and is_prime(i):
            yield i

def factor1(n):
    i = 2
    factors = list()
    while n > 1:
        
        print("n", n, "i", i)
            
        if n % i == 0:
            factors.append(i)
            n = n/i
        else:
            i += 1
    return factors

print(factor1(225))

    
##num = 24
##print([item for item in factors(num)])
##print(get_final_list([item for item in factors(num)], num))

        
