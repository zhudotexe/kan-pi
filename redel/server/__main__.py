"""
This is the minimal configuration for a ReDel visualization server with web browsing.
"""

import logging

from redel import AUTOGENERATE_TITLE
from redel.tools.browsing import Browsing
from .server import VizServer

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("redel-server")

# Define the configuration for each interactive session
redel_config = dict(
    title=AUTOGENERATE_TITLE,
    tool_configs={
        Browsing: {"always_include": True},
    },
)

log.info("Launching a minimal ReDel server with web browsing...")
log.info("Please open the URL below in your favorite web browser.")

# configure and start the server
server = VizServer(redel_kwargs=redel_config)
server.serve()
