from Npp import editor
import re

# it is assumed that chords and text is correctly aligned
# and that the ordering is always one line of chords followed by one line of lyric
# reformats from 
#       A    B       C
#       Some text to sing
# to
# [A]Some [B] text to [C] sing

in_text_line = False
new_content = ''
chords = []

for line in editor.getText().splitlines():

    if line.strip():  # skip empty lines
        
        if in_text_line:
            
            if len(chords) == 1:
                new_content += '[{0}]{1}\r\n'.format(chords[0][1], line)
            else:
                for i, chord in enumerate(chords[:-1]):
                    _line = line[chords[i][0][0]:chords[i+1][0][0]]
                    new_content += '[{0}]{1} '.format(chords[i][1], _line).replace('[]','')
                    
                # last element in list
                _line = line[chords[-1][0][0]:]
                new_content += '[{0}]{1}\r\n'.format(chords[-1][1], _line).replace('[]','')

            # next line must be a chord line
            chords = []  # .clear()
            in_text_line = False
            
        else:  # in chord lines
            chords = [(m.span(), m.group()) for m in re.finditer('[^ ]+', line)]
            # add a dummy entry if the chord does not start at the beginning of the line
            if chords[0][0][0] > 0:
                chords.insert(0, ((0,0), ''))
            # next line must be a text line
            in_text_line = True
        
editor.setText(new_content)