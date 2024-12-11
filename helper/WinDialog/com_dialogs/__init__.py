"""
COM Dialog Implementation Module

This module provides the implementation of existing built-in COM dialogs.
It includes a base class `FileDialog` that serves as the foundation for specific dialogs such as FileOpenDialog, FileSaveDialog, and more.

The module also includes enums and constants related to specific dialogs.
"""

from enum import IntEnum
from dataclasses import dataclass, field
from typing import Optional, List
from abc import abstractmethod
from ctypes import (
    POINTER, Structure, HRESULT, ARRAY, WINFUNCTYPE,
    c_void_p, c_int,
    byref, cast
)
from ctypes.wintypes import HWND, UINT, LPCWSTR, DWORD, LPWSTR

from ..win_helper import (
    GUID, CoInitialize, CoCreateInstance, CoUninitialize, SHCreateItemFromParsingName
)
from Npp import notepad

class FOS(IntEnum):
    # https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/ne-shobjidl_core-_fileopendialogoptions
    OVERWRITEPROMPT          = 0x2
    STRICTFILETYPES          = 0x4
    NOCHANGEDIR              = 0x8
    PICKFOLDERS              = 0x20
    FORCEFILESYSTEM          = 0x40
    ALLNONSTORAGEITEMS       = 0x80
    NOVALIDATE               = 0x100
    ALLOWMULTISELECT         = 0x200
    PATHMUSTEXIST            = 0x800
    FILEMUSTEXIST            = 0x1000
    CREATEPROMPT             = 0x2000
    SHAREAWARE               = 0x4000
    NOREADONLYRETURN         = 0x8000
    NOTESTFILECREATE         = 0x10000
    HIDEMRUPLACES            = 0x20000
    HIDEPINNEDPLACES         = 0x40000
    NODEREFERENCELINKS       = 0x100000
    OKBUTTONNEEDSINTERACTION = 0x200000
    DONTADDTORECENT          = 0x2000000
    FORCESHOWHIDDEN          = 0x10000000
    DEFAULTNOMINIMODE        = 0x20000000
    FORCEPREVIEWPANEON       = 0x40000000
    SUPPORTSTREAMABLEITEMS   = 0x80000000

class SIGDN(IntEnum):
    # https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/ne-shobjidl_core-sigdn
    NORMALDISPLAY               = 0
    PARENTRELATIVEPARSING       = 0x80018001
    DESKTOPABSOLUTEPARSING      = 0x80028000
    PARENTRELATIVEEDITING       = 0x80031001
    DESKTOPABSOLUTEEDITING      = 0x8004c000
    FILESYSPATH                 = 0x80058000
    URL                         = 0x80068000
    PARENTRELATIVEFORADDRESSBAR = 0x8007c001
    PARENTRELATIVE              = 0x80080001
    PARENTRELATIVEFORUI         = 0x80094001

# class SICHINTF(IntEnum):
    # # https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/ne-shobjidl_core-_sichintf
    # DISPLAY	                      = 0
    # ALLFIELDS	                  = 0x80000000
    # CANONICAL	                  = 0x10000000
    # TEST_FILESYSPATH_IF_NOT_EQUAL = 0x20000000


class COMDLG_FILTERSPEC(Structure):
    # https://learn.microsoft.com/en-us/windows/win32/api/shtypes/ns-shtypes-comdlg_filterspec
    _fields_ = [
        ("name", LPCWSTR),
        ("spec", LPCWSTR),
    ]


@dataclass
class IShellItemArray:
    # https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nn-shobjidl_core-ishellitemarray
    this: c_void_p
    __vtable: ARRAY = field(init=False)
    __release: WINFUNCTYPE = field(init=False)

    def __post_init__(self):
        vtable_ptr = cast(self.this, POINTER(POINTER(c_void_p))).contents
        self.__vtable = cast(vtable_ptr, POINTER(ARRAY(c_void_p, 10))).contents
        self.__release = WINFUNCTYPE(HRESULT, c_void_p)(self.__vtable[2])
        # self.__bind_to_handler = WINFUNCTYPE(HRESULT, c_void_p, ...)(self.__vtable[3])
        # self.__get_property_store = WINFUNCTYPE(HRESULT, c_void_p, ...)(self.__vtable[4])
        # self.__get_property_description_list = WINFUNCTYPE(HRESULT, c_void_p, ...)(self.__vtable[5])
        # self.__get_attributes = WINFUNCTYPE(HRESULT, c_void_p, ...)(self.__vtable[6])
        self.__get_count = WINFUNCTYPE(HRESULT, c_void_p, POINTER(DWORD))(self.__vtable[7])
        self.__get_item_at = WINFUNCTYPE(HRESULT, c_void_p, DWORD, POINTER(c_void_p))(self.__vtable[8])
        # self.__enum_items = WINFUNCTYPE(HRESULT, c_void_p, ...)(self.vtable[9])

    def release(self):
        self.__release(self.this)

    def getCount(self):
        count = DWORD()
        if self.__get_count(self.this, byref(count)) == 0:
            return count.value
        return None

    def getItemAt(self, index):
        ishell_object = c_void_p()
        if self.__get_item_at(self.this, index, byref(ishell_object)) == 0:
            ishell_item = IShellItem(ishell_object)
            selected_item = ishell_item.get_display_name()
            ishell_item.release()
            return selected_item


