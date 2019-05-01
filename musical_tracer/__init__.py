"""Main app."""

from contextlib import suppress
from itertools import count
import configparser
import logging
import asyncio
import json

from .music import Player

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
    """Execute player for each line received."""

    async def client_connected(reader, writer):
        """Client connected callback."""
        player = Player()
        player.reset(config=config, logger=logger)
        for event in count(0):
            try:
                result = (await reader.readline()).decode()
                player.add_note({**json.loads(result), **dict(eventno=event)})
                player.run()
            except json.JSONDecodeError:
                pass
            except:
                logger.get_logger().exception('cant_load')

    await asyncio.start_unix_server(client_connected, socket)

    while True:
        await asyncio.sleep(1)


def main():
    """Main."""
    application = Application()
    application.add(MusicalTracerServerCommand())
    application.run()
