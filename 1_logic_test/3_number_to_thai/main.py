"""
เขียบนโปรแกรมแปลงตัวเลยเป็นคำอ่านภาษาไทย

[Input]
number: positive number rang from 0 to 10_000_000

[Output]
num_text: string of thai number call

[Example 1]
input = 101
output = หนึ่งร้อยเอ็ด

[Example 2]
input = -1
output = number can not less than 0
"""


class Solution:
    def number_to_thai(self, number: int) -> str:
        if number < 0:
            return "number can not less than 0"
        if number > 10000000:
            return "number can not more than 10,000,000"
        if number == 0:
            return "ศูนย์"
        if number == 10000000:
            return "สิบล้าน"

        th_digits = ["", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
        th_positions = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน"]

        num_str = str(number)
        length = len(num_str)
        num_text = ""

        for i in range(length):
            digit = int(num_str[i])
            position = length - i - 1 

            if digit == 0:
                continue

            if position == 1:
                if digit == 1:
                    num_text += "สิบ"
                elif digit == 2:
                    num_text += "ยี่สิบ"
                else:
                    num_text += th_digits[digit] + "สิบ"
            elif position == 0:
                if length > 1 and digit == 1:
                    num_text += "เอ็ด"
                else:
                    num_text += th_digits[digit]
            else:
                num_text += th_digits[digit] + th_positions[position]

        return "Output = " + num_text


def main():
    solution = Solution()
    raw_input = input("Input number: ").strip()

    if not raw_input:
        print("number can not blank")
        return

    try:
        user_input = int(raw_input)
        print(solution.number_to_thai(user_input))
    except ValueError:
        print("number must be an integer")


if __name__ == "__main__":
    main()