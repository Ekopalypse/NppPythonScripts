import os
import json
import logging
from Npp import notepad

from . import lsp_protocol
from .io_handler import COMMUNICATION_MANAGER
from .client import LSPCLIENT

'''
LSP client implementation for notepad++
'''

__version__ = '0.1'
__all__ = [lsp_protocol, LSPCLIENT, logging, COMMUNICATION_MANAGER]

single_instance = None


def __check_lsp_server_config(lsp_server_configs):
    lsp_configs = dict()
    if isinstance(lsp_server_configs, list):
        for config in lsp_server_configs:
            if isinstance(config, dict):
                for item in config:
                    missing_keys = ''
                    missing_keys += '' if 'pipe' in config[item] else ' pipe'
                    missing_keys += '' if 'executable' in config[item] else ' executable'
                    if missing_keys:
                        print(f'{item} missing_keys {missing_keys}')
                        continue

                    if config[item]['pipe'] in ['tcp', 'io']:
                        if config[item]['pipe'] == 'tcp' and 'tcpretries' in config[item]:
                            if isinstance(config[item]['tcpretries'], int):
                                if config[item]['tcpretries'] < 0:
                                    config[item]['tcpretries'] = 3
                            else:
                                config[item]['tcpretries'] = 3
                    else:
                        print(f'{item} invalid pipe mode:{config[item]["pipe"]}')
                        continue

                    if not os.path.exists(config[item]['executable']):
                        print(f'{item} executable does not exists:{config[item]["executable"]}')
                        continue

                    if 'args' in config[item]:
                        if isinstance(config[item]['args'], list):
                            for arg in config[item]['args']:
                                if not isinstance(arg, str):
                                    print(f'{item} expected string but got {type(arg)} -> {arg}')
                                    continue

                    lsp_configs[item] = config[item]

    if lsp_configs:
        return lsp_configs
    else:
        raise ValueError('No valid lsp server configuration found in config file')


def __check_config(config_file):
    mandatory_keys = ['version', 'loglevel', 'logpath', 'lspservers']
    with open(config_file, 'rb') as f:
        print(f'load:{config_file}')
        config = json.load(f)
    if not all(key in config for key in mandatory_keys):
        raise KeyError(f'Corrupt config file. Missing mandatory key(s):{mandatory_keys}')

    return config


def start(config_file=None):
    '''
        Starts the notepad++ lsp client implementation
        and configures the logging behavior

        Args:
            config_file: expected full path to the config file which must be a valid json file
                         the specification of the file must meet the requirements as shown below

        Returns: True
        Raises: file error if config_file cannot be found or is invalid

        config_file format must be at least like this, if one of these keys is missing
        it is treated as invalid format

        {
            "version": "0.1",
            "loglevel": "info",
            "logpath": "C:\\temp\\npplsplog.txt",
            "lspservers": [
                {
                    "PYTHON": {
                        "pipe": "tcp",
                        "tcpretries" : 3,
                        "executable": "C:\\Python\\Python38_64\\Scripts\\pyls.exe",
                        "args": ["--tcp", "--check-parent-process", "--log-file", "C:\\temp\\log.txt", "-v"]
                    }
                },
                {
                    "RUST": {
                        "pipe": "io",
                        "executable": "C:\\Users\\USERNAME\\.cargo\\bin\\rls.exe"
                    }
                },
                {
                    "TEMPLATE": {
                        "pipe": "io or tcp",
                        "executable": "SOMEDRIVE:\\SOMEPATH\\SOME.exe",
                        "args": ["empty, string or comma delimited strings"]
                    }
                }
            ]
        }
    '''

    global single_instance

    if config_file is None:
        raise ValueError('start method is missing config_file parameter')
    else:
        config = __check_config(config_file)
        if config:
            lsp_server_config = __check_lsp_server_config(config['lspservers'])
            if lsp_server_config:
                logging.basicConfig(
                    filename=config['logpath'],
                    level={
                        'notset': logging.NOTSET,
                        'debug': logging.DEBUG,
                        'info': logging.INFO,
                        'warning': logging.WARNING,
                        'error': logging.ERROR,
                        'fatal': logging.FATAL,
                        'critical': logging.CRITICAL,
                    }.get(config['loglevel'], 'notset'),
                    format='[%(asctime)-15s] [%(thread)-5d] [%(levelname)-10s] %(funcName)-20s  %(message)s'
                )
                logging.info(config)
                # logging.disable(logging.INFO)
                single_instance = LSPCLIENT(lsp_server_config)
                args = {'bufferID': notepad.getCurrentBufferID()}
                single_instance.on_buffer_activated(args)
        else:
            notepad.messageBox('There seems to be an issue with the configuration file!', 'LSP start error')


def stop():
    '''
        trying to stop all running lsp server processes
        and destroying all created objects
    '''
    global single_instance
    if isinstance(single_instance, LSPCLIENT):
        single_instance.terminate()
    single_instance = None


def _send_documet_symbol():
    if isinstance(single_instance, LSPCLIENT):
        single_instance._send_documet_symbol()


def format_document():
    if isinstance(single_instance, LSPCLIENT):
        single_instance._send_document_formatting()


def _send_goto_definition():
    if isinstance(single_instance, LSPCLIENT):
        single_instance._send_goto_definition()


def clear_peek_definition():
    if isinstance(single_instance, LSPCLIENT):
        single_instance._clear_peek_definition()


def peek_definition():
    if isinstance(single_instance, LSPCLIENT):
        single_instance._send_peek_definition()


def hover():
    if isinstance(single_instance, LSPCLIENT):
        single_instance._send_hover()


def _send_references():
    if isinstance(single_instance, LSPCLIENT):
        single_instance._send_references()


def _send_codeLens():
    if isinstance(single_instance, LSPCLIENT):
        single_instance._send_codeLens()


def rename():
    if isinstance(single_instance, LSPCLIENT):
        single_instance._send_rename()


def _send_prepareRename():
    if isinstance(single_instance, LSPCLIENT):
        single_instance._send_prepareRename()


def _send_foldingRange():
    if isinstance(single_instance, LSPCLIENT):
        single_instance._send_foldingRange()


def _send_goto_declaration():
    if isinstance(single_instance, LSPCLIENT):
        single_instance._send_goto_declaration()


def _send_type_definition():
    if isinstance(single_instance, LSPCLIENT):
        single_instance._send_type_definition()


def _send_documentHighlight():
    if isinstance(single_instance, LSPCLIENT):
        single_instance._send_documentHighlight()


def _send_workspace_symbol():
    if isinstance(single_instance, LSPCLIENT):
        single_instance._send_workspace_symbol()


def _send_resolve():
    if isinstance(single_instance, LSPCLIENT):
        single_instance._send_resolve()
