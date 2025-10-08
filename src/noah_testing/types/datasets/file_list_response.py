# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel

__all__ = ["FileListResponse", "Data"]


class Data(BaseModel):
    id: str
    """Unique identifier for the file"""

    created_at: str
    """Timestamp when the file was created"""

    filename: str
    """Original filename"""

    size: int
    """Size of the file in bytes"""


class FileListResponse(BaseModel):
    data: List[Data]
    """List of file objects"""

    has_more: bool
    """Whether there are more files available"""