@dataclass
class IShellItem:
    # https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nn-shobjidl_core-ishellitem
    this: c_void_p
    __vtable: ARRAY = field(init=False)
    __release: WINFUNCTYPE = field(init=False)
    __get_display_name: WINFUNCTYPE = field(init=False)

    def __post_init__(self):
        vtable_ptr = cast(self.this, POINTER(POINTER(c_void_p))).contents
        self.__vtable = cast(vtable_ptr, POINTER(ARRAY(c_void_p, 8))).contents
        self.__release = WINFUNCTYPE(HRESULT, c_void_p)(self.__vtable[2])
        # self.__bind_to_handler = WINFUNCTYPE(HRESULT, c_void_p, ...)(self.__vtable[3])
        # self.__get_parent = WINFUNCTYPE(HRESULT, c_void_p, ...)(self.__vtable[4])
        self.__get_display_name = WINFUNCTYPE(HRESULT, c_void_p, c_int, POINTER(LPWSTR))(self.__vtable[5])
        # self.__get_attributes = WINFUNCTYPE(HRESULT, c_void_p, ...)(self.__vtable[6])
        # self.__compare = WINFUNCTYPE(HRESULT, c_void_p, ...)(self.__vtable[7])

    def release(self):
        self.__release(self.this)

    def get_display_name(self) -> Optional[str]:
        ppszName = LPWSTR()
        if self.__get_display_name(self.this, SIGDN.FILESYSPATH, byref(ppszName)) == 0:
            return ppszName.value
        return None


