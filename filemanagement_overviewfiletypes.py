r"""
================================================================================
  FILE TYPE CLEANER
  Overview and cleanup of file types in a folder tree on Windows
================================================================================

PURPOSE
  Data recovered from damaged drives usually contains huge amounts of useless
  files: fragments, temporary files, caches and leftovers of the operating
  system. This program shows which file types exist in a folder and all of its
  subfolders and deletes exactly the file types you no longer need.

MODES (main menu)
  1  Scan            Lists every file type (extension) with number of files
                     and total size, sorted by number of files.
  2  Delete          Deletes all files of the file types you type in, for
                     example ".chk .tmp". Without a scan there is no list
                     and no preselection, see SELECTING FILE TYPES.
  3  Scan + delete   Scans first, then you choose the file types to delete,
                     either in the selection window or in the console by
                     their number in the list, by a range with exclusions or
                     by typing the extension.

SELECTING FILE TYPES
  After a scan (mode 3) the console asks whether to open the selection
  window, see SELECTION WINDOW. Otherwise the file types are chosen in the
  console from the numbered list:
    5                   number 5 of the list
    1 3 5-7             numbers 1, 3 and 5 to 7
    10-30 (22 24)       numbers 10 to 30 except 22 and 24
    1-40 (5-9 .jpg)     numbers 1 to 40 except 5 to 9 and the file type .jpg
    .chk .tmp           file types by their extension
  All forms can be combined, separated by spaces, commas or semicolons.
  Exclusions in brackets belong to the range directly in front of them and
  must lie inside of it. Numbers outside of the list, file types the scan did
  not find, broken ranges and missing brackets are rejected with a message
  and the question is asked again.
  Without a scan (mode 2) the program does not know which file types exist,
  so there is no list and no preselection: the file types are typed by their
  extension, numbers and ranges are rejected. File types the folder does not
  contain are simply not found.
  In both modes a single "." stands for all files without extension, see
  FILES WITHOUT EXTENSION, and a file type made of digits is typed with its
  dot, for example .001, because digits alone are read as a number. File
  types containing spaces, commas, semicolons or brackets can only be chosen
  by their number after a scan.
  Only files whose last extension, or for files without extension whose
  name, equals one of the chosen file types are deleted, upper and lower case
  do not matter. Pressing Enter without input cancels the selection and
  nothing is deleted.

FILES WITHOUT EXTENSION
  A file without extension, for example .gitignore, README or Makefile,
  forms a file type of its own, named after the file. Upper and lower case
  do not matter, so README and readme are one file type. Like extensions
  the names are shown in lower case: the scan lists "no extension: readme"
  with the number of files of that name.
  After a scan (mode 3) files without extension can be chosen one by one,
  by their number or in the selection window, and a single "." chooses all
  of them at once. In the selection window the filter "no extension" shows
  all of them, "Select all" then ticks them together. Without a scan
  (mode 2) only "." is possible, it chooses all files without extension
  whatever their name.
  Typed, .gitignore always means an extension, as in backup.gitignore, so a
  file named .gitignore itself is chosen by its number or in the window.

SELECTION WINDOW (dark mode)
  Lists every file type of the scan with the number of its files and a
  checkbox, made for long lists with hundreds or thousands of file types.
  It opens with nothing ticked.
  * Ticked file types are deleted: every file of these types in the target
    folder and all its subfolders. Ticked rows are red.
  * Click a checkbox or press Space to switch the selected rows. Ctrl+A
    selects all rows.
  * "Select all" ticks and "Deselect all" unticks every file type shown, so
    together with the filter for example all file types containing "tmp".
  * Click a column title to sort by file type or by number of files.
  * "Continue with the ticked file types" hands the ticks to the console,
    which shows the deletion plan and asks before anything is deleted.
    Closing the window cancels, nothing is deleted.
  The window needs PySide6. Without it the file types are chosen in the
  console.

ARCHIVES
  ZIP files and other archives (.7z, .rar, .tar, .gz, .cab, ...) are never
  opened or searched. They count as files of their own type, for example
  .zip, and are deleted as a whole when that type is chosen. Only the last
  extension counts, so backup.tar.gz is a .gz file.

OPTIONS ASKED FOR EVERY RUN
  * Operating system files: include or exclude. A system file is any file or
    folder with the Windows "System" attribute plus well known system items
    such as $RECYCLE.BIN, System Volume Information, pagefile.sys, desktop.ini
    or Thumbs.db (also when the attribute got lost during the recovery).
    Excluded system folders are not entered at all.
  * Reports: save the overview and a log of every deleted file as text files
    in the folder "reports" next to this script.
  * Deletion method: recycle bin (default), permanent, or a simulation that
    only shows what would be deleted.
  * Empty folders after deleting: keep them, remove only the folders that
    became empty through the deletion, or remove all empty folders. Empty
    folders go the same way as the files: to the recycle bin, deleted
    permanently, or only shown in a simulation. A folder is moved to the
    recycle bin only if it is still empty right then. Every folder goes to
    the recycle bin on its own, so nested empty folders become separate
    entries there: restoring a folder does not bring back its subfolders.

STATUS OUTPUT
  * A live counter shows that the program is working.
  * Every minute a status line shows the elapsed time and the current folder.
  * At the end: files and size per file type, deleted and failed files,
    removed folders, skipped items and the duration.

SAFETY
  * Only the target folder and its subfolders are touched. Links, junctions
    and other reparse points are never followed or deleted, so the program
    cannot reach anything outside of the target folder. This matters for
    recovered system drives, whose junctions can point to your current C: drive.
  * The recycle bin and System Volume Information currently used by Windows
    on that drive are never entered.
  * Windows, Program Files, ProgramData, your user profile and every folder
    containing one of them are refused as target folder.
  * The program never deletes itself. Windows does not stop a running script
    from deleting its own file, so the program compares paths: the script is
    skipped by the scan and the deletion, and a folder holding it is never
    removed. Only the script itself is protected: other files next to it,
    for example other scripts or older reports in the folder "reports", are
    treated like all other files when they lie in the target folder. The
    deletion log being written is locked by Windows and cannot be deleted.
  * A real deletion only starts after the deletion plan was shown and
    confirmed by typing "yes" (recycle bin) or "delete" (permanent).
  * The recycle bin is only offered for drives that have one (internal and
    external hard disks, not USB sticks or network drives). If Windows cannot
    recycle a single file, for example because it is larger than the recycle
    bin, a Windows dialog asks before that file is deleted permanently.

REQUIREMENTS
  * Windows 10 or 11
  * Python 3.8 or newer, the console uses only the standard library
  * PySide6 6.5 or newer for the optional selection window, installed with
    python -m pip install PySide6
  * Administrator rights only for files your user account may not delete

USAGE
  Start with the target folder:
    python filemanagement_overviewfiletypes.py "F:\Recovered"
  Start without, the program asks for it:
    python filemanagement_overviewfiletypes.py
  Instead of typing the command, the folder can be dragged onto the script file.
  A folder given at start that does not exist or is not allowed is refused
  with a message and the program does not start. In the program the folder
  is asked for every run: Enter keeps the last one, or type, paste or drag
  another one into the console window.
  Questions show the possible answers in parentheses, for example (y/n), and
  the default in brackets, for example [n]. Enter takes the default.
  While the selection window is open the console waits, closing the window
  or "Continue with the ticked file types" brings you back to the console.
  Ctrl+C stops a running scan or deletion safely and shows the results so far.
  During a question it returns to the main menu, in the selection window it
  closes the window.
  Clicking into the console window pauses the program (QuickEdit mode of
  Windows), press Esc to let it continue.
  Intervals, batch size and other values can be adjusted in SETTINGS below.
================================================================================
"""

# ==============================================================================
#   IMPORTS
# ==============================================================================

from __future__ import annotations

import argparse
import ctypes
import os
import re
import shutil
import signal
import stat
import string
import sys
import time
import traceback
from ctypes import wintypes
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Callable, Dict, Iterable, Iterator, List, NamedTuple, Optional, Set, Tuple

try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError as pyside_import_error:
    # Only the optional selection window needs PySide6, the console works without it
    PYSIDE_IMPORT_ERROR = str(pyside_import_error)
else:
    PYSIDE_IMPORT_ERROR = ""


# ==============================================================================
#   SETTINGS
# ==============================================================================

STATUS_INTERVAL_SECONDS = 60            # status line with the current folder
LIVE_COUNTER_INTERVAL_SECONDS = 0.5     # refresh rate of the live counter line
RECYCLE_BIN_BATCH_SIZE = 100            # files per recycle bin call, more is faster
CONSOLE_EXAMPLE_LIMIT = 15              # paths listed per problem type in the console
STORED_EXAMPLE_LIMIT = 100_000          # paths kept per problem type for reports
CONSOLE_TYPE_COLUMN_WIDTH = 24          # width of the file type column in the console
REPORT_TYPE_COLUMN_WIDTH = 60           # width of the file type column in report files
REPORT_FOLDER_NAME = "reports"          # created next to this script when saving reports


# ==============================================================================
#   DEFINITIONS
# ==============================================================================

# ==== General =================================================================

PROGRAM_TITLE = "FILE TYPE CLEANER"
PROGRAM_SUBTITLE = "Overview and cleanup of file types in a folder and all its subfolders"
SCRIPT_FILE_NAME = os.path.basename(__file__)   # shown in the start hints
# Location of this script with links resolved. Windows lets a running script delete its own file,
# so every path the program deletes is compared with it.
SCRIPT_PATH = os.path.realpath(__file__)
LINE_WIDTH = 80
NO_EXTENSION_LABEL = "no extension"     # shown before the name of a file without extension
NO_EXTENSION_TYPE_PREFIX = "/"          # file type of a file without extension: this prefix and its name.
                                        # A slash cannot occur in names, and extensions start with a dot
ALL_NO_EXTENSION_TYPE = NO_EXTENSION_TYPE_PREFIX    # all files without extension, chosen by "." without scan
ALL_NO_EXTENSION_LABEL = "all without extension"  # fits into the file type column of the console
NO_EXTENSION_INPUT = "."                # typed by the user to select all files without extension
YES_ANSWERS = frozenset({"y", "yes", "j", "ja"})
NO_ANSWERS = frozenset({"n", "no", "nein"})

# ==== Operating system items ==================================================

# Folder names that always belong to Windows, compared in lower case
OPERATING_SYSTEM_FOLDER_NAMES = frozenset({
    "$recycle.bin",                     # recycle bin since Windows Vista
    "recycler",                         # recycle bin of Windows XP
    "recycled",                         # recycle bin of Windows 98 and old FAT drives
    "system volume information",        # restore points, search index, volume data
    "$windows.~bt",                     # Windows upgrade data
    "$windows.~ws",                     # Windows upgrade data
    "$winreagent",                      # Windows recovery agent data
    "$sysreset",                        # Windows reset data
    "config.msi",                       # Windows Installer rollback data
})

# File names that always belong to Windows, compared in lower case
OPERATING_SYSTEM_FILE_NAMES = frozenset({
    "pagefile.sys", "swapfile.sys", "hiberfil.sys",     # virtual memory and hibernation
    "desktop.ini", "thumbs.db", "ehthumbs.db",          # Explorer folder settings and thumbnails
    "ehthumbs_vista.db", "iconcache.db",                # Explorer caches
    "bootmgr", "bootnxt", "bootsect.bak",               # Windows boot manager
    "ntldr", "ntdetect.com", "boot.ini",                # Windows XP boot files
    "io.sys", "msdos.sys",                              # DOS and Windows 98 boot files
    "dumpstack.log", "dumpstack.log.tmp",               # crash dump logs
})

# Folders in the root of a drive that Windows is using right now.
# They are never entered, not even when system files are included.
ACTIVE_VOLUME_FOLDER_NAMES = ("$recycle.bin", "system volume information")

# ==== Paths and names =========================================================

EXTENDED_PATH_PREFIX = "\\\\?\\"            # lifts the 260 character limit of Windows paths
EXTENDED_UNC_PATH_PREFIX = "\\\\?\\UNC\\"   # the same for network paths
UNSAFE_NAME_CHARACTERS = frozenset('<>:"|?*')   # invalid in Windows names, * and ? are wildcards
RESERVED_DEVICE_NAMES = frozenset(
    ["CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"]
    + [f"COM{number}" for number in range(10)]
    + [f"LPT{number}" for number in range(10)]
)

# ==== Windows API =============================================================

FO_DELETE = 0x0003                      # SHFileOperationW: delete operation
FOF_SILENT = 0x0004                     # no progress dialog
FOF_NOCONFIRMATION = 0x0010             # no "are you sure" questions
FOF_ALLOWUNDO = 0x0040                  # use the recycle bin
FOF_NOERRORUI = 0x0400                  # no error dialogs
FOF_WANTNUKEWARNING = 0x4000            # ask before a file is deleted permanently instead of recycled
RECYCLE_BIN_FLAGS = (FOF_ALLOWUNDO | FOF_NOCONFIRMATION | FOF_SILENT
                     | FOF_NOERRORUI | FOF_WANTNUKEWARNING)
SHELL_MAX_PATH_LENGTH = 259             # MAX_PATH without the terminating null character
VOLUME_PATH_BUFFER_LENGTH = 32768
DRIVE_FIXED = 3                         # GetDriveTypeW: internal or external hard disk
HWND_TOPMOST = -1                       # SetWindowPos: show a window above all others
HWND_NOTOPMOST = -2
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_SHOWWINDOW = 0x0040

DRIVE_TYPE_NAMES = {
    0: "unknown drive",
    1: "invalid drive",
    2: "removable drive",
    3: "hard disk",
    4: "network drive",
    5: "optical drive",
    6: "RAM disk",
}

# Return codes of SHFileOperationW
SHELL_ERROR_MESSAGES = {
    0x02: "file not found",
    0x05: "access denied",
    0x20: "file is used by another program",
    0x75: "cancelled in the Windows dialog",
    0x78: "access denied",
    0x79: "path too deep",
    0x7C: "invalid path",
    0x81: "file name too long",
    0x85: "file too large for the recycle bin",
    0x402: "unknown error of the Windows shell",
    0x4C7: "cancelled in the Windows dialog",
}
SHELL_CANCEL_CODES = frozenset({0x75, 0x4C7})

# ==== Selection window ========================================================

WINDOW_TITLE = "File Type Cleaner"
TABLE_COLUMN_TITLES = ("File type", "Files")
COLUMN_TYPE, COLUMN_FILES = range(2)
FILES_COLUMN_WIDTH = 130
FILTER_ENTRY_WIDTH = 260
WINDOW_WIDTH = 900                      # in pixels, at most the width of the screen
WINDOW_SCREEN_HEIGHT_SHARE = 0.85       # part of the screen height the window covers when it opens
INTERRUPT_CHECK_MILLISECONDS = 250      # lets Ctrl+C in the console reach the window

