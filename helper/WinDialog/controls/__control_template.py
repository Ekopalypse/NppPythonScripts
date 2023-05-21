from ctypes import create_unicode_buffer
from ctypes.wintypes import DWORD, WORD, SHORT
from ..win_helper import (
    WindowStyle as WS
)

from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Control:
    '''
    Base class for dialog controls.

    This class provides the implementation of a dialog control. It serves as a base class for
    specific controls such as buttons, labels, etc. It is not intended to be instantiated directly.

    Attributes:
        title (str): The title or text displayed on the control.
        size (tuple[int, int]): The width and height of the control.
        position (tuple[int, int]): The x and y coordinates of the control.
        style (int): The style flags for the control.
        ex_style (int): The extended style flags for the control.
        window_class (str): The window class name for the control.
        id (int): The identifier for the control.
        hwnd (int): The handle of the control's window.
        registered_commands (Dict): A dictionary of registered command messages and their associated handlers.
        registered_notifications (Dict): A dictionary of registered notification messages and their associated handlers.

    Methods:
        create(self) -> bytearray:
            Create the control template structure.

            Returns:
                The byte array representing the control template structure.

    Note:
        Do not instantiate this class directly. It should be subclassed by specific controls.
    '''
    # DO NOT CHANGE ORDER !!
    title: str                     = ''
    size: (int, int)               = (10, 10)
    position: (int, int)           = (10, 10)
    style: int                     = WS.VISIBLE | WS.CHILD
    ex_style: int                  = 0
    window_class: str              = ''
    id: int                        = 0
    hwnd: int                      = None
    registered_commands: Dict      = field(default_factory=dict)
    registered_notifications: Dict = field(default_factory=dict)

    def create(self) -> bytearray:
        '''
        Create the control template structure.

        Parameters:
            None.

        Returns:
            bytearray: The byte array representing the control template structure.

        '''
        # DO NOT CHANGE ORDER !!
        # https://learn.microsoft.com/en-us/windows/win32/dlgbox/dlgitemtemplateex
        self._array = bytearray()
        self._array += DWORD(0)  # helpID
        self._array += DWORD(self.ex_style)
        self._array += DWORD(self.style)
        self._array += SHORT(self.position[0])  # x
        self._array += SHORT(self.position[1])  # y
        self._array += SHORT(self.size[0])  # cx
        self._array += SHORT(self.size[1])  # cy
        self._array += DWORD(self.id)
        self._array += create_unicode_buffer(self.window_class)
        self._array += create_unicode_buffer(self.title)
        self._array += WORD(0)  # extraCount
        return self._array
