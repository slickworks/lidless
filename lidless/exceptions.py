from os import linesep as br

class UserError(Exception):
    """
    Base class for errors that will be reported to the user.
    """
    def __init__(self, message) -> None:
        super().__init__()
        self.message = message

    def __str__(self) -> str:
        return f"{self.message}"


class DataclassInitErr(UserError):
    def __init__(self, tool, error) -> None:
        """
        Parses something like:
        Rsync.__init__() missing 1 required positional argument: 'dest'
        Rsync.__init__() got an unexpected keyword argument 'dest'
        """
        error_msg = str(error)
        if ".__init__()" in error_msg:
            error_msg = error_msg.replace(".__init__()", " error:")
        super().__init__(error_msg)


class DuplicateDestinationsError(UserError):

    def __init__(self, duplicates) -> None:
        
        lines = [
            "Collected multiple paths with same destinations.",
            "This would result in data being overwritten.",
        ]
        for dest, paths in duplicates.items():
            lines.extend([
                f'Destination "{dest}" is used by following paths:{br}'
            ])
            for path in paths:
                lines.append(f"    {path}")
        super().__init__(br.join(lines) + br)


class LidlessConfigError(UserError):
    def __str__(self) -> str:
        return f"Configuration error: {self.message}"
