__package__ = 'hovo'

import random
import sys

from hovo.structural import rse


class Rgb:
    def rgb(hex_color):
        return {
            'rgbColor': {
                'red':   int(hex_color[1:3], 16)/255.,
                'green': int(hex_color[3:5], 16)/255.,
                'blue':  int(hex_color[5:7], 16)/255.,
            }
        }

    ACID_GREEN = rgb('#8FFE09')
    BEER = rgb('#FBB117')
    BLACK = rgb('#000000')
    BRIGHT_ORANGE = rgb('#FF5B00')
    GERALDINE = rgb('#FB8989')
    HAWKES_BLUE = rgb('#D4E2FC')
    JORDY_BLUE = rgb('#8AB9F1')
    LIGHT_ROSE = rgb('#FFC5CB')
    LIGHTNING_YELLOW = rgb('#FCC01E')
    MOONRAKER = rgb('#D6CEF6')
    NAPLES_YELLOW = rgb('#FADA5E')
    RED = rgb('#FF0000')
    WARM_RED = rgb('#FF3F00')
    

    RANDOM = {'red': random.random(), 'green': random.random(), 'blue': random.random()}

    ZERO_STAR = RED
    ONE_STAR = WARM_RED
    TWO_STARS = BEER
    THREE_STARS = LIGHTNING_YELLOW
    S3NS = JORDY_BLUE
    JOINT = NAPLES_YELLOW
    GOOGLE = GERALDINE

# ANSI escape codes for text colors
class Ansi:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    GRAY = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    __msgs_count = 0

    @staticmethod
    def __init__():
        Ansi.__msgs_count = 0
    @staticmethod
    def print(message, color=RESET, kill_line=False, **kwargs):
        Ansi.__msgs_count += 1
        print(("\r\033[K" if kill_line else "\n")
              + color + message + Ansi.RESET, end='', **kwargs)
    @staticmethod
    def flash(message, kill_line=False, **kwargs):
        Ansi.print(message, color=Ansi.MAGENTA, kill_line=kill_line, file=sys.stderr, **kwargs)
    @staticmethod
    def note(message, kill_line=False, **kwargs):
        Ansi.print(message, color=Ansi.WHITE, kill_line=kill_line, file=sys.stderr, **kwargs)
    @staticmethod
    def info(message, kill_line=False, **kwargs):
        Ansi.print(message, color=Ansi.GRAY, kill_line=kill_line, file=sys.stderr, **kwargs)
    @staticmethod
    def warning(message, kill_line=False, **kwargs):
        Ansi.print(message, color=Ansi.BRIGHT_YELLOW, kill_line=kill_line, file=sys.stderr, **kwargs)
    @staticmethod
    def error(message, kill_line=False, **kwargs):
        Ansi.print(message, color=Ansi.BRIGHT_RED, kill_line=kill_line, file=sys.stderr, **kwargs)
    @staticmethod
    def msgs_count():
        return Ansi.__msgs_count
    @staticmethod
    def kill_line():
        print("\r\033[")