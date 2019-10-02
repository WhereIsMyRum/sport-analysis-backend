#!/usr/bin/env python
import re
from rabbitConnection import rabbitConnection

message_dispatcher = rabbitConnection()
message_dispatcher.declare_exchange("bucketevents", "fanout")
message_dispatcher.declare_queue("message_dispatcher_queue")
message_dispatcher.bind_queue("bucketevents", "message_dispatcher_queue")
message_dispatcher.bind_consume(message_dispatcher.callback, "message_dispatcher_queue")

message_dispatcher.consume()