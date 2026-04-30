#!/usr/bin/env python3
import sys, re, os, time, threading
from pathlib import Path
from datetime import datetime

class PhaseRunner:
def init(self):
self.phases = []
self.results = []
self.spinner_running = False

