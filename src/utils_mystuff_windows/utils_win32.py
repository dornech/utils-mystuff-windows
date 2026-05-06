# utilities - Windows-OS specific utilities

"""
Module provides various routines to deal with application windows.
NOTE: Windows platform only


Example / doctest:
```
>>> import utils_mystuff_windows
>>> print(find_window_ctypes("Excel"))
>>> print(find_window_win32gui("Excel"))
>>> print(find_window_ctypes("Access"))
>>> print(find_window_win32gui("Access"))

```
"""


# ruff and mypy per file settings
#
# empty lines
# ruff: noqa: E302, E303, E305
# naming conventions
# ruff: noqa: N801, N802, N803, N806, N812, N813, N815, N816, N818, N999
# others
# ruff: noqa: FBT001, FBT002, E501, F403, F405, F841, PLR0917, S605
#
# disable mypy errors
# mypy: disable-error-code = "name-defined, attr-defined"

# fmt: off



from typing import Any

import os
import ctypes
import win32gui
import psutil

import time

from enum import Enum

import utils_mystuff as Utils


# read file association info via Win323API

# Constants for AssocQuery: flags enumeration
class ASSOCF(Enum):
    NONE = 0x0
    INIT_NOREMAPCLSID = 0x1
    INIT_BYEXENAME = 0x2
    OPEN_BYEXENAME = 0x2
    INIT_DEFAULTTOSTAR = 0x4
    INIT_DEFAULTTOFOLDER = 0x8
    NOUSERSETTINGS = 0x10
    NOTRUNCATE = 0x20
    VERIFY = 0x40
    REMAPRUNDLL = 0x80
    NOFIXUPS = 0x100
    IGNOREBASECLASS = 0x200
    INIT_IGNOREUNKNOWN = 0x400

# Constants for AssocQuery: command enumeration
class ASSOCSTR(Enum):
    COMMAND = 1
    EXECUTABLE = 2
    FRIENDLYDOCNAME = 3
    FRIENDLYAPPNAME = 4
    NOOPEN = 5
    SHELLNEWVALUE = 6
    DDECOMMAND = 7
    DDEIFEXEC = 8
    DDEAPPLICATION = 9
    DDETOPIC = 10
    INFOTIP = 11
    QUICKTIP = 12
    TILEINFO = 13
    CONTENTTYPE = 14
    DEFAULTICON = 15
    SHELLEXTENSION = 16

# Load the Windows shlwapi DLL
shlwapi = ctypes.WinDLL('shlwapi', use_last_error=True)

# define AssocQueryString function signature - ANSI
AssocQueryStringA = shlwapi.AssocQueryStringA
AssocQueryStringA.argtypes = [
    ctypes.wintypes.DWORD,  # flags
    ctypes.wintypes.DWORD,  # str
    ctypes.wintypes.LPCSTR,  # pszAssoc
    ctypes.wintypes.LPCSTR,  # pszExtra
    ctypes.wintypes.LPSTR,  # pszOut
    ctypes.POINTER(ctypes.wintypes.DWORD)  # pcchOut
]
AssocQueryStringA.restype = ctypes.HRESULT
# define AssocQueryString function signature - double byte
AssocQueryStringW = shlwapi.AssocQueryStringW
AssocQueryStringW.argtypes = [
    ctypes.wintypes.DWORD,  # flags
    ctypes.wintypes.DWORD,  # str
    ctypes.wintypes.LPCWSTR,  # pszAssoc
    ctypes.wintypes.LPCWSTR,  # pszExtra
    ctypes.wintypes.LPWSTR,  # pszOut
    ctypes.POINTER(ctypes.wintypes.DWORD)  # pcchOut
]
AssocQueryStringW.restype = ctypes.HRESULT

