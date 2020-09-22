from datetime import datetime
import sys
import unittest, functools
from operator import mul

class Factor:
    
    def __init__(self, num, *args):
        self.num = num
        self.args = args
        self.factors = list()
        
        i = 2
        while num > 1: 
            if num % i == 0:
                self.factors.append(i)
                num = num / i
            else: i += 1

    def __str__(self):
        return f'{self.factors}'

    def _get_factors(self):
        return self.factors


class Ratio:

    def add_ratio(ratio1, ratio2):   #static method, but should it be

        num1, denom1 = ratio1._get_ratio()
        num2, denom2 = ratio2._get_ratio()
        new_num1 = denom2 * num1
        new_num2 = denom1 * num2
        new_num = new_num1 + new_num2
        new_denom = denom2 * denom1
        return f'{new_num}/{new_denom}'

    def remove_common_elements(self, num, den):
        for item in num[:]:
            if item in den:
                num.remove(item)
                den.remove(item)      

    def __init__(self, num, denom):

        num_fact = Factor(num)
        denom_fact = Factor(denom)
        numerator_list = num_fact._get_factors()  #evaluate given Factors to get lists of prime factors
        denominator_list = denom_fact._get_factors()
        
        self.remove_common_elements(numerator_list, denominator_list) # mutates given lists
        
        self.num = functools.reduce(lambda x, y: x * y, numerator_list)    # multiply the remaining (actual, prime) factors together,
        self.denom = functools.reduce(lambda x, y: x * y, denominator_list)  # and initialize numerator and denominator properties

    def __str__(self):
        return f'{self.num}/{self.denom}'

    def _get_ratio(self):
        return self.num, self.denom


class test_Ratio (unittest.TestCase):

    def set_up(self):
        self.ratio = Ratio(480, 560)
        self.expected_ratio = '6/7'
        self.expected_lists1 = '([7], [8])'
        self.expected_lists2 = '([17, 1, 11], [])'

    def test_init(self):
        self.assertEquals(str(self.ratio), self.expected_ratio)

##    def test_remove_common_elements(self):
##        self.assertEquals(str(self.ratio.remove_common_elements([7, 5, 2], [2, 5, 8])), self.expected_lists1)
##        self.assertEquals(str(self.ratio.remove_common_elements([1, 17, 11, 1, 11], [1, 11])), self.expected_lists2)


    
if '__main__' == __name__:

    test = test_Ratio()
    test.set_up()
    test.test_init()
    #test.test_remove_common_elements()
    
    num = 60
    factor = Factor(num)

    six_sevenths = Ratio(480, 560)
    ten_elevenths = Ratio(20, 22)

    print(six_sevenths)
    print(ten_elevenths)

    print(Ratio.add_ratio(six_sevenths, ten_elevenths))

##    print(factor)
##    print(repr(factor))
##    print(type(repr(factor)))
##    print(type(eval(repr(factor))))
