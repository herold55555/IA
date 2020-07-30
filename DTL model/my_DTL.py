import math


def get_classification(line):
    values = line.split('\t')
    size = len(values)
    return values[size - 1]


class DTL:
    train = None
    test = None
    my_first_line = None

    def __init__(self, a_train, a_test):
        self.my_first_line = a_train[len(a_train) - 1]
        a_train.pop(len(a_train) - 1)
        self.train = a_train
        self.test = a_test

    def next_node(self):
        attr_line = self.my_first_line.split('\t')
        first_line = attr_line
        list_of_attr_kinds = list()
        for _ in range(len(attr_line) - 1):
            list_of_attr_kinds.append(list())
        num_of_line = 0
        num_of_positive = 0
        # loop to retrieve informations about the train data, e.g num of lines and positive lines
        for line in self.train:
            if len(line) == 0 or line == '':
                continue
            num_of_line = num_of_line + 1
            attr_line = line.split('\t')
            if attr_line[len(attr_line) - 1] == "yes":
                num_of_positive = num_of_positive + 1
            # if an attribute not in our list of attributes add it
            for i in range(len(list_of_attr_kinds)):
                if attr_line[i] not in list_of_attr_kinds[i]:
                    list_of_attr_kinds[i].append(attr_line[i])
        # sorting in alphabetical order
        for attr_list in list_of_attr_kinds:
            attr_list.sort()
        yes_porportion = num_of_positive / num_of_line
        no_proportion = (num_of_line - num_of_positive) / num_of_line
        log_yes = math.log10(yes_porportion) / math.log10(2)
        log_no = math.log10(no_proportion) / math.log10(2)
        entropy = -yes_porportion * log_yes - no_proportion * log_no
        mini_entropy = [None] * (len(attr_line) - 1)
        for i in range(len(mini_entropy)):
            mini_entropy[i] = self.pre_gain(None, None, list_of_attr_kinds[i], i)
        gain = [None] * len(list_of_attr_kinds)
        for i in range(len(list_of_attr_kinds)):
            gain[i] = entropy - mini_entropy[i]
        max_gain = gain[0]
        place_of_dominating_gain = 0
        for i in range(len(gain)):
            if gain[i] > max_gain:
                max_gain = gain[i]
                place_of_dominating_gain = i
        for i in range(len(list_of_attr_kinds[place_of_dominating_gain])):
            try:
                with open('output.txt', 'a') as f:
                    f.write(first_line[place_of_dominating_gain] + '=' + list_of_attr_kinds[place_of_dominating_gain][i])
            except:
                print('FILE DONT OPEN')
            my_list = list()
            my_list.append(first_line[place_of_dominating_gain])
            self.do_dtl_total(None, None, list_of_attr_kinds[place_of_dominating_gain][i], my_list, list_of_attr_kinds, 0)
            try:
                with open('output.txt', 'a') as f:
                    f.write('\n')
            except:
                print('FILE DONT OPEN')
        try:
            with open('output.txt', 'a') as f:
                f.write('\n')
        except:
            print('FILE DONT OPEN')

    def look_for_leaf(self):
        lines_of_tree = list()
        with open('output.txt', 'r+') as f:
            data = f.read()
            lines_of_output = data.split('\n')
        for line in lines_of_output:
            if len(line) == 0 or line == '':
                break
            lines_of_tree.append(line)
        dtl_pred = list()
        first_line = self.my_first_line.split('\t')
        for line in self.test:
            if len(line) == 0 or line == '':
                continue
            line_attr = line.split('\t')
            down_with_value = list()
            depth = 0
            do_skip = False
            jump_over_this_deep = -1
            for line_on_tree in lines_of_tree:
                if len(line_on_tree) == 0 or line_on_tree == '':
                    continue
                if depth == 0:
                    down_with_value = line_on_tree.split('=')
                else:
                    line_attr_on_tree = line_on_tree.split('\\|')
                    if len(line_attr_on_tree[0]) == len(line_on_tree):
                        jump_over_this_deep = -1
                        do_skip = False
                        depth = 0
                        down_with_value = line_attr_on_tree[0].split('=')
                    elif jump_over_this_deep != len(line_attr_on_tree[0]) and do_skip:
                        continue
                    else:
                        down_with_value = line_attr_on_tree[1].split('=')
                spot_of_factor = 0
                for i in range(len(line_attr) - 1):
                    if first_line[i] == down_with_value[0]:
                        spot_of_factor = i
                        break
                attr_with_answer = down_with_value[1].split(':')
                if not attr_with_answer[0] == down_with_value[1]:
                    if attr_with_answer[0] == line_attr[spot_of_factor]:
                        dtl_pred.append(attr_with_answer[1])
                        break
                else:
                    depth = depth + 1
                    if not down_with_value[1] == line_attr[spot_of_factor]:
                        if not do_skip:
                            jump_over_this_deep = depth - 1
                        do_skip = True
                    else:
                        do_skip = False
        return dtl_pred

    def do_dtl_total(self, previous_branches, attr_previous_branches, new_branch, name_attr, list_of_attr_kinds, depth):
        num_of_positive = 0
        num_total = 0
        first_line = self.my_first_line.split('\t')
        new_previous_branch = list()
        new_attr_previous_branch = list()
        if previous_branches is not None:
            for branches in previous_branches:
                new_previous_branch.append(branches)
            for attr in attr_previous_branches:
                new_attr_previous_branch.append(attr)
        new_previous_branch.append(new_branch)
        new_attr_previous_branch.append(name_attr[len(name_attr) - 1])
        num_line = 0
        for line in self.train:
            if len(line) == 0 or line == '':
                continue
            num_line = num_line + 1
            attr_line = line.split('\t')
            counter = 0
            for i in range(len(attr_line) - 1):
                for j in range(len(new_previous_branch)):
                    if first_line[i] == name_attr[j]:
                        if attr_line[i] == new_previous_branch[j]:
                            counter = counter + 1
            if len(new_previous_branch) == counter:
                num_total = num_total + 1
                if attr_line[len(attr_line) - 1] == 'yes':
                    num_of_positive = num_of_positive + 1
        # case 2 : all the examples have the same classification => return the classification
        if num_total != 0 and num_of_positive == num_total:
            with open('output.txt', 'a') as f:
                f.write(':' + 'yes')
        elif num_total != 0 and num_of_positive == 0:
            with open('output.txt', 'a') as f:
                f.write(':' + 'no')
        elif num_total == 0 and previous_branches is not None:
            counter2 = 0
            line_attr = self.my_first_line.split('\t')
            for line in self.train:
                if len(line) == 0 or line == '':
                    continue
                attr_line = line.split('\t')
                for i in range(len(previous_branches)):
                    for j in range(len(attr_line) - 1):
                        if attr_line[j] == previous_branches[i] and line_attr[j] == attr_previous_branches[i]:
                            counter2 = counter2 + 1
                if len(previous_branches) <= counter2:
                    num_total = num_total + 1
                    if attr_line[len(attr_line) - 1] == 'yes':
                        num_of_positive = num_of_positive + 1
            if num_of_positive >= num_total - num_of_positive:
                with open('output.txt', 'a') as f:
                    f.write(':' + 'yes')
            else:
                with open('output.txt', 'a') as f:
                    f.write(':' + 'no')
        # case3 : attributes is empty => returning the majority class
        elif len(new_previous_branch) == len(list_of_attr_kinds):
            if num_of_positive >= num_total - num_of_positive:
                with open('output.txt', 'a') as f:
                    f.write(':' + 'yes')
            else:
                with open('output.txt', 'a') as f:
                    f.write(':' + 'no')
        # case4: Selecting the dominating Attribute and apply doDtl to all of its value
        else:
            size_of_new_array = len(list_of_attr_kinds) - len(new_previous_branch)
            remain_attr = list()
            for _ in range(size_of_new_array):
                remain_attr.append(list())
            name_remain_attr = list()
            place_of_remain_attr = [0] * len(remain_attr)
            k = 0
            for i in range(len(first_line) - 1):
                for j in range(len(name_attr)):
                    if first_line[i] not in name_attr:
                        for att in list_of_attr_kinds[i]:
                            remain_attr[k].append(att)
                        place_of_remain_attr[k] = i
                        k = k + 1
                        break
            entropy = 0
            if num_of_positive == num_total or num_of_positive == 0:
                entropy = 0
            else:
                yes_proportion = num_of_positive / num_total
                no_proportion = (num_total - num_of_positive) / num_total
                log_yes = math.log10(yes_proportion) / math.log10(2)
                log_no = math.log10(no_proportion) / math.log10(2)
                entropy = -yes_proportion * log_yes - no_proportion * log_no
            mini_entropy = [0] * len(remain_attr)
            for i in range(len(mini_entropy)):
                mini_entropy[i] = self.pre_gain(new_previous_branch, new_attr_previous_branch,
                                                remain_attr[i], place_of_remain_attr[i])
            gain = [0] * len(remain_attr)
            for i in range(len(gain)):
                gain[i] = entropy - mini_entropy[i]
            max_gain = gain[0]
            place_of_dominating_gain = 0
            for i in range(len(gain)):
                if gain[i] > max_gain:
                    max_gain = gain[i]
                    place_of_dominating_gain = i
            remain_name = list()
            for i in range(len(first_line)):
                remain_name.append(first_line[i])
            for i in range(len(new_attr_previous_branch)):
                if new_attr_previous_branch[i] in remain_name:
                    remain_name.remove(new_attr_previous_branch[i])
            for i in range(len(remain_attr[place_of_dominating_gain])):
                with open('output.txt', 'a') as f:
                    f.write('\n')
                    for j in range(depth + 1):
                        f.write('\t')
                    f.write('|' + first_line[place_of_remain_attr[place_of_dominating_gain]] + '='
                            + remain_attr[place_of_dominating_gain][i])
                name_attr.append(remain_name[place_of_dominating_gain])
                self.do_dtl_total(new_previous_branch, new_attr_previous_branch,
                                  remain_attr[place_of_dominating_gain][i], name_attr, list_of_attr_kinds, depth + 1)
                name_attr.remove(remain_name[place_of_dominating_gain])

    def pre_gain(self, decision, attr_decision, type_of_an_attr, index_in_line_attr):
        w, h = 2, len(type_of_an_attr)
        mini_entropies = [[0 for x in range(w)] for y in range(h)]
        num_kind_of_a_attribut = list()
        for i in range(len(type_of_an_attr)):
            num_kind_of_a_attribut.append(0)
        attr_num_lines = 0
        for i in range(len(type_of_an_attr)):
            mini_entropies[i] = self.calculate_entropy(decision, attr_decision, type_of_an_attr[i], index_in_line_attr)
        total = 0
        for i in range(len(type_of_an_attr)):
            total = total + mini_entropies[i][1]
        pre_attributes_gain = 0
        for i in range(len(mini_entropies)):
            pre_attributes_gain = pre_attributes_gain + ((mini_entropies[i][1] / total) * mini_entropies[i][0])
        return pre_attributes_gain

    def calculate_entropy(self, decision, attr_decision, value_of_attribute, index_in_line_attr):
        count_yes_on_attribute = 0
        count_no_on_attribute = 0
        entrop = [0] * 2
        line_attr = self.my_first_line.split('\t')
        counter_3 = 0
        for line in self.train:
            if len(line) == 0 or line == '':
                continue
            attr_line = line.split('\t')
            if decision is None:
                if attr_line[index_in_line_attr] == value_of_attribute:
                    if attr_line[len(attr_line) - 1] == 'yes':
                        count_yes_on_attribute = count_yes_on_attribute + 1
                    else:
                        count_no_on_attribute = count_no_on_attribute + 1
            else:
                counter_3 = 0
                for i in range(len(decision)):
                    for j in range(len(attr_line) - 1):
                        if attr_line[j] == decision[i] and line_attr[j] == attr_decision[i]:
                            counter_3 = counter_3 + 1
                if len(decision) == counter_3:
                    if attr_line[index_in_line_attr] == value_of_attribute:
                        if attr_line[len(attr_line) - 1] == 'yes':
                            count_yes_on_attribute = count_yes_on_attribute + 1
                        else:
                            count_no_on_attribute = count_no_on_attribute + 1
        yes_and_no_number = count_yes_on_attribute + count_no_on_attribute
        entrop[1] = yes_and_no_number
        if count_yes_on_attribute == 0 or count_no_on_attribute == 0:
            entrop[0] = 0
        else:
            entrop[0] = -(count_yes_on_attribute / yes_and_no_number) * (
                math.log10(count_yes_on_attribute / yes_and_no_number) / math.log10(2)) - (
                count_no_on_attribute / yes_and_no_number) * (
                math.log10((count_no_on_attribute / yes_and_no_number)) / math.log10(2))
        return entrop

