"""
เขียบนโปรแกรมหา index ของตัวเลขที่มีค่ามากที่สุดใน list

[Input]
numbers: list of numbers

[Output]
index: index of maximum number in list

[Example 1]
input = [1,2,1,3,5,6,4]
output = 5

[Example 2]
input = []
output = list can not blank
"""


class Solution:

    def find_max_index(self, numbers: list) -> int | str:
        max_index = 0
        for i in range(1, len(numbers)):
            if numbers[i] > numbers[max_index]:
                max_index = i
        return max_index

def main():
    solution = Solution()
    user_input = input("List of Numbers with comma-separated: ").strip()

    if not user_input:
        print("list can not blank")
    else:
        numbers = [int(x) for x in user_input.split(",")]
        print(solution.find_max_index(numbers))

if __name__ == "__main__":
    main()
