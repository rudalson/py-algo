import sys
import time

from multiprocessing import Process, Lock, Queue

list_hobby = []


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


def find_one_loop(loop, index_increment):
    basis = loop[0]
    matched_max = count_set_bits(basis & loop[1])
    solution.add(index_increment, index_increment + 1, matched_max)
    # print("basis ({}, {}) - count({}) start".format(basis, loop[1], matched_max))
    for i in range(2, len(loop)):
        matched_value = basis & loop[i]
        matched_count = count_set_bits(matched_value)
        # print("{} : ({}, {}) - count({})".format(i, basis, loop[i], matched_count))
        if matched_count >= solution.get_max_matched():
            solution.add(index_increment, i + index_increment, matched_count)

    return solution


def find_best_couple(hobbys):
    for i in range(len(hobbys) - 1):
        find_one_loop(hobbys[i:], i)
    print(solution)


def find_one_loop_parallel(loop, index_increment, q):
    # solution = Solution()
    solution = q.get()
    basis = loop[0]
    matched_count = numberOfSetBits(basis & loop[1])
    solution.add(index_increment, index_increment + 1, matched_count)
    # print("basis ({}, {}) - count({}) start".format(basis, loop[1], matched_count))
    for i in range(2, len(loop)):
        matched_value = basis & loop[i]
        matched_count = numberOfSetBits(matched_value)
        # print("{} : ({}, {}) - count({})".format(i, basis, loop[i], matched_count))
        if matched_count >= solution.get_max_matched():
            solution.add(index_increment, i + index_increment, matched_count)
    q.put(solution)


def find_best_couple_parallel(hobbys):
    procs = []

    q = Queue()
    q.put(Solution())

    for i in range(len(hobbys) - 1):
        proc = Process(target=find_one_loop_parallel, args=(hobbys[i:], i, q))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    s = q.get()
    print(s)
    # print(solution_manager.get_max_count(), solution_manager.get_couples())


def count_set_bits(n):
    count = 0
    while (n):
        count += n & 1
        n >>= 1
    return count


def numberOfSetBits(i):
    i = i - ((i >> 1) & 0x55555555)
    i = (i & 0x33333333) + ((i >> 2) & 0x33333333)
    return (((i + (i >> 4) & 0xF0F0F0F) * 0x1010101) & 0xffffffff) >> 24


def convert_numeric(characters):
    value = 0
    for c in characters:
        value |= 1 << ord(c) - ord('A')
    return value


def load_data(filename):
    start_time = time.perf_counter()
    with open(filename) as raw_data:
        lines = raw_data.readlines()

    count = lines[0].rstrip()
    print("loaded the {} data".format(count))

    dic = {}
    perfect = {}

    for line in lines[1:]:
        characters = line.rstrip().split(" ")
        numeric_value = convert_numeric(characters)
        list_hobby.append(numeric_value)

        index = len(list_hobby)
        if dic.get(numeric_value) is None:
            dic[numeric_value] = [index]
        else:
            dic[numeric_value].append(index)
            perfect[numeric_value] = dic.get(numeric_value)

    # if len(perfect) > 0:
    #     print_result(perfect.values())
    # else:
    find_best_couple_parallel(list_hobby)
        # find_best_couple(list_hobby)

    finish_time = time.perf_counter()
    print(f'Finished in {round(finish_time - start_time, 2)} seconds(s)')


def print_result(set_values):
    couples_result = []
    for couples in set_values:
        for i in range(len(couples) - 1):
            basis = couples[i]
            for j in range(i + 1, len(couples)):
                couples_result.append("{} - {}".format(basis, couples[j]))
    print(", ".join(couples_result))


if __name__ == '__main__':
    if len(sys.argv) is 1:
        print("No data")
        sys.exit(0)

    load_data(sys.argv[1])