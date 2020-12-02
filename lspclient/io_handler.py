'''
    Responsible for starting, stoping and communicating with the respective LSP servers
    by monitoring the input/output channels
    Sends an NEW_LSP_MESSAGE_RECEIVED event when receiving new messages from LSP servers
'''

import threading
import subprocess
import queue
import socket
import select
import time
import logging
log = logging.info


class TCP_OBJECT:
    def __init__(self, proc_config):
        self.config = proc_config


    def start(self):
        ''' start_process '''
        def _start_tcp_client(self, port, max_tcp_retry=0, ip=None):
                ''' _start_tcp_client '''
                _socket = None
                if ip is None:
                    ip = 'localhost'
                while max_tcp_retry >= 0:
                    try:
                        _socket = socket.create_connection((ip, port))
                        max_tcp_retry = -1
                    except Exception as e:  # pylint: disable=W0703
                        log(f'{e}')
                        time.sleep(1)
                        max_tcp_retry -= 1
                return _socket

        executable = self.config['executable']
        args = self.config.get('args', None)
        if args is None:
            args = [executable]
        else:
            args.insert(0, executable)

        max_tcp_retries = self.config['tcpretries']
        port = self.config.get('port', 2087)

        si = subprocess.STARTUPINFO()
        si.dwFlags = subprocess.STARTF_USESTDHANDLES
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        process = None
        _socket = None
        try:
            process = subprocess.Popen(args,
                                 startupinfo=si,
                                 cwd=executable.rpartition('\\')[0],
                                 close_fds=False)
            if process:
                _socket = self._start_tcp_client(port, max_tcp_retries)
                if _socket is None:
                    log('failed to establish a connection - going to stop lsp process')
                    process.kill()
                    process = None

        except Exception as e:  # pylint: disable=W0703
            log(f'{e}')
            process = None
            _socket = None
        return process, _socket


    def stop(self):
        raise NotImplementedError


    def send_to(self, message):
        raise NotImplementedError


    def read_from(self):
        raise NotImplementedError


class PIPE_OBJECT:
    def __init__(self, proc_config):
        log('PIPE_OBJECT')
        self.config = proc_config
        self.process = None


    def start(self):
        ''' start_process '''
        log(f'{self.config["executable"]}')
        executable = self.config['executable']
        args = self.config.get('args', None)
        if args is None:
            args = [executable]
        else:
            args.insert(0, executable)

        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        try:
            self.process = subprocess.Popen(args,
                                            stdin=subprocess.PIPE,
                                            stdout=subprocess.PIPE,
                                            startupinfo=si,
                                            cwd=executable.rpartition('\\')[0],
                                            close_fds=False)
            log(f'{self.process.pid}')
        except Exception as e:  # pylint: disable=W0703
            log(f'{e}')
            self.process = None
        return self, None


    def stop(self):
        raise NotImplementedError


    def send_to(self, message):
        log(f"{message.encode('UTF-8')}")
        self.process.stdin.write(message.encode('UTF-8'))
        self.process.stdin.flush()


    def read_from(self):
        raise NotImplementedError


