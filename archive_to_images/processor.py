"""Processor module"""

from typing import Any, Set

import os


class Processor:
    """
    Processor class
    """

    _ARCHIVE_EXT = ".zip"
    _NAME_TAG = "name"
    _INDEX_TAG = "index"
    _PADDING_TAG = "padding"
    _IMAGE_EXTENSION = ".png"

    def __init__(self, paths, verbose=False):
        """
        Processor class constructor.
        """
        self._input_paths = paths
        self._verbose = verbose
        self._file_set: Set[str] = set()
        self._progress = None

    def _initialize(self) -> None:
        """
        Initializes the processor before a conversion.
        """
        self._file_set = set()

    def _collect_input_files(self) -> None:
        """
        Collects input files via directory walking.
        """
        self._info("Collecting input files")
        for input_file in self._input_paths:
            if os.path.isdir(input_file):
                self._debug(f"Walking directory {input_file}")
                for path, _, directory_files in os.walk(input_file):
                    for file in directory_files:
                        self._file_set.add(os.path.join(path, file))
                        self._debug(f"Adding file {file}")
            else:
                self._file_set.add(input_file)
                self._debug(f"Adding file {input_file}")

    def _add_progress_task(self, bar_text: str, total_iterations: int) -> Any:
        """
        Add task to the progress bar.
        """
        if self._progress:
            return self._progress.add_task(f"[red]{bar_text}", total=total_iterations)

        return None

    def _update_progress_task(self, progress_task: Any, advance: int) -> None:
        """
        Update task to the progress bar.
        """
        if self._progress:
            self._progress.update(progress_task, advance=advance)

    def _debug(self, message: str) -> None:
        """
        Show debug message.
        """
        if self._progress and self._verbose:
            self._progress.console.print(f"[*] {message}")

    def _info(self, message: str) -> None:
        """
        Show info message.
        """
        if self._progress:
            self._progress.console.print(f"[green][+] {message}")

    def _warning(self, message: str) -> None:
        """
        Show warning message.
        """
        if self._progress:
            self._progress.console.print(f"[yellow][-] {message}")

    def _error(self, message: str) -> None:
        """
        Show error message.
        """
        if self._progress:
            self._progress.console.print(f"[red][!] {message}")
