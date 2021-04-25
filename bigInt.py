import random
import warnings


class bigInt():

    def __init__(self, number):
        if len(number) == 0:
            raise Exception("Number cannot be empty")

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
            ans = ''
            if self.isSmaller(num1, num2):
                l1, l2 = l2, l1
                sign1, sign2 = sign2, sign1
                num1, num2 = num2, num1
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
            return bigInt(sign1+ans)

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
#     if((a >= b) != (a1 >= b1)):
#         print(f"{a},{b} === {a1.number},{b1.number}")
#     # print(str((a+b)) == (a1+b1).number)
#     print((a+b),(a1+b1).number)
#     print(a-b,(a1-b1).number)

x1 = bigInt('-10')
x2 = bigInt('-7')
print((x1-x2).number)