def get_assoc_query(extension: str, assoc_str: int = ASSOCSTR.EXECUTABLE.value) -> str:
    """
    get_assoc_query - read file extension association info via Win32API

    file extension association info is read via Win32API call.
    Watch out for ANSI vs double byte version(s)! Since UTF-8 ist standard in Python,
    using the double byte version avoids some conversion stuff.

    Args:
        extension (str): extension association info is looked for
        assoc_str (ASSOCSTR): association info index

    Returns:
        value
    """
    # Step 1: Determine buffer size
    buffer_len = ctypes.wintypes.DWORD(0)
    hr = AssocQueryStringA(ASSOCF.NONE.value, assoc_str, extension.encode('cp1252'), None, None, ctypes.byref(buffer_len))
    # hr = AssocQueryStringW(ASSOCF.NONE.value, assoc_str, extension, None, None, ctypes.byref(buffer_len))
    if buffer_len.value == 0:
        return ""

    # Step 2: Allocate buffer and retrieve the value
    buffer = ctypes.create_string_buffer(buffer_len.value)
    hr = AssocQueryStringA(ASSOCF.NONE.value, assoc_str, extension.encode('cp1252'), None, buffer, ctypes.byref(buffer_len))
    result = buffer.value.decode()
    # buffer = ctypes.create_unicode_buffer(buffer_len.value)
    # hr = AssocQueryStringW(ASSOCF.NONE.value, assoc_str, extension, None, buffer, ctypes.byref(buffer_len))
    # result = buffer.value
    if hr != 0:  # S_OK is 0
        return ""

    return result


# find windows from title

# variant using ctypes
# http://makble.com/how-to-find-window-with-wildcard-in-python-and-win32gui
def find_window_ctypes(title: str, partial_allowed: bool = True) -> Any:
    """
    find_window_ctypes - find windows from title, variant using ctypes

    Args:
        title (str): window title
        partial_allowed (bool): partial matching of title allowed

    Returns:
        Union[str, bool]: title if found, False otherwise
    """
    titles = []

    def foreach_window_gettitle(hwnd, lParam):
        if ctypes.windll.user32.IsWindowVisible(hwnd):
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            classname = ctypes.create_unicode_buffer(100 + 1)
            ctypes.windll.user32.GetClassNameW(hwnd, classname, 100 + 1)
            buff = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
            titles.append((hwnd, buff.value.encode(), classname.value, ctypes.windll.user32.IsIconic(hwnd)))
        return True

    def refresh_wins() -> Any:
        titles: list[str] = []
        ctypes.windll.user32.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.POINTER(ctypes.c_int))(foreach_window_gettitle), 0)

    refresh_wins()
    # exact matching of title
    for item in titles:
        if title == str(item[1].decode()):
            return item[0]
    # partial matching of title
    if partial_allowed:
        for item in titles:
            if title in str(item[1].decode()):
                return item[0]
    return False

# variant using win32gui
def find_window_win32gui(title: str, partial_allowed: bool = True) -> Any:
    """
    find_window_ctypes - find windows from title, variant using win32gui

    Args:
        title (str): window title
        partial_allowed (bool): partial matching of title allowed

    Returns:
        Union[str, bool]: title if found, False otherwise
    """
    titles = []

    def foreach_window_gettitle(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd):
            classname = win32gui.GetClassName(hwnd)
            title = win32gui.GetWindowText(hwnd)
            titles.append((hwnd, title, classname, win32gui.IsIconic(hwnd)))
        return True

    def refresh_wins():
        titles = []
        win32gui.EnumWindows(foreach_window_gettitle, 0)

    refresh_wins()
    # exact matching of title
    for item in titles:
        if title == str(item[1]):
            return item[0]
    # partial matching of title
    if partial_allowed:
        for item in titles:
            if title in str(item[1]):
                return item[0]
    return False


# close window / application depending on title

WM_CLOSE = 0x0010

# variant using ctypes
def close_app_windowtitle_ctypes(title: str, partial_allowed: bool = True, timeout: int = 5) -> None:
    """
    close_app_windowtitle_ctypes - close window / application depending on title, variant using ctypes

    Args:
        title (str): window title
        partial_allowed (bool): partial matching of title allowed
        timeout (int): timeout for waiting after closing
    """
    hwnd = find_window_ctypes(title, partial_allowed)
    if hwnd:
        ctypes.windll.user32.SendMessageA(hwnd, WM_CLOSE, 0, 0)
        starttime = time.time()
        while ctypes.windll.user32.IsWindow(hwnd) and time.time() < starttime + timeout:
            time.sleep(0.1)

# variant using win32gui
def close_app_windowtitle_win32gui(title: str, partial_allowed: bool = True, timeout: int = 5) -> None:
    """
    close_app_windowtitle_win32gui - close window / application depending on title, variant using win32gui

    Args:
        title (str): window title
        partial_allowed (bool): partial matching of title allowed
        timeout (int): timeout for waiting after closing
    """
    hwnd = find_window_win32gui(title, partial_allowed)
    if hwnd:
        win32gui.SendMessage(hwnd, WM_CLOSE, 0, 0)
        starttime = time.time()
        while win32gui.IsWindow(hwnd) and time.time() < starttime + timeout:
            time.sleep(0.1)

