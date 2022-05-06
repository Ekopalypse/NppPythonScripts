# -*- coding: utf-8 -*-
'''
    Makes the builtin errorlist lexer available for npp.
    
    To toggle the escape characters on/off one can
    create another script with these two lines of code.
    
    error_list_lexer.show_escape_chars = not error_list_lexer.show_escape_chars
    editor.styleSetVisible(error_list_lexer.SCE_ERR_ESCSEQ, error_list_lexer.show_escape_chars)

'''

from Npp import notepad, editor, NOTIFICATION
from ctypes import windll, WINFUNCTYPE
from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM, HMODULE, LPCWSTR, LPCSTR, LPVOID

class ErrorListLexer:

    def __init__(self):
        '''
            Initialize the class, should be called only once.
        '''

        # **************** configuration area ****************
        # files with these extensions and a null lexer,
        # aka normal text, assigned do get handled
        self.known_extensions = ['log', 'txt']
        #
        self.show_escape_chars = False
        self.separate_path_and_line_number = '0'
        self.interpret_escape_sequences = '1'
        # ****************************************************
        
        self.SCE_ERR_DEFAULT =0
        self.SCE_ERR_PYTHON =1
        self.SCE_ERR_GCC =2
        self.SCE_ERR_MS =3
        self.SCE_ERR_CMD =4
        self.SCE_ERR_BORLAND =5
        self.SCE_ERR_PERL =6
        self.SCE_ERR_NET =7
        self.SCE_ERR_LUA =8
        self.SCE_ERR_CTAG =9
        self.SCE_ERR_DIFF_CHANGED = 10
        self.SCE_ERR_DIFF_ADDITION = 11
        self.SCE_ERR_DIFF_DELETION = 12
        self.SCE_ERR_DIFF_MESSAGE = 13
        self.SCE_ERR_PHP = 14
        self.SCE_ERR_ELF = 15
        self.SCE_ERR_IFC = 16
        self.SCE_ERR_IFORT = 17
        self.SCE_ERR_ABSF = 18
        self.SCE_ERR_TIDY = 19
        self.SCE_ERR_JAVA_STACK = 20
        self.SCE_ERR_VALUE = 21
        self.SCE_ERR_GCC_INCLUDED_FROM = 22
        self.SCE_ERR_ESCSEQ = 23
        self.SCE_ERR_ESCSEQ_UNKNOWN = 24
        self.SCE_ERR_ES_BLACK = 40
        self.SCE_ERR_ES_RED = 41
        self.SCE_ERR_ES_GREEN = 42
        self.SCE_ERR_ES_BROWN = 43
        self.SCE_ERR_ES_BLUE = 44
        self.SCE_ERR_ES_MAGENTA = 45
        self.SCE_ERR_ES_CYAN = 46
        self.SCE_ERR_ES_GRAY = 47
        self.SCE_ERR_ES_DARK_GRAY = 48
        self.SCE_ERR_ES_BRIGHT_RED = 49
        self.SCE_ERR_ES_BRIGHT_GREEN = 50
        self.SCE_ERR_ES_YELLOW = 51
        self.SCE_ERR_ES_BRIGHT_BLUE = 52
        self.SCE_ERR_ES_BRIGHT_MAGENTA = 53
        self.SCE_ERR_ES_BRIGHT_CYAN = 54
        self.SCE_ERR_ES_WHITE = 55

        self.kernel32 = windll.kernel32
        self.user32 = windll.user32

        notepad_hwnd = self.user32.FindWindowW(u'Notepad++', None)
        self.editor1_hwnd = self.user32.FindWindowExW(notepad_hwnd, None, u"Scintilla", None)
        self.editor2_hwnd = self.user32.FindWindowExW(notepad_hwnd, self.editor1_hwnd, u"Scintilla", None)

        self.kernel32.GetModuleHandleW.argtypes = [LPCWSTR]
        self.kernel32.GetModuleHandleW.restype = HMODULE
        self.kernel32.GetProcAddress.argtypes = [HMODULE, LPCSTR]
        self.kernel32.GetProcAddress.restype = LPVOID
        handle = self.kernel32.GetModuleHandleW(None)
        create_lexer_ptr = self.kernel32.GetProcAddress(handle, b'CreateLexer')

        CL_FUNCTYPE = WINFUNCTYPE(LPVOID, LPCSTR)
        self.create_lexer_func = CL_FUNCTYPE(create_lexer_ptr)
        
        self.user32.SendMessageW.argtypes = [HWND, UINT, WPARAM, LPARAM]

        notepad.callback(self.on_langchanged, [NOTIFICATION.LANGCHANGED])
        notepad.callback(self.on_bufferactivated, [NOTIFICATION.BUFFERACTIVATED])


    def init_lexer(self):
        '''
            Initializes the lexer and its properties
            Args:
                None
            Returns:
                None
        '''
        editor.styleSetFore(self.SCE_ERR_DEFAULT, notepad.getEditorDefaultForegroundColor())
        editor.styleSetFore(self.SCE_ERR_PYTHON, (255,0,0))
        editor.styleSetFore(self.SCE_ERR_GCC, (255,0,0))
        editor.styleSetFore(self.SCE_ERR_MS, (255,0,0))
        editor.styleSetFore(self.SCE_ERR_CMD, (255,0,0))
        editor.styleSetFore(self.SCE_ERR_BORLAND, (255,0,0))
        editor.styleSetFore(self.SCE_ERR_PERL, (255,0,0))
        editor.styleSetFore(self.SCE_ERR_NET, (255,0,0))
        editor.styleSetFore(self.SCE_ERR_LUA, (255,0,0))
        editor.styleSetFore(self.SCE_ERR_CTAG, (255,0,0))
        editor.styleSetFore(self.SCE_ERR_DIFF_CHANGED, (255,0,0))
        editor.styleSetFore(self.SCE_ERR_DIFF_ADDITION, (255,0,0))
        editor.styleSetFore(self.SCE_ERR_DIFF_DELETION, (255,0,0))
        editor.styleSetFore(self.SCE_ERR_DIFF_MESSAGE, (255,0,0))
        editor.styleSetFore(self.SCE_ERR_PHP, (255,0,0))
        editor.styleSetFore(self.SCE_ERR_ELF, (255,0,0))
        editor.styleSetFore(self.SCE_ERR_IFC, (255,0,0))
        editor.styleSetFore(self.SCE_ERR_IFORT, (255,0,0))
        editor.styleSetFore(self.SCE_ERR_ABSF, (255,0,0))
        editor.styleSetFore(self.SCE_ERR_TIDY, (255,0,0))
        editor.styleSetFore(self.SCE_ERR_JAVA_STACK, (255,0,0))
        editor.styleSetFore(self.SCE_ERR_VALUE, (255,0,0))
        editor.styleSetFore(self.SCE_ERR_GCC_INCLUDED_FROM, (255,0,0))

        editor.styleSetFore(self.SCE_ERR_ESCSEQ, (30,30,30))
        editor.styleSetVisible(self.SCE_ERR_ESCSEQ, self.show_escape_chars)
        editor.styleSetFore(self.SCE_ERR_ESCSEQ_UNKNOWN, (255,255,120))
        editor.styleSetVisible(self.SCE_ERR_ESCSEQ_UNKNOWN, self.show_escape_chars)

        editor.styleSetFore(self.SCE_ERR_ES_BLACK, notepad.getEditorDefaultForegroundColor())
        editor.styleSetFore(self.SCE_ERR_ES_RED, (255,0,0))
        editor.styleSetFore(self.SCE_ERR_ES_GREEN, (0,255,0))
        editor.styleSetFore(self.SCE_ERR_ES_BROWN, (150,75,0))
        editor.styleSetFore(self.SCE_ERR_ES_BLUE, (0,0,255))
        editor.styleSetFore(self.SCE_ERR_ES_MAGENTA, (255,200,255))
        editor.styleSetFore(self.SCE_ERR_ES_CYAN, (255,200,100))
        editor.styleSetFore(self.SCE_ERR_ES_GRAY, (128,128,128))
        editor.styleSetFore(self.SCE_ERR_ES_DARK_GRAY, (255,200,100))
        editor.styleSetFore(self.SCE_ERR_ES_BRIGHT_RED, (170, 1, 20))
        editor.styleSetFore(self.SCE_ERR_ES_BRIGHT_GREEN, (255,200,100))
        editor.styleSetFore(self.SCE_ERR_ES_YELLOW, (255,255,0))
        editor.styleSetFore(self.SCE_ERR_ES_BRIGHT_BLUE, (9,84,190))
        editor.styleSetFore(self.SCE_ERR_ES_BRIGHT_MAGENTA, (229,8,194))
        editor.styleSetFore(self.SCE_ERR_ES_BRIGHT_CYAN, (27,244,207))
        editor.styleSetFore(self.SCE_ERR_ES_WHITE, (255,255,255))

        # ordering is important
        self.ilexer_ptr = self.create_lexer_func(b'errorlist')
        editor_hwnd = self.editor1_hwnd if notepad.getCurrentView() == 0 else self.editor2_hwnd
        self.user32.SendMessageW(editor_hwnd, 4033, 0, self.ilexer_ptr)
        editor.setProperty('lexer.errorlist.value.separate', self.separate_path_and_line_number)
        editor.setProperty('lexer.errorlist.escape.sequences', self.interpret_escape_sequences)

    def check_lexers(self):
        '''
            Checks if the current document is of interest.

            Args:
                None
            Returns:
                None
        '''

        has_no_lexer_assigned = editor.getLexerLanguage() == 'null'
        _, _, file_extension = notepad.getCurrentFilename().rpartition('.')
        if has_no_lexer_assigned and file_extension in self.known_extensions:
            self.init_lexer()


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
            Simulates the buffer_activated event to enforce 
            detection of current document and potential styling.

            Args:
                None
            Returns:
                None
        '''
        self.on_bufferactivated(None)


error_list_lexer = ErrorListLexer()
error_list_lexer.main()
