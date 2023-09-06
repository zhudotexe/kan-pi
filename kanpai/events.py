import abc
from typing import Literal

from kani import ChatMessage
from pydantic import BaseModel


class BaseEvent(BaseModel, abc.ABC):
    type: str


# server events
class Error(BaseEvent):
    type: Literal["error"] = "error"
    msg: str


class KaniSpawn(BaseEvent):
    """A new kani was spawned.
    The ID can be the same as an existing ID, in which case this event should overwrite the previous state.
    """

    type: Literal["kani_spawn"] = "kani_spawn"
    id: str
    parent: str | None
    always_included_messages: list[ChatMessage]
    chat_history: list[ChatMessage]


class KaniMessage(BaseEvent):
    """A kani added a message to its chat history."""

    type: Literal["kani_message"] = "kani_message"
    id: str
    msg: ChatMessage


class RootMessage(BaseEvent):
    """The root kani has a new result."""

    type: Literal["root_message"] = "root_message"
    msg: ChatMessage


# user events
class SendMessage(BaseEvent):
    type: Literal["send_message"] = "send_message"
    content: str
