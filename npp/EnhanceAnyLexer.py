# -*- coding: utf-8 -*-
'''
    Provides additional color options and should be used in conjunction with 
    either an built-in or an user defined lexer.
    An indicator is used to avoid style collisions.
    Although the Scintilla documentation states that indicators 0-7 are reserved for the lexers,
    indicator 0 is used. Change self.INDICATOR_ID if there is a problem.
    
    Even when using more than one regex, it is not necessary to define more than one indicator
    because the class uses the flag SC_INDICFLAG_VALUEFORE.
    See https://www.scintilla.org/ScintillaDoc.html#Indicators for more information on that topic

'''
import sys
from Npp import (notepad, editor, editor1, editor2,
                 NOTIFICATION, SCINTILLANOTIFICATION,
                 INDICATORSTYLE, INDICFLAG, INDICVALUE)

if sys.version_info[0] == 2:
    from collections import OrderedDict as _dict
else:
    _dict = dict

                       
class EnhanceLexer:

    def __init__(self):
        '''
            Initialize the class, should be called once only.
        '''
        
        current_version = notepad.getPluginVersion()
        if  current_version < '1.5.4.0':
            notepad.messageBox('It is needed to run PythonScript version 1.5.4.0 or higher', 
                               'Unsupported PythonScript verion: {}'.format(current_version))
            return
        
        self.INDICATOR_ID = 0
        self.registered_lexers = _dict()
        
        self.document_is_of_interest = False
        self.lexer_name = ''
        
        self.regexes = _dict()
        self.excluded_styles = []
        
        editor1.indicSetStyle(self.INDICATOR_ID, INDICATORSTYLE.TEXTFORE)
        editor1.indicSetFlags(self.INDICATOR_ID, INDICFLAG.VALUEFORE)
        editor2.indicSetStyle(self.INDICATOR_ID, INDICATORSTYLE.TEXTFORE)
        editor2.indicSetFlags(self.INDICATOR_ID, INDICFLAG.VALUEFORE)
        
        editor.callbackSync(self.on_updateui, [SCINTILLANOTIFICATION.UPDATEUI])
        editor.callbackSync(self.on_marginclick, [SCINTILLANOTIFICATION.MARGINCLICK])
        notepad.callback(self.on_langchanged, [NOTIFICATION.LANGCHANGED])
        notepad.callback(self.on_bufferactivated, [NOTIFICATION.BUFFERACTIVATED])
        

    @staticmethod
    def rgb(r, g, b):
        '''
            Helper function
            Retrieves rgb color triple and converts it
            into its integer representation

            Args:
                r = integer, red color value in range of 0-255
                g = integer, green color value in range of 0-255
                b = integer, blue color value in range of 0-255
            Returns:
                integer
        '''
        return (b << 16) + (g << 8) + r


    def register_lexer(self, lexer_name, _regexes, excluded_styles):
        '''
            reformat provided regexes and cache everything
            within registered_lexers dictionary.

            Args:
                lexer_name = string, expected values as returned by notepad.getLanguageName
                                without the "udf - " if it is an user defined language
                _regexes = dict, in the form of
                                _regexes[(int, (r, g, b))] = (r'', [int])
                excluded_styles = list of integers
            Returns:
                None
        '''
        regexes = _dict()
        for k, v in _regexes.items():
            regexes[(k[0], self.rgb(*k[1]) | INDICVALUE.BIT)] = v
        self.registered_lexers[lexer_name.lower()] = (regexes, excluded_styles)


    def paint_it(self, color, match_position, length, start_position, end_position):
        '''
            This is where the actual coloring takes place.
            Color, the position of the first character and
            the length of the text to be colored must be provided.
            Coloring occurs only if the character at the current position 
            has not a style from the excluded styles list assigned.

            Args:
                color = integer, expected in range of 0-16777215
                match_position = integer,  denotes the start position of a match
                length = integer, denotes how many chars need to be colored.
                start_position = integer,  denotes the start position of the visual area
                end_position = integer,  denotes the end position of the visual area
            Returns:
                None
        '''
        if (match_position + length < start_position or
            match_position > end_position or
            editor.getStyleAt(match_position) in self.excluded_styles):
            return

        editor.setIndicatorCurrent(0)
        editor.setIndicatorValue(color)
        editor.indicatorFillRange(match_position, length)


    def style(self):
        '''
            Calculates the text area to be searched for in the current document.
            Calls up the regexes to find the position and
            calculates the length of the text to be colored.
            Deletes the old indicators before setting new ones.
            
            Args:
                None
            Returns:
                None
        '''
        
        start_line = editor.docLineFromVisible(editor.getFirstVisibleLine())
        end_line = editor.docLineFromVisible(start_line + editor.linesOnScreen())
        if editor.getWrapMode():
            end_line = sum([editor.wrapCount(x) for x in range(end_line)])

        onscreen_start_position = editor.positionFromLine(start_line)
        onscreen_end_pos = editor.getLineEndPosition(end_line)

        editor.setIndicatorCurrent(0)
        editor.indicatorClearRange(0, editor.getTextLength())
        for color, regex in self.regexes.items():
            editor.research(regex[0],
                            lambda m: self.paint_it(color[1],
                                                    m.span(regex[1])[0],
                                                    m.span(regex[1])[1] - m.span(regex[1])[0],
                                                    onscreen_start_position,
                                                    onscreen_end_pos),
                            0,
                            onscreen_start_position,
                            onscreen_end_pos)

    def check_lexers(self):
        '''
            Checks if the current document of each view is of interest
            and sets the flag accordingly

            Args:
                None
            Returns:
                None
        '''
        
        current_language = notepad.getLanguageName(notepad.getLangType()).replace('udf - ','').lower()
        self.document_is_of_interest = current_language in self.registered_lexers
        if self.document_is_of_interest:
            self.regexes, self.excluded_styles = self.registered_lexers[current_language]
            


    def on_marginclick(self, args):
        if args['margin'] == 2 and self.document_is_of_interest :
            self.style()


    def on_bufferactivated(self, args):
        '''
            Callback which gets called every time one switches a document.
            Triggers the check if the document is of interest.

            Args:
                provided by notepad object but none are of interest
            Returns:
                None
        '''
        self.check_lexers()


    def on_updateui(self, args):
        '''
            Callback which gets called every time scintilla
            (aka the editor) changed something within the document.

            Triggers the styling function if the document is of interest.

            Args:
                provided by scintilla but none are of interest
            Returns:
                None
        '''
        if self.document_is_of_interest:
            self.style()


    def on_langchanged(self, args):
        '''
            Callback gets called every time one uses the Language menu to set a lexer
            Triggers the check if the document is of interest

            Args:
                provided by notepad object but none are of interest
            Returns:
                None
        '''
        self.check_lexers()


    def main(self):
        '''
            Main function entry point.
            Simulates two events to enforce detection of current document
            and potential styling.

            Args:
                None
            Returns:
                None
        '''
        self.on_bufferactivated(None)
        self.on_updateui(None)



