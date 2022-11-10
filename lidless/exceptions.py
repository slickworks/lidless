
class LidlessConfigError(BaseException):
    pass

    # TODO: create custom exception for duplicates:
    # You are trying to sync multiple directories to the same remote path.
    # This is not allowed as the last sync would delete files from any previous syncs.