@dataclass
class FileDialog:
    # https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nn-shobjidl_core-ifiledialog
    '''
    FileDialog Class

    Represents the standard COM-based file dialog window.

    The FileDialog class provides the base functionality of all COM-based dialogs.

    Attributes:
        None

    Note:
        The FileDialog class is intended to be subclassed for specific dialog implementations like FileOpenDialog.
    '''

    this: c_void_p = field(default_factory=c_void_p)  # Represents the COM object instance
    _vtable: ARRAY = field(init=False)

    def __post_init__(self, rclsid, riid, extend_vtable):
        CoInitialize(None)

        result = CoCreateInstance(byref(rclsid), None, 1, byref(riid), byref(self.this))
        if result != 0:
            raise Exception(f"Unable to create dialog, CoCreateInstance failed with {result}")

        vtable_ptr = cast(self.this, POINTER(POINTER(c_void_p))).contents
        self._vtable = cast(vtable_ptr, POINTER(ARRAY(c_void_p, 27+extend_vtable))).contents

        # self._vtable[0] = QueryInterface and self._vtable[1] = AddRef  - not of interest
        self._release = WINFUNCTYPE(HRESULT, c_void_p)(self._vtable[2])
        self._show = WINFUNCTYPE(HRESULT, c_void_p, HWND)(self._vtable[3])
        self._set_file_types = WINFUNCTYPE(HRESULT, c_void_p, UINT, POINTER(COMDLG_FILTERSPEC))(self._vtable[4])
        # self._set_file_type_index = WINFUNCTYPE(HRESULT, c_void_p, UINT)(self._vtable[5])
        # self._get_file_type_index = WINFUNCTYPE(HRESULT, c_void_p, POINTER(UINT))(self._vtable[6])
        # self._advise = WINFUNCTYPE(HRESULT, c_void_p, c_void_p, DWORD)(self._vtable[7])  # IN - IFileDialogEvents
        # self._unadvise = WINFUNCTYPE(HRESULT, c_void_p, DWORD)(self._vtable[8])
        self._set_options = WINFUNCTYPE(HRESULT, c_void_p, DWORD)(self._vtable[9])
        self._get_options = WINFUNCTYPE(HRESULT, c_void_p, POINTER(DWORD))(self._vtable[10])
        self._set_default_folder = WINFUNCTYPE(HRESULT, c_void_p, c_void_p)(self._vtable[11])
        self._set_folder = WINFUNCTYPE(HRESULT, c_void_p, c_void_p)(self._vtable[12])
        # self._get_folder = WINFUNCTYPE(HRESULT, c_void_p, POINTER(c_void_p))(self._vtable[13])  # OUT - IShellItem **ppsi
        # self._get_current_selection = WINFUNCTYPE(HRESULT, c_void_p, POINTER(c_void_p))(self._vtable[14])
        self._set_file_name = WINFUNCTYPE(HRESULT, c_void_p, LPCWSTR)(self._vtable[15])
        # self._get_file_name = WINFUNCTYPE(HRESULT, c_void_p, LPWSTR)(self._vtable[16])
        self._set_title = WINFUNCTYPE(HRESULT, c_void_p, LPCWSTR)(self._vtable[17])
        self._set_ok_button_label = WINFUNCTYPE(HRESULT, c_void_p, LPCWSTR)(self._vtable[18])
        self._set_file_name_label = WINFUNCTYPE(HRESULT, c_void_p, LPCWSTR)(self._vtable[19])
        # self._get_result = WINFUNCTYPE(HRESULT, c_void_p, POINTER(c_void_p))(self._vtable[20])
        self._add_place = WINFUNCTYPE(HRESULT, c_void_p, c_void_p, UINT)(self._vtable[21])
        self._set_default_extension = WINFUNCTYPE(HRESULT, c_void_p, LPCWSTR)(self._vtable[22])
        # self._close = WINFUNCTYPE(HRESULT, c_void_p, HRESULT)(self._vtable[23])
        # self._set_client_guid = WINFUNCTYPE(HRESULT, c_void_p, GUID)(self._vtable[24])
        # self._clear_client_data = WINFUNCTYPE(HRESULT, c_void_p) (self._vtable[25])
        # self._set_filter = WINFUNCTYPE(HRESULT, c_void_p, c_void_p)(self._vtable[26])  # IN IShellItemFilter

    def __del__(self):
        if self.this.value is not None:
            self._release(self.this)
            self.this = None
            CoUninitialize()

    @abstractmethod
    def show(self):
        """
        ...

        Args:
            None.

        Returns:
            None.
        """
        raise NotImplementedError

    def setOptions(self, options):
        """
        ...

        Args:
            None.

        Returns:
            None.
        """
        self._set_options(self.this, options)

    def getOptions(self):
        """
        ...

        Args:
            None.

        Returns:
            None.
        """
        options = DWORD()
        self._get_options(self.this, byref(options))
        return options.value

    # def getResult(self):
        # ishell_object = c_void_p()
        # self._get_result(self.this, byref(ishell_object))

    def setTitle(self, title):
        """
        ...

        Args:
            None.

        Returns:
            None.
        """
        self._set_title(self.this, title)

    def setOkButtonLabel(self, label):
        """
        ...

        Args:
            None.

        Returns:
            None.
        """
        self._set_ok_button_label(self.this, label)

    def setFileName(self, file_name):
        """
        ...

        Args:
            None.

        Returns:
            None.
        """
        self._set_file_name(self.this, file_name)

    def setFileNameLabel(self, label):
        """
        ...

        Args:
            None.

        Returns:
            None.
        """
        self._set_file_name_label(self.this, label)

    def setFileTypes(self, list_of_filters):
        """
        ...

        Args:
            None.

        Returns:
            None.
        """
        count = len(list_of_filters)
        comdlg_filterspec = (COMDLG_FILTERSPEC * count)()
        for i in range(count):
            comdlg_filterspec[i].name = list_of_filters[i][0]
            comdlg_filterspec[i].spec = list_of_filters[i][1]
        self._set_file_types(self.this, count, byref(comdlg_filterspec[0]))

    def __create_shellitem_from_name(self, name):
        item = c_void_p(None)
        SHCreateItemFromParsingName(name, None, GUID('43826D1E-E718-42EE-BC55-A1E261C37BFE'), byref(item))
        return item

    def setDefaultFolder(self, folder_path):
        """
        ...

        Args:
            None.

        Returns:
            None.
        """
        try:
            item = self.__create_shellitem_from_name(folder_path)
            if item.value:
                self._set_default_folder(self.this, item)
        except:
            raise

    def setFolder(self, folder_path):
        """
        ...

        Args:
            None.

        Returns:
            None.
        """
        try:
            item = self.__create_shellitem_from_name(folder_path)
            if item.value:
                self._set_folder(self.this, item)
        except:
            raise

    def addPlace(self, folder_path):
        """
        ...

        Args:
            None.

        Returns:
            None.
        """
        try:
            item = self.__create_shellitem_from_name(folder_path)
            if item.value:
                self._add_place(self.this, item, 1)
        except:
            raise

    def setDefaultExtension(self, default_ext):
        """
        ...

        Args:
            None.

        Returns:
            None.
        """
        self._set_default_extension(self.this, default_ext)