class PROCESS_MONITOR(threading.Thread):
    def __init__(self, queue_obj=None, com_obj=None, callback=None, ready_event=None):
        log('PROCESS_MONITOR')
        super(PROCESS_MONITOR, self).__init__()
        self.keep_reading = True
        self.queue = queue_obj
        self.com_obj = com_obj
        self.callback = callback
        self.ready = ready_event


    def enqueue_io_messsage(self, out):
        ''' enqueue_io_messsage '''
        log(f'{out}')
        self.ready.set()
        while self.keep_reading:
            for line in iter(out.readline, ''):
                log(line)
                if line == b'\r\n':
                    continue
                parts = line.split(b'\r\n')
                if parts[0].find(b'Content-Length: ') > -1:
                    log(f'{parts[0]=}')
                    header_parts = parts[0].split()
                    log(f'{header_parts=}')
                    if len(header_parts) > 1:
                        expected_content_length = int(header_parts[1])
                        log(f'{expected_content_length=}')
                        content = out.read(expected_content_length).lstrip()
                        log(f'{content=}')
                        while (start_json := content.find(b'{')) != 0:
                            log(f'{start_json=}')
                            if start_json > 0:
                                content += out.read(expected_content_length-len(content)+start_json)
                                break
                            elif start_json == -1:
                                content += out.read(expected_content_length)
                        log(f'full: {content=}')
                    else:
                        log(f'Content header without length !! ???? {parts}')
                        break

                log(f'callback: {content.decode()[-expected_content_length:]}')
                self.callback(content.decode()[-expected_content_length:])
                break
            time.sleep(0.1)


    def enqueue_tcp_messsage(self, _socket, queue):
        ''' enqueue_output '''
        self.ready.set()
        BUFF_SIZE = 4096
        fragments = []
        try:
            while _socket:
                infds, outfds, errfds = select.select([_socket], [_socket], [], None)
                if len(infds) != 0:
                    chunck = _socket.recv(BUFF_SIZE)
                    if b'Content-Length: ' in chunck:
                        if chunck.startswith(b'Content-Length: '):
                            if len(fragments) > 0:
                                self.callback(''.join(fragments))
                                fragments = []
                            fragments.append(chunck)
                        else:
                            split_position = chunck.find(b'Content-Length: ')
                            fragments.append(chunck[:split_position])
                            self.callback(''.join(fragments))
                            fragments = []
                            fragments.append(chunck[split_position:])
                    else:
                        fragments.append(chunck)
                else:
                    if len(fragments) > 0:
                        msg = ''.join(fragments)
                        length = int(msg[16:msg.find('\r\n')].strip())
                        content = len(msg[msg.find('{'):])
                        if length == content:
                            self.callback(msg)
                            fragments = []
                    else:
                        time.sleep(.1)
        except Exception as e:  # pylint: disable=W0703
            log(f'{e}')
        finally:
            log('going to close socket')
            _socket.close()


    def run(self):
        log('process monitor started')
        if isinstance(self.com_obj, PIPE_OBJECT):
            self.enqueue_io_messsage(self.com_obj.process.stdout)
        # elif isinstance(self.com_obj, socket._socketobject):
            # self.enqueue_tcp_messsage(self.com_obj, self.queue)
        else:
            log(f'unknown object:{self.com_obj}')


class COMMUNICATION_MANAGER:
    def __init__(self, lsp_server_configs, on_receive_callback):
        log('communication manager')
        self.available_servers = lsp_server_configs
        self.running_servers = dict()
        self.callback = on_receive_callback
        self.com_obj = None
        self.current_queue = None
        self.max_queue_wait_time = 2.0


    def start_process(self, proc_config):
        ''' start_process '''
        log(f'{proc_config}')
        if proc_config['pipe'] == 'io':
            process, _socket = PIPE_OBJECT(proc_config).start()
        else:
            process, _socket = TCP_OBJECT(proc_config).start()

        return process, _socket


    def send(self, lspmessage, waiting_for_msg=True):
        ''' Called by client on various notepad++ and scintilla events '''
        self.com_obj.send_to(lspmessage)


    def already_initialized(self, language):
        log(f'{language}')
        if language in self.running_servers:
            self.com_obj = self.running_servers[language][1]
            self.current_queue = self.running_servers[language][0].queue
            return True
        else:
            obj, _socket = self.start_process(self.available_servers[language])
            if obj:
                if _socket:
                    self.com_obj = _socket
                else:
                    self.com_obj = obj
                self.current_queue = queue.Queue()
                ready = threading.Event()
                process_monitor = PROCESS_MONITOR(self.current_queue, self.com_obj, self.callback, ready)
                process_monitor.setDaemon(True)
                start = time.time()
                process_monitor.start()
                ready.wait(2)
                log(f'thread start took {time.time() - start}')
                log(f'self.com_obj:{type(self.com_obj)}')
                self.running_servers[language] = (process_monitor, self.com_obj)
        return False


    def stop_monitoring_thread(self, language):
        log(f'{language}')
        self.com_obj = language[1]
        language[0].keep_reading = False


    def running_monitoring_threads(self):
        for language in self.running_servers.keys():
            yield self.running_servers[language]