DELETE_HINT_TEXT = ("Ticked file types are deleted: every file of these types in the target folder "
                    "and all its subfolders.")
LIST_HELP_TEXT = "Click a checkbox or press Space to switch the selected rows. Click a column title to sort."
CONFIRMATION_HINT_TEXT = "Nothing is deleted yet, the console shows the deletion plan and asks before deleting."
EVERYTHING_TICKED_TEXT = "All file types are ticked, every file found by the scan will be deleted."

# ==== Window theme ============================================================

# Spacing in pixels
WINDOW_MARGIN = 12
CARD_PADDING = 12
CARD_SPACING = 8
ROW_PADDING = 6                         # space above and below the content of a list row

# Neutral dark greys, one blue accent, red for ticked file types, amber for warnings
WINDOW_COLOR = "#1e1f22"                # background behind the panels
SURFACE_COLOR = "#2b2d30"               # panels
BASE_COLOR = "#1e1f22"                  # lists and input fields inside the panels
BORDER_COLOR = "#393b40"
BUTTON_COLOR = "#36383c"
BUTTON_HOVER_COLOR = "#424549"
BUTTON_BORDER_COLOR = "#4e5157"
TEXT_COLOR = "#dfe1e5"
SECONDARY_TEXT_COLOR = "#8c9096"
DISABLED_TEXT_COLOR = "#5f6268"
ACCENT_COLOR = "#3574f0"
ACCENT_HOVER_COLOR = "#4a84f5"
SELECTION_COLOR = "#2e436e"
DELETE_ROW_COLOR = "#3a2427"            # ticked file type
DELETE_TEXT_COLOR = "#f08b84"
WARNING_TEXT_COLOR = "#e0b45a"
SCROLLBAR_COLOR = "#4e5157"

# $NAME stands for the color constant of the same name. Column titles keep room for the sort arrow on the right.
STYLE_SHEET_TEMPLATE = """
QWidget { color: $TEXT_COLOR; }
QMainWindow, QWidget#root { background: $WINDOW_COLOR; }
QFrame#card { background: $SURFACE_COLOR; border: 1px solid $BORDER_COLOR; border-radius: 8px; }
QLabel { background: transparent; border: none; }
QLabel#sectionTitle { color: $SECONDARY_TEXT_COLOR; font-weight: 600; letter-spacing: 1px; }
QLabel#secondary { color: $SECONDARY_TEXT_COLOR; }
QLabel#warning { color: $WARNING_TEXT_COLOR; font-weight: 600; }
QLabel#badge { background: $BUTTON_COLOR; border: 1px solid $BUTTON_BORDER_COLOR; border-radius: 4px;
               padding: 1px 7px; font-weight: 600; }
QPushButton { background: $BUTTON_COLOR; border: 1px solid $BUTTON_BORDER_COLOR; border-radius: 5px;
              padding: 5px 12px; }
QPushButton:hover { background: $BUTTON_HOVER_COLOR; }
QPushButton:pressed { background: $BORDER_COLOR; }
QPushButton:disabled { color: $DISABLED_TEXT_COLOR; border-color: $BORDER_COLOR; }
QPushButton#primary { background: $ACCENT_COLOR; border-color: $ACCENT_COLOR; color: #ffffff; font-weight: 600; }
QPushButton#primary:hover { background: $ACCENT_HOVER_COLOR; border-color: $ACCENT_HOVER_COLOR; }
QLineEdit { background: $BASE_COLOR; border: 1px solid $BUTTON_BORDER_COLOR; border-radius: 5px;
            padding: 4px 8px; selection-background-color: $SELECTION_COLOR; }
QLineEdit:focus { border-color: $ACCENT_COLOR; }
QTreeView { background: $BASE_COLOR; border: 1px solid $BORDER_COLOR; outline: none;
            selection-background-color: $SELECTION_COLOR; selection-color: $TEXT_COLOR; }
QHeaderView { background: $SURFACE_COLOR; border: none; }
QHeaderView::section { background: $SURFACE_COLOR; color: $SECONDARY_TEXT_COLOR; border: none;
                       border-bottom: 1px solid $BORDER_COLOR; padding: 5px 24px 5px 8px; font-weight: 600; }
QScrollBar:vertical { background: transparent; width: 11px; margin: 0px; }
QScrollBar:horizontal { background: transparent; height: 11px; margin: 0px; }
QScrollBar::handle:vertical { background: $SCROLLBAR_COLOR; border-radius: 4px; min-height: 32px; margin: 2px; }
QScrollBar::handle:horizontal { background: $SCROLLBAR_COLOR; border-radius: 4px; min-width: 32px; margin: 2px; }
QScrollBar::handle:hover { background: $SECONDARY_TEXT_COLOR; }
QScrollBar::add-line, QScrollBar::sub-line { width: 0px; height: 0px; }
QScrollBar::add-page, QScrollBar::sub-page { background: none; }
QToolTip { background: $SURFACE_COLOR; color: $TEXT_COLOR; border: 1px solid $BORDER_COLOR; padding: 4px; }
QMenu { background: $SURFACE_COLOR; border: 1px solid $BORDER_COLOR; padding: 4px; }
QMenu::item { padding: 5px 18px; border-radius: 4px; }
QMenu::item:selected { background: $SELECTION_COLOR; }
QMenu::separator { height: 1px; background: $BORDER_COLOR; margin: 4px 6px; }
"""

# ==== Choices =================================================================


class RunMode(Enum):
    """Modes of the main menu."""

    SCAN = "scan"
    DELETE = "delete"
    SCAN_AND_DELETE = "scan and delete"


class DeletionMethod(Enum):
    """How matching files are removed."""

    RECYCLE_BIN = "move to the recycle bin"
    PERMANENT = "delete permanently"
    SIMULATION = "simulation, nothing is deleted"


class EmptyFolderPolicy(Enum):
    """What happens with empty folders after deleting."""

    KEEP = "keep all folders"
    REMOVE_EMPTIED = "remove folders that became empty through this deletion"
    REMOVE_ALL = "remove all empty folders"


# ==============================================================================
#   CLASSES
# ==============================================================================

# ==== Data structures =========================================================


class FileRecord(NamedTuple):
    """A file found by the folder walk."""

    path: str               # extended length path, used for all file operations
    extension: str          # file type: lower case extension with dot, see get_file_type for files without one
    size_bytes: int


class FolderContent(NamedTuple):
    """Everything the folder walk found in one folder."""

    path: str                       # extended length path
    parent_path: Optional[str]      # None for the target folder itself
    files: List[FileRecord]         # files that may be processed
    entry_count: Optional[int]      # all entries including skipped ones, None if unreadable


@dataclass
class SelectionPart:
    """One entry of a typed selection, for example "10-30 (22 24)"."""

    token: str                                      # number, range or file type
    exclusion_tokens: Optional[List[str]] = None    # tokens in brackets behind it, None without brackets


@dataclass
class TypeStatistics:
    """Number of files and total size of one file type."""

    file_count: int = 0
    total_bytes: int = 0

    def add(self, size_bytes: int) -> None:
        """Count one more file of this type."""
        self.file_count += 1
        self.total_bytes += size_bytes


@dataclass
class PathCollection:
    """Counts paths of one kind and keeps the first ones as examples."""

    count: int = 0
    total_bytes: int = 0
    examples: List[Tuple[str, str]] = field(default_factory=list)

    def add(self, path: str, note: str = "", size_bytes: int = 0) -> None:
        """Count a path and keep it as example while the limit allows."""
        self.count += 1
        self.total_bytes += size_bytes
        if len(self.examples) < STORED_EXAMPLE_LIMIT:
            self.examples.append((path, note))


@dataclass
class WalkStatistics:
    """Folders read by the walk and everything it skipped."""

    folders_read: int = 0
    skipped_system_files: PathCollection = field(default_factory=PathCollection)
    skipped_system_folders: PathCollection = field(default_factory=PathCollection)
    skipped_links: PathCollection = field(default_factory=PathCollection)
    unreadable_items: PathCollection = field(default_factory=PathCollection)
    skipped_own_script: PathCollection = field(default_factory=PathCollection)


@dataclass
class ScanResult:
    """Outcome of a scan."""

    root_folder: str
    include_system_files: bool
    statistics_by_type: Dict[str, TypeStatistics]
    walk_statistics: WalkStatistics
    duration_seconds: float
    was_cancelled: bool

    @property
    def total_files(self) -> int:
        return sum(statistics.file_count for statistics in self.statistics_by_type.values())

    def sorted_types(self) -> List[Tuple[str, TypeStatistics]]:
        """File types sorted by number of files, largest first."""
        return sorted(self.statistics_by_type.items(),
                      key=lambda item: (-item[1].file_count, item[0]))


@dataclass
class DeletionPlan:
    """All decisions for one deletion run."""

    root_folder: str
    include_system_files: bool
    extensions: Set[str]
    method: DeletionMethod
    empty_folder_policy: EmptyFolderPolicy
    expected_file_total: Optional[int] = None      # known when a scan ran before


@dataclass
class DeletionResult:
    """Outcome of a deletion run."""

    plan: DeletionPlan
    deleted_by_type: Dict[str, TypeStatistics] = field(default_factory=dict)
    failed_by_type: Dict[str, TypeStatistics] = field(default_factory=dict)
    failed_files: PathCollection = field(default_factory=PathCollection)
    removed_folders: PathCollection = field(default_factory=PathCollection)
    failed_folders: PathCollection = field(default_factory=PathCollection)
    walk_statistics: WalkStatistics = field(default_factory=WalkStatistics)
    files_checked: int = 0
    duration_seconds: float = 0.0
    was_cancelled: bool = False

    @property
    def deleted_count(self) -> int:
        return sum(statistics.file_count for statistics in self.deleted_by_type.values())

    @property
    def deleted_bytes(self) -> int:
        return sum(statistics.total_bytes for statistics in self.deleted_by_type.values())

    @property
    def failed_count(self) -> int:
        return sum(statistics.file_count for statistics in self.failed_by_type.values())


@dataclass
class FolderState:
    """Bookkeeping of one folder for the removal of empty folders."""

    parent_path: Optional[str]
    entry_count: Optional[int]          # None if the folder could not be read
    removed_entry_count: int = 0        # deleted files plus removed subfolders


# ==== Windows integration =====================================================


class ShellFileOperation(ctypes.Structure):
    """SHFILEOPSTRUCTW of the Windows shell API, byte packed on 32 bit Python."""

    _pack_ = 1 if ctypes.sizeof(ctypes.c_void_p) == 4 else 8
    _fields_ = [
        ("hwnd", wintypes.HWND),
        ("wFunc", wintypes.UINT),
        ("pFrom", wintypes.LPCWSTR),
        ("pTo", wintypes.LPCWSTR),
        ("fFlags", wintypes.WORD),
        ("fAnyOperationsAborted", wintypes.BOOL),
        ("hNameMappings", wintypes.LPVOID),
        ("lpszProgressTitle", wintypes.LPCWSTR),
    ]


class TargetVolume:
    """Drive that holds the target folder and whether it has a recycle bin."""

    def __init__(self, folder: str) -> None:
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        get_volume_path_name = kernel32.GetVolumePathNameW
        get_volume_path_name.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
        get_volume_path_name.restype = wintypes.BOOL
        get_drive_type = kernel32.GetDriveTypeW
        get_drive_type.argtypes = [wintypes.LPCWSTR]
        get_drive_type.restype = wintypes.UINT

        volume_path_buffer = ctypes.create_unicode_buffer(VOLUME_PATH_BUFFER_LENGTH)
        if get_volume_path_name(folder, volume_path_buffer, VOLUME_PATH_BUFFER_LENGTH):
            self.root_path = volume_path_buffer.value
        else:
            self.root_path = os.path.splitdrive(folder)[0] + "\\"
        self.drive_type = int(get_drive_type(self.root_path))

    @property
    def supports_recycle_bin(self) -> bool:
        """Windows offers a recycle bin only on hard disks."""
        return self.drive_type == DRIVE_FIXED

    @property
    def description(self) -> str:
        """Drive root and drive type for messages."""
        return f"{self.root_path} ({DRIVE_TYPE_NAMES.get(self.drive_type, 'unknown drive')})"


class RecycleBin:
    """Moves files and empty folders to the Windows recycle bin through the Windows shell."""

    def __init__(self) -> None:
        shell32 = ctypes.WinDLL("shell32")
        self._shell_file_operation = shell32.SHFileOperationW
        self._shell_file_operation.argtypes = [ctypes.POINTER(ShellFileOperation)]
        self._shell_file_operation.restype = ctypes.c_int

    def move_files(self, file_paths: List[str]) -> Dict[str, Optional[str]]:
        """Recycle files and return an error message per path, None means success."""
        outcomes: Dict[str, Optional[str]] = {}
        shell_paths: Dict[str, str] = {}
        for file_path in file_paths:
            display_path = to_display_path(file_path)
            if is_path_usable_by_shell(display_path):
                shell_paths[file_path] = display_path
            else:
                outcomes[file_path] = ("the recycle bin cannot handle this path (too long or special name), "
                                       "use permanent deletion")
        if shell_paths:
            outcomes.update(self._recycle_and_verify(shell_paths))
        return outcomes

    def _recycle_and_verify(self, shell_paths: Dict[str, str]) -> Dict[str, Optional[str]]:
        """Recycle a group of files and check which of them are really gone."""
        return_code, operations_aborted = self._run_shell_operation(list(shell_paths.values()))
        outcomes: Dict[str, Optional[str]] = {}
        remaining_paths: Dict[str, str] = {}
        for file_path, display_path in shell_paths.items():
            if os.path.lexists(file_path):
                remaining_paths[file_path] = display_path
            else:
                outcomes[file_path] = None
        if not remaining_paths:
            return outcomes

        was_cancelled = return_code in SHELL_CANCEL_CODES or (operations_aborted and return_code == 0)
        if len(shell_paths) == 1 or was_cancelled:
            error_message = describe_shell_result(return_code, was_cancelled)
            outcomes.update((file_path, error_message) for file_path in remaining_paths)
            return outcomes

        # The shell stops a group at the first problem, so the rest is retried one by one
        for file_path, display_path in remaining_paths.items():
            outcomes.update(self._recycle_and_verify({file_path: display_path}))
        return outcomes

    def _run_shell_operation(self, display_paths: List[str]) -> Tuple[int, bool]:
        """Call SHFileOperationW once for all paths and return its result."""
        # The shell expects all paths in one buffer, separated and ended by null characters
        path_list = "\0".join(display_paths) + "\0\0"
        path_buffer = ctypes.create_string_buffer(path_list.encode("utf-16-le", "surrogatepass"))
        operation = ShellFileOperation()
        operation.hwnd = None
        operation.wFunc = FO_DELETE
        operation.pFrom = wintypes.LPCWSTR(ctypes.addressof(path_buffer))
        operation.pTo = None
        operation.fFlags = RECYCLE_BIN_FLAGS
        return_code = self._shell_file_operation(ctypes.byref(operation))
        return return_code & 0xFFFFFFFF, bool(operation.fAnyOperationsAborted)


class InterruptGuard:
    """Turns Ctrl+C into a flag, so running work can stop at a safe point."""

    def __init__(self) -> None:
        self.was_requested = False
        self._previous_handler = None

    def __enter__(self) -> InterruptGuard:
        self.was_requested = False
        self._previous_handler = signal.signal(signal.SIGINT, self._request_stop)
        return self

    def __exit__(self, *exception_info) -> None:
        signal.signal(signal.SIGINT, self._previous_handler or signal.default_int_handler)

    def _request_stop(self, signal_number, stack_frame) -> None:
        """Signal handler for Ctrl+C, only sets the flag."""
        if not self.was_requested:
            print("\n  Ctrl+C received, stopping at the next safe point ...", flush=True)
        self.was_requested = True


# ==== Folder walk =============================================================


class FolderWalker:
    """Walks through all subfolders of the target folder without ever leaving it.

    Links, junctions and other reparse points are neither followed nor
    returned, so the walk cannot be redirected to a place outside the target.
    """

    def __init__(self, root_folder: str, include_system_items: bool, volume_root: str) -> None:
        self.root_folder = to_extended_path(root_folder)
        self.include_system_items = include_system_items
        self.statistics = WalkStatistics()
        extended_volume_root = to_extended_path(volume_root)
        self._active_volume_folders = frozenset(
            os.path.normcase(os.path.join(extended_volume_root, folder_name))
            for folder_name in ACTIVE_VOLUME_FOLDER_NAMES
        )

    def iterate_folders(self) -> Iterator[FolderContent]:
        """Yield the content of every folder, the target folder first."""
        pending_folders: List[Tuple[str, Optional[str]]] = [(self.root_folder, None)]
        while pending_folders:
            folder_path, parent_path = pending_folders.pop()
            try:
                # The complete listing is read first, so deleting files afterwards is safe
                with os.scandir(folder_path) as folder_iterator:
                    entries = list(folder_iterator)
            except OSError as error:
                self.statistics.unreadable_items.add(to_display_path(folder_path), describe_os_error(error))
                yield FolderContent(folder_path, parent_path, [], None)
                continue

            self.statistics.folders_read += 1
            files: List[FileRecord] = []
            subfolders: List[str] = []
            for entry in entries:
                self._classify_entry(entry, files, subfolders)
            # Reversed, so the first subfolder is processed next
            pending_folders.extend((subfolder, folder_path) for subfolder in reversed(subfolders))
            yield FolderContent(folder_path, parent_path, files, len(entries))

    def _classify_entry(self, entry: os.DirEntry, files: List[FileRecord], subfolders: List[str]) -> None:
        """Add an entry to files or subfolders, or record why it is skipped."""
        try:
            # Without following links the data comes from the folder listing itself
            entry_stat = entry.stat(follow_symlinks=False)
        except OSError as error:
            self.statistics.unreadable_items.add(to_display_path(entry.path), describe_os_error(error))
            return
        attributes = entry_stat.st_file_attributes

        if attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            self.statistics.skipped_links.add(to_display_path(entry.path))
            return

        if attributes & stat.FILE_ATTRIBUTE_DIRECTORY:
            if os.path.normcase(entry.path) in self._active_volume_folders:
                self.statistics.skipped_system_folders.add(to_display_path(entry.path), "in use by Windows")
            elif not self.include_system_items and is_operating_system_item(entry.name, attributes,
                                                                            is_folder=True):
                self.statistics.skipped_system_folders.add(to_display_path(entry.path))
            else:
                subfolders.append(entry.path)
            return

        # This script is never counted or deleted, also when it lies in the target folder
        if leads_to_own_script(entry.path):
            self.statistics.skipped_own_script.add(to_display_path(entry.path))
            return
        if not self.include_system_items and is_operating_system_item(entry.name, attributes, is_folder=False):
            self.statistics.skipped_system_files.add(to_display_path(entry.path), size_bytes=entry_stat.st_size)
            return
        files.append(FileRecord(entry.path, get_file_type(entry.name), entry_stat.st_size))


# ==== Progress output =========================================================


class ProgressReporter:
    """Shows a live counter line and a status line with the current folder every minute."""

    def __init__(self, activity: str, progress_text: Callable[[], str]) -> None:
        self.activity = activity
        self.current_folder = ""
        self._progress_text = progress_text
        self._show_live_counter = sys.stdout.isatty()
        self._line_width = max(40, shutil.get_terminal_size().columns - 1)
        self._live_line_visible = False
        self._start_time = time.monotonic()
        self._next_status_time = self._start_time + STATUS_INTERVAL_SECONDS
        self._next_live_time = self._start_time

    def __enter__(self) -> ProgressReporter:
        self._start_time = time.monotonic()
        self._next_status_time = self._start_time + STATUS_INTERVAL_SECONDS
        self._next_live_time = self._start_time
        return self

    def __exit__(self, *exception_info) -> None:
        self.clear_live_line()

    def tick(self) -> None:
        """Called often by the running work, prints only when an interval is due."""
        now = time.monotonic()
        if now >= self._next_status_time:
            self._next_status_time = now + STATUS_INTERVAL_SECONDS
            self._print_status(now)
        if self._show_live_counter and now >= self._next_live_time:
            self._next_live_time = now + LIVE_COUNTER_INTERVAL_SECONDS
            self._draw_live_line(now)

    def clear_live_line(self) -> None:
        """Remove the live counter line, so the next output starts on a clean line."""
        if self._live_line_visible:
            sys.stdout.write("\r" + " " * self._line_width + "\r")
            sys.stdout.flush()
            self._live_line_visible = False

    def _draw_live_line(self, now: float) -> None:
        """Overwrite the live counter line in place."""
        elapsed = format_duration(now - self._start_time)
        live_text = f"  {self.activity} {elapsed} | {self._progress_text()}"
        sys.stdout.write("\r" + shorten_text(live_text, self._line_width).ljust(self._line_width))
        sys.stdout.flush()
        self._live_line_visible = True

    def _print_status(self, now: float) -> None:
        """Print the status line with the elapsed time and the current folder."""
        self.clear_live_line()
        elapsed = format_duration(now - self._start_time)
        print(f"[{clock_time()}] Still running for {elapsed} | {self._progress_text()}")
        print(f"           Current folder: {self.current_folder}", flush=True)


# ==== Scan ====================================================================


class FileTypeScanner:
    """Counts files and total size per file type in the target folder."""

    def __init__(self, root_folder: str, include_system_files: bool, volume_root: str) -> None:
        self.root_folder = root_folder
        self.include_system_files = include_system_files
        self._walker = FolderWalker(root_folder, include_system_files, volume_root)
        self._statistics_by_type: Dict[str, TypeStatistics] = {}
        self._file_count = 0
        self._total_bytes = 0

    def run(self) -> ScanResult:
        """Walk through all folders and count every file by its type. Ctrl+C stops early."""
        start_time = time.monotonic()
        was_cancelled = False
        interrupt_guard = InterruptGuard()
        reporter = ProgressReporter("Scanning", self._progress_text)
        with interrupt_guard, reporter:
            for folder_content in self._walker.iterate_folders():
                if interrupt_guard.was_requested:
                    was_cancelled = True
                    break
                reporter.current_folder = to_display_path(folder_content.path)
                for file_record in folder_content.files:
                    add_to_type_statistics(self._statistics_by_type, file_record.extension, file_record.size_bytes)
                    self._file_count += 1
                    self._total_bytes += file_record.size_bytes
                reporter.tick()
        return ScanResult(
            root_folder=self.root_folder,
            include_system_files=self.include_system_files,
            statistics_by_type=self._statistics_by_type,
            walk_statistics=self._walker.statistics,
            duration_seconds=time.monotonic() - start_time,
            was_cancelled=was_cancelled,
        )

    def _progress_text(self) -> str:
        """Counters shown in the live line and the status line."""
        return (f"{format_count(self._file_count)} files | "
                f"{format_count(self._walker.statistics.folders_read)} folders | "
                f"{format_size(self._total_bytes)}")


# ==== Selection window ========================================================

