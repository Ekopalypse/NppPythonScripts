'''
lsp protocol implementation
https://microsoft.github.io/language-server-protocol/specification
encodes and decodes lsp messages
'''

import json
import enum
from urllib.request import pathname2url


class CompletionItemKind(enum.IntEnum):
    Text = 1
    Method = 2
    Function = 3
    Constructor = 4
    Field = 5
    Variable = 6
    Class = 7
    Interface = 8
    Module = 9
    Property = 10
    Unit = 11
    Value = 12
    Enum = 13
    Keyword = 14
    Snippet = 15
    Color = 16
    File = 17
    Reference = 18
    Folder = 19
    EnumMember = 20
    Constant = 21
    Struct = 22
    Event = 23
    Operator = 24
    TypeParameter = 25


class SymbolKind(enum.IntEnum):
    File = 1
    Module = 2
    Namespace = 3
    Package = 4
    Class = 5
    Method = 6
    Property = 7
    Field = 8
    Constructor = 9
    Enum = 10
    Interface = 11
    Function = 12
    Variable = 13
    Constant = 14
    String = 15
    Number = 16
    Boolean = 17
    Array = 18
    Object = 19
    Key = 20
    Null = 21
    EnumMember = 22
    Struct = 23
    Event = 24
    Operator = 25
    TypeParameter = 26


class ErrorCodes(enum.IntEnum):
    # Defined by JSON RPC
    ParseError = -32700
    InvalidRequest = -32600
    MethodNotFound = -32601
    InvalidParams = -32602
    InternalError = -32603
    serverErrorStart = -32099
    serverErrorEnd = -32000
    ServerNotInitialized = -32002
    UnknownErrorCode = -32001
    # Defined by the protocol.
    RequestCancelled = -32800
    ContentModified = -32801


class MarkupKind:
    PlainText = 'plaintext'
    Markdown = 'markdown'


class ResourceOperationKind:
    Create = 'create'
    Rename = 'rename'
    Delete = 'delete'


class FailureHandlingKind:
    Abort = 'abort'
    Transactional = 'transactional'
    TextOnlyTransactional = 'textOnlyTransactional'
    Undo = 'undo'


class InitializeError(enum.IntEnum):
    unknownProtocolVersion = 1


class TextDocumentSyncKind(enum.IntEnum):
    NONE = 0
    Full = 1
    Incremental = 2


class MessageType(enum.IntEnum):
    Error = 1
    Warning = 2
    Info = 3
    Log = 4


class FileChangeType(enum.IntEnum):
    Created = 1
    Changed = 2
    Deleted = 3


class WatchKind(enum.IntEnum):
    Create = 1
    Change = 2
    Delete = 4


class TextDocumentSaveReason(enum.IntEnum):
    Manual = 1
    AfterDelay = 2
    FocusOut = 3


class CompletionTriggerKind(enum.IntEnum):
    Invoked = 1
    TriggerCharacter = 2
    TriggerForIncompleteCompletions = 3


class InsertTextFormat(enum.IntEnum):
    PlainText = 1
    Snippet = 2


