import abc
from typing import Literal

from kani import ChatMessage, ChatRole
from pydantic import BaseModel

from .state import KaniState, RunState


class BaseEvent(BaseModel, abc.ABC):
    __log_event__ = True  # whether or not the event should be logged
    type: str


# server events
class Error(BaseEvent):
    type: Literal["error"] = "error"
    msg: str


class KaniSpawn(KaniState, BaseEvent):
    """A new kani was spawned.
    The ID can be the same as an existing ID, in which case this event should overwrite the previous state.
    """

    type: Literal["kani_spawn"] = "kani_spawn"


class KaniStateChange(BaseEvent):
    """A kani's run state changed."""

    type: Literal["kani_state_change"] = "kani_state_change"
    id: str
    state: RunState


class TokensUsed(BaseEvent):
    """A kani just finishes a request to the engine, which used this many tokens."""

    type: Literal["tokens_used"] = "tokens_used"
    id: str
    prompt_tokens: int
    completion_tokens: int


class KaniMessage(BaseEvent):
    """A kani added a message to its chat history."""

    type: Literal["kani_message"] = "kani_message"
    id: str
    msg: ChatMessage


class RootMessage(BaseEvent):
    """The root kani has a new result."""

    type: Literal["root_message"] = "root_message"
    msg: ChatMessage


class StreamDelta(BaseEvent):
    """A kani is streaming and emitted a new token."""

    __log_event__ = False

    type: Literal["kani_message"] = "stream_delta"
    id: str
    delta: str
    role: ChatRole


# user events
class SendMessage(BaseEvent):
    type: Literal["send_message"] = "send_message"
    content: str