# Usage:
#
#   Only the active document and for performance reasons, only the currently visible area
#   is scanned and colored.
#   This means, that a regular expression match is assumed to reflect only one line of code 
#   and not to extend over multiple lines.
#   As an illustration, in python one can define, for example, a function like this
#
#       def my_function(param1, param2, param3, param4):
#           pass
#
#   but it is also valid to define it like this
#
#       def my_function(param1, 
#                       param2,
#                       param3, 
#                       param4):
#           pass
#
#   Now, if a regular expression like "(?:(?:def)\s\w+)\s*\((.+)\):" were used to color all parameters,
#   then this would only work as long as the line "def my_function(param1," is visible.
#
#   A possible approach to avoid this would be to define an offset range.
#
#   offset_start_line = start_line - offset
#   if offset_start_line < 0 then offset_start_line = 0
#   
#   Not sure if this is the best approach - still investigating.
#
# Definition of colors and regular expressions
#   Note, the order in which a regular expressions will be processed is determined by its creation,
#   that is, the first definition is processed first, then the 2nd, and so on
#
#   The basic structure always looks like this
#
#       regexes[(a, b)] = (c, d)
#
#
#   regexes = an ordered dictionary which ensures that the regular expressions 
#             are always processed in the same order. 
#   a = an unique number - suggestion, start with 0 and always increase by one (per lexer)
#   b = color tuple in the form of (r,g,b). Example (255,0,0) for the color red.
#   c = raw byte string, describes the regular expression. Example r'\w+'
#   d = integer, denotes which match group should be considered

# Example
# builtin lexers - like python
py_regexes = _dict()

# cls and self objects - return match 0
py_regexes[(0, (224, 108, 117))] = (r'\b(cls|self)\b', 0)
# function parameters - return match 1
py_regexes[(1, (209, 154, 102))] = (r'(?:(?:def)\s\w+)\s*\((.+)\):', 1)
# args and kwargs - return match 0
py_regexes[(2, (86, 182, 194))]  = (r'(\*|\*\*)(?=\w)', 0)
# functions and class instances but not definitions - return match 1
py_regexes[(3, (79, 175, 239))]  = (r'class\s*\w+?(?=\()|def\s*\w+?(?=\()|(\w+?(?=\())', 1)
# dunder functions and special keywords - return match 0
py_regexes[(4, (86, 182, 194))]  = (r'\b(editor|editor1|editor2|notepad|console|__\w+__|super|object|type|print)\b', 0)

# There is no standardization in defining the style IDs of lexers attributes,
# hence one has to check the stylers.xml (or THEMENAME.xml) to see which
# IDs are defined by the respective lexer and what its purposes are to 
# create an list of style ids which shouldn't be altered.
py_excluded_styles = [1, 3, 4, 6, 7, 12, 16, 17, 18, 19]

# user defined lexers
# Definition of which area should not be styled
# 0 = default style
# 1 = comment style
# 2 = comment line style
# 3 = numbers style
# 4 = keyword1 style
# ...
# 11 = keyword8 style
# 12 = operator style
# 13 = fold in code 1 style
# 14 = fold in code 2 style
# 15 = fold in comment style
# 16 = delimiter1 style
# ...
# 23 = delimiter8 style
# excluded_styles = [1, 2, 16, 17, 18, 19, 20, 21, 22, 23]

md_regexes = _dict()
# single underscores
md_regexes[(0, (224, 108, 117))] = (r'_.*?_', 0)
# double underscores but only the word part
md_regexes[(1, (209, 154, 102))] = (r'__(.*?)__', 1)

md_excluded_styles = [1, 2, 16, 17, 18, 19, 20, 21, 22, 23]

_enhance_lexer = EnhanceLexer()

_enhance_lexer.register_lexer('python', py_regexes, py_excluded_styles)
_enhance_lexer.register_lexer('Markdown (Default)', md_regexes, md_excluded_styles)

# start
_enhance_lexer.main()