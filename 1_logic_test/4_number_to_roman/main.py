"""
เขียบนโปรแกรมแปลงตัวเลยเป็นตัวเลข roman

[Input]
number: list of numbers

[Output]
roman_text: roman number

[Example 1]
input = 101
output = CI

[Example 2]
input = -1
output = number can not less than 0
"""


class Solution:

    def number_to_roman(self, number: int) -> str:
        roman_numerals = {
            1: 'I',
            4: 'IV',
            5: 'V',
            9: 'IX',
            10: 'X',
            40: 'XL',
            50: 'L',
            90: 'XC',
            100: 'C',
            400: 'CD',
            500: 'D',
            900: 'CM',
            1000: 'M'
        }

        roman_text = ''
        if number < 0:
            return "number can not less than 0"
        for value in sorted(roman_numerals.keys(), reverse=True):
            while number >= value:
                roman_text += roman_numerals[value]
                number -= value
        return roman_text
    
def main():
    solution = Solution()
    user_input = input("Input number: ").strip()

    if not user_input:
        print("number can not blank")
        return

    try:
        user_input = int(user_input)
        print("Output = " + solution.number_to_roman(user_input))
    except ValueError:
        print("number must be an integer")

if __name__ == "__main__":
    main()
