from os import linesep as br

class UserError(Exception):
    """
    Base class for errors that will be reported to the user.
    """

    # def __init__(self, message, *args: object) -> None:
    #     self.message = message
    #     super().__init__(*args)


class LidlessConfigError(UserError):
    def __str__(self) -> str:
        return f"Configuration error: {self.message}"
       

class DuplicateDestinationsError(UserError):

    def __init__(self, duplicates) -> None:
        super().__init__()
        self.duplicates = duplicates

    def __str__(self) -> str:
        lines = [
            "Collected multiple paths with same destinations.",
            "This would result in data being overwritten.",
        ]
        for dest, paths in self.duplicates.items():
            lines.extend([
                f'Destination "{dest}" is used by following paths:{br}'
            ])
            for path in paths:
                lines.append(f"    {path}")
        return br.join(lines) + br
