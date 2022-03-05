import logging
from typing import Optional
from copy import deepcopy
from typing import List, Dict, Set, Any

class Persist:
    """
    Class to run globally (called in pytestxrd) and persistently
    store

    o the files that have been opened during the session
    o the history of human inputs
    """

    def __init__(self):
        logging.debug("Initialising an empty FileTable")
        self.filetable: dict[str, int] = {}

    def ft_add_entry(self, path_name: str, fhandle: int) -> None:
        if path_name not in self.filetable:
            self.filetable[path_name] = fhandle
            logging.debug(
                f"File '{path_name}' with fhandle value {fhandle} has been entered into filetable"
            )
            return
        else:
            # this should never happen
            # that the file isnt already open should already be ascertained
            logging.warning(f"File '{path_name}' is already open, aborting")
            return

    def ft_prepare_deletion_dict(
        self, path_names: Optional[List[str]] = None
    ) -> Dict[str, int]:
        if path_names:
            try:
                # key-value pairs in a dict where key is in path_names
                out_dict = {
                    x: self.filetable[x] for x in self.filetable if x in path_names
                }
                logging.debug(f"Prepared dictionary with {len(out_dict)} entries")
                return deepcopy(out_dict)
            except KeyError:
                logging.warning("KeyError has been raised, check the pathnames again")
                return {}
        else:
            logging.debug(
                f"Preparing entire filetable dictionary with {len(self.filetable)} entries"
            )
            return deepcopy(self.filetable)

    def ft_remove_entry(self, path_name: str) -> None:
        del self.filetable[path_name]
        logging.debug(f"File '{path_name}' has been removed from filetable")
        return

    def ft_entry_exists(self, path_name: str) -> bool:
        is_in: bool = path_name in self.filetable
        if is_in:
            logging.debug(f"File '{path_name}' is aleady open")
        else:
            logging.debug(f"File '{path_name}' is not open yet")
        return is_in
