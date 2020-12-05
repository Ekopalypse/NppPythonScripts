'''
    Implements the notepad++ related lsp functionality
'''
import os
from urllib.request import url2pathname
import pprint
import logging

from Npp import (editor, editor1, editor2, notepad, console,
                 NOTIFICATION, SCINTILLANOTIFICATION,
                 ANNOTATIONVISIBLE, ORDERING, STATUSBARSECTION)
from .io_handler import COMMUNICATION_MANAGER
from .lsp_protocol import MESSAGES, TextDocumentSaveReason

log = logging.info
pp = pprint.PrettyPrinter(indent=4)


class LSPCLIENT():

    def __init__(self, lsp_server_configs):
        log('LSPCLIENT')
        self.available_lsp_servers = lsp_server_configs.keys()
        self.com_manager = COMMUNICATION_MANAGER(lsp_server_configs, self.on_receive)
        self.lsp_msg = MESSAGES()
        self.lsp_doc_flag = False
        self.current_language = None
        self.current_triggers = dict()
        self.current_file = ''
        self.open_files_dict = dict()
        self.sent_didopen_files = []
        self.open_results = dict()
        self.setup()
        self.waiting_for_completion_response = False
        self.current_hover_position = -1


    def setup(self):
        log('register callbacks etc...')
        notepad.callback(self.on_buffer_activated, [NOTIFICATION.BUFFERACTIVATED])
        notepad.callback(self.on_file_saved, [NOTIFICATION.FILESAVED])
        notepad.callback(self.on_file_closed, [NOTIFICATION.FILECLOSED])
        notepad.callback(self.on_file_before_save, [NOTIFICATION.FILEBEFORESAVE])
        editor.callbackSync(self.on_char_added, [SCINTILLANOTIFICATION.CHARADDED])
        editor.callbackSync(self.on_dwell_end, [SCINTILLANOTIFICATION.DWELLEND])
        editor.callbackSync(self.on_dwell_start, [SCINTILLANOTIFICATION.DWELLSTART])

        fg_color = editor.styleGetFore(32)
        darker_bg_color = tuple([x - 10 if x > 10 else x for x in editor.styleGetBack(32)])

        CALLTIP_STYLE = 38
        editor1.styleSetBack(CALLTIP_STYLE, darker_bg_color)
        editor1.styleSetFore(CALLTIP_STYLE, fg_color)
        editor2.styleSetBack(CALLTIP_STYLE, darker_bg_color)
        editor2.styleSetFore(CALLTIP_STYLE, fg_color)

        editor1.callTipUseStyle(80)  # 80 = tab width in pixels
        editor2.callTipUseStyle(80)

        editor1.autoCSetSeparator(10)
        editor1.autoCSetOrder(ORDERING.CUSTOM)
        editor2.autoCSetSeparator(10)
        editor2.autoCSetOrder(ORDERING.CUSTOM)

        self.PEEK_STYLE = 60
        editor1.styleSetFore(self.PEEK_STYLE, fg_color)
        editor1.styleSetBack(self.PEEK_STYLE, darker_bg_color)
        editor2.styleSetFore(self.PEEK_STYLE, fg_color)
        editor2.styleSetBack(self.PEEK_STYLE, darker_bg_color)

        editor1.setMouseDwellTime(500)
        editor2.setMouseDwellTime(500)

        self.open_files_dict = {x[1]: x[0] for x in notepad.getFiles()}
        

    def terminate(self):
        log('clear callbacks...')
        notepad.clearCallbacks([NOTIFICATION.BUFFERACTIVATED,
                                NOTIFICATION.FILESAVED,
                                NOTIFICATION.FILECLOSED])
        editor.clearCallbacks([SCINTILLANOTIFICATION.CHARADDED,
                               SCINTILLANOTIFICATION.DWELLEND,
                               SCINTILLANOTIFICATION.DWELLSTART])

        for monitor_thread in self.com_manager.running_monitoring_threads():
            self.com_manager.stop_monitoring_thread(monitor_thread)
            self.com_manager.send(self.lsp_msg.exit())
            self.com_manager.send(self.lsp_msg.shutdown())


    def __TextDocumentIdentifier(self):
        _version = self._get_file_version()
        return self.current_file, _version


    def __TextDocumentPositionParams(self, cur_pos=None):
        if cur_pos is None:
            cur_pos = editor.getCurrentPos()
        _line = editor.lineFromPosition(cur_pos)
        _character_pos = editor.getColumn(cur_pos)
        _file, _version = self.__TextDocumentIdentifier()
        return _file, _version, _line, _character_pos


    def __DocumentFormattingParams(self):
        _file, _version = self.__TextDocumentIdentifier()
        # TODO:
        # /**
         # * The format options.
         # */
        # options: FormattingOptions;

        # /**
         # * Value-object describing what options formatting should use.
         # */
        # interface FormattingOptions {
            # /**
             # * Size of a tab in spaces.
             # */
            # tabSize: number;

            # /**
             # * Prefer spaces over tabs.
             # */
            # insertSpaces: boolean;

            # /**
             # * Signature for further properties.
             # */
            # [key: string]: boolean | number | string;
        return _file, _version


    def _get_trigger_chars(self, dict_var, key_list):
        for k, v in dict_var.items():
            if k in key_list:
                yield k, v
            elif isinstance(v, dict):
                for _k, _v in self._get_trigger_chars(v, key_list):
                    yield _k, _v


    def _get_file_version(self):
        log('called')
        file_version = editor.getPropertyInt('fileversion', 0)
        # editor.setProperty('fileversion', file_version + 1)
        return file_version


    def _set_file_version(self):
        log('called')
        file_version = editor.getPropertyInt('fileversion', 0) + 1
        editor.setProperty('fileversion', file_version)
        return file_version


    def _send_did_change(self, version=None):
        version = self._get_file_version() if version is None else version
        self.com_manager.send(self.lsp_msg.didChange(self.current_file,
                                                     self.current_language.lower(),
                                                     version,
                                                     editor.getText()))


    def _send_documet_symbol(self):
        self.com_manager.send(self.lsp_msg.documentSymbol(self.current_file,
                                                          self._get_file_version()))
        self.open_results[self.lsp_msg.request_id] = self.document_symbol_response_handler


    def _send_document_formatting(self):
        self.com_manager.send(self.lsp_msg.formatting(self.current_file,
                                                      self._get_file_version()))
        self.open_results[self.lsp_msg.request_id] = self.document_formatting_handler

    def _send_document_range_formatting(self):
        _start_pos = editor.getSelectionStart()
        start_line = editor.lineFromPosition(_start_pos)
        start_char_pos = _start_pos - editor.positionFromLine(start_line)
        _end_pos = editor.getSelectionEnd()
        end_line = editor.lineFromPosition(_end_pos)
        end_char_pos = _end_pos - editor.positionFromLine(end_line)
        
        self.com_manager.send(self.lsp_msg.rangeFormatting(self.current_file,
                                                           self._get_file_version(),
                                                           (start_line, start_char_pos),
                                                           (end_line, end_char_pos)))
        self.open_results[self.lsp_msg.request_id] = self.document_range_formatting_handler


    def _send_goto_definition(self):
        self.com_manager.send(self.lsp_msg.definition(*self.__TextDocumentPositionParams()))
        self.open_results[self.lsp_msg.request_id] = self.goto_definition_response_handler


    def _send_peek_definition(self):
        self.com_manager.send(self.lsp_msg.definition(*self.__TextDocumentPositionParams()))
        self.open_results[self.lsp_msg.request_id] = self.peek_definition_response_handler


    def _send_hover(self, hover_position):
        self.current_hover_position = hover_position
        self.com_manager.send(self.lsp_msg.hover(*self.__TextDocumentPositionParams(hover_position)))
        self.open_results[self.lsp_msg.request_id] = self.hover_response_handler


    def _send_references(self):
        self.com_manager.send(self.lsp_msg.references(*self.__TextDocumentPositionParams()))
        self.open_results[self.lsp_msg.request_id] = self.reference_response_handler


    def _send_codeLens(self):
        self.com_manager.send(self.lsp_msg.codeLens(*self.__TextDocumentIdentifier()))
        self.open_results[self.lsp_msg.request_id] = self.code_lens_response_handler


    def _send_prepareRename(self):
        self.com_manager.send(self.lsp_msg.prepareRename(*self.__TextDocumentPositionParams()))
        self.open_results[self.lsp_msg.request_id] = self.prepare_rename_response_handler


    def _send_foldingRange(self):
        self.com_manager.send(self.lsp_msg.foldingRange(*self.__TextDocumentIdentifier()))
        self.open_results[self.lsp_msg.request_id] = self.folding_range_response_handler


    def _send_goto_declaration(self):
        self.com_manager.send(self.lsp_msg.declaration(*self.__TextDocumentPositionParams()))
        self.open_results[self.lsp_msg.request_id] = self.declaration_response_handler


    def _send_type_definition(self):
        self.com_manager.send(self.lsp_msg.typeDefinition(*self.__TextDocumentPositionParams()))
        self.open_results[self.lsp_msg.request_id] = self.type_definition_response_handler


    def _send_documentHighlight(self):
        self.com_manager.send(self.lsp_msg.documentHighlight(*self.__TextDocumentPositionParams()))
        self.open_results[self.lsp_msg.request_id] = self.document_highlight_response_handler


    def _send_workspace_symbol(self, _query):
        self.com_manager.send(self.lsp_msg.workspace_symbol(_query))
        self.open_results[self.lsp_msg.request_id] = self.workspace_symbol_response_handler


    def _send_resolve(self, _label):
        self.com_manager.send(self.lsp_msg.resolve(_label))
        self.open_results[self.lsp_msg.request_id] = self.resolve_response_handler


    def _notification_handler(self, decoded_message):
        _method = decoded_message.get('method', None)
        if _method == 'textDocument/publishDiagnostics':
            # if editor.getModify():
                # return
            # TODO: for now every diagnostic message clears the console
            console.clear()
            _file = url2pathname(decoded_message['params']['uri'].replace('file:', ''))
            if decoded_message['params']['diagnostics']:
                diag_dict = dict()
                console_output = []
                for item in decoded_message['params']['diagnostics']:
                    # _code = item.get('code', '')
                    _message = item.get('message', 'MESSAGE:???')
                    _severity = item.get('severity', '1')
                    _source = item.get('source', 'SOURCE:???')
                    __range = item.get('range', None)
                    if __range:
                        _start = (__range['start']['line'], __range['start']['character'])
                        _end = (__range['end']['line'], __range['end']['character'])
                        _range = (_start, _end)
                        console_output.append(f'  File "{_file}", line {_start[0]+1}  -  {_message}')
                    else:
                        _range = 'RANGE:???'
                    
                    if _severity not in diag_dict:
                        diag_dict[_severity] = f'    {_range} {_source} {_message}'
                    else:
                        diag_dict[_severity] += f'    {_range} {_source} {_message}'
                    diag_dict[_severity] += '\n'

                error_msgs = ''
                warning_msgs = ''
                info_msgs = ''
                hint_msgs = ''
                for k, v in diag_dict.items():
                    num = max([v.count('\n'), v.count('\r')])
                    if k == 1:
                        error_msgs += '  Errors ({})\n'.format(num) + v
                    elif k == 2:
                        warning_msgs += '  Warning ({})\n'.format(num) + v
                    elif k == 3:
                        info_msgs += '  Info ({})\n'.format(num) + v
                    else:  # k == 4
                        hint_msgs += '  Hint ({})\n'.format(num) + v

                diag_msgs = error_msgs + warning_msgs + info_msgs + hint_msgs
                log(f'{_file}, {diag_msgs}')
                print('\n'.join(console_output))

        elif _method == 'window/progress':
            if decoded_message['params']['done']:
                pass  # TODO: reset statusbar
            else:
                _message = decoded_message['params']['message']
                _title = decoded_message['params']['title']
                notepad.setStatusBar(STATUSBARSECTION.DOCTYPE, f'{_title} - {_message}')
        else:
            log(f'unknown notification received: {decoded_message}')


    @staticmethod
    def signature_response_handler(decoded_message):
        if decoded_message['result'].get('signatures', None):
            tip = '{}\n\n{}'.format(decoded_message['result']['signatures'][0]['label'],
                                    decoded_message['result']['signatures'][0]['documentation'][:1000])
            if tip.strip():
                editor.callTipShow(editor.getCurrentPos(), tip)


    @staticmethod
    def _show_completion_list(_completion_list):
        editor.autoCCancel()
        editor.autoCSetSeparator(ord('\n'))
        editor.autoCSetOrder(ORDERING.CUSTOM)
        editor.autoCShow(0, '\n'.join(_completion_list))


    def completion_response_handler(self, decoded_message):
        self.waiting_for_completion_response = False
        if 'items' in decoded_message['result']:
            if decoded_message['result']['items']:
                if 'label' in decoded_message['result']['items'][0]:
                    if decoded_message['result']['isIncomplete'] is False:
                        completion_list = [x['insertText'] for x in decoded_message['result']['items']]
                        # editor.autoCShow(0, '\n'.join(sorted(completion_list)))
                        self._show_completion_list(completion_list)
                    else:
                        log('wait for additional data')
                else:
                    log('?? something else ??')
        else:
            if decoded_message['result']:
                completion_list = [x['insertText'] for x in decoded_message['result']]
                self._show_completion_list(completion_list)

 
    def document_symbol_response_handler(self, decoded_message):
        # How to visualize is the question??
        # {"jsonrpc":"2.0","id":2,"result":[
        # {"name":"json","containerName":null,"location":{"uri":"...","range":{"start":{"line":0,"character":0},"end":{"line":0,"character":11}}},"kind":2},
        # {"name":"Test","containerName":null,"location":{"uri":"...","range":{"start":{"line":3,"character":0},"end":{"line":13,"character":0}}},"kind":5},
        # {"name":"t",   "containerName":null,"location":{"uri":"...","range":{"start":{"line":15,"character":0},"end":{"line":15,"character":10}}},"kind":13}]}    
        # {"name":"__init__","containerName":"Test","location":{"uri":"...","range":{"start":{"line":5,"character":4},"end":{"line":7,"character":0}}},"kind":6},
        # {"name":"start",   "containerName":"Test","location":{"uri":"...","range":{"start":{"line":8,"character":4},"end":{"line":10,"character":0}}},"kind":6},
        # {"name":"stop",    "containerName":"Test","location":{"uri":"...","range":{"start":{"line":11,"character":4},"end":{"line":13,"character":0}}},"kind":6},
        symbol_list = []
        for symbol in decoded_message['result']:
            if symbol['kind'] in [5, 6, 12]:
                symbol_list.append(f'{symbol["containerName"]}->{symbol["name"]}')
        log('\n'.join(symbol_list))


    @staticmethod
    def __format_document(item):
        new_content = item['newText']
        _start_line = item['range']['start']['line']
        _start_char_pos = item['range']['start']['character']
        _end_line = item['range']['end']['line']
        _end_char_pos = item['range']['end']['character']
        start = editor.positionFromLine(_start_line) + _start_char_pos
        end = editor.positionFromLine(_end_line) + _end_char_pos
        if start == -1 or end == -1:
            log(f'ABORTED - negative position found:{item}')
            return
        editor.setTargetRange(start, end)
        editor.replaceTarget(new_content)


    def document_formatting_handler(self, decoded_message):
        log(decoded_message)
        editor.beginUndoAction()
        current_caret_pos = editor.getCurrentPos()
        for item in reversed(decoded_message['result']):
            self.__format_document(item)
        # editor.setText(decoded_message['result'][0]['newText'])
        editor.gotoPos(current_caret_pos)
        editor.endUndoAction()


    def document_range_formatting_handler(self, decoded_message):
        log(decoded_message)
        editor.beginUndoAction()
        current_caret_pos = editor.getCurrentPos()
        for item in reversed(decoded_message['result']):
            self.__format_document(item)
        editor.gotoPos(current_caret_pos)
        editor.endUndoAction()


    def goto_definition_response_handler(self, decoded_message):
        log(decoded_message)
        if decoded_message['result']:
            _file = url2pathname(decoded_message['result'][0]['uri'].replace('file:', ''))
            notepad.activateFile(_file)
            editor.gotoLine(decoded_message['result'][0]['range']['start']['line'])


    def _clear_peek_definition(self):
        editor.annotationClearAll()


    def peek_definition_response_handler(self, decoded_message):
        log(decoded_message)
        if decoded_message['result']:
            _file = url2pathname(decoded_message['result'][0]['uri'].replace('file:', ''))
            _line_number = decoded_message['result'][0]['range']['start']['line']
            with open(_file) as f:
                for i, line in enumerate(f):
                    if i == _line_number:
                        break
            cursor_line = editor.lineFromPosition(editor.getCurrentPos())
            editor.annotationSetText(cursor_line, '\n{}\n'.format(line[:-1] if line.endswith('\n') else line))
            editor.annotationSetStyle(cursor_line, self.PEEK_STYLE)
            editor.annotationSetVisible(ANNOTATIONVISIBLE.STANDARD)


    def hover_response_handler(self, decoded_message):
        log(decoded_message)
        if 'contents' in decoded_message['result']:
            tip = decoded_message['result']['contents']
            if tip and self.current_hover_position != -1:
                if isinstance(tip[0], dict) and 'value' in tip[0]:
                    editor.callTipShow(self.current_hover_position, tip[0]['value'])
                else:
                    editor.callTipShow(self.current_hover_position, tip[0][:500])
                self.current_hover_position = -1


    def reference_response_handler(self, decoded_message):
        log(decoded_message)
        # {'jsonrpc': '2.0', 'id': 4, 'result': [
        # {'uri': 'file:///d:/.../test.py', 'range': {'start': {'line': 8, 'character': 8}, 'end': {'line': 8, 'character': 13}}}, 
        # {'uri': 'file:///d:/.../test.py', 'range': {'start': {'line': 16, 'character': 2}, 'end': {'line': 16, 'character': 7}}}]}
        # How to visualize is the question??
        references = []
        if decoded_message['result']:
            for reference in decoded_message['result']:
                _line = reference['range']['start']['line']
                _file = url2pathname(reference['uri'].replace('file:', ''))
                references.append((_file, _line))
            log('\n'.join(['{}\r\n  {}'.format(*x) for x in references]))


    def code_lens_response_handler(self, decoded_message):
        if decoded_message['result']:
            log(decoded_message)


    def _send_rename(self):
        _current_word = editor.getWord()
        new_name = notepad.prompt('Provide the new name to be used', 'Rename to ...', _current_word)
        log(f'{new_name=}')
        self.com_manager.send(self.lsp_msg.rename(*self.__TextDocumentPositionParams(), _new_name=new_name))
        self.open_results[self.lsp_msg.request_id] = self.rename_response_handler


    def rename_response_handler(self, decoded_message):
        log(decoded_message)
        # 'result': {'documentChanges': [{'edits': [{'newText': u"...",
        # 'range': {'end': {'character': 0, 'line': 417},
        # 'start': {'character': 0, 'line': 0}}}],
        # 'textDocument': {'uri': 'file:///d:/...', 'version': None}}]}}
        if decoded_message['result']:
            editor.beginUndoAction()
            for changes in decoded_message['result']['documentChanges']:
                for change in changes['edits']:
                    _file = url2pathname(changes['textDocument']['uri'].replace('file:', ''))
                    notepad.open(_file)
                    start_line = change['range']['start']['line']
                    end_line = change['range']['end']['line']
                    start_position = editor.positionFromLine(start_line) + change['range']['start']['character']
                    end_position = editor.positionFromLine(end_line) + change['range']['end']['character']
                    editor.setTargetRange(start_position, end_position)
                    editor.replaceTarget(change['newText'])
            editor.endUndoAction()


    def prepare_rename_response_handler(self, decoded_message):
        log(decoded_message)


    def folding_range_response_handler(self, decoded_message):
        log(decoded_message)


    def declaration_response_handler(self, decoded_message):
        log(decoded_message)


    def type_definition_response_handler(self, decoded_message):
        log(decoded_message)


    def document_highlight_response_handler(self, decoded_message):
        log(decoded_message)


    def workspace_symbol_response_handler(self, decoded_message):
        log(decoded_message)


    def _result_handler(self, decoded_message):
        if decoded_message['id'] in self.open_results:
            _handler = self.open_results.pop(decoded_message['id'])
            if 'error' in decoded_message or not decoded_message['result']:
                return
            _handler(decoded_message)
        else:
            log(f'Unexpected message received: {decoded_message}')


    def resolve_response_handler(self, decoded_message):
        log(decoded_message)


    def on_receive(self, message):
        ''' called from process manager if message was read from msg_queue
            message is a dict created by json.loads
        '''
        if message:
            log(message)
            decoded_message, error = self.lsp_msg.decode(message)
            if error:
                log(decoded_message)
            else:
                if decoded_message:
                    if 'result' in decoded_message:
                        if not decoded_message['result'] is None and 'capabilities' in decoded_message['result']:
                            self.com_manager.send_initialized(self.lsp_msg.initialized())
                            for k, v in self._get_trigger_chars(decoded_message, ['signatureHelpProvider',
                                                                                  'completionProvider']):
                                triggers = [ord(x) for x in v.get('triggerCharacters', [])]
                                if k == 'signatureHelpProvider':
                                    self.current_triggers[self.current_language]['signatureHelpProvider'] = triggers
                                elif k == 'completionProvider':
                                    self.current_triggers[self.current_language]['completionProvider'] = triggers
                        else:
                            self._result_handler(decoded_message)
                    elif 'error' in decoded_message:
                        self._result_handler(decoded_message)
                    elif 'id' not in decoded_message:
                        self._notification_handler(decoded_message)
                    else:
                        self.com_manager.send(self.lsp_msg.response(decoded_message))
        else:
            log(f'got corrupted message:{message}')


    def on_buffer_activated(self, args):
        log(f'{args}')
        self.current_language = notepad.getLanguageName(notepad.getLangType()).upper()
        if args['bufferID'] not in self.open_files_dict:
            self.current_file = notepad.getCurrentFilename()
            self.open_files_dict[args['bufferID']] = self.current_file
        else:
            self.current_file = self.open_files_dict[args['bufferID']]

        # temporary files are not supported
        if self.current_file.rpartition('\\')[0] == '':
            log('temporary files are not supported (yet?)')
            self.lsp_doc_flag = False
            return

        if self.current_language in self.available_lsp_servers:
            self.lsp_doc_flag = True
            if not self.com_manager.already_initialized(self.current_language):
                self.current_triggers[self.current_language] = {'signatureHelpProvider': [],
                                                                'completionProvider': []}
                self.com_manager.send(self.lsp_msg.initialize(self.current_file.rpartition('\\')[0], os.getpid()))
                self.com_manager.waiting_for_initialize_result = True

            _version = self._get_file_version()

            if _version == 0:
                log(f'file {self.current_file} first seen')
                self.com_manager.send(self.lsp_msg.didOpen(self.current_file,
                                                           self.current_language.lower(),
                                                           _version,
                                                           editor.getText()
                                                           ))
                self.sent_didopen_files.append(args['bufferID'])
        else:
            log(f'{self.current_language} not in {self.available_lsp_servers}')
            self.lsp_doc_flag = False


    def on_file_before_save(self, args):
        if self.lsp_doc_flag:
            _version = self._set_file_version()
            _reason = TextDocumentSaveReason.Manual
            self.com_manager.send(self.lsp_msg.willSave(self.current_file, _version, _reason))


    def on_file_saved(self, args):
        if self.lsp_doc_flag:
            _version = self._set_file_version()
            self._send_did_change(_version)
            self.com_manager.send(self.lsp_msg.didSave(self.current_file, _version))


    def on_file_closed(self, args):
        if args['bufferID'] in self.sent_didopen_files:
            self.sent_didopen_files.remove(args['bufferID'])
            self.com_manager.send(self.lsp_msg.didClose(self.open_files_dict[args['bufferID']]))
            # if self._dialog:
                # self._dialog.sci_ctrl.SetDiagnostics(self.open_files_dict[args['bufferID']], '')


    def on_char_added(self, args):
        if self.lsp_doc_flag:

            if chr(args['ch']) == ')':
                editor.callTipCancel()
            elif (args['ch'] in self.current_triggers[self.current_language]['signatureHelpProvider'] or
                  args['ch'] in self.current_triggers[self.current_language]['completionProvider']):

                cur_pos = editor.getCurrentPos()
                _line = editor.lineFromPosition(cur_pos)
                _character_pos = cur_pos - editor.positionFromLine(_line)
                _version = self._set_file_version()

                self._send_did_change(_version)

                if args['ch'] in self.current_triggers[self.current_language]['signatureHelpProvider']:
                    self.com_manager.send(self.lsp_msg.signatureHelp(self.current_file,
                                                                     self.current_language.lower(),
                                                                     _version,
                                                                     editor.getText(),
                                                                     _line,
                                                                     _character_pos))
                    self.open_results[self.lsp_msg.request_id] = self.signature_response_handler

                else:
                    self.com_manager.send(self.lsp_msg.completion(*self.__TextDocumentPositionParams()))
                    self.open_results[self.lsp_msg.request_id] = self.completion_response_handler


    def on_dwell_end(self, args):
        editor.callTipCancel()


    def on_dwell_start(self, args):
        if args['position'] != -1:
            self._send_hover(args['position'])
