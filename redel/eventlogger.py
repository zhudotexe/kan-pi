import json
import logging
import pathlib
import time
from collections import Counter
from typing import TYPE_CHECKING

from . import events
from .utils import read_jsonl

if TYPE_CHECKING:
    from .app import Kanpai

DEFAULT_LOG_DIR = pathlib.Path(__file__).parents[1] / ".kanpai/instances"
DEFAULT_LOG_DIR.mkdir(parents=True, exist_ok=True)

log = logging.getLogger(__name__)


class EventLogger:
    def __init__(self, app: "Kanpai", session_id: str, log_dir: pathlib.Path = None, clear_existing_log: bool = False):
        self.app = app
        self.session_id = session_id
        self.last_modified = time.time()
        self.log_dir = log_dir or (DEFAULT_LOG_DIR / session_id)
        self.log_dir.mkdir(exist_ok=True)

        self.aof_path = self.log_dir / "events.jsonl"
        self.state_path = self.log_dir / "state.json"

        if clear_existing_log:
            self.event_file = open(self.aof_path, "w", buffering=1)
            self.event_count = Counter()

        else:
            if self.aof_path.exists():
                existing_events = read_jsonl(self.aof_path)
                self.event_count = Counter(event["type"] for event in existing_events)
            else:
                self.event_count = Counter()
            self.event_file = open(self.aof_path, "a", buffering=1)

    async def log_event(self, event: events.BaseEvent):
        if not event.__log_event__:
            return
        self.last_modified = time.time()
        # since this is a synch operation we don't need a lock here (though it is thread-unsafe)
        self.event_file.write(event.model_dump_json())
        self.event_file.write("\n")
        self.event_count[event.type] += 1

    async def write_state(self):
        """Write the full state of the app to the state file, with a basic checksum against the AOF to check validity"""
        state = [ai.get_save_state().model_dump(mode="json") for ai in self.app.kanis.values()]
        data = {
            "id": self.session_id,
            "title": self.app.title,
            "last_modified": self.last_modified,
            "n_events": self.event_count.total(),
            "state": state,
        }
        with open(self.state_path, "w") as f:
            json.dump(data, f, indent=2)

    async def close(self):
        await self.write_state()
        self.event_file.close()
