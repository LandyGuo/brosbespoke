#coding=utf8

class Error(Exception):
    """Base class for utils in this module."""
    pass

class LengthError(Error):
    """Exception raised for length-problem in the input.
    """
    pass

class InputTypeError(Error):
    """Exception raised for type-problem in the input.
    """
    pass
class SizeTypeError(Error):
    """Exception raised for sizeType-problem in the input.
    """
    pass

class ListValueTypeError(Error):
    """Exception raised for errors in the input.
    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class TransitionError(Error):
    """Raised when the user  size seems not normal.
    Attributes:
        message -- explanation of why the exception occured
    """

    def __init__(self,message):
        self.message = message