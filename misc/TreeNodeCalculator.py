# -*- coding: utf-8 -*-
'''
    TreeNodeCalculator scans a tree-like text and sums up the items.
    The folder-like lines are not counted.
    Number of items is added on position 80 on each folder-like line.
    It is assumed that the data is 
        a) using either space or tabs doing the intend but NOT mixed ones
        b) one root node in a document
        c) items are only in the last level and NOT in between.
'''
from Npp import editor

# example test data
# root
    # level1
        # item1
        # item2
    # level1
        # level2
            # item3
            # item4
        # level2
            # level3
                # item5
                # item6
    # level1
        # item7
        # item8

# would be modified to

# root                                                                            8
    # level1                                                                      2
        # item1
        # item2
    # level1                                                                      4
        # level2                                                                  2
            # item3
            # item4
        # level2                                                                  2
            # level3                                                              2
                # item5
                # item6
    # level1                                                                      2
        # item7
        # item8

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

    def add(self):
        '''
            add the current found item and call its parents recursively
        '''
        if self.parent:
            self.parent.add()
        self.items += 1

    def result(self):
        '''
            return the calculated items for each parent together with the parent line
        '''
        if self.parent:
            self.parent.result()
        return self.line, self.items


# Calculate the level
def get_level(line): return len(line) - len(line.lstrip())


lines = editor.getText().splitlines()
max_lines = len(lines)-1
current_line = 0
level_stack = []
save_popped_levels = []

# loop through all lines and build the needed Node objects
while current_line < max_lines:
    if lines[current_line].strip() != '':
        current_level = get_level(lines[current_line])

        if current_level >= get_level(lines[current_line+1]):
            level_stack[-1][0].add()
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
        level_stack[-1][0].add()

# create a list of all Node objects
results = [x[0].result() for x in level_stack]
results.extend([x[0].result() for x in save_popped_levels])

# reformat the resulting content
for line, _sum in sorted(results):
    lines[line] = '{0:<{1}}{2}'.format(lines[line][:80],
                                       80, 
                                       _sum)
# set the new content
editor.setText('\r\n'.join(lines))
