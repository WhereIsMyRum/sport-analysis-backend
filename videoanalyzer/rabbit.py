#!/usr/bin/env python
import re
from c_videoanalyzer import c_videoanalyzer

video_analyzer = c_videoanalyzer()
video_analyzer.declare_queue("video_analyzer_queue")
video_analyzer.bind_consume(video_analyzer.callback, "video_analyzer_queue")

video_analyzer.consume()