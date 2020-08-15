# -*- coding: utf-8 -*-
'''
    IHEX_VALIDATOR calculates the checksum of a single intel hex formatted record
'''

from Npp import notepad, editor, NOTIFICATION, SCINTILLANOTIFICATION, ANNOTATIONVISIBLE, MARGINTYPE
import struct

# Record Format
# :LLAAAATT[DD...]CC

# :     is the colon that starts every Intel HEX record.
# LL    is the record-length field that represents the number of data bytes (dd) in the record.
# AAAA  is the address field that represents the starting address for subsequent data in the record.
# TT    is the field that represents the HEX record type, which may be one of the following:
#   00 - data record
#   01 - end-of-file record
#   02 - extended segment address record
#   04 - extended linear address record
#   05 - start linear address record (MDK-ARM only)
# DD    is a data field that represents one byte of data. A record may have multiple data bytes. 
#       The number of data bytes in the record must match the number specified by the ll field.
# CC    is the checksum field that represents the checksum of the record. 
#       The checksum is calculated by summing the values of all hexadecimal digit pairs in 
#       the record modulo 256 and taking the two's complement.
#
# example = :10246200464C5549442050524F46494C4500464C33
#
# : 10 2462 00 464C5549442050524F46494C4500464C 33
# | || |||| || ||                               CC->Checksum
# | || |||| || DD->Data
# | || |||| TT->Record Type
# | || AAAA->Address
# | LL->Record Length
# :->Colon


# testdata
# :10001300AC12AD13AE10AF1112002F8E0E8F0F2244
# :10000300E50B250DF509E50A350CF5081200132259
# :03000000020023D8
# :0C002300787FE4F6D8FD7581130200031D
# :10002F00EFF88DF0A4FFEDC5F0CEA42EFEEC88F016
# :04003F00A42EFE22CB
# :00000001FF


class IHEX_VALIDATOR:

    def __init__(self):
        self.document_is_of_interest = False
        self.debug_mode = False
        self.ANON_STYLE = 20  # (0-18 reserved by ihex lexer)

        editor.callbackSync(self.on_updateui, [SCINTILLANOTIFICATION.UPDATEUI])
        notepad.callback(self.on_langchanged, [NOTIFICATION.LANGCHANGED])
        notepad.callback(self.on_bufferactivated, [NOTIFICATION.BUFFERACTIVATED])

        
    def __set_annotation(self, line, text):
        '''
            Shows an annotated line under the caret line
            Args:
                line = integer, 0-based line number of the caret line
                text = string, text to be shown
            Returns:
                None
        '''    

        editor.styleSetFore(self.ANON_STYLE, (128,255,0))
        editor.styleSetBack(self.ANON_STYLE, notepad.getEditorDefaultBackgroundColor())
        editor.annotationSetVisible(ANNOTATIONVISIBLE.STANDARD)
        editor.annotationSetText(line, text)
        editor.annotationSetStyle(line, self.ANON_STYLE)


    def calculate_checksum(self):
        '''
            Calculates the checksum of the caret line
            Args:
                None
            Returns:
                None
        '''    
        line = editor.getCurLine().strip()
        line_length = len(line)
        record_length = line_length-1
        if line.startswith(':') and line_length > 10 and (record_length % 2 == 0):
            if record_length == int(line[1:3],16) *2 + 8:
                length_assumed = True
                x = line[1:].decode('hex')
            else:
                length_assumed = False
                x = line[1:-2].decode('hex')
            total = sum(struct.unpack('<' + 'B'*len(x), x))
            int_checksum = ~total & 0xFF
            checksum = format(0 if int_checksum == 0xFF else int_checksum+1, '02X')
            if self.debug_mode:
                print('calculated checksum is {}'.format(checksum))
            if checksum != line[-2:]:
                self.__set_annotation(editor.lineFromPosition(editor.getCurrentPos()),
                                      '{}{}'.format(' '*line_length if length_assumed else ' '*(line_length-2),
                                                    checksum))
            else:
                editor.annotationClearAll()            


    def check_lexer(self):
        '''
            Checks if the current document is of interest
            and sets the flag accordingly
            Args:
                None
            Returns:
                None
        '''
        self.document_is_of_interest = notepad.getLanguageName(notepad.getLangType()) == 'Intel HEX'
        if self.debug_mode:
            print('document is of interest:{}'.format(self.document_is_of_interest))


    def on_bufferactivated(self, args):
        '''
            Callback which gets called every time one switches a document.
            Triggers the check if the document is of interest.
            Args:
                provided by notepad object but none are of interest
            Returns:
                None
        '''
        self.check_lexer()


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
            self.calculate_checksum()


    def on_langchanged(self, args):
        '''
            Callback gets called every time one uses the Language menu to set a lexer
            Triggers the check if the document is of interest
            Args:
                provided by notepad object but none are of interest
            Returns:
                None
        '''
        self.check_lexer()


    def main(self):
        '''
            Main function entry point.
            Simulates two events to enforce detection of current document
            and potential validating.
            Args:
                None
            Returns:
                None
        '''
        self.on_bufferactivated(None)
        self.on_updateui(None)
        

IHEX_VALIDATOR().main()
        