# The window is built on PySide6. Without it these classes are not defined and the
# file types are chosen in the console.
if not PYSIDE_IMPORT_ERROR:

    class FileTypeTableModel(QtCore.QAbstractTableModel):
        """File types of the scan with a checkbox each, read directly from the scan result.

        The view asks only for the rows on the screen, so lists with thousands of
        file types open at once, and ticking all of them is a single change.
        """

        ticks_changed = QtCore.Signal()

        def __init__(self, sorted_types: List[Tuple[str, TypeStatistics]], parent: QtCore.QObject) -> None:
            super().__init__(parent)
            self.ticked_extensions: Set[str] = set()
            self._statistics_by_extension = dict(sorted_types)
            self._search_texts = {extension: format_extension(extension).lower() for extension, _ in sorted_types}
            self._all_types = list(sorted_types)
            self._shown_types = list(sorted_types)
            self._filter_text = ""
            self._delete_background = QtGui.QBrush(QtGui.QColor(DELETE_ROW_COLOR))
            self._delete_foreground = QtGui.QBrush(QtGui.QColor(DELETE_TEXT_COLOR))
            self._secondary_foreground = QtGui.QBrush(QtGui.QColor(SECONDARY_TEXT_COLOR))
            self._count_alignment = QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter
            line_height = QtGui.QFontMetrics(QtWidgets.QApplication.font()).height()
            self._row_size_hint = QtCore.QSize(-1, line_height + ROW_PADDING)
            # The view asks every row for its flags whenever it lays out the list, so the answers are ready
            row_flags = (QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable
                         | QtCore.Qt.ItemFlag.ItemNeverHasChildren)
            self._column_flags = {COLUMN_TYPE: row_flags | QtCore.Qt.ItemFlag.ItemIsUserCheckable,
                                  COLUMN_FILES: row_flags}
            self._tick_roles = [QtCore.Qt.ItemDataRole.CheckStateRole, QtCore.Qt.ItemDataRole.ForegroundRole,
                                QtCore.Qt.ItemDataRole.BackgroundRole]

        # ==== Structure =======================================================

        def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
            # A tree view asks every row for children, a file type has none
            return 0 if parent.isValid() else len(self._shown_types)

        def columnCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
            return 0 if parent.isValid() else len(TABLE_COLUMN_TITLES)

        def headerData(self, section: int, orientation: QtCore.Qt.Orientation,
                       role: int = QtCore.Qt.ItemDataRole.DisplayRole):
            if orientation != QtCore.Qt.Orientation.Horizontal:
                return None
            if role == QtCore.Qt.ItemDataRole.DisplayRole:
                return TABLE_COLUMN_TITLES[section]
            if role == QtCore.Qt.ItemDataRole.TextAlignmentRole and section == COLUMN_FILES:
                return self._count_alignment
            return None

        def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlag:
            if not index.isValid():
                return QtCore.Qt.ItemFlag.NoItemFlags
            return self._column_flags[index.column()]

        def extension_at(self, row: int) -> str:
            """File type of a shown row."""
            return self._shown_types[row][0]

        def shown_extensions(self) -> List[str]:
            """File types the filter shows, in their current order."""
            return [extension for extension, _ in self._shown_types]

        @property
        def shown_count(self) -> int:
            return len(self._shown_types)

        @property
        def total_count(self) -> int:
            return len(self._all_types)

        # ==== Content =========================================================

        def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.ItemDataRole.DisplayRole):
            """Content of a row, ticked file types are red."""
            if not index.isValid():
                return None
            # The height is asked for often, a ready answer keeps long lists fast
            if role == QtCore.Qt.ItemDataRole.SizeHintRole:
                return self._row_size_hint
            extension, statistics = self._shown_types[index.row()]
            is_ticked = extension in self.ticked_extensions
            column = index.column()
            if role == QtCore.Qt.ItemDataRole.DisplayRole:
                if column == COLUMN_TYPE:
                    return to_window_text(format_extension(extension))
                return format_count(statistics.file_count)
            if role == QtCore.Qt.ItemDataRole.CheckStateRole and column == COLUMN_TYPE:
                return QtCore.Qt.CheckState.Checked if is_ticked else QtCore.Qt.CheckState.Unchecked
            if role == QtCore.Qt.ItemDataRole.TextAlignmentRole and column == COLUMN_FILES:
                return self._count_alignment
            if role == QtCore.Qt.ItemDataRole.ForegroundRole:
                if is_ticked:
                    return self._delete_foreground
                return None if column == COLUMN_TYPE else self._secondary_foreground
            if role == QtCore.Qt.ItemDataRole.BackgroundRole and is_ticked:
                return self._delete_background
            if role == QtCore.Qt.ItemDataRole.ToolTipRole:
                return (f"{to_window_text(format_extension(extension))}: "
                        f"{format_quantity(statistics.file_count, 'file')}, {format_size(statistics.total_bytes)}")
            return None

        def setData(self, index: QtCore.QModelIndex, value, role: int = QtCore.Qt.ItemDataRole.EditRole) -> bool:
            """The checkbox of a row ticks or unticks its file type."""
            if not index.isValid() or index.column() != COLUMN_TYPE or role != QtCore.Qt.ItemDataRole.CheckStateRole:
                return False
            is_ticked = QtCore.Qt.CheckState(value) == QtCore.Qt.CheckState.Checked
            self.set_ticks([self.extension_at(index.row())], is_ticked)
            return True

        # ==== Ticks ===========================================================

        def set_ticks(self, extensions: Iterable[str], is_ticked: bool) -> None:
            """Tick or untick file types. The view redraws only the rows on the screen."""
            if is_ticked:
                self.ticked_extensions.update(extensions)
            else:
                self.ticked_extensions.difference_update(extensions)
            if self._shown_types:
                # Naming the changed roles tells the view that no row changes its height
                self.dataChanged.emit(self.index(0, 0),
                                      self.index(len(self._shown_types) - 1, len(TABLE_COLUMN_TITLES) - 1),
                                      self._tick_roles)
            self.ticks_changed.emit()

        def ticked_totals(self) -> Tuple[int, int, int]:
            """Ticked file types, their files and bytes, also those the filter hides."""
            ticked_statistics = [self._statistics_by_extension[extension] for extension in self.ticked_extensions]
            return (len(ticked_statistics), sum(statistics.file_count for statistics in ticked_statistics),
                    sum(statistics.total_bytes for statistics in ticked_statistics))

        # ==== Order and filter ================================================

        def sort(self, column: int, order: QtCore.Qt.SortOrder = QtCore.Qt.SortOrder.AscendingOrder) -> None:
            """Sort by file type or by number of files, called when a column title is clicked."""
            is_descending = order == QtCore.Qt.SortOrder.DescendingOrder
            # Sorted by file type first, so file types with the same number of files stay in alphabetical order
            ordered_types = sorted(self._all_types, key=lambda item: item[0])
            if column == COLUMN_FILES:
                ordered_types.sort(key=lambda item: item[1].file_count, reverse=is_descending)
            elif is_descending:
                ordered_types.reverse()
            self.beginResetModel()
            self._all_types = ordered_types
            self._shown_types = self._filtered(ordered_types)
            self.endResetModel()

        def set_filter(self, text: str) -> None:
            """Show only file types containing the text, upper and lower case do not matter. Empty shows all."""
            self.beginResetModel()
            self._filter_text = text.strip().lstrip("*").lower()
            self._shown_types = self._filtered(self._all_types)
            self.endResetModel()

        def _filtered(self, types: List[Tuple[str, TypeStatistics]]) -> List[Tuple[str, TypeStatistics]]:
            """File types whose display text contains the filter text."""
            if not self._filter_text:
                return list(types)
            return [item for item in types if self._filter_text in self._search_texts[item[0]]]

    class FileTypeTreeView(QtWidgets.QTreeView):
        """List of the file types. Space switches the selected rows between keep and delete."""

        toggle_requested = QtCore.Signal()

        def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
            """Space asks to switch the selected rows, all other keys work as usual."""
            if event.key() == QtCore.Qt.Key.Key_Space:
                self.toggle_requested.emit()
            else:
                super().keyPressEvent(event)

    class FileTypeSelectionWindow(QtWidgets.QMainWindow):
        """Window to tick the file types to delete, made for long lists."""

        @classmethod
        def show_and_wait(cls, scan_result: ScanResult) -> Optional[Set[str]]:
            """Open the window and wait until it is closed. Return the ticked file types, None if cancelled."""
            application = QtWidgets.QApplication.instance()
            if application is None:
                application = QtWidgets.QApplication([sys.argv[0]])
                apply_dark_theme(application)
            window = cls(scan_result)
            return window._run(application)

        def __init__(self, scan_result: ScanResult) -> None:
            super().__init__()
            self._scan_result = scan_result
            self._was_confirmed = False
            self._model = FileTypeTableModel(scan_result.sorted_types(), self)
            self._model.ticks_changed.connect(self._update_summary)

            self.setWindowTitle(f"{WINDOW_TITLE}: tick the file types to delete")
            self._build_layout()
            self._fill_list()
            self._update_type_count()
            self._update_summary()
            resize_and_center(self, WINDOW_WIDTH, WINDOW_SCREEN_HEIGHT_SHARE)

        # ==== Window lifecycle ================================================

        def _run(self, application: QtWidgets.QApplication) -> Optional[Set[str]]:
            """Show the window and wait until it closes. Ctrl+C in the console closes it as well."""
            previous_handler = signal.signal(signal.SIGINT, self._handle_interrupt)
            # Qt runs in C++, this timer lets Python notice Ctrl+C in the console
            interrupt_timer = QtCore.QTimer(self)
            interrupt_timer.timeout.connect(lambda: None)
            interrupt_timer.start(INTERRUPT_CHECK_MILLISECONDS)
            try:
                self.show()
                bring_window_to_front(self)
                self._tree.setFocus()
                application.exec()
            finally:
                interrupt_timer.stop()
                signal.signal(signal.SIGINT, previous_handler)
            return set(self._model.ticked_extensions) if self._was_confirmed else None

        def _cancel(self) -> None:
            """Close the window without handing over the ticks."""
            self._was_confirmed = False
            self.close()

        def _continue(self) -> None:
            """Hand the ticks to the console. Asks first if every file type is ticked."""
            ticked_type_count, _, _ = self._model.ticked_totals()
            if not ticked_type_count:
                QtWidgets.QMessageBox.information(self, WINDOW_TITLE, "No file type is ticked for deletion.")
                return
            if ticked_type_count == self._model.total_count and not self._ask_yes_no(
                    "All file types are ticked, so every file found by the scan will be deleted.\n\n"
                    "Continue anyway?"):
                return
            self._was_confirmed = True
            self.close()

        def _handle_interrupt(self, signal_number: int, stack_frame) -> None:
            """Ctrl+C in the console closes the window like Cancel."""
            print("\n  Ctrl+C received, closing the selection window ...", flush=True)
            self._cancel()

        # ==== Layout ==========================================================

        def _build_layout(self) -> None:
            """Target folder on top, then the list of file types, the footer below."""
            root_widget = QtWidgets.QWidget()
            root_widget.setObjectName("root")
            layout = QtWidgets.QVBoxLayout(root_widget)
            layout.setContentsMargins(WINDOW_MARGIN, WINDOW_MARGIN, WINDOW_MARGIN, WINDOW_MARGIN)
            layout.setSpacing(WINDOW_MARGIN)
            layout.addLayout(self._build_folder_bar())
            layout.addWidget(self._build_list_card(), 1)
            layout.addWidget(self._build_footer())
            self.setCentralWidget(root_widget)

        def _build_folder_bar(self) -> QtWidgets.QHBoxLayout:
            """The target folder in one line, a long path is cut off instead of widening the window."""
            layout = QtWidgets.QHBoxLayout()
            layout.setSpacing(CARD_SPACING)
            badge = QtWidgets.QLabel("Target folder")
            badge.setObjectName("badge")
            layout.addWidget(badge)
            folder_text = to_window_text(self._scan_result.root_folder)
            folder_label = create_secondary_label(folder_text, word_wrap=False)
            folder_label.setToolTip(folder_text)
            folder_label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
            folder_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Preferred)
            layout.addWidget(folder_label, 1)
            return layout

        def _build_list_card(self) -> QtWidgets.QWidget:
            """Panel with the deletion hint, filter, select buttons and the list."""
            card, layout = create_card("File types")
            hint_label = QtWidgets.QLabel(DELETE_HINT_TEXT)
            hint_label.setWordWrap(True)
            layout.addWidget(hint_label)

            toolbar_layout = QtWidgets.QHBoxLayout()
            toolbar_layout.setSpacing(CARD_SPACING)
            self._filter_entry = QtWidgets.QLineEdit()
            self._filter_entry.setPlaceholderText("Filter, for example tmp")
            self._filter_entry.setClearButtonEnabled(True)
            self._filter_entry.setFixedWidth(FILTER_ENTRY_WIDTH)
            self._filter_entry.textChanged.connect(self._apply_filter)
            toolbar_layout.addWidget(self._filter_entry)
            toolbar_layout.addWidget(create_button("Select all", lambda: self._tick_shown_types(True),
                                                   tooltip="Tick every file type shown, they will be deleted"))
            toolbar_layout.addWidget(create_button("Deselect all", lambda: self._tick_shown_types(False),
                                                   tooltip="Untick every file type shown, they will be kept"))
            toolbar_layout.addStretch(1)
            self._type_count_label = create_secondary_label("", word_wrap=False)
            toolbar_layout.addWidget(self._type_count_label)
            layout.addLayout(toolbar_layout)

            # The file types are filled in by _fill_list once the window is built
            self._tree = FileTypeTreeView()
            self._tree.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
            self._tree.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
            self._tree.setUniformRowHeights(True)           # Qt measures one row instead of all of them
            self._tree.setRootIsDecorated(False)
            self._tree.setItemsExpandable(False)
            self._tree.setAllColumnsShowFocus(True)
            self._tree.toggle_requested.connect(self._toggle_selected_rows)
            layout.addWidget(self._tree, 1)
            layout.addWidget(create_secondary_label(LIST_HELP_TEXT))
            return card

        def _build_footer(self) -> QtWidgets.QWidget:
            """Ticked file types and a hint on the left, Cancel and Continue on the right."""
            card = QtWidgets.QFrame()
            card.setObjectName("card")
            layout = QtWidgets.QHBoxLayout(card)
            layout.setContentsMargins(CARD_PADDING, CARD_SPACING, CARD_PADDING, CARD_SPACING)
            text_layout = QtWidgets.QVBoxLayout()
            text_layout.setSpacing(2)
            self._summary_label = QtWidgets.QLabel()
            summary_font = self._summary_label.font()
            summary_font.setBold(True)
            self._summary_label.setFont(summary_font)
            text_layout.addWidget(self._summary_label)
            # Hint and warning share the second line, so the footer keeps its height
            self._confirmation_label = create_secondary_label(CONFIRMATION_HINT_TEXT, word_wrap=False)
            text_layout.addWidget(self._confirmation_label)
            self._warning_label = QtWidgets.QLabel(EVERYTHING_TICKED_TEXT)
            self._warning_label.setObjectName("warning")
            text_layout.addWidget(self._warning_label)
            layout.addLayout(text_layout, 1)
            layout.addWidget(create_button("Cancel", self._cancel, tooltip="Close the window, nothing is deleted"))
            continue_button = create_button(
                "Continue with the ticked file types", self._continue, is_primary=True,
                tooltip="Back to the console, it shows the deletion plan and asks before deleting")
            continue_button.setDefault(True)
            layout.addWidget(continue_button)
            return card

        # ==== List ============================================================

        def _fill_list(self) -> None:
            """Hand the file types to the list, sorted as in the scan with the most files first.

            Every widget added to the window lays out the whole list again, which takes
            seconds with very long lists, so the list gets its content last.
            """
            self._tree.setModel(self._model)
            header = self._tree.header()
            header.setStretchLastSection(False)
            header.setSectionResizeMode(COLUMN_TYPE, QtWidgets.QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(COLUMN_FILES, QtWidgets.QHeaderView.ResizeMode.Fixed)
            header.resizeSection(COLUMN_FILES, FILES_COLUMN_WIDTH)
            header.setSortIndicator(COLUMN_FILES, QtCore.Qt.SortOrder.DescendingOrder)
            self._tree.setSortingEnabled(True)

        def _apply_filter(self, text: str) -> None:
            """Filter the list and update the number of shown file types."""
            self._model.set_filter(text)
            self._update_type_count()

        def _tick_shown_types(self, is_ticked: bool) -> None:
            """Tick or untick every file type the filter shows."""
            self._model.set_ticks(self._model.shown_extensions(), is_ticked)

        def _toggle_selected_rows(self) -> None:
            """Tick all selected file types, or untick them if all of them are ticked."""
            extensions = [self._model.extension_at(index.row())
                          for index in self._tree.selectionModel().selectedRows(COLUMN_TYPE)]
            if extensions:
                is_ticked = any(extension not in self._model.ticked_extensions for extension in extensions)
                self._model.set_ticks(extensions, is_ticked)

        def _update_type_count(self) -> None:
            """Show how many file types the filter shows."""
            shown_count, total_count = self._model.shown_count, self._model.total_count
            if shown_count == total_count:
                self._type_count_label.setText(format_quantity(total_count, "file type"))
            else:
                self._type_count_label.setText(f"{format_count(shown_count)} of "
                                               f"{format_quantity(total_count, 'file type')} shown")

        def _update_summary(self) -> None:
            """Show the ticked file types with files and size, warn if all are ticked."""
            type_count, file_count, total_bytes = self._model.ticked_totals()
            if type_count:
                self._summary_label.setText(f"{format_quantity(type_count, 'file type')} ticked for deletion: "
                                            f"{format_quantity(file_count, 'file')}, {format_size(total_bytes)}")
            else:
                self._summary_label.setText("No file type ticked, nothing will be deleted")
            is_everything_ticked = type_count == self._model.total_count
            self._warning_label.setVisible(is_everything_ticked)
            self._confirmation_label.setVisible(not is_everything_ticked)

        # ==== Messages ========================================================

        def _ask_yes_no(self, question: str) -> bool:
            """Warning dialog with Yes and No, No is the default."""
            answer = QtWidgets.QMessageBox.warning(
                self, WINDOW_TITLE, question,
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                QtWidgets.QMessageBox.StandardButton.No)
            return answer == QtWidgets.QMessageBox.StandardButton.Yes


# ==== Deletion ================================================================


class FileDeleter:
    """Deletes all files of the chosen types and optionally removes empty folders."""

    def __init__(self, plan: DeletionPlan, volume_root: str, deletion_log: Optional[DeletionLog]) -> None:
        self.plan = plan
        self.result = DeletionResult(plan=plan)
        self._walker = FolderWalker(plan.root_folder, plan.include_system_files, volume_root)
        self._deletion_log = deletion_log
        self._is_simulation = plan.method is DeletionMethod.SIMULATION
        self._recycle_bin = RecycleBin() if plan.method is DeletionMethod.RECYCLE_BIN else None
        self._batch_size = RECYCLE_BIN_BATCH_SIZE if self._recycle_bin else 1
        self._pending_files: List[Tuple[FileRecord, FolderState, str]] = []   # with the chosen type it counts for
        self._folder_states: Dict[str, FolderState] = {}
        self._visit_order: List[str] = []
        self._deleted_count = 0
        self._failed_count = 0
        self._interrupt_guard = InterruptGuard()
        activity = "Simulating" if self._is_simulation else "Deleting"
        self._reporter = ProgressReporter(activity, self._progress_text)

    def run(self) -> DeletionResult:
        """Delete the matching files, then remove empty folders as planned. Ctrl+C stops early."""
        start_time = time.monotonic()
        with self._interrupt_guard, self._reporter:
            completed = self._delete_matching_files()
            if completed and self.plan.empty_folder_policy is not EmptyFolderPolicy.KEEP:
                self._remove_empty_folders()
        self.result.walk_statistics = self._walker.statistics
        self.result.duration_seconds = time.monotonic() - start_time
        return self.result

    # ==== Files ===============================================================

    def _delete_matching_files(self) -> bool:
        """Walk through all folders and delete matching files. False if cancelled."""
        for folder_content in self._walker.iterate_folders():
            self._reporter.current_folder = to_display_path(folder_content.path)
            folder_state = FolderState(folder_content.parent_path, folder_content.entry_count)
            self._folder_states[folder_content.path] = folder_state
            self._visit_order.append(folder_content.path)
            for file_record in folder_content.files:
                if self._interrupt_guard.was_requested:
                    break
                self.result.files_checked += 1
                selected_type = self._selected_type(file_record.extension)
                if selected_type is not None:
                    self._queue_file(file_record, folder_state, selected_type)
            if self._interrupt_guard.was_requested:
                self.result.was_cancelled = True
                return False
            self._reporter.tick()
        self._process_pending_files()
        return True

    def _selected_type(self, file_type: str) -> Optional[str]:
        """Chosen file type a file counts for, None if it is not chosen.

        Without scan a single "." chooses all files without extension, whatever their name.
        """
        if file_type in self.plan.extensions:
            return file_type
        if is_no_extension_type(file_type) and ALL_NO_EXTENSION_TYPE in self.plan.extensions:
            return ALL_NO_EXTENSION_TYPE
        return None

    def _queue_file(self, file_record: FileRecord, folder_state: FolderState, selected_type: str) -> None:
        """Collect a file and delete the collected files once the batch is full."""
        self._pending_files.append((file_record, folder_state, selected_type))
        if len(self._pending_files) >= self._batch_size:
            self._process_pending_files()

    def _process_pending_files(self) -> None:
        """Delete all queued files and record the outcome of each one."""
        if not self._pending_files:
            return
        batch, self._pending_files = self._pending_files, []
        outcomes = self._delete_files([file_record.path for file_record, _, _ in batch])
        for file_record, folder_state, selected_type in batch:
            error_message = outcomes.get(file_record.path, "no result from the deletion")
            display_path = to_display_path(file_record.path)
            if error_message is None:
                add_to_type_statistics(self.result.deleted_by_type, selected_type, file_record.size_bytes)
                folder_state.removed_entry_count += 1
                self._deleted_count += 1
                self._log("WOULD DELETE" if self._is_simulation else "DELETED", display_path)
            else:
                add_to_type_statistics(self.result.failed_by_type, selected_type, file_record.size_bytes)
                self.result.failed_files.add(display_path, error_message)
                self._failed_count += 1
                self._log("FAILED", display_path, error_message)
        self._reporter.tick()

    def _delete_files(self, file_paths: List[str]) -> Dict[str, Optional[str]]:
        """Delete files with the chosen method and return an error message per path."""
        outcomes: Dict[str, Optional[str]] = {}
        deletable_paths: List[str] = []
        for file_path in file_paths:
            # The folder walk skips this script already, this check is the last line of defence
            if leads_to_own_script(file_path):
                outcomes[file_path] = "this script itself, it is never deleted"
            elif has_unsafe_characters(os.path.basename(file_path)):
                outcomes[file_path] = "file name contains characters Windows cannot handle"
            else:
                deletable_paths.append(file_path)

        if self.plan.method is DeletionMethod.SIMULATION:
            outcomes.update((file_path, None) for file_path in deletable_paths)
        elif self.plan.method is DeletionMethod.PERMANENT:
            outcomes.update((file_path, remove_path(file_path, os.remove)) for file_path in deletable_paths)
        elif deletable_paths and self._recycle_bin is not None:
            outcomes.update(self._recycle_bin.move_files(deletable_paths))
        return outcomes

    # ==== Empty folders =======================================================

    def _remove_empty_folders(self) -> None:
        """Remove empty folders bottom up with the method of the files, never the target folder itself."""
        remove_all = self.plan.empty_folder_policy is EmptyFolderPolicy.REMOVE_ALL
        # The reversed visiting order handles every subfolder before its parent
        for folder_path in reversed(self._visit_order):
            if self._interrupt_guard.was_requested:
                self.result.was_cancelled = True
                return
            folder_state = self._folder_states[folder_path]
            if folder_state.parent_path is None or folder_state.entry_count is None:
                continue
            if folder_state.entry_count > folder_state.removed_entry_count:
                continue
            if folder_state.entry_count == 0 and not remove_all:
                continue

            display_path = to_display_path(folder_path)
            self._reporter.current_folder = display_path
            error_message = self._remove_folder(folder_path)
            if error_message is None:
                self.result.removed_folders.add(display_path)
                self._folder_states[folder_state.parent_path].removed_entry_count += 1
                self._log("WOULD REMOVE" if self._is_simulation else "REMOVED", display_path + "\\")
            else:
                self.result.failed_folders.add(display_path, error_message)
                self._log("FAILED", display_path + "\\", error_message)
            self._reporter.tick()

    def _remove_folder(self, folder_path: str) -> Optional[str]:
        """Remove an empty folder with the method chosen for the files. Return an error message, None on success."""
        # The folder of this script is never empty, this check is the last line of defence
        if leads_to_own_script(folder_path):
            return "holds this script, it is never removed"
        if self._is_simulation:
            return None
        # Permanent deletion, the recycle bin object exists only for its own method
        if self._recycle_bin is None:
            return remove_path(folder_path, os.rmdir)
        # The shell would also recycle a folder with content, os.rmdir only removes empty folders
        folder_change = describe_folder_change(folder_path)
        if folder_change is not None:
            return folder_change
        return self._recycle_bin.move_files([folder_path]).get(folder_path, "no result from the recycle bin")

    # ==== Output ==============================================================

    def _log(self, status: str, display_path: str, note: str = "") -> None:
        """Write a line to the deletion log if reports are saved."""
        if self._deletion_log is not None:
            self._deletion_log.write_entry(status, display_path, note)

    def _progress_text(self) -> str:
        """Counters shown in the live line and the status line."""
        checked_text = format_count(self.result.files_checked)
        if self.plan.expected_file_total:
            checked_text += f"/{format_count(self.plan.expected_file_total)}"
        verb = "matched" if self._is_simulation else "deleted"
        progress_text = (f"checked {checked_text} | {verb} {format_count(self._deleted_count)} | "
                         f"failed {format_count(self._failed_count)}")
        if self.result.removed_folders.count:
            progress_text += f" | folders removed {format_count(self.result.removed_folders.count)}"
        return progress_text


# ==== Reports =================================================================


class ReportBuilder:
    """Builds the text lines shown in the console and written to report files."""

    @staticmethod
    def plan_lines(plan: DeletionPlan, scan_result: Optional[ScanResult]) -> List[str]:
        """Summary of the deletion plan, shown before the confirmation."""
        lines = section_lines("DELETION PLAN")
        lines.append(f"  Target folder  : {plan.root_folder}")
        lines.append(f"  File types     : {join_extensions(plan.extensions)}")
        if scan_result is not None:
            selected_statistics = [scan_result.statistics_by_type[extension] for extension in plan.extensions
                                   if extension in scan_result.statistics_by_type]
            file_count = sum(statistics.file_count for statistics in selected_statistics)
            total_bytes = sum(statistics.total_bytes for statistics in selected_statistics)
            lines.append(f"  Matching files : {format_count(file_count)} files, "
                         f"{format_size(total_bytes)} (found by the scan)")
        else:
            lines.append("  Matching files : unknown, no scan was run")
        lines.append(f"  System files   : {'included' if plan.include_system_files else 'excluded'}")
        lines.append(f"  Method         : {plan.method.value}")
        lines.append(f"  Empty folders  : {plan.empty_folder_policy.value}")
        lines.append(f"  Created        : {datetime.now():%Y-%m-%d %H:%M:%S}")
        return lines

    @staticmethod
    def scan_lines(result: ScanResult, example_limit: int, type_column_width: int) -> List[str]:
        """Scan result with the numbered table of file types and everything that was skipped."""
        title = "SCAN RESULT" + ("   (cancelled, incomplete)" if result.was_cancelled else "")
        lines = section_lines(title)
        lines.append(f"  Target folder : {result.root_folder}")
        lines.append(f"  System files  : {'included' if result.include_system_files else 'excluded'}")
        lines.append(f"  Duration      : {format_duration(result.duration_seconds)}")
        lines.append("")
        sorted_types = result.sorted_types()
        if sorted_types:
            lines.append(f"  {format_count(len(sorted_types))} different file types found:")
            lines.append("")
            lines += ReportBuilder._scan_table(sorted_types, type_column_width)
        else:
            lines.append("  No files found.")
        lines += ReportBuilder.walk_lines(result.walk_statistics, example_limit)
        walk_statistics = result.walk_statistics
        if not result.include_system_files and (walk_statistics.skipped_system_files.count
                                                or walk_statistics.skipped_system_folders.count):
            lines.append("")
            lines.append("  Tip: run again with system files included to see their file types as well.")
        return lines

    @staticmethod
    def deletion_lines(result: DeletionResult, example_limit: int, type_column_width: int) -> List[str]:
        """Deletion result per file type with removed folders, failures and skipped items."""
        plan = result.plan
        is_simulation = plan.method is DeletionMethod.SIMULATION
        title = "SIMULATION RESULT (nothing was deleted)" if is_simulation else "DELETION RESULT"
        if result.was_cancelled:
            title += "   (cancelled, incomplete)"
        lines = section_lines(title)
        lines.append(f"  Target folder : {plan.root_folder}")
        lines.append(f"  File types    : {join_extensions(plan.extensions)}")
        lines.append(f"  System files  : {'included' if plan.include_system_files else 'excluded'}")
        lines.append(f"  Method        : {plan.method.value}")
        lines.append(f"  Files checked : {format_count(result.files_checked)}")
        lines.append(f"  Duration      : {format_duration(result.duration_seconds)}")
        lines.append("")
        lines += ReportBuilder._deletion_table(result, is_simulation, type_column_width)

        if plan.empty_folder_policy is not EmptyFolderPolicy.KEEP:
            verb = "that would be removed" if is_simulation else "removed"
            lines.append("")
            lines.append(f"  Empty folders {verb}: {format_count(result.removed_folders.count)}")
            if result.failed_folders.count:
                lines.append(f"  Empty folders not removed: {format_count(result.failed_folders.count)}")
                lines += ReportBuilder._example_lines(result.failed_folders, example_limit)
        if result.failed_files.count:
            lines.append("")
            lines.append(f"  Files not deleted: {format_count(result.failed_files.count)}")
            lines += ReportBuilder._example_lines(result.failed_files, example_limit)
        lines += ReportBuilder.walk_lines(result.walk_statistics, example_limit)
        return lines

    @staticmethod
    def walk_lines(statistics: WalkStatistics, example_limit: int) -> List[str]:
        """Folders read and items skipped by the folder walk, with example paths."""
        lines = ["", f"  {'Folders read':<29}: {format_count(statistics.folders_read)}"]
        sections = [
            ("Skipped system files", statistics.skipped_system_files, True),
            ("Skipped system folders", statistics.skipped_system_folders, False),
            ("Skipped links and junctions", statistics.skipped_links, False),
            ("Unreadable folders or files", statistics.unreadable_items, False),
            ("Protected, this script", statistics.skipped_own_script, False),
        ]
        for title, collection, show_size in sections:
            if collection.count == 0:
                continue
            amount_text = format_count(collection.count)
            if show_size:
                amount_text += f" ({format_size(collection.total_bytes)})"
            lines.append(f"  {title:<29}: {amount_text}")
            lines += ReportBuilder._example_lines(collection, example_limit)
        return lines

    @staticmethod
    def _scan_table(sorted_types: List[Tuple[str, TypeStatistics]], type_column_width: int) -> List[str]:
        """Numbered table of the file types with files and size, closed by a total line."""
        number_width = max(3, len(str(len(sorted_types))))
        longest_label = max(len(format_extension(extension)) for extension, _ in sorted_types)
        type_width = max(len("File type"), min(type_column_width, longest_label))

        def table_row(number_text: str, type_text: str, count_text: str, size_text: str) -> str:
            return f"  {number_text:>{number_width}}  {type_text:<{type_width}}  {count_text:>13}  {size_text:>11}"

        separator = table_row("-" * number_width, "-" * type_width, "-" * 13, "-" * 11)
        lines = [table_row("No.", "File type", "Files", "Size"), separator]
        for number, (extension, statistics) in enumerate(sorted_types, start=1):
            lines.append(table_row(str(number), shorten_text(format_extension(extension), type_width),
                                   format_count(statistics.file_count), format_size(statistics.total_bytes)))
        lines.append(separator)
        total_files = sum(statistics.file_count for _, statistics in sorted_types)
        total_bytes = sum(statistics.total_bytes for _, statistics in sorted_types)
        lines.append(table_row("", "Total", format_count(total_files), format_size(total_bytes)))
        return lines

    @staticmethod
    def _deletion_table(result: DeletionResult, is_simulation: bool, type_column_width: int) -> List[str]:
        """Deleted and failed files per chosen file type, closed by a total line."""
        empty_statistics = TypeStatistics()
        extensions = sorted(result.plan.extensions, key=lambda extension: (
            -result.deleted_by_type.get(extension, empty_statistics).file_count, extension))
        longest_label = max(len(format_extension(extension)) for extension in extensions)
        type_width = max(len("File type"), min(type_column_width, longest_label))

        def table_row(type_text: str, deleted_text: str, size_text: str, failed_text: str) -> str:
            return f"  {type_text:<{type_width}}  {deleted_text:>13}  {size_text:>11}  {failed_text:>10}"

        separator = table_row("-" * type_width, "-" * 13, "-" * 11, "-" * 10)
        lines = [table_row("File type", "Would delete" if is_simulation else "Deleted", "Size", "Failed"),
                 separator]
        for extension in extensions:
            deleted = result.deleted_by_type.get(extension, empty_statistics)
            failed = result.failed_by_type.get(extension, empty_statistics)
            lines.append(table_row(shorten_text(format_extension(extension), type_width),
                                   format_count(deleted.file_count), format_size(deleted.total_bytes),
                                   format_count(failed.file_count)))
        lines.append(separator)
        lines.append(table_row("Total", format_count(result.deleted_count), format_size(result.deleted_bytes),
                               format_count(result.failed_count)))
        return lines

    @staticmethod
    def _example_lines(collection: PathCollection, example_limit: int) -> List[str]:
        """Example paths of a collection and how many more were not listed."""
        lines = []
        for path, note in collection.examples[:example_limit]:
            lines.append(f"      {path}" + (f"   [{note}]" if note else ""))
        not_listed_count = collection.count - min(example_limit, len(collection.examples))
        if not_listed_count > 0:
            lines.append(f"      ... and {format_count(not_listed_count)} more")
        return lines


class ReportWriter:
    """Creates report files in the reports folder next to this script."""

    def __init__(self) -> None:
        script_folder = os.path.dirname(os.path.abspath(__file__))
        self.folder = os.path.join(script_folder, REPORT_FOLDER_NAME)

    def new_report_path(self, report_name: str) -> str:
        """Create the reports folder if needed and return a new file path with timestamp."""
        os.makedirs(self.folder, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.folder, f"{report_name}_{timestamp}.txt")

    def save_lines(self, report_name: str, lines: List[str]) -> str:
        """Write the lines to a new report file and return its path."""
        report_path = self.new_report_path(report_name)
        with open(report_path, "w", encoding="utf-8", errors="replace") as report_file:
            report_file.write("\n".join(lines) + "\n")
        return report_path


class DeletionLog:
    """Log file with one line for every deleted, failed or removed item."""

    def __init__(self, file_path: str, header_lines: List[str]) -> None:
        self.file_path = file_path
        self._log_file = open(file_path, "w", encoding="utf-8", errors="replace")
        self.write_lines(header_lines + [""])

    def __enter__(self) -> DeletionLog:
        return self

    def __exit__(self, *exception_info) -> None:
        self._log_file.close()

    def write_entry(self, status: str, path: str, note: str = "") -> None:
        """One line per item with status, path and an optional note."""
        line = f"{status:<14}{path}"
        if note:
            line += f"   [{note}]"
        self._log_file.write(line + "\n")

    def write_lines(self, lines: List[str]) -> None:
        """Free text lines, used for the deletion plan and the result."""
        self._log_file.write("\n".join(lines) + "\n")


# ==== Console dialog ==========================================================


class ConsoleDialog:
    """Asks the user all questions. Every question repeats until the answer is valid."""

    def ask_main_menu(self) -> Optional[RunMode]:
        """Return the chosen mode or None to exit."""
        print("\n".join(section_lines("MAIN MENU")))
        choice = self._choose([
            ("1", "Scan            list all file types with number of files and size"),
            ("2", "Delete          delete all files of the file types you enter"),
            ("3", "Scan + delete   list all file types, then choose which ones to delete"),
            ("0", "Exit"),
        ], default_key=None, footer="Ctrl+C cancels a running step and returns to this menu.")
        return {"1": RunMode.SCAN, "2": RunMode.DELETE, "3": RunMode.SCAN_AND_DELETE}.get(choice)

    def ask_target_folder(self, current_folder: Optional[str]) -> str:
        """Keep the current folder or enter another one. Without a usable current folder one must be entered."""
        print()
        usable_folder: Optional[str] = None
        if current_folder is not None:
            # A drive may have been removed meanwhile
            usable_folder, error_message = resolve_target_folder(current_folder)
            if usable_folder is None:
                print(f"  {error_message}")
        if usable_folder is not None:
            print("Target folder: press Enter to keep it, or type, paste or drag another folder here.")
            prompt = f"Folder [{usable_folder}]: "
        else:
            print("Target folder: type, paste or drag the folder to examine here.")
            prompt = "Folder: "
        while True:
            answer = input(prompt).strip() or usable_folder or ""
            folder, error_message = resolve_target_folder(answer)
            if folder is not None:
                print(f"  Using: {folder}")
                return folder
            print(f"  {error_message}")

    def ask_include_system_files(self) -> bool:
        """Explain operating system files and ask whether to include them."""
        print()
        print('Operating system files are files and folders with the Windows "System" attribute')
        print("and well known system items such as $RECYCLE.BIN, System Volume Information,")
        print("pagefile.sys, desktop.ini or Thumbs.db. Excluded system folders are not entered.")
        return self._ask_yes_no("Include operating system files?", default=False)

    def ask_save_reports(self, mode: RunMode, report_folder: str) -> bool:
        """Ask whether to save reports, the question fits the mode."""
        question = {
            RunMode.SCAN: "Save the overview as a text file?",
            RunMode.DELETE: "Save a log of the deletion as a text file?",
            RunMode.SCAN_AND_DELETE: "Save the overview and the deletion log as text files?",
        }[mode]
        print()
        print(f"Reports are saved in {report_folder}")
        return self._ask_yes_no(question, default=False)

    def ask_types_to_delete(self) -> Set[str]:
        """Ask for typed file types. An empty set means cancel."""
        print()
        print("No scan was run, so there is no list and no preselection: type the file types.")
        print(f'Example: .chk .tmp bak     A single "{NO_EXTENSION_INPUT}" stands for all files without extension.')
        print("Separate them by spaces or commas. Press Enter without input to cancel.")
        print("Tip: mode 3 (Scan + delete) lists all file types first, you choose them by number or in a window.")
        while True:
            answer = input("File types: ").strip()
            if not answer:
                return set()
            extensions, error_messages = parse_typed_extensions(answer)
            if not error_messages:
                print(f"  Selected file types ({len(extensions)}): {join_extensions(extensions)}")
                return extensions
            for error_message in error_messages:
                print(f"  {error_message}")

    def ask_types_from_scan(self, sorted_types: List[Tuple[str, TypeStatistics]]) -> Set[str]:
        """Ask for numbers from the scan table or typed file types. An empty set means skip."""
        print()
        print("Choose the file types to delete:")
        print("  by number from the list   e.g.  1 3 5-7")
        print("  range with exclusions     e.g.  10-30 (22 24)   10 to 30 except 22 and 24")
        print("  by file type              e.g.  .chk .tmp")
        print(f'  Files without extension are listed by name, a single "{NO_EXTENSION_INPUT}" chooses all of them.')
        print("  All forms can be combined. File types made of digits need the dot: .001")
        print("  Press Enter without input to skip the deletion.")
        numbered_extensions = [extension for extension, _ in sorted_types]
        while True:
            answer = input("Selection: ").strip()
            if not answer:
                return set()
            extensions, error_messages = parse_scan_selection(answer, numbered_extensions)
            if not error_messages:
                self.show_scan_selection(extensions, len(numbered_extensions))
                return extensions
            for error_message in error_messages:
                print(f"  {error_message}")

    def ask_open_selection_window(self) -> bool:
        """False without asking if PySide6 is missing, then the file types are chosen in the console."""
        print()
        if PYSIDE_IMPORT_ERROR:
            print(f"The selection window is not available, it needs PySide6 ({PYSIDE_IMPORT_ERROR}).")
            print("Install it with:  python -m pip install PySide6")
            return False
        print("The selection window lists all file types with a checkbox, handy for long lists.")
        return self._ask_yes_no("Choose the file types in the selection window?", default=True)

    def show_scan_selection(self, extensions: Set[str], scan_type_count: int) -> None:
        """Repeat the file types chosen after a scan, with a warning if these are all of them."""
        print(f"  Selected file types ({len(extensions)}): {join_extensions(extensions)}")
        if len(extensions) == scan_type_count:
            print("  These are all file types of the scan, every file found will be deleted.")

    def ask_deletion_method(self, volume: TargetVolume) -> DeletionMethod:
        """Ask for recycle bin, permanent deletion or simulation. Without recycle bin the simulation is the default."""
        print()
        print("How should the files be deleted?")
        options = []
        if volume.supports_recycle_bin:
            options.append(("1", "Move to the recycle bin"))
            default_key = "1"
        else:
            print(f"  The recycle bin is not available on {volume.description}.")
            default_key = "3"
        options.append(("2", "Delete permanently, cannot be undone"))
        options.append(("3", "Simulation only, shows what would be deleted"))
        choice = self._choose(options, default_key)
        return {"1": DeletionMethod.RECYCLE_BIN, "2": DeletionMethod.PERMANENT,
                "3": DeletionMethod.SIMULATION}[choice]

    def ask_empty_folder_policy(self) -> EmptyFolderPolicy:
        """Ask what happens with empty folders after deleting."""
        print()
        print("What should happen with empty folders after deleting?")
        print("Empty folders are removed with the method chosen for the files.")
        choice = self._choose([
            ("1", "Keep all folders"),
            ("2", "Remove folders that became empty through this deletion"),
            ("3", "Remove all empty folders, also those that were empty before"),
        ], default_key="2")
        return {"1": EmptyFolderPolicy.KEEP, "2": EmptyFolderPolicy.REMOVE_EMPTIED,
                "3": EmptyFolderPolicy.REMOVE_ALL}[choice]

    def confirm_deletion(self, plan: DeletionPlan) -> bool:
        """Ask for the keyword before a real deletion, a simulation starts without asking."""
        if plan.method is DeletionMethod.SIMULATION:
            print("\nSimulation: nothing will be deleted.")
            return True
        print()
        if plan.method is DeletionMethod.PERMANENT:
            print("WARNING: permanently deleted files cannot be restored.")
            keyword = "delete"
        else:
            keyword = "yes"
        answer = input(f'Type "{keyword}" to start, anything else cancels: ').strip().lower()
        return answer == keyword

    def _choose(self, options: List[Tuple[str, str]], default_key: Optional[str], footer: str = "") -> str:
        """Print the options with their keys and return the chosen key. Enter takes the default."""
        for key, label in options:
            default_marker = "   (default)" if key == default_key else ""
            print(f"  {key}  {label}{default_marker}")
        if footer:
            print(footer)
        valid_keys = [key for key, _ in options]
        prompt = f"Choice [{default_key}]: " if default_key else "Choice: "
        while True:
            answer = input(prompt).strip()
            if not answer and default_key:
                return default_key
            if answer in valid_keys:
                return answer
            print(f"  Please enter {', '.join(valid_keys[:-1])} or {valid_keys[-1]}.")

    def _ask_yes_no(self, question: str, default: bool) -> bool:
        """Ask a yes or no question. Enter takes the default, shown in brackets like in the other questions."""
        default_text = "y" if default else "n"
        while True:
            answer = input(f"{question} (y/n) [{default_text}]: ").strip().lower()
            if not answer:
                return default
            if answer in YES_ANSWERS:
                return True
            if answer in NO_ANSWERS:
                return False
            print("  Please answer y (yes) or n (no).")


# ==== Application =============================================================


class FileTypeCleanerApp:
    """Main menu and the flow of the three modes."""

    def __init__(self, root_folder: Optional[str]) -> None:
        self._dialog = ConsoleDialog()
        self._report_writer = ReportWriter()
        self._last_folder = root_folder         # None until a folder is given at start or in the dialog

    def run(self) -> int:
        """Show the main menu until the user exits. Return the exit code."""
        print_banner()
        if self._last_folder is not None:
            print(f"Target folder: {self._last_folder}")

        while True:
            try:
                mode = self._dialog.ask_main_menu()
            except (KeyboardInterrupt, EOFError):
                print()
                break
            if mode is None:
                break
            try:
                self._run_mode(mode)
            except KeyboardInterrupt:
                print("\n\nCancelled, back to the main menu.")
            except EOFError:
                print("\n\nNo more input, exiting.")
                break
            except OSError as error:
                # For example a disconnected drive or a full disk while writing a report
                print(f"\n\nError: {error}\nBack to the main menu.")
        print("Goodbye.")
        return 0

    def _run_mode(self, mode: RunMode) -> None:
        """Ask for the options of a run, then scan, choose and delete as the mode requires."""
        root_folder = self._dialog.ask_target_folder(self._last_folder)
        self._last_folder = root_folder
        volume = TargetVolume(root_folder)
        include_system_files = self._dialog.ask_include_system_files()
        save_reports = self._dialog.ask_save_reports(mode, self._report_writer.folder)

        scan_result: Optional[ScanResult] = None
        if mode is RunMode.DELETE:
            extensions = self._dialog.ask_types_to_delete()
        else:
            scan_result = self._run_scan(root_folder, include_system_files, volume, save_reports)
            if mode is RunMode.SCAN:
                return
            if scan_result.was_cancelled:
                print("\nThe scan was cancelled, so nothing will be deleted.")
                return
            if not scan_result.statistics_by_type:
                print("\nNo files found, nothing to delete.")
                return
            extensions = self._choose_types_from_scan(scan_result)
        if not extensions:
            print("\nNo file types selected, nothing was deleted.")
            return

        plan = DeletionPlan(
            root_folder=root_folder,
            include_system_files=include_system_files,
            extensions=extensions,
            method=self._dialog.ask_deletion_method(volume),
            empty_folder_policy=self._dialog.ask_empty_folder_policy(),
            expected_file_total=scan_result.total_files if scan_result is not None else None,
        )
        plan_lines = ReportBuilder.plan_lines(plan, scan_result)
        print("\n".join(plan_lines))
        if not self._dialog.confirm_deletion(plan):
            print("Cancelled, nothing was deleted.")
            return
        self._run_deletion(plan, volume, plan_lines, save_reports)

    def _run_scan(self, root_folder: str, include_system_files: bool,
                  volume: TargetVolume, save_reports: bool) -> ScanResult:
        """Scan with progress output, show the result and save it if reports are wanted."""
        print()
        print(f"[{clock_time()}] Scan started in {root_folder}")
        result = FileTypeScanner(root_folder, include_system_files, volume.root_path).run()
        state = "cancelled" if result.was_cancelled else "finished"
        print(f"[{clock_time()}] Scan {state} after {format_duration(result.duration_seconds)}")
        print("\n".join(ReportBuilder.scan_lines(result, CONSOLE_EXAMPLE_LIMIT, CONSOLE_TYPE_COLUMN_WIDTH)))
        if save_reports:
            self._save_report("scan_report",
                              ReportBuilder.scan_lines(result, STORED_EXAMPLE_LIMIT, REPORT_TYPE_COLUMN_WIDTH))
        return result

    def _choose_types_from_scan(self, scan_result: ScanResult) -> Set[str]:
        """Tick the file types in the selection window or choose them in the console. An empty set means skip."""
        if self._dialog.ask_open_selection_window():
            return self._choose_types_in_window(scan_result)
        return self._dialog.ask_types_from_scan(scan_result.sorted_types())

    def _choose_types_in_window(self, scan_result: ScanResult) -> Set[str]:
        """Open the selection window and wait for it. If the window fails, the console takes over."""
        print()
        print(f"[{clock_time()}] The selection window is open. If you do not see it, look in the taskbar.")
        print('           Close it or press "Continue with the ticked file types" to come back here.')
        try:
            extensions = FileTypeSelectionWindow.show_and_wait(scan_result)
        except Exception:
            traceback.print_exc()
            print("The selection window failed, see above. Choose the file types here instead.")
            return self._dialog.ask_types_from_scan(scan_result.sorted_types())
        if extensions is None:
            print("The selection window was closed without continuing.")
            return set()
        self._dialog.show_scan_selection(extensions, len(scan_result.statistics_by_type))
        return extensions

    def _run_deletion(self, plan: DeletionPlan, volume: TargetVolume,
                      plan_lines: List[str], save_reports: bool) -> None:
        """Delete with a deletion log if reports are wanted. If the log cannot be created, nothing is deleted."""
        if not save_reports:
            self._execute_deletion(plan, volume, None)
            return
        try:
            deletion_log = DeletionLog(self._report_writer.new_report_path("deletion_log"), plan_lines)
        except OSError as error:
            print(f"The deletion log could not be created ({describe_os_error(error)}), nothing was deleted.")
            return
        with deletion_log:
            self._execute_deletion(plan, volume, deletion_log)
        print(f"\nDeletion log saved: {deletion_log.file_path}")

    def _execute_deletion(self, plan: DeletionPlan, volume: TargetVolume,
                          deletion_log: Optional[DeletionLog]) -> None:
        """Delete with progress output, show the result and add it to the log."""
        print()
        if plan.method is DeletionMethod.RECYCLE_BIN:
            print("Note: if Windows cannot recycle a file, for example because it is larger than")
            print("the recycle bin, a Windows dialog asks before deleting it permanently.")
        activity = "Simulation" if plan.method is DeletionMethod.SIMULATION else "Deletion"
        print(f"[{clock_time()}] {activity} started in {plan.root_folder}")
        result = FileDeleter(plan, volume.root_path, deletion_log).run()
        state = "cancelled" if result.was_cancelled else "finished"
        print(f"[{clock_time()}] {activity} {state} after {format_duration(result.duration_seconds)}")
        print("\n".join(ReportBuilder.deletion_lines(result, CONSOLE_EXAMPLE_LIMIT, CONSOLE_TYPE_COLUMN_WIDTH)))
        if deletion_log is not None:
            deletion_log.write_lines([""] + ReportBuilder.deletion_lines(result, STORED_EXAMPLE_LIMIT,
                                                                         REPORT_TYPE_COLUMN_WIDTH))

    def _save_report(self, report_name: str, lines: List[str]) -> None:
        """Save a report file and show its path, a failure does not stop the run."""
        try:
            report_path = self._report_writer.save_lines(report_name, lines)
            print(f"\nReport saved: {report_path}")
        except OSError as error:
            print(f"\nThe report could not be saved: {describe_os_error(error)}")


# ==============================================================================
#   FUNCTIONS
# ==============================================================================

# ==== Paths ===================================================================


def to_extended_path(path: str) -> str:
    """Absolute path with the long path prefix, so deep paths and odd names work."""
    if path.startswith(EXTENDED_PATH_PREFIX):
        return path
    absolute_path = os.path.abspath(path)
    if absolute_path.startswith("\\\\"):
        return EXTENDED_UNC_PATH_PREFIX + absolute_path[2:]
    return EXTENDED_PATH_PREFIX + absolute_path


def to_display_path(path: str) -> str:
    """Path without the long path prefix, for output and for the Windows shell."""
    if path.startswith(EXTENDED_UNC_PATH_PREFIX):
        return "\\\\" + path[len(EXTENDED_UNC_PATH_PREFIX):]
    if path.startswith(EXTENDED_PATH_PREFIX) and path[5:6] == ":":
        return path[len(EXTENDED_PATH_PREFIX):]
    return path


def is_same_or_inside(path: str, base_path: str) -> bool:
    """True if path equals base_path or lies somewhere inside of it."""
    normalized_path = os.path.normcase(os.path.normpath(path))
    normalized_base_path = os.path.normcase(os.path.normpath(base_path))
    try:
        return os.path.commonpath([normalized_path, normalized_base_path]) == normalized_base_path
    except ValueError:
        return False


def find_protection_violation(folder: str) -> Optional[str]:
    """Return why a folder must not be used as target folder, or None if it is allowed."""
    windows_locations = [
        os.environ.get("SystemRoot"),
        os.environ.get("ProgramFiles"),
        os.environ.get("ProgramFiles(x86)"),
        os.environ.get("ProgramW6432"),
        os.environ.get("ProgramData"),
    ]
    for location in filter(None, windows_locations):
        if is_same_or_inside(folder, location):
            return f"it lies inside the Windows location {location}"
        if is_same_or_inside(location, folder):
            return f"it contains the Windows location {location}"
    user_profile = os.environ.get("USERPROFILE")
    if user_profile and is_same_or_inside(user_profile, folder):
        return f"it contains your user profile {user_profile}"
    volume_root = TargetVolume(folder).root_path
    for folder_name in ACTIVE_VOLUME_FOLDER_NAMES:
        active_folder = os.path.join(volume_root, folder_name)
        if is_same_or_inside(folder, active_folder):
            return f"Windows is using {active_folder} right now, empty the recycle bin with Windows instead"
    return None


def resolve_target_folder(raw_input: str) -> Tuple[Optional[str], str]:
    """Turn user input into an existing, allowed folder. Return (folder, error message)."""
    cleaned_input = raw_input.strip().strip('"').strip("'").strip()
    if not cleaned_input:
        return None, "No folder entered."
    expanded_input = os.path.expandvars(os.path.expanduser(cleaned_input))
    if re.fullmatch(r"[A-Za-z]:", expanded_input):
        expanded_input += "\\"
    absolute_path = os.path.abspath(expanded_input)
    if os.path.isfile(absolute_path):
        return None, f"This is a file, not a folder: {absolute_path}"
    if not os.path.isdir(absolute_path):
        return None, f"Folder not found: {absolute_path}"
    # Links and substituted drives are resolved, so the protection check sees the real location
    resolved_path = to_display_path(os.path.realpath(absolute_path))
    violation = find_protection_violation(resolved_path)
    if violation:
        return None, f"This folder is not allowed because {violation}."
    return resolved_path, ""


def leads_to_own_script(path: str) -> bool:
    """True if the path is this script or a folder holding it, upper and lower case do not matter.

    Windows lets a running script delete its own file, so the paths are compared. Both are
    compared without the long path prefix, the target folder and this script have their links resolved.
    """
    script_key = os.path.normcase(to_display_path(SCRIPT_PATH))
    path_key = os.path.normcase(to_display_path(path)).rstrip("\\")
    return script_key == path_key or script_key.startswith(path_key + "\\")


def is_path_usable_by_shell(display_path: str) -> bool:
    """Check if the Windows shell addresses exactly this path and nothing else."""
    if display_path.startswith(EXTENDED_PATH_PREFIX) or len(display_path) > SHELL_MAX_PATH_LENGTH:
        return False
    for path_component in os.path.splitdrive(display_path)[1].split("\\"):
        if not path_component:
            continue
        # The shell would silently cut trailing dots and spaces or treat * and ? as wildcards
        if path_component[-1] in ". " or has_unsafe_characters(path_component):
            return False
        if path_component.split(".")[0].rstrip(" ").upper() in RESERVED_DEVICE_NAMES:
            return False
    return True


# ==== Files and folders =======================================================


def get_file_type(file_name: str) -> str:
    """Lower case extension including the dot, for example .jpg.

    A file without extension, for example .gitignore or README, forms a file type of its own:
    NO_EXTENSION_TYPE_PREFIX followed by its lower case name.
    """
    extension = os.path.splitext(file_name)[1].lower()
    if extension and extension != ".":
        return extension
    return NO_EXTENSION_TYPE_PREFIX + file_name.lower()


def is_no_extension_type(file_type: str) -> bool:
    """True for the file type of files without extension, also for all of them chosen by "."."""
    return file_type.startswith(NO_EXTENSION_TYPE_PREFIX)


def is_operating_system_item(name: str, attributes: int, is_folder: bool) -> bool:
    """True for items with the Windows system attribute or a well known system name."""
    if attributes & stat.FILE_ATTRIBUTE_SYSTEM:
        return True
    known_names = OPERATING_SYSTEM_FOLDER_NAMES if is_folder else OPERATING_SYSTEM_FILE_NAMES
    return name.lower() in known_names


def has_unsafe_characters(name: str) -> bool:
    """True if a name contains wildcards, control characters or characters invalid in Windows."""
    return any(character in UNSAFE_NAME_CHARACTERS or ord(character) < 32 for character in name)


def remove_path(path: str, remove_function: Callable[[str], None]) -> Optional[str]:
    """Run os.remove or os.rmdir and return an error message or None on success.

    A read only attribute blocks deleting on Windows, so it is cleared once if needed.
    """
    try:
        remove_function(path)
        return None
    except FileNotFoundError:
        return "no longer exists"
    except PermissionError as error:
        if not clear_read_only_attribute(path):
            return describe_os_error(error)
        try:
            remove_function(path)
            return None
        except OSError as retry_error:
            return describe_os_error(retry_error)
    except OSError as error:
        return describe_os_error(error)


def clear_read_only_attribute(path: str) -> bool:
    """Clear the read only attribute. True if it was set and is cleared now."""
    try:
        attributes = os.stat(path, follow_symlinks=False).st_file_attributes
        if not attributes & stat.FILE_ATTRIBUTE_READONLY:
            return False
        os.chmod(path, stat.S_IWRITE)
        return True
    except OSError:
        return False


def describe_folder_change(folder_path: str) -> Optional[str]:
    """Why a folder is no longer the empty folder the walk found, None if it is still empty."""
    try:
        if os.stat(folder_path, follow_symlinks=False).st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            return "is a link now"
        with os.scandir(folder_path) as folder_iterator:
            if next(folder_iterator, None) is not None:
                return "no longer empty"
    except FileNotFoundError:
        return "no longer exists"
    except OSError as error:
        return describe_os_error(error)
    return None


def describe_os_error(error: OSError) -> str:
    """Short readable reason of an operating system error."""
    return error.strerror or str(error)


def describe_shell_result(return_code: int, was_cancelled: bool) -> str:
    """Readable reason why the Windows shell did not recycle a file."""
    if was_cancelled:
        return "cancelled in the Windows dialog"
    if return_code == 0:
        return "could not be moved to the recycle bin"
    return SHELL_ERROR_MESSAGES.get(return_code, f"Windows shell error 0x{return_code:X}")


def add_to_type_statistics(statistics_by_type: Dict[str, TypeStatistics], file_type: str, size_bytes: int) -> None:
    """Count a file under a file type, the entry is created when the type first appears."""
    type_statistics = statistics_by_type.get(file_type)
    if type_statistics is None:
        type_statistics = statistics_by_type[file_type] = TypeStatistics()
    type_statistics.add(size_bytes)


# ==== User input ==============================================================


def split_selection(text: str) -> Tuple[List[SelectionPart], List[str]]:
    """Split typed input into entries with the exclusions in brackets behind them. Return (parts, errors)."""
    parts: List[SelectionPart] = []
    error_messages: List[str] = []
    bracket_tokens: Optional[List[str]] = None      # collects the tokens while a bracket is open
    # "10 - 30" is read as "10-30", brackets are tokens of their own
    normalized_text = re.sub(r"(?<=\d)\s*-\s*(?=\d)", "-", text)
    for token in re.findall(r"[()]|[^\s,;()]+", normalized_text):
        if token == "(":
            if bracket_tokens is None:
                bracket_tokens = []
            else:
                error_messages.append("Brackets cannot be nested.")
        elif token == ")":
            if bracket_tokens is None:
                error_messages.append('")" has no opening bracket "(".')
            elif not parts:
                error_messages.append(f'"({" ".join(bracket_tokens)})": exclusions must follow a range, '
                                      f'for example 10-30 (22 24).')
            else:
                # Several brackets behind one range are combined
                parts[-1].exclusion_tokens = (parts[-1].exclusion_tokens or []) + bracket_tokens
            bracket_tokens = None
        elif bracket_tokens is not None:
            bracket_tokens.append(token)
        else:
            parts.append(SelectionPart(token))
    if bracket_tokens is not None:
        error_messages.append('The closing bracket ")" is missing.')
    return parts, error_messages


def is_number_or_range(token: str) -> bool:
    """True for tokens made only of digits and dashes, like 5, 5-7 or the broken range 5-."""
    return re.fullmatch(r"[\d-]+", token) is not None


def parse_extension_token(token: str) -> Tuple[Optional[str], str]:
    """Turn a typed file type like "tmp", ".TMP" or "*.tmp" into ".tmp". Return (extension, error).

    A single "." stands for all files without extension.
    """
    if token == NO_EXTENSION_INPUT:
        return ALL_NO_EXTENSION_TYPE, ""
    extension = token[1:] if token.startswith("*.") else token
    if not extension.startswith("."):
        extension = "." + extension
    extension_body = extension[1:]
    if not extension_body:
        return None, f'"{token}" is not a file type.'
    if has_unsafe_characters(extension_body) or "\\" in extension_body or "/" in extension_body:
        return None, f'"{token}" contains characters that are not allowed, wildcards are not supported.'
    if "." in extension_body:
        return None, f'"{token}": only the last extension counts, for example .gz instead of .tar.gz.'
    return extension.lower(), ""


def parse_typed_extensions(text: str) -> Tuple[Set[str], List[str]]:
    """Parse file types typed for a deletion without scan. Return (extensions, error messages)."""
    parts, error_messages = split_selection(text)
    extensions: Set[str] = set()
    for part in parts:
        if is_number_or_range(part.token):
            error_messages.append(f'"{part.token}": numbers and ranges need the list of a scan, use mode 3 '
                                  f'(Scan + delete). File types made of digits need the dot, for example .001')
        elif part.exclusion_tokens is not None:
            error_messages.append(f'"{part.token} ({" ".join(part.exclusion_tokens)})": exclusions in brackets '
                                  f'need the list of a scan, use mode 3 (Scan + delete).')
        else:
            extension, error_message = parse_extension_token(part.token)
            if extension is None:
                error_messages.append(error_message)
            else:
                extensions.add(extension)
    if not parts and not error_messages:
        error_messages.append("No file type entered. Press Enter without input to cancel.")
    return extensions, error_messages


def parse_scan_selection(text: str, numbered_extensions: List[str]) -> Tuple[Set[str], List[str]]:
    """Parse numbers, ranges with exclusions and file types chosen from the scan table.

    Return (extensions, error messages).
    """
    parts, error_messages = split_selection(text)
    number_by_extension = {extension: number for number, extension in enumerate(numbered_extensions, start=1)}
    selected_numbers: Set[int] = set()
    for part in parts:
        numbers, error_message = resolve_scan_token(part.token, number_by_extension)
        if numbers is None:
            error_messages.append(error_message)
            continue
        if part.exclusion_tokens is not None:
            numbers = remove_exclusions(part, numbers, number_by_extension, error_messages)
        selected_numbers.update(numbers)
    if not parts and not error_messages:
        error_messages.append("No file type selected. Press Enter without input to skip the deletion.")
    return {numbered_extensions[number - 1] for number in selected_numbers}, error_messages


def resolve_scan_token(token: str, number_by_extension: Dict[str, int]) -> Tuple[Optional[Set[int]], str]:
    """Turn a number, a range or a file type into numbers of the scan table. Return (numbers, error)."""
    if not is_number_or_range(token):
        extension, error_message = parse_extension_token(token)
        if extension is None:
            return None, error_message
        if extension == ALL_NO_EXTENSION_TYPE:
            numbers = {number for file_type, number in number_by_extension.items() if is_no_extension_type(file_type)}
            if not numbers:
                return None, f'"{token}": the scan found no files without extension.'
            return numbers, ""
        if extension not in number_by_extension:
            error_message = f'"{token}": the file type {format_extension(extension)} was not found by the scan.'
            # A typed name like .gitignore or README may mean the file without extension of that name
            no_extension_number = number_by_extension.get(NO_EXTENSION_TYPE_PREFIX + token.lower())
            if no_extension_number is not None:
                error_message += f' The file without extension "{token}" has the number {no_extension_number}.'
            return None, error_message
        return {number_by_extension[extension]}, ""

    number_match = re.fullmatch(r"(\d+)(?:-(\d+))?", token)
    if number_match is None:
        return None, f'"{token}" is not a valid number or range, write a range like 5-7.'
    # 001 is far more likely the file type .001 than the number 1
    if re.search(r"(?<!\d)0\d", token):
        return None, (f'"{token}": numbers are written without leading zeros. '
                      f'File types made of digits need the dot, for example .001')
    first_number = int(number_match.group(1))
    last_number = int(number_match.group(2) or first_number)
    first_number, last_number = min(first_number, last_number), max(first_number, last_number)
    row_count = len(number_by_extension)
    if first_number < 1 or last_number > row_count:
        available_numbers = "only the number 1" if row_count == 1 else f"the numbers 1 to {row_count}"
        return None, f'"{token}": the list has {available_numbers}.'
    return set(range(first_number, last_number + 1)), ""


def remove_exclusions(part: SelectionPart, numbers: Set[int], number_by_extension: Dict[str, int],
                      error_messages: List[str]) -> Set[int]:
    """Remove the numbers and file types in brackets from a range. Problems are added to error_messages."""
    if not re.fullmatch(r"\d+-\d+", part.token):
        error_messages.append(f'"{part.token} ({" ".join(part.exclusion_tokens or [])})": exclusions in '
                              f'brackets only work behind a range, for example 10-30 (22 24).')
        return set()
    excluded_numbers: Set[int] = set()
    for exclusion_token in part.exclusion_tokens or []:
        exclusion_numbers, error_message = resolve_scan_token(exclusion_token, number_by_extension)
        if exclusion_numbers is None:
            error_messages.append(error_message)
        elif exclusion_token == NO_EXTENSION_INPUT:
            # "." stands for all files without extension, those inside the range are excluded
            if exclusion_numbers & numbers:
                excluded_numbers.update(exclusion_numbers & numbers)
            else:
                error_messages.append(f'"{exclusion_token}": no file without extension lies inside the range '
                                      f'{part.token}.')
        elif not exclusion_numbers <= numbers:
            error_messages.append(f'"{exclusion_token}" is not inside the range {part.token} '
                                  f'and cannot be excluded from it.')
        else:
            excluded_numbers.update(exclusion_numbers)
    remaining_numbers = numbers - excluded_numbers
    if not remaining_numbers:
        error_messages.append(f'"{part.token}": every number of the range is excluded, nothing is left.')
    return remaining_numbers


# ==== Formatting ==============================================================


def format_count(number: int) -> str:
    """Number with thousands separators, for example 12,345."""
    return f"{number:,}"


def format_quantity(number: int, noun: str) -> str:
    """Number with a noun in singular or plural, for example 1 file or 2 files."""
    return f"{number:,} {noun}" + ("" if number == 1 else "s")


def format_size(size_bytes: int) -> str:
    """Readable size with 1024 based units, as shown by Windows Explorer."""
    units = ("B", "KB", "MB", "GB", "TB", "PB")
    size = float(size_bytes)
    unit_index = 0
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    if unit_index == 0:
        return f"{size_bytes:,} B"
    return f"{size:,.1f} {units[unit_index]}"


def format_duration(seconds: float) -> str:
    """Duration as hours, minutes and seconds, for example 01:05:09."""
    hours, remainder = divmod(int(seconds), 3600)
    minutes, remaining_seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"


def format_extension(extension: str) -> str:
    """Display text of a file type, files without extension show their name.

    Odd ones are quoted, so spaces and control characters are visible.
    """
    if extension == ALL_NO_EXTENSION_TYPE:
        return ALL_NO_EXTENSION_LABEL
    is_name = is_no_extension_type(extension)
    text = extension[len(NO_EXTENSION_TYPE_PREFIX):] if is_name else extension
    if text != text.strip() or not text.isprintable():
        text = repr(text)
    return f"{NO_EXTENSION_LABEL}: {text}" if is_name else text


def join_extensions(extensions: Set[str]) -> str:
    """Sorted file types as one line separated by commas."""
    return ", ".join(format_extension(extension) for extension in sorted(extensions))


def to_window_text(text: str) -> str:
    """Text the window can show, broken characters of damaged file names become question marks."""
    return text.encode("utf-8", "replace").decode("utf-8")


def shorten_text(text: str, maximum_length: int) -> str:
    """Cut a text to the maximum length and mark the cut with three dots."""
    if len(text) <= maximum_length:
        return text
    return text[:max(0, maximum_length - 3)] + "..."


def clock_time() -> str:
    """Current time of day for status lines."""
    return datetime.now().strftime("%H:%M:%S")


def section_lines(title: str) -> List[str]:
    """Title between two separator lines, preceded by an empty line."""
    return ["", "=" * LINE_WIDTH, f"  {title}", "=" * LINE_WIDTH]


# ==== Window ==================================================================


def apply_dark_theme(application: QtWidgets.QApplication) -> None:
    """Dark colors and the style sheet for all windows of the program, also the title bar where Windows allows it."""
    application.setStyle("Fusion")
    try:
        application.styleHints().setColorScheme(QtCore.Qt.ColorScheme.Dark)
    except AttributeError:
        pass                    # older PySide6, the palette below still makes the window dark
    palette = QtGui.QPalette()
    color_roles = {
        QtGui.QPalette.ColorRole.Window: WINDOW_COLOR,
        QtGui.QPalette.ColorRole.WindowText: TEXT_COLOR,
        QtGui.QPalette.ColorRole.Base: BASE_COLOR,
        QtGui.QPalette.ColorRole.AlternateBase: SURFACE_COLOR,
        QtGui.QPalette.ColorRole.ToolTipBase: SURFACE_COLOR,
        QtGui.QPalette.ColorRole.ToolTipText: TEXT_COLOR,
        QtGui.QPalette.ColorRole.PlaceholderText: DISABLED_TEXT_COLOR,
        QtGui.QPalette.ColorRole.Text: TEXT_COLOR,
        QtGui.QPalette.ColorRole.Button: BUTTON_COLOR,
        QtGui.QPalette.ColorRole.ButtonText: TEXT_COLOR,
        QtGui.QPalette.ColorRole.BrightText: DELETE_TEXT_COLOR,
        QtGui.QPalette.ColorRole.Highlight: SELECTION_COLOR,
        QtGui.QPalette.ColorRole.HighlightedText: TEXT_COLOR,
        QtGui.QPalette.ColorRole.Link: ACCENT_COLOR,
    }
    for color_role, color in color_roles.items():
        palette.setColor(color_role, QtGui.QColor(color))
    for color_role in (QtGui.QPalette.ColorRole.Text, QtGui.QPalette.ColorRole.ButtonText,
                       QtGui.QPalette.ColorRole.WindowText):
        palette.setColor(QtGui.QPalette.ColorGroup.Disabled, color_role, QtGui.QColor(DISABLED_TEXT_COLOR))
    application.setPalette(palette)
    application.setStyleSheet(build_style_sheet())


def build_style_sheet() -> str:
    """Style sheet with the colors of the window theme filled in."""
    theme_colors = {
        "WINDOW_COLOR": WINDOW_COLOR, "SURFACE_COLOR": SURFACE_COLOR, "BASE_COLOR": BASE_COLOR,
        "BORDER_COLOR": BORDER_COLOR, "BUTTON_COLOR": BUTTON_COLOR, "BUTTON_HOVER_COLOR": BUTTON_HOVER_COLOR,
        "BUTTON_BORDER_COLOR": BUTTON_BORDER_COLOR, "TEXT_COLOR": TEXT_COLOR,
        "SECONDARY_TEXT_COLOR": SECONDARY_TEXT_COLOR, "DISABLED_TEXT_COLOR": DISABLED_TEXT_COLOR,
        "ACCENT_COLOR": ACCENT_COLOR, "ACCENT_HOVER_COLOR": ACCENT_HOVER_COLOR, "SELECTION_COLOR": SELECTION_COLOR,
        "WARNING_TEXT_COLOR": WARNING_TEXT_COLOR, "SCROLLBAR_COLOR": SCROLLBAR_COLOR,
    }
    return string.Template(STYLE_SHEET_TEMPLATE).substitute(theme_colors)


def create_card(title: str) -> Tuple[QtWidgets.QFrame, QtWidgets.QVBoxLayout]:
    """Panel with a rounded border and a small title, the building block of the window."""
    card = QtWidgets.QFrame()
    card.setObjectName("card")
    layout = QtWidgets.QVBoxLayout(card)
    layout.setContentsMargins(CARD_PADDING, CARD_PADDING, CARD_PADDING, CARD_PADDING)
    layout.setSpacing(CARD_SPACING)
    title_label = QtWidgets.QLabel(title.upper())
    title_label.setObjectName("sectionTitle")
    layout.addWidget(title_label)
    return card, layout


def create_button(text: str, callback: Callable[[], None], is_primary: bool = False,
                  tooltip: str = "") -> QtWidgets.QPushButton:
    """Button in the style of the window, a primary button is blue and marks the main action."""
    button = QtWidgets.QPushButton(text)
    if is_primary:
        button.setObjectName("primary")
    if tooltip:
        button.setToolTip(tooltip)
    button.clicked.connect(callback)
    return button


def create_secondary_label(text: str, word_wrap: bool = True) -> QtWidgets.QLabel:
    """Grey label for hints and paths."""
    label = QtWidgets.QLabel(text)
    label.setObjectName("secondary")
    label.setWordWrap(word_wrap)
    return label


def resize_and_center(window: QtWidgets.QWidget, width: int, height_share: float) -> None:
    """Size a window to a width in pixels and a share of the screen height, then center it."""
    available_geometry = QtGui.QGuiApplication.primaryScreen().availableGeometry()
    window.resize(min(width, available_geometry.width()), int(available_geometry.height() * height_share))
    frame_geometry = window.frameGeometry()
    frame_geometry.moveCenter(available_geometry.center())
    window.move(frame_geometry.topLeft())


def bring_window_to_front(window: QtWidgets.QWidget) -> None:
    """Show a window above the console. Windows does not hand it the focus on its own."""
    user32 = ctypes.WinDLL("user32")
    set_window_position = user32.SetWindowPos
    set_window_position.argtypes = [wintypes.HWND, wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                    ctypes.c_int, wintypes.UINT]
    set_window_position.restype = wintypes.BOOL
    window_handle = wintypes.HWND(int(window.winId()))
    position_flags = SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW
    # Topmost for a moment lifts the window above the console, then it behaves normally again
    set_window_position(window_handle, wintypes.HWND(HWND_TOPMOST), 0, 0, 0, 0, position_flags)
    set_window_position(window_handle, wintypes.HWND(HWND_NOTOPMOST), 0, 0, 0, 0, position_flags)
    window.raise_()
    window.activateWindow()


# ==== Program start ===========================================================


def print_banner() -> None:
    """Program title and subtitle shown at the start."""
    print("=" * LINE_WIDTH)
    print(f"  {PROGRAM_TITLE}")
    print(f"  {PROGRAM_SUBTITLE}")
    print("=" * LINE_WIDTH)


def configure_console_output() -> None:
    """Replace characters the console cannot show instead of crashing on odd file names."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass


def wait_for_enter(prompt: str) -> None:
    """Keep a console window opened by double click open until the user has read the output."""
    try:
        input(prompt)
    except (EOFError, KeyboardInterrupt):
        pass


def parse_command_line_arguments() -> argparse.Namespace:
    """Read the optional target folder from the command line."""
    parser = argparse.ArgumentParser(
        description="Lists all file types in a folder tree and deletes the file types you choose.")
    # Several arguments are accepted, so a path with spaces but without quotes gets a readable message
    parser.add_argument("folders", nargs="*", metavar="folder", help="target folder, optional")
    return parser.parse_args()


def find_start_folder(folder_arguments: List[str]) -> Tuple[Optional[str], str]:
    """Check the target folder given at start. Return (folder, error message), no folder at all is allowed."""
    if not folder_arguments:
        return None, ""
    if len(folder_arguments) > 1:
        return None, (f"{len(folder_arguments)} arguments were given instead of one folder. "
                      f"Put paths with spaces in quotes.")
    return resolve_target_folder(folder_arguments[0])


def show_start_error(error_message: str) -> int:
    """Explain why the program cannot start and return the exit code."""
    print_banner()
    print()
    print("The program cannot start with this target folder.")
    print(f"  {error_message}")
    print()
    print("Start it with the target folder, for example:")
    print(f'  python {SCRIPT_FILE_NAME} "F:\\Recovered"')
    print(f"or drag the folder onto {SCRIPT_FILE_NAME}, or start it without a folder.")
    wait_for_enter("\nPress Enter to close ...")
    return 2


# ==============================================================================
#   MAIN
# ==============================================================================


def main() -> int:
    """Check the platform and the start folder, then show the main menu. Return the exit code."""
    if os.name != "nt":
        print("This program runs on Windows only.")
        return 1
    configure_console_output()
    arguments = parse_command_line_arguments()
    try:
        root_folder, error_message = find_start_folder(arguments.folders)
        if error_message:
            return show_start_error(error_message)
        return FileTypeCleanerApp(root_folder).run()
    except Exception:
        # Last line of defence, keeps a console window opened by double click open to show the error
        traceback.print_exc()
        wait_for_enter("\nAn unexpected error occurred, see above. Press Enter to close ...")
        return 1


if __name__ == "__main__":
    sys.exit(main())
