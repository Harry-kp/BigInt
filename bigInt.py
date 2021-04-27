import random
import warnings
from math import floor

class bigInt():

    def __init__(self, number):
        if len(number) == 0:
            raise Exception("Number cannot be empty")

        if number[0] == '-' or number[0] == '+':
            if not number[1:].isdigit():
                raise Exception("Only integers are allowed")
        else:
            if not number.isdigit():
                raise Exception("Only integers are allowed")
        if not number[0] in ['+', '-']:
            warnings.warn(
                "+ sign is considered if you do not specify the sign of the number")
            number = "+" + number
        self.number = self.removeLeadingZeroes(number)

#--------Utilities-------#

    @staticmethod
    def removeLeadingZeroes(obj):
        """This function removes leading zeroes from the number and if all digits are zero then all zeroes are removed but one.
        """
        sign = obj[0]
        num = obj[1:].lstrip("0")

        if len(num) == 0:
            num = "0"
        return sign+num

    @staticmethod
    def isSmaller(str1, str2):
        l1 = len(str1)
        l2 = len(str2)

        if (l1 < l2):
            return True
        if (l1 > l2):
            return False

        for i in range(l1):
            if (str1[i] < str2[i]):
                return True
            elif (str1[i] > str2[i]):
                return False
        return False

    # Method for division .Now works for only if divisor is small and dividend can be large
    @staticmethod
    def __floordiv_util__(dividend, divisor):
        l1 = len(dividend)
        ans = ''
        pos = 0
        divisor = int(divisor)
        prefix = ord(dividend[pos])-48

        while(pos+1<l1 and prefix < divisor):
            pos += 1
            prefix = prefix*10+ord(dividend[pos])-48

        pos += 1

        while len(dividend) > pos:
            ans += chr(prefix//divisor + 48)

            prefix = ((prefix % divisor)*10 + ord(dividend[pos])-48)

            pos += 1

        mod = (prefix + divisor)%divisor

        ans += chr((prefix//divisor)+48)

        if len(ans) == 0:
            return '0'

        return ans,mod

    def __neg__(self):
        return bigInt('-'+self.number[1:])

# =========Arithmetic Operators======== #
    def __add__(self, other):
        num1 = self.number[1:]
        num2 = other.number[1:]

        l1 = len(num1)
        l2 = len(num2)

        sign1 = self.number[0]
        sign2 = other.number[0]

        ans = ''
        if sign1 != sign2:
            temp1 = bigInt(other.number)
            if temp1.number[0] == '-':
                temp1.number = '+' + temp1.number[1:]
            else:
                temp1.number = '-' + temp1.number[1:]
            return self-temp1
        else:
            max1 = max(l1, l2)
            car = 0
            for i in range(1, max1+1):
                try:
                    op1 = ord(num1[-i]) - 48
                except:
                    op1 = 0
                try:
                    op2 = ord(num2[-i]) - 48
                except:
                    op2 = 0
                sum1 = op1 + op2 + car
                car = (sum1)//10
                ans = chr(sum1 % 10 + 48) + ans
            ans = chr(car+48) + ans
            return bigInt(sign1+ans)

    def __sub__(self, other):
        num1 = self.number[1:]
        num2 = other.number[1:]

        l1 = len(num1)
        l2 = len(num2)

        sign1 = self.number[0]
        sign2 = other.number[0]

        if sign1 != sign2:
            temp1 = bigInt(other.number)
            if temp1.number[0] == '+':
                temp1.number = '-' + temp1.number[1:]
            else:
                temp1.number = '+' + temp1.number[1:]

            return self+temp1
        else:
            if bigInt.isSmaller(num1, num2):
                if sign1 == '-':
                    ans_sign = '+'
                else:
                    ans_sign = '-'

                l1, l2 = l2, l1
                num1, num2 = num2, num1
            else:
                ans_sign = sign1
            ans = ''
            max1 = max(l1, l2)
            car = 0
            for i in range(1, max1+1):
                try:
                    op1 = ord(num1[-i]) - 48
                except:
                    op1 = 0
                try:
                    op2 = ord(num2[-i]) - 48
                except:
                    op2 = 0
                min1 = op1 - op2 - car
                if min1 < 0:
                    min1 += 10
                    car = 1
                else:
                    car = 0
                ans = str(min1) + ans
            return bigInt(ans_sign+ans)

    def __mul__(self, other):
        sign1 = self.number[0]
        sign2 = other.number[0]

        if sign1 != sign2:
            ans_sign = '-'
        else:
            ans_sign = '+'

        num1 = self.number[1:]
        num2 = other.number[1:]

        l1 = len(num1)
        l2 = len(num2)

        if num1 == '0' or num2 == '0':
            return bigInt(ans_sign + '0')

        ans = [0]*(l1+l2)
        pos1 = 0
        pos2 = 0

        for i in range(l1-1, -1, -1):
            carry = 0
            op1 = ord(num1[i])-48
            pos2 = 0

            for j in range(l2-1, -1, -1):
                op2 = ord(num2[j])-48
                sum1 = op1*op2+ans[pos1+pos2]+carry
                carry = sum1//10

                ans[pos1+pos2] = sum1 % 10

                pos2 += 1

            if carry > 0:
                ans[pos1+pos2] += carry

            pos1 += 1

        out = ''
        for digit in ans:
            out = chr(digit+48)+out

        return bigInt(ans_sign+out)

    def __floordiv__(self, other):
        if other.number[1:] == '0':
            raise Exception('Division by zero')

        num1 = self.number[1:]
        num2 = other.number[1:]
        sign1 = self.number[0]
        sign2 = other.number[0]

        ans,mod = bigInt.__floordiv_util__(num1, num2)
        ans = bigInt(ans)

        if sign1 != sign2:
            ans.number = '-' + ans.number[1:]
        else:
            ans.number = '+' + ans.number[1:]
        
        if sign1!=sign2:
            if num1!='0' and mod:
                ans+=bigInt('-1')
        return ans
        
    # def __mod__(self,other):
    #     sign1 = self.number[0]
    #     sign2  = other.number[0]

    #     num1 = self.number[1:]
    #     num2 = other.number[1:]
    #     # base case
    #     if num1 == '0':
    #         return self
    #     ans, mod = bigInt.__floordiv_util__(num1,num2)
    #     small = bigInt.isSmaller(num1,num2)
    #     if sign2 == '-':
    #         mod = -mod
    #     if small:
    #         if sign1 == '+' and sign2 == '-':
    #             mod = -7 - mod
    #         elif sign1 == '-' and sign2 == '+':
    #             mod = 7 - mod
    #     return bigInt(str(mod))

# =========Comparison Operators======== #


    def __lt__(self, other):
        sign1 = self.number[0]
        sign2 = other.number[0]

        num1 = self.number[1:]
        num2 = other.number[1:]

        ans = False
        reverse = False

        if sign1 == '-' and sign2 == '+':
            return True
        elif sign1 == '+' and sign2 == '-':
            return False
        elif sign1 == '-' and sign2 == '-':
            if num1 == num2:
                return False
            return not self.isSmaller(num1, num2)
        else:
            if num1 == num2:
                return False
            return self.isSmaller(num1, num2)

        if reverse:
            return not ans
        return ans

    def __eq__(self, other):
        sign1 = self.number[0]
        sign2 = other.number[0]

        num1 = self.number[1:]
        num2 = other.number[1:]

        if sign1 != sign2:
            return False
        else:
            if num1 == num2:
                return True
            return False

    def __ne__(self, other):
        return not self == other

    def __le__(self, other):
        if self < other or self == other:
            return True
        return False

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        if self > other or self == other:
            return True
        return False



# for i in range(10):
#     a = random.randint(-10, 10)
#     b = random.randint(-10, 10)

#     a1 = bigInt(str(a))
#     b1 = bigInt(str(b))
# # #     if((a >= b) != (a1 >= b1)):
#     print(f"{a},{b} === {a1.number},{b1.number}")
# # #     # print(str((a+b)) == (a1+b1).number)
# # #     print((a+b),(a1+b1).number)
#     print(a//b,(a1//b1).number)

# print((bigInt('-7')%bigInt('-2')).number,'==',-7%-2)
# print((bigInt('+7')%bigInt('+2')).number,'==',+7%+2)
# print((bigInt('+7')%bigInt('-2')).number,'==',+7%-2)
# print((bigInt('-7')%bigInt('+2')).number,'==',-7%+2)

# print((bigInt('-2')%bigInt('-2')).number,'==',-2%-2)
# print((bigInt('+2')%bigInt('+2')).number,'==',+2%+2)
# print((bigInt('-2')%bigInt('+2')).number,'==',-2%+2)
# print((bigInt('+2')%bigInt('-2')).number,'==',+2%-2)

# print((bigInt('-2')%bigInt('-7')).number,'==',-2%-7)
# print((bigInt('+2')%bigInt('+7')).number,'==',+2%+7)
# print((bigInt('+2')%bigInt('-7')).number,'==',+2%-7)
# print((bigInt('-2')%bigInt('+7')).number,'==',-2%+7)
# print((bigInt('-0')%bigInt('-7')).number, '==',-0%-2)
# print((bigInt('+0')%bigInt('+7')).number,'==',+0%+7)
# print((bigInt('+0')%bigInt('-7')).number,'==',+0%-7)
# print((bigInt('-0')%bigInt('+7')).number,'==',-0%+7)

# print((bigInt('-7')//bigInt('-1')).number, '==', -7//-1)
# print((bigInt('+7')//bigInt('+1')).number, '==', +7//+1)
# print((bigInt('+7')//bigInt('-1')).number, '==', +7//-1)
# print((bigInt('-7')//bigInt('+1')).number, '==', -7//+1)

# a = bigInt('-1')
# b = bigInt('-1')
# print((a+b).number)
