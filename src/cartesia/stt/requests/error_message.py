# This file was auto-generated by Fern from our API Definition.

import typing_extensions
import typing_extensions


class ErrorMessageParams(typing_extensions.TypedDict):
    request_id: typing_extensions.NotRequired[str]
    """
    The request ID associated with the error, if applicable.
    """

    message: str
    """
    Human-readable error message describing what went wrong.
    """
