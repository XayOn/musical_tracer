"""Main app."""

from contextlib import suppress
import configparser
import logging
import asyncio
import json

from .music import play_from

from cleo import Command
from cleo import Application

import pygogo


class MusicalTracerServerCommand(Command):
    """Starts api service.

    start_server
        {--socket=/tmp/musical.sock: socket file}
        {--config=config.ini : Config file}
        {--debug : Debug and verbose mode}
    """

    def handle(self):
        """Handle command."""
        logger = pygogo.Gogo(
            __name__,
            low_formatter=pygogo.formatters.structured_formatter,
            verbose=self.option('debug'))

        if self.option('debug'):
            logging.basicConfig(level=logging.DEBUG)

        logger.get_logger().debug("starting")

        config = configparser.ConfigParser()
        config.read(self.option('config') or '')
        asyncio.get_event_loop().run_until_complete(
            main_server(logger, config, self.option('socket')))


async def main_server(logger, config, socket):
    async def client_connected(reader, writer):
        while True:
            with suppress(Exception):
                result = (await reader.readline()).decode()
                play_from(json.loads(result))

    await asyncio.start_unix_server(client_connected, socket)
    while True:
        await asyncio.sleep(1)


def main():
    """Main."""
    application = Application()
    application.add(MusicalTracerServerCommand())
    application.run()
