import my_DTL


line_string_dict = dict()


class KNN:
    k = 0

    def __init__(self, number):
        self.k = number

    def do_knn_total(self, test, train):
        knn_output = list()
        for line in test:
            classi = self.do_knn_for_a_line(line, train)
            knn_output.append(classi)
        return knn_output

    def do_knn_for_a_line(self, line, train):
        count = 0
        values = dict()
        nearest_neighboors = list()
        test_string = create_string(line)
        j = 0
        for train_line in train:
            if len(train_line) == 0 or train_line == '':
                continue
            train_string = create_string(train_line)
            ham_dist = hamming_dist(test_string, train_string)
            values[train_string] = ham_dist
        while len(nearest_neighboors) < 5:
            if len(nearest_neighboors) == 5:
                break
            for line, value in values.items():
                if len(nearest_neighboors) == 5:
                    break
                if value == j:
                    nearest_neighboors.append(line)
            j = j + 1
        for neighboor in nearest_neighboors:
            classification = get_classification(line_string_dict[neighboor])
            if classification == "yes":
                count = count + 1
        if count > (self.k / 2):
            return 'yes'
        else:
            return 'no'


def hamming_dist(input1, input2):
    i = 0
    equalDist = 0
    my_length = len(input1)
    my_second_length = len(input2)
    while i < my_length and i < my_second_length:
        if input1[i] == input2[i]:
            equalDist = equalDist + 1
        i = i + 1
    return my_length - equalDist


def load_data(filename):
    with open(filename, 'r') as my_file:
        data = my_file.read()
        lines = data.split('\n')
    first_line = lines[0]
    lines.pop(0)
    for line in lines:
        if len(line) == 0 or line == '':
            lines.remove(line)
    size = lines.__len__()
    return lines, size, first_line


def create_string(line):
    values = line.split('\t')
    size = len(values)
    my_string = ''
    for i in range(size - 1):
        my_string += values[i]
    line_string_dict[my_string] = line
    return my_string


def get_classification(line):
    values = line.split('\t')
    size = len(values)
    return values[size - 1]


def do_KNN(train_set, test_set):
    my_count = 0
    my_Knn = KNN(5)
    real_value = list()
    knn_pred = my_Knn.do_knn_total(test_set, train_set)
    for line in test_set:
        classi = get_classification(line)
        real_value.append(classi)
    for i in range(len(test_set)):
        if knn_pred[i] == real_value[i]:
            my_count = my_count + 1
    accuracy = my_count / len(test_set)
    with open('output.txt', 'a') as file:
        file.write('\t' + str(accuracy))


def do_NB(train_set, test_set):
    my_count = 0
    real_value = list()
    nb_pred = do_NB_total(train_set, test_set)
    for line in test_set:
        classi = get_classification(line)
        real_value.append(classi)
    for i in range(len(test_set)):
        if nb_pred[i] == real_value[i]:
            my_count = my_count + 1
    accuracy = my_count / len(test_set)
    with open('output.txt', 'a') as file:
        file.write('\t' + str(accuracy) + '\n')


def do_NB_total(train, test):
    num_attr = make_a_count(train)
    nb_pred = list()
    for line in test:
        if len(line) == 0 or line == '':
            continue
        table_counters = do_NB_for_a_line(line, train)
        probabilities = list()
        for _ in range(len(table_counters)):
            probabilities.append(0)
        for i in range(len(num_attr) - 2):
            probabilities[2 * i] = (table_counters[2 * i] + 1) / (num_attr[len(num_attr) - 2] + num_attr[i])
            probabilities[(2 * i) + 1] = (table_counters[(2 * i) + 1] + 1) / (
                    (num_attr[len(num_attr) - 1] - num_attr[len(num_attr) - 2]) + num_attr[i])
        sum_of_yes_prob = 1
        sum_of_no_prob = 1
        for i in range(len(num_attr) - 2):
            sum_of_yes_prob = sum_of_yes_prob * probabilities[2 * i]
            sum_of_no_prob = sum_of_no_prob * probabilities[(2 * i) + 1]
        sum_of_yes_prob = sum_of_yes_prob * (num_attr[len(num_attr) - 2] / num_attr[len(num_attr) - 1])
        sum_of_no_prob = sum_of_no_prob * (
                (num_attr[len(num_attr) - 1] - num_attr[len(num_attr) - 2]) / num_attr[len(num_attr) - 1])
        if sum_of_yes_prob > sum_of_no_prob:
            nb_pred.append("yes")
        else:
            nb_pred.append("no")
    return nb_pred


def do_NB_for_a_line(my_line, train):
    test_att = my_line.split('\t')
    size = len(test_att) - 1
    table_counters = list()
    for i in range(size * 2):
        table_counters.append(0)
    for line in train:
        if len(line) == 0 or line == '':
            continue
        att = line.split('\t')
        if att[len(att) - 1] == 'yes':
            j = 0
            for i in range(len(att) - 1):
                if att[i] == test_att[i]:
                    table_counters[j] = table_counters[j] + 1
                j = j + 2
        else:
            j = 1
            for i in range(len(att) - 1):
                if att[i] == test_att[i]:
                    table_counters[j] = table_counters[j] + 1
                j = j + 2
    return table_counters


def make_a_count(train):
    num_attribut = list()
    num_of_attribut = len(train[0].split('\t'))
    list_of_attr_kinds = list()
    for _ in range(num_of_attribut + 1):
        num_attribut.append(0)
    for _ in range(num_of_attribut - 1):
        list_of_attr_kinds.append(list())
    for line in train:
        if len(line) == 0 or line == '':
            continue
        attr_line = line.split('\t')
        num_attribut[len(num_attribut) - 1] = num_attribut[len(num_attribut) - 1] + 1
        if attr_line[len(attr_line) - 1] == 'yes':
            num_attribut[len(num_attribut) - 2] = num_attribut[len(num_attribut) - 2] + 1
        for i in range(len(attr_line) - 1):
            if attr_line[i] not in list_of_attr_kinds[i]:
                list_of_attr_kinds[i].append(attr_line[i])
    for i in range(num_of_attribut - 1):
        num_attribut[i] = len(list_of_attr_kinds[i])
    return num_attribut


def do_DTL(train_set, test_set, first_line):
    my_count = 0
    real_value = list()
    train_set.append(first_line)
    my_dtl = my_DTL.DTL(train_set, test_set)
    #my_dtl.next_node()
    dtl_pred = my_dtl.look_for_leaf()
    for line in test_set:
        classi = get_classification(line)
        real_value.append(classi)
    for i in range(len(test_set)):
        if dtl_pred[i] == real_value[i]:
            my_count = my_count + 1
    accuracy = my_count / len(test_set)
    with open('output.txt', 'a') as file:
        file.write(str(accuracy))


def main():
    train, train_size, train_first_line = load_data('train.txt')
    test, test_size, test_first_line = load_data('test.txt')
    do_DTL(train, test, train_first_line)
    do_KNN(train, test)
    do_NB(train, test)


main()