class MESSAGES:
    '''
        Implements request, response and notification messages as per specifiaction
    '''

    def __init__(self):
        self.lsp_header = 'Content-Length: {}\r\n\r\n'
        self.response_skeleton = {'jsonrpc': '2.0', 'id': None}
        self.notif_skeleton = {'jsonrpc': '2.0', 'method': None, 'params': None}
        self.request_skeleton = {'jsonrpc': '2.0', 'id': None, 'method': None, 'params': None}
        self.empty_dict = dict()
        self.request_id = 0


    def _next_id(self):
        self.request_id += 1
        return self.request_id


    def _create_lsp_message(self, content_part):
        _json_data = json.dumps(content_part)
        return f'{self.lsp_header.format(len(_json_data))}{_json_data}'


    def _notif(self, method, params=None):
        '''
            A notification message.
            A processed notification message must not send a response back.
            They work like events.

            Args:
                method: expected a string like 'textDocument/didOpen'
                params: expected either None or dict associated to method

            Returns: Nothing
            Raises: Nothing
        '''
        self.notif_skeleton['method'] = method
        self.notif_skeleton['params'] = params if params is not None else self.empty_dict
        return self._create_lsp_message(self.notif_skeleton)


    def _request(self, method, params=None):
        '''
            A request message to describe a request between the client and the server.
            Every processed request must send a response back to the sender of the request.

            Args:
                method: expected a string like 'textDocument/signatureHelp'
                params: expected either None or dict associated to method

            Returns: Nothing
            Raises: Nothing
        '''
        self.request_skeleton['id'] = self._next_id()
        self.request_skeleton['method'] = method
        self.request_skeleton['params'] = params if params is not None else self.empty_dict
        return self._create_lsp_message(self.request_skeleton)


    def _response(self, id, result=None, error=None):
        '''
            A Response Message sent as a result of a request.
            If a request doesn't provide a result value the receiver of a request still needs
            to return a response message to conform to the JSON RPC specification.
            The result property of the ResponseMessage should be set to null in this case
            to signal a successful request.

            Args:
                id: expected integer or string which was provided by a former request message
                result: expected None or string | number | boolean | object
                error: expected None or ResponseError<any>.

            Returns: Nothing
            Raises: Nothing
        '''
        # self.response_skeleton = {'jsonrpc': '2.0'}
        self.response_skeleton['id'] = id
        if error is None:
            self.response_skeleton['result'] = result
        else:  # error class provided
            self.response_skeleton['error'] = error
        return self._create_lsp_message(self.response_skeleton)


    def decode(self, msg):
        try:
            decoded_msg = json.loads(msg)
            return decoded_msg, False
        except Exception as e:
            return e, True


    # --------------------------------------------------------------------------------------------------------------------
    # Response


    def response(self, message):
        return self._response(message.get('id'))


    # --------------------------------------------------------------------------------------------------------------------
    # Notifications


    def initialized(self):
        return self._notif('initialized', None)


    def didOpen(self, _file, _languageId, _version, _text):
        params = {'textDocument': {
                  'uri': f'file:{pathname2url(_file)}',
                  'languageId': _languageId,
                  'version': _version,  # increase after each change, including undo/redo
                  # 'text': json.dumps(_text)
                  'text': _text
                  }
                  }
        return self._notif('textDocument/didOpen', params)


    def didChange(self, _file, _languageId, _version, _changes):
        params = {'textDocument': {
            'uri': f'file:{pathname2url(_file)}',
            'languageId': _languageId,
            'version': _version  # increase after each change, including undo/redo
        },
            'contentChanges': [{'text': _changes}]
        }
        return self._notif('textDocument/didChange', params)


    def didSave(self, _file, _version):
        params = {'textDocument': {
            'uri': f'file:{pathname2url(_file)}',
            'version': _version  # increase after each change, including undo/redo
        }
        }
        return self._notif('textDocument/didSave', params)


    def willSave(self, _file, _version, _reason):
        params = {'textDocument': {
            'uri': f'file:{pathname2url(_file)}',
            'version': _version
        },
            'reason': _reason
        }
        return self._notif('textDocument/willSave', params)


    def exit(self): return self._notif('exit', None)


    def didClose(self, _file):
        params = {'textDocument': {
            'uri': f'file:{pathname2url(_file)}'
        }
        }
        return self._notif('textDocument/didClose', params)

    # TODO: clarify settings param
    def didChangeConfiguration(self, _settings):
        params = {'settings': _settings}
        return self._notif('workspace/didChangeConfiguration', params)

    # --------------------------------------------------------------------------------------------------------------------
    # Requests
    def initialize(self, rootUri, pid):
        params = {
            # The process Id of the parent process that started
            # the server. Is null if the process has not been started by another process.
            # If the parent process is not alive then the server should exit (see exit notification) its process.
            #
            # processId: number | null;
            'processId': pid,

            # The rootPath of the workspace. Is null
            # if no folder is open.
            #
            # @deprecated in favour of rootUri.
            #
            # rootPath?: string | null;

            # The rootUri of the workspace. Is null if no
            # folder is open. If both `rootPath` and `rootUri` are set
            # `rootUri` wins.
            #
            # rootUri: DocumentUri | null;
            'rootUri': f'file:{pathname2url(rootUri)}',

            #
            # User provided initialization options.
            #
            # initializationOptions?: any;
            'initializationOptions': dict(),
            #
            # The capabilities provided by the client
            #
            # capabilities: ClientCapabilities;
            'capabilities': {
                'workspace': {
                    'applyEdit': True,
                    'workspaceEdit': {
                        'documentChanges': False
                    },
                    'didChangeConfiguration': {
                        'dynamicRegistration': False
                    },
                    'didChangeWatchedFiles': {
                        'dynamicRegistration': False
                    },
                    'symbol': {
                        'dynamicRegistration': False,
                        'symbolKind': {
                            'valueSet': [SymbolKind.File,
                                         SymbolKind.Module,
                                         SymbolKind.Namespace,
                                         SymbolKind.Package,
                                         SymbolKind.Class,
                                         SymbolKind.Method,
                                         SymbolKind.Property,
                                         SymbolKind.Field,
                                         SymbolKind.Constructor,
                                         SymbolKind.Enum,
                                         SymbolKind.Interface,
                                         SymbolKind.Function,
                                         SymbolKind.Variable,
                                         SymbolKind.Constant,
                                         SymbolKind.String,
                                         SymbolKind.Number,
                                         SymbolKind.Boolean,
                                         SymbolKind.Array,
                                         SymbolKind.Object,
                                         SymbolKind.Key,
                                         SymbolKind.Null,
                                         SymbolKind.EnumMember,
                                         SymbolKind.Struct,
                                         SymbolKind.Event,
                                         SymbolKind.Operator,
                                         SymbolKind.TypeParameter]
                        }
                    },
                    'executeCommand': {
                        'dynamicRegistration': False
                    },
                    'configuration': True,
                    'workspaceFolders': True
                },
                'textDocument': {
                    'publishDiagnostics': {'relatedInformation': True},
                    'synchronization': {
                        'dynamicRegistration': False,
                        'willSave': True,
                        'willSaveWaitUntil': False,
                        'didSave': True
                    },
                    'completion': {
                        'dynamicRegistration': False,
                        'contextSupport': True,
                        'completionItem': {
                            'snippetSupport': True,
                            'commitCharactersSupport': True,
                            'documentationFormat': ['plaintext'],
                            'deprecatedSupport': True
                        },
                        'completionItemKind': {
                            'valueSet': [CompletionItemKind.Text,
                                         CompletionItemKind.Method,
                                         CompletionItemKind.Function,
                                         CompletionItemKind.Constructor,
                                         CompletionItemKind.Field,
                                         CompletionItemKind.Variable,
                                         CompletionItemKind.Class,
                                         CompletionItemKind.Interface,
                                         CompletionItemKind.Module,
                                         CompletionItemKind.Property,
                                         CompletionItemKind.Unit,
                                         CompletionItemKind.Value,
                                         CompletionItemKind.Enum,
                                         CompletionItemKind.Keyword,
                                         CompletionItemKind.Snippet,
                                         CompletionItemKind.Color,
                                         CompletionItemKind.File,
                                         CompletionItemKind.Reference,
                                         CompletionItemKind.Folder,
                                         CompletionItemKind.EnumMember,
                                         CompletionItemKind.Constant,
                                         CompletionItemKind.Struct,
                                         CompletionItemKind.Event,
                                         CompletionItemKind.Operator,
                                         CompletionItemKind.TypeParameter]
                        }
                    },
                    'hover': {
                        'dynamicRegistration': False,
                        'contentFormat': ['plaintext']
                    },
                    'signatureHelp': {
                        'dynamicRegistration': False,
                        'signatureInformation': {
                            'documentationFormat': ['plaintext']
                        }
                    },
                    'definition': {'dynamicRegistration': False},
                    'references': {'dynamicRegistration': False},
                    'documentHighlight': {'dynamicRegistration': False},
                    'documentSymbol': {
                        'dynamicRegistration': False,
                        'symbolKind': {
                            'valueSet': [SymbolKind.File,
                                         SymbolKind.Module,
                                         SymbolKind.Namespace,
                                         SymbolKind.Package,
                                         SymbolKind.Class,
                                         SymbolKind.Method,
                                         SymbolKind.Property,
                                         SymbolKind.Field,
                                         SymbolKind.Constructor,
                                         SymbolKind.Enum,
                                         SymbolKind.Interface,
                                         SymbolKind.Function,
                                         SymbolKind.Variable,
                                         SymbolKind.Constant,
                                         SymbolKind.String,
                                         SymbolKind.Number,
                                         SymbolKind.Boolean,
                                         SymbolKind.Array,
                                         SymbolKind.Object,
                                         SymbolKind.Key,
                                         SymbolKind.Null,
                                         SymbolKind.EnumMember,
                                         SymbolKind.Struct,
                                         SymbolKind.Event,
                                         SymbolKind.Operator,
                                         SymbolKind.TypeParameter]
                        }
                    },
                    'codeAction': {'dynamicRegistration': False},
                    'codeLens': {'dynamicRegistration': False},
                    'formatting': {'dynamicRegistration': False},
                    'rangeFormatting': {'dynamicRegistration': False},
                    'onTypeFormatting': {'dynamicRegistration': False},
                    'rename': {'dynamicRegistration': False},
                    'documentLink': {'dynamicRegistration': False},
                    'typeDefinition': {'dynamicRegistration': False},
                    'implementation': {'dynamicRegistration': False},
                    'colorProvider': {'dynamicRegistration': False},
                    'foldingRange': {
                        'dynamicRegistration': False,
                        'rangeLimit': 5000,
                        'lineFoldingOnly': True
                    }
                }
            },

            #
            # The initial trace setting. If omitted trace is disabled ('off').
            #
            # trace?: 'off' | 'messages' | 'verbose';
            'trace': 'off',

            #
            # The workspace folders configured in the client when the server starts.
            # This property is only available if the client supports workspace folders.
            # It can be `null` if the client supports workspace folders but none are
            # configured.
            #
            # Since 3.6.0
            #
            # workspaceFolders?: WorkspaceFolder[] | null;
            # params += '"workspaceFolders": [{"uri": "file:///Users/octref/Code/css-test", "name": "css-test"}]'
            'workspaceFolders': None

        }
        return self._request('initialize', params)


    def completion(self, _file, _version, _line, _character):
        params = {'textDocument': {'uri': f'file:{pathname2url(_file)}',
                                   'version': _version
                                   },
                  'position': {'line': _line,
                               'character': _character
                               },
                  'context': {'triggerKind': CompletionTriggerKind.Invoked}
                  }
        return self._request('textDocument/completion', params)


    def signatureHelp(self, _file, _languageId, _version, _text, _line, _character):
        params = {'textDocument': {'uri': f'file:{pathname2url(_file)}',
                                   'languageId': _languageId,
                                   'version': _version,  # increase after each change, including undo/redo
                                   'text': _text
                                   },
                  'position': {'line': _line,
                               'character': _character
                               }
                  }
        return self._request('textDocument/signatureHelp', params)


    def shutdown(self):
        return self._request('shutdown', None)


    def cancelRequest(self, id):
        params = {'CancelParams': {'id': id}}
        return self._request('$/cancelRequest', params)


    def documentSymbol(self, _file, _version):
        params = {'textDocument': {'uri': f'file:{pathname2url(_file)}',
                                   'version': _version}}
        return self._request('textDocument/documentSymbol', params)


    def formatting(self, _file, _version):
        params = {'textDocument': {'uri': f'file:{pathname2url(_file)}',
                                   'version': _version}}
        return self._request('textDocument/formatting', params)


    def definition(self, _file, _version, _line, _character):
        params = {'textDocument': {'uri': f'file:{pathname2url(_file)}',
                                   'version': _version
                                   },
                  'position': {'line': _line,
                               'character': _character
                               }
                  }
        return self._request('textDocument/definition', params)


    def hover(self, _file, _version, _line, _character):
        params = {'textDocument': {'uri': f'file:{pathname2url(_file)}',
                                   'version': _version
                                   },
                  'position': {'line': _line,
                               'character': _character
                               }
                  }
        return self._request('textDocument/hover', params)


    def references(self, _file, _version, _line, _character, _includeDeclaration=True):
        params = {'textDocument': {'uri': f'file:{pathname2url(_file)}',
                                   'version': _version
                                   },
                  'position': {'line': _line,
                               'character': _character
                               },
                  'context': {'includeDeclaration': _includeDeclaration}
                  }
        return self._request('textDocument/references', params)


    def codeLens(self, _file, _version):
        params = {'textDocument': {'uri': f'file:{pathname2url(_file)}',
                                   'version': _version
                                   }
                  }
        return self._request('textDocument/codeLens', params)


    def rename(self, _file, _version, _line, _character, _new_name):
        params = {'textDocument': {'uri': f'file:{pathname2url(_file)}',
                                   'version': _version
                                   },
                  'position': {'line': _line,
                               'character': _character
                               },
                  'newName': _new_name
                  }
        return self._request('textDocument/rename', params)


    def prepareRename(self, _file, _version, _line, _character):
        params = {'textDocument': {'uri': f'file:{pathname2url(_file)}',
                                   'version': _version
                                   },
                  'position': {'line': _line,
                               'character': _character
                               }
                  }
        return self._request('textDocument/prepareRename', params)


    def foldingRange(self, _file, _version):
        params = {'textDocument': {'uri': f'file:{pathname2url(_file)}',
                                   'version': _version
                                   }
                  }
        return self._request('textDocument/foldingRange', params)


    def declaration(self, _file, _version, _line, _character):
        params = {'textDocument': {'uri': f'file:{pathname2url(_file)}',
                                   'version': _version
                                   },
                  'position': {'line': _line,
                               'character': _character
                               }
                  }
        return self._request('textDocument/declaration', params)


    def typeDefinition(self, _file, _version, _line, _character):
        params = {'textDocument': {'uri': f'file:{pathname2url(_file)}',
                                   'version': _version
                                   },
                  'position': {'line': _line,
                               'character': _character
                               }
                  }
        return self._request('textDocument/typeDefinition', params)


    def documentHighlight(self, _file, _version, _line, _character):
        params = {'textDocument': {
                  'uri': f'file:{pathname2url(_file)}',
                  'version': _version},
                  'position': {
                  'line': _line,
                  'character': _character}
                  }
        return self._request('textDocument/documentHighlight', params)


    def workspace_symbol(self, _query):
        params = {'WorkspaceSymbolParams ': {'query': _query}}
        return self._request('workspace/symbol', params)


    def resolve(self, _label):
        params = {'CompletionItem ': {'label': _label}}
        # label: string;
        # kind?: number;
        # detail?: string;
        # documentation?: string | MarkupContent;
        # deprecated?: boolean;
        # preselect?: boolean;
        # sortText?: string;
        # filterText?: string;
        # insertText?: string;
        # insertTextFormat?: InsertTextFormat;
        # textEdit?: TextEdit;
        # additionalTextEdits?: TextEdit[];
        # commitCharacters?: string[];
        # command?: Command;
        # data?: any
        return self._request('completionItem/resolve', params)


    # not implemented yet


    def __codeAction(self, params): return self._request('textDocument/codeAction', params)

    def __codeLens_resolve(self, params): return self._request('codeLens/resolve', params)

    def __colorPresentation(self, params): return self._request('textDocument/colorPresentation', params)

    def __documentColor(self, params): return self._request('textDocument/documentColor', params)

    def __documentLink(self, params): return self._request('textDocument/documentLink', params)

    def __implementation(self, params): return self._request('textDocument/implementation', params)

    def __onTypeFormatting(self, params): return self._request('textDocument/onTypeFormatting', params)

    def __rangeFormatting(self, params): return self._request('textDocument/rangeFormatting', params)

    def __willSaveWaitUntil(self, params): return self._request('textDocument/willSaveWaitUntil', params)

    def __didChangeWatchedFiles(self, params): return self._request('workspace/didChangeWatchedFiles', params)

    def __didChangeWorkspaceFolders(self, params): return self._request('workspace/didChangeWorkspaceFolders', params)

    def __executeCommand(self, params): return self._request('workspace/executeCommand', params)


    # --------------------------------------------------------------------------------------------------------------------
    # sent from server to client
    #
    # def showMessage(self, params): return self._request('window/showMessage', params)
    # def showMessageRequest(self, params): return self._request('window/showMessageRequest', params)
    # def logMessage(self, params): return self._request('window/logMessage', params)
    # def telemetry_event(self, params): return self._request('telemetry/event', params)
    # def registerCapability(self, params): return self._request('client/registerCapability', params)
    # def unregisterCapability(self, params): return self._request('client/unregisterCapability', params)
    # def workspaceFolders(self, params): return self._request('workspace/workspaceFolders', params)
    # def configuration(self, params): return self._request('workspace/configuration', params)
    # def applyEdit(self, params): return self._request('workspace/applyEdit', params)
