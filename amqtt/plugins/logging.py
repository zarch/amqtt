# Copyright (c) 2015 Nicolas JOUANIN
#
# See the file license.txt for copying permission.


import logging
from functools import partial


class EventLoggerPlugin:
    def __init__(self, context):
        self.context = context

    async def log_event(self, *args, **kwargs):
        self.context.logger.info(
            "### '%s' EVENT FIRED ###" % kwargs["event_name"].replace("old", ""),
        )

    def __getattr__(self, name):
        if name.startswith("on_"):
            return partial(self.log_event, event_name=name)
        raise AttributeError(f"'EventLoggerPlugin' object has no attribute {name!r}")


class PacketLoggerPlugin:
    def __init__(self, context):
        self.context = context

    async def on_mqtt_packet_received(self, *args, **kwargs):
        packet = kwargs.get("packet")
        session = kwargs.get("session", None)
        if self.context.logger.isEnabledFor(logging.DEBUG):
            if session:
                self.context.logger.debug(
                    f"{session.client_id} <-in-- {packet!r}",
                )
            else:
                self.context.logger.debug("<-in-- %s" % repr(packet))

    async def on_mqtt_packet_sent(self, *args, **kwargs):
        packet = kwargs.get("packet")
        session = kwargs.get("session", None)
        if self.context.logger.isEnabledFor(logging.DEBUG):
            if session:
                self.context.logger.debug(
                    f"{session.client_id} -out-> {packet!r}",
                )
            else:
                self.context.logger.debug("-out-> %s" % repr(packet))
