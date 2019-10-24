import sys
import time


class Solution:
    def __init__(self):
        self.max_matched = 0
        self.couple_set = []

    def __str__(self):
        text_result = []
        for s in self.couple_set:
            text_result.append("{} - {}".format(s[0], s[1]))
        return ", ".join(text_result)

    def get_max_matched(self):
        return self.max_matched

    def add(self, first, second, count):
        if count < self.max_matched:
            return
        elif count > self.max_matched:
            self.max_matched = count
            self.couple_set.clear()

        self.couple_set.append((first + 1, second + 1))  # +1은 index 보정값, 0부터 시작이냐 1부터 시작이냐


solution = Solution()
dic = {}


def process_one_row(loop, offset):
    basis = loop[0]
    solution.add(offset, offset + 1, count_set_bits(basis & loop[1]))
    # print("basis ({}, {}) - count({}) start".format(basis, loop[1], matched_max))

    for i in range(2, len(loop)):
        matched_value = basis & loop[i]
        matched_count = count_set_bits(matched_value)
        # print("{} : ({}, {}) - count({})".format(i, basis, loop[i], matched_count))
        if matched_count >= solution.get_max_matched():
            solution.add(offset, i + offset, matched_count)

    return solution


def find_best_couple(hobbys):
    for i in range(len(hobbys) - 1):
        process_one_row(hobbys[i:], i)

    print(solution)


# http://graphics.stanford.edu/~seander/bithacks.html#CountBitsSetTable
POPCOUNT_TABLE16 = [0] * 2 ** 16
for index in range(len(POPCOUNT_TABLE16)):
    POPCOUNT_TABLE16[index] = (index & 1) + POPCOUNT_TABLE16[index >> 1]


def count_set_bits(v):
    return (POPCOUNT_TABLE16[v & 0xffff] +
            POPCOUNT_TABLE16[(v >> 16) & 0xffff])


def convert_numeric(characters):
    value = 0
    for c in characters:
        value |= 1 << ord(c) - ord('A')
    return value


def print_result(set_values):
    couples_result = []
    for couples in set_values:
        for i in range(len(couples) - 1):
            basis = couples[i]
            for j in range(i + 1, len(couples)):
                couples_result.append("{} - {}".format(basis, couples[j]))
    print(", ".join(couples_result))


def load_data(filename):
    with open(filename) as raw_data:
        lines = raw_data.readlines()

    count = lines[0].rstrip()
    print("loaded the {} data".format(count))

    perfect = {}
    list_hobby = []
    global dic

    for line in lines[1:]:
        characters = line.rstrip().split(" ")
        numeric_value = convert_numeric(characters)
        list_hobby.append(numeric_value)

        if dic.get(numeric_value) is None:
            dic[numeric_value] = [len(list_hobby)]
        else:
            dic[numeric_value].append(len(list_hobby))
            perfect[numeric_value] = dic.get(numeric_value)

    # print("original", list_hobby)

    if len(perfect) > 0:
        print_result(perfect.values())
    else:
        del perfect
        del dic
        find_best_couple(list_hobby)


if __name__ == '__main__':
    if len(sys.argv) is 1:
        print("No data")
        sys.exit(0)

    start_time = time.perf_counter()

    load_data(sys.argv[1])

    finish_time = time.perf_counter()
    print(f'Finished in {round(finish_time - start_time, 2)} seconds(s)')
