from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional
import re


@dataclass(frozen=True)
class ListResponse:
    """
    This represents an action that was performed on a list, and not really the state of the list. For example, when
    the user clicks on the list, or double-clicks. It holds the row that was selected and the action type.
    """

    class ResponseType(Enum):
        SELECT_ITEM = 0
        INVOKE_ITEM = 1

    """The row that was selected."""
    row: int

    """The action that was performed."""
    response_type: ResponseType

    def __str__(self):
        return f"{self.row}:{1 if self.response_type == ListResponse.ResponseType.INVOKE_ITEM else 0}"

    @staticmethod
    def from_string(value) -> Optional[ListResponse]:
        """
        Deserialize a ListResponse from a string if possible or return empty
        :param: value the string to decode
        :return: either a ListResponse or empty.
        """
        list_response_pattern = "^(\\d+):(\\d)$"

        matcher = re.match(list_response_pattern, value)
        if matcher:
            row = int(matcher.group(1))
            response_type = (
                ListResponse.ResponseType.INVOKE_ITEM
                if int(matcher.group(2)) == 1
                else ListResponse.ResponseType.SELECT_ITEM
            )

            return ListResponse(row, response_type)

        return None