# variant using taskkill
# https://stackoverflow.com/questions/52203803/wildcard-in-taskkill-windowtitle
# note:
# - execution is pretty slow
# - watch out % vs %% in direct entry vs cmd-files
def close_app_windowtitle_taskkill(title: str) -> None:
    """
    close_app_windowtitle_taskkill - close window / application depending on title, variant using taskkill

    Args:
        title (str): window title
    """
    # os.system("taskkill /F /FI 'WINDOWTITLE eq {title}*'")   # wildcard not allowed at beginning of title
    os.system(f"for /f \"tokens=2 delims=,\" %a in ('tasklist /v /fo:csv /nh ^| findstr /r \"{title}\"') do taskkill /pid %a")
    time.sleep(0.1)

# callpoint
def close_app_windowtitle(title: str, partial_allowed: bool = True, timeout: int = 5) -> None:
    """
    close_app_windowtitle - close window / application depending on title

    Args:
        title (str): window title
        partial_allowed (bool): partial matching of title allowed
        timeout (int): timeout for waiting after closing
    """
    close_app_windowtitle_win32gui(title, partial_allowed, timeout)


# wait for open window (overcome delay in asynchronuous processing subprocess.Popen)

# variant using ctypes
def wait_for_window_ctypes(title: str, partial_allowed: bool = True, timeout: int = 5, wait: float = 0.25) -> None:
    """
    wait_for_window_ctypes - wait for close window (overcome delay in asynchronous processing subprocess.Popen)

    Args:
        title (str): window title
        partial_allowed (bool): partial matching of title allowed
        timeout (int, optional): timeout time. Defaults to 5.
        wait (float, optional): wait time. Defaults to 0.25.
    """
    starttime = time.time()
    while time.time() < starttime + timeout:
        hwnd = find_window_ctypes(title, partial_allowed)
        if hwnd:
            return
        else:
            time.sleep(wait)
    return

# variant using win32gui
def wait_for_window_win32gui(title: str, partial_allowed: bool = True, timeout: int = 5, wait: float = 0.25) -> None:
    """
    wait_for_window_win32gui - wait for close window (overcome delay in asynchronous processing subprocess.Popen)

    Args:
        title (str): window title
        partial_allowed (bool): partial matching of title allowed
        timeout (int, optional): timeout time. Defaults to 5.
        wait (float, optional): wait time. Defaults to 0.25.
    """
    starttime = time.time()
    while time.time() < starttime + timeout:
        hwnd = find_window_win32gui(title, partial_allowed)
        if hwnd:
            return
        else:
            time.sleep(wait)
    return

# callpoint
def wait_for_window(title: str, partial_allowed: bool = True, timeout: int = 5, wait: float = 0.25) -> None:
    """
    wait_for_window - wait for close window (overcome delay in asynchronous processing subprocess.Popen)

    Args:
        title (str): window title
        partial_allowed (bool): partial matching of title allowed
        timeout (int, optional): timeout time. Defaults to 5.
        wait (float, optional): wait time. Defaults to 0.25.
    """
    wait_for_window_win32gui(title, partial_allowed, timeout, wait)



# close file
def close_app_file(filename: str, msg: str, title: str, partial_allowed: bool = True, timeout: int = 5, kill_app: bool = True) -> None:
    """
    close_app_file - close data file opened by an application

    Args:
        filename (str): filename
        msg (str): message for alert box
        title (str): title for alert box
        partial_allowed (bool): partial matching of title allowed
        timeout (int): timeout for waiting after closing
        kill_app (bool): kill application locking file to be closed
    """

    # first attempt: close by window title
    if Utils.file_locked(filename):
        close_app_windowtitle(filename, partial_allowed, timeout)
    if Utils.file_locked(filename):
        close_app_windowtitle(os.path.splitext(os.path.basename(filename))[0], partial_allowed, timeout)
    # second attempt: kill respective process
    if Utils.file_locked(filename):
        executable = get_assoc_query(os.path.splitext(filename)[1])
        for proc in psutil.process_iter(['exe']):
            try:
                if proc.info['exe'] and os.path.normcase(proc.info['exe']) == os.path.normcase(executable):
                    proc.kill()
                    proc.wait(timeout=5)
                    starttime = time.time()
                    while Utils.file_locked(filename) and time.time() < starttime + timeout:
                        time.sleep(0.1)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                pass
    # third attempt:request to close manually
    while Utils.file_locked(filename):
        Utils.alertbox(msg, title)
