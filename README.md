# DeleteSpecificFileTypes
Windows tool that gives an overview of all file types in a folder tree, with the number of files and total size of each, and deletes the file types you no longer need. Built for cleaning up recovered data.

<br>
The program shows which file types exist in a folder and all of its subfolders and deletes exactly the ones you no longer need. It was built for data recovered from damaged drives, which is usually full of fragments, temporary files, caches and leftovers of the operating system.

The program has three modes:
- Scan: lists every file type with its number of files and total size, sorted by number of files.
- Delete: deletes all files of the file types you type in, for example .chk .tmp.
- Scan + delete: scans first, then you choose the file types to delete. You can pick them by number, by range with exclusions, by extension, or by ticking them in an optional selection window.

For every run you decide whether operating system files are included. You also choose whether files go to the recycle bin, are deleted permanently or only simulated, and what happens with folders that are empty afterwards. The overview and a log of every deleted file can be saved as text files. A live counter shows the progress, and Ctrl+C stops safely at any time.

The program only works inside the chosen folder. Links and junctions are never followed, system locations such as Windows or Program Files are refused as target folders, and nothing is deleted before the deletion plan has been shown and confirmed.

Requirements: Windows 10 or 11, Python 3.8 or newer (standard library only). PySide6 is optional and needed only for the selection window.
