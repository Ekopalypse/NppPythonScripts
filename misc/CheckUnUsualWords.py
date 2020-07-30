from Npp import notepad, editor, NOTIFICATION, SCINTILLANOTIFICATION, STATUSBARSECTION, MODIFICATIONFLAGS
import os


class WORD_CHECKER:

    def __init__(self):
        print('__init__')
        self.report = ('Total: {0:<5}  '
                       'Unique: {1:<5}  '
                       'Total non-misspelled: {2:<5}({3:.1%})  '
                       'Total misspelled: {4:<4}({5:.1%})  '
                       'Unique misspelled: {6:<4}({7:.1%})')

        editor.callbackSync(self.on_modified, [SCINTILLANOTIFICATION.MODIFIED])
        notepad.callback(self.on_buffer_activated, [NOTIFICATION.BUFFERACTIVATED])
        current_dict_path = os.path.join(notepad.getPluginConfigDir(), 'Hunspell')
        current_dict_file = os.path.join(current_dict_path, 'ES-5000.dic')
        with open(current_dict_file, 'r') as f:
            self.current_dict = [word.decode('utf8')
                                 for word in f.read().splitlines()[1:]]   # skip length entry

        self.DEBUG_MODE = False
        self.on_buffer_activated({})  # must be last line here as it triggers check_words
        

    def check_words(self):
        
        words = []

        def __get_words(m):
            if m.group(2):
                words.append(m.group(2).decode('utf8'))
        
        editor.research('(^//.*)|([[:alpha:]]+(?=\h|[[:punct:]]|\R|\Z))', __get_words)
        
        if self.DEBUG_MODE:
            print(u'words contains:\n  {}'.format('  '.join(words)))
            
        error_words = [word.lower() 
                       for word in words 
                       if word.lower() not in self.current_dict and    # insensitive word check
                       not word.isupper()  # ignore all uppercase only words
                       ]
        if self.DEBUG_MODE:
            print(u'error_words contains:\n  {}'.format('  '.join(error_words)))
            print(u'error_words unique contains:\n  {}'.format('  '.join(set(error_words))))
        
        total = len(words)
        unique = len(set(words))
        misspelled = len(error_words)
        misspelled_unique = len(set(error_words))
        notepad.setStatusBar(STATUSBARSECTION.DOCTYPE, 
                             self.report.format(total,
                                                unique,
                                                total-misspelled,  # non-misspelled
                                                (float(total-misspelled) / total) if misspelled else 1,  # non-misspelled %
                                                misspelled,
                                                (float(misspelled) / total) if misspelled else 0,
                                                misspelled_unique,
                                                (float(misspelled_unique) / total) if misspelled_unique else 0))


    def on_modified(self, args):
        if ((args['modificationType'] & MODIFICATIONFLAGS.INSERTTEXT) or 
            (args['modificationType'] & MODIFICATIONFLAGS.DELETETEXT)):
            self.check_words()


    def on_buffer_activated(self, args):
        self.check_words()


WORD_CHECKER()
