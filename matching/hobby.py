import sys

list_hobby = []


# dic = {}


def method1(hobbys):
    matched_count = 0
    for i in range(len(hobbys) - 1):
        basis = hobbys[i]
        matched_count = basis & hobbys[i + 1]
        print("{} : ({}, {}) - {}. count({})".format(i, basis, hobbys[i + 1], matched_count,
                                                     count_set_bits(matched_count)))

    # print("list2 :", list_member)


def count_set_bits(n):
    count = 0
    while (n):
        count += n & 1
        n >>= 1
    return count


def convert_numeric(characters):
    value = 0
    for c in characters:
        value |= 1 << ord(c) - ord('A')

    list_hobby.append(value)

    # if dic.get(value) is None:
    #     dic[value] = [len(list_hobby)]
    # else:
    #     dic[value].append(len(list_hobby))


def load_data(filename):
    with open(filename) as raw_data:
        lines = raw_data.readlines()

    count = lines[0].rstrip()
    print("loaded the {} data".format(count))

    for line in lines[1:]:
        characters = line.rstrip().split(" ")
        convert_numeric(characters)
    # print(list_hobby)

    sorted_hobby = list_hobby.copy()
    sorted_hobby.sort()
    print(sorted_hobby)
    method1(sorted_hobby)


if __name__ == '__main__':
    if len(sys.argv) is 1:
        print("No data")
        sys.exit(0)

    load_data(sys.argv[1])
