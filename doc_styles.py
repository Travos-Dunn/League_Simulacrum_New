# Sphinx Rendering Example
def example_function(required_param: int, 
                     optional_param: str = None, 
                     default_param: float = 3.14, 
                     optional_default_param: bool = True) -> str:
    """
    This function demonstrates how to document optional, default, and both optional/default parameters using Sphinx.

    :param required_param: A required integer parameter.
    :type required_param: int

    :param optional_param: An optional parameter (defaults to None).
    :type optional_param: str, optional

    :param default_param: A required parameter with a default value of 3.14.
    :type default_param: float

    :param optional_default_param: An optional parameter with a default value of True.
    :type optional_default_param: bool, optional

    :return: A string message.
    :rtype: str
    """
    return f"Params received: {required_param}, {optional_param}, {default_param}, {optional_default_param}"

# Documenting Classes
class ExampleClass:
    """
    A simple example class.

    :param name: The name of the example.
    :type name: str
    :param value: A numerical value, defaults to 42.
    :type value: int, optional
    """

    def __init__(self, name: str, value: int = 42):
        self.name = name
        self.value = value

    def describe(self) -> str:
        """
        Return a description of the example.

        :return: A string describing the instance.
        :rtype: str
        """
        return f"{self.name} has a value of {self.value}."

# Documenting Exceptions
def divide(a: float, b: float) -> float:
    """
    Divide two numbers.

    :param a: Numerator.
    :type a: float
    :param b: Denominator.
    :type b: float
    :raises ValueError: If b is zero.
    :return: The result of the division.
    :rtype: float
    """
    if b == 0:
        raise ValueError("Denominator cannot be zero.")
    return a / b

# Documenting Modules
"""
This module provides utility functions for data processing.

Functions:
    - load_data(file_path: str) -> dict
    - save_data(file_path: str, data: dict) -> None
"""

# Cross-Referencing with `:class:` and `:func:`
"""
This function processes an :class:`ExampleClass` instance.

:param example: An instance of :class:`ExampleClass`.
:type example: ExampleClass
:return: A processed string.
:rtype: str
"""

# Sphinx Docstring Styles
# reStructuredText (reST) - See above


# Google Style
def my_function(param1: int, param2: str = "default") -> bool:
    """
    Summary of the function.

    Args:
        param1 (int): The first parameter.
        param2 (str, optional): The second parameter. Defaults to "default".

    Returns:
        bool: True if successful, False otherwise.
    """
    return True

# NumPy Style
def my_function(param1: int, param2: str = "default") -> bool:
    """
    Summary of the function.

    Parameters
    ----------
    param1 : int
        The first parameter.
    param2 : str, optional
        The second parameter. Defaults to "default".

    Returns
    -------
    bool
        True if successful, False otherwise.
    """
    return True
