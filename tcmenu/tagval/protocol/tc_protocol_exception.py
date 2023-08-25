class TcProtocolException(IOError):
    """An exception that indicates a problem during protocol conversion."""

    def __init__(self, message, cause=None):
        super().__init__(message)
        self.cause = cause

        # If there's a cause, modify the message to include it
        if self.cause:
            self.args = (f"{message} (caused by: {str(cause)})",)