@dataclass
class FileOpenDialog(FileDialog):
    # https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nn-shobjidl_core-ifileopendialog
    '''
    FileOpenDialog Class

    Represents the standard COM-based file open dialog window.

    The FileOpenDialog class provides a template for creating and managing dialog windows.
    It encapsulates properties and behaviors common to dialog windows, such as
    title, size, position, styles, and controls.

    Attributes:
        title (str): The title of the dialog window.
        parent (int): The handle of the parent window for the dialog.

    Note:
        The FileOpenDialog class is intended to be subclassed for specific dialog implementations.
        It provides a base template and common functionality for creating dialog windows.
    '''

    selectedItems: List = field(default_factory=list)
    parent: int = notepad.hwnd

    def __post_init__(self):
        """
        Perform post-initialization tasks for the FileOpenDialog object.

        This method is automatically called after the initialization of the FileOpenDialog object.
        It creates the com object and its vtable (object methods).

        Args:
            None.

        Returns:
            None.
        """
        super().__post_init__(GUID('DC1C5A9C-E88A-4DDE-A5A1-60F82A20AEF7'), GUID('D57C7288-D4AD-4768-BE02-9D969532D960'), 2)
        self._get_results = WINFUNCTYPE(HRESULT, c_void_p, POINTER(c_void_p))(self._vtable[27])
        # self._get_selected_items = WINFUNCTYPE(HRESULT, c_void_p, POINTER(c_void_p))(self._vtable[28])

    def show(self):
        '''
        This method displays the dialog on the screen.
        The method blocks until the dialog is closed.

        Args:
            None

        Returns:
            list: The list of the selected items
        '''
        try:
            self.selectedItems.clear()
            self._show(self.this, self.parent)
            ishell_object = c_void_p()
            if self._get_results(self.this, byref(ishell_object)) == 0:
                ishell_item_array = IShellItemArray(ishell_object)
                count = ishell_item_array.getCount()
                if count:
                    for i in range(count):
                        self.selectedItems.append(ishell_item_array.getItemAt(i))
                ishell_item_array.release()
        except OSError as e:
            if len(e.args) > 3 and e.args[3] == -2147023673:
                pass  # User cancelled dialog
            else:
                raise
        return self.selectedItems


@dataclass
class DirectoryPicker(FileOpenDialog):
    '''
    DirectoryPicker Class

    Represents the standard COM-based file open dialog window.

    The DirectoryPicker class provides a template for creating and managing dialog windows.
    It encapsulates properties and behaviors common to dialog windows, such as
    title, size, position, styles, and controls.

    Attributes:
        title (str): The title of the dialog window.
        parent (int): The handle of the parent window for the dialog.

    '''
    def __post_init__(self):
        """
        Perform post-initialization tasks for the DirectoryPicker object.

        This method is automatically called after the initialization of the DirectoryPicker object.
        It creates the com object, its vtable (object methods) and sets the PICKFOLDERS option.

        Args:
            None.

        Returns:
            None.
        """
        super().__post_init__()
        self._set_options(self.this, FOS.PICKFOLDERS)

    def setOptions(self, options):
        default_options = DWORD()
        if self._get_options(self.this, byref(default_options)) == 0:
            self._set_options(self.this, default_options.value | options)


# @dataclass
# class FileSaveDialog(FileDialog):
    # # https://learn.microsoft.com/en-us/windows/win32/api/shobjidl_core/nn-shobjidl_core-ifilesavedialog
    # '''
    # FileSaveDialog Class

    # Represents the standard COM-based file open dialog window.

    # The FileSaveDialog class provides a template for creating and managing dialog windows.
    # It encapsulates properties and behaviors common to dialog windows, such as
    # title, size, position, styles, and controls.

    # Attributes:
        # title (str): The title of the dialog window.
        # parent (int): The handle of the parent window for the dialog.
    # '''

    # def __post_init__(self):
        # """
        # Perform post-initialization tasks for the FileSaveDialog object.

        # This method is automatically called after the initialization of the FileSaveDialog object.
        # It creates the com object and its vtable (object methods).

        # Args:
            # None.

        # Returns:
            # None.
        # """
        # super().__post_init__(GUID('C0B4E2F3-BA21-4773-8DBA-335EC946EB8B'), GUID('84BCCD23-5FDE-4CDB-AEA4-AF64B83D78AB'), 5)

    # def show(self, hwnd=None):
        # try:
            # self._show(self.this, hwnd)
        # except OSError as e:
            # if len(e.args) > 3 and e.args[3] == -2147023673:
                # pass  # User cancelled dialog
            # else:
                # raise
