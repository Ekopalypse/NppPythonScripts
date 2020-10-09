# -*- coding: utf-8 -*-
'''
    TreeNodeCalculator scans a tree-like text and sums up the items.
    The folder-like lines are not counted.
    Number of items is added on position 80 on each folder-like line.
    It is assumed that the data is 
        a) using either space or tabs doing the intend but NOT mixed ones
        b) one root node in a document
        c) items are only in the last level and NOT in between.
        
    [Changes since initial version]
    v0.2 - count each occurance if additional filters per line.

'''
from Npp import editor, notepad, MESSAGEBOXFLAGS

# example test data
# work
    # names 1
        # × antonio
        # bernard #
        # joseph
        # alex
        # # francisco
        # suzana
        # × victor
        # amanda #
        # # victoria
        # xxxxx
        # yy # yyy
        # aaaa
    # names 2
        # aaaaa
        # qqqqq #
        # × wwwww
        # a111111
        # b222222
        # c3333 # 33
        # # wwwww
        # wwwww
        # # 1111111 # 12121212 # 5555555 # 323232323 # 444 # 11
    # names 3
        # aaaaa
        # qqqqq
# would be modified to

# work                                                                            (23, 17)
    # names 1                                                                     (12, 7)
        # × antonio
        # bernard #
        # joseph
        # alex
        # # francisco
        # suzana
        # × victor
        # amanda #
        # # victoria
        # xxxxx
        # yy # yyy
        # aaaa
    # names 2                                                                     (9, 10)
        # aaaaa
        # qqqqq #
        # × wwwww
        # a111111
        # b222222
        # c3333 # 33
        # # wwwww
        # wwwww
        # # 1111111 # 12121212 # 5555555 # 323232323 # 444 # 11
    # names 3                                                                     (2, 0)
        # aaaaa
        # qqqqq

class Node:
    '''
        helper class which counts the items and updates the parents recursively.
    '''
    def __init__(self, line, parent=None):
        '''
            store on which line the parent is and initialze the object itself
        '''
        self.line = line
        self.parent = parent
        self.items = 0
        self.additional_flags = 0

    def add(self, additional_flags):
        '''
            add the current found item and call its parents recursively
        '''
        if self.parent:
            self.parent.add(additional_flags)
        self.items += 1
        if additional_flags:
            self.additional_flags += additional_flags

    def result(self):
        '''
            return the calculated items for each parent together with the parent line
        '''
        if self.parent:
            self.parent.result()
        return self.line, self.items, self.additional_flags


# Calculate the level
def get_level(line): return len(line) - len(line.lstrip())


lines = editor.getText().splitlines()
max_lines = len(lines)-1
current_line = 0
level_stack = []
save_popped_levels = []
additional_filters = ['#', '×']

# loop through all lines and build the needed Node objects
while current_line < max_lines:
    if lines[current_line].strip() != '':
        current_level = get_level(lines[current_line])

        if current_level >= get_level(lines[current_line+1]):
            found_additional_filters = [lines[current_line].count(x) for x in additional_filters]
            level_stack[-1][0].add(sum(found_additional_filters))
        else:
            if current_level == 0:
                level_stack = []
                p = Node(current_line, None)
            else:
                while True:
                    if level_stack[-1][1] >= current_level:
                        save_popped_levels.append(level_stack.pop())
                    else:
                        break
                p = Node(current_line, level_stack[-1][0])

            level_stack.append((p, current_level))

    current_line +=1

# last line
prev_level = current_level
if lines[current_line].strip() != '':
    if prev_level == get_level(lines[current_line]):
        found_additional_filters = [lines[current_line].count(x) for x in additional_filters]
        level_stack[-1][0].add(sum(found_additional_filters))

# create a list of all Node objects
results = [x[0].result() for x in level_stack]
results.extend([x[0].result() for x in save_popped_levels])

# reformat the resulting content
if notepad.messageBox('Should additional filtering be applied?',
                      '',
                      MESSAGEBOXFLAGS.YESNO) == MESSAGEBOXFLAGS.RESULTYES:
    for line, _sum, _additional_filters in sorted(results):
        lines[line] = '{0:<{1}}({2}{3}{4})'.format(lines[line][:80],
                                             80, 
                                             _sum,
                                             ', ',
                                             _additional_filters)
else:
    for line, _sum, _ in sorted(results):
        lines[line] = '{0:<{1}}({2})'.format(lines[line][:80],
                                             80, 
                                             _sum)
    
# set the new content
editor.setText('\r\n'.join(lines))
