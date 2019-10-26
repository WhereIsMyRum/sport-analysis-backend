#!/usr/bin/env python
import re
from c_videoformatter import c_videoformatter

video_formatter = c_videoformatter()
video_formatter.declare_queue("video_formatter_queue")
video_formatter.bind_consume(video_formatter.callback, "video_formatter_queue")

video_formatter.consume()