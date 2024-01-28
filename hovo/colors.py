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
    HAWKES_BLUE = rgb('#D4E2FC')
    LIGHT_ROSE = rgb('#FFC5CB')
    LIGHTNING_YELLOW = rgb('#FCC01E')
    MOONRAKER = rgb('#D6CEF6')
    RED = rgb('#FF0000')
    WARM_RED = rgb('#FF3F00')

    RANDOM = {'red': random.random(), 'green': random.random(), 'blue': random.random()}

    ZERO_STAR = RED
    ONE_STAR = WARM_RED
    TWO_STARS = BEER
    THREE_STARS = LIGHTNING_YELLOW
    S3NS = HAWKES_BLUE
    JOINT = MOONRAKER
    GOOGLE = LIGHT_ROSE

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
    @staticmethod
    def print(message, color=RESET, **kwargs):
        print(color + message + Ansi.RESET, **kwargs)
    @staticmethod
    def flash(message, **kwargs):
        print(Ansi.MAGENTA + message + Ansi.RESET, file=sys.stderr, **kwargs)
    @staticmethod
    def note(message, **kwargs):
        print(Ansi.WHITE + message + Ansi.RESET, file=sys.stderr, **kwargs)
    @staticmethod
    def info(message, **kwargs):
        print(Ansi.GRAY + message + Ansi.RESET, file=sys.stderr, **kwargs)
    @staticmethod
    def warning(message, **kwargs):
        print(Ansi.BRIGHT_YELLOW + message + Ansi.RESET, file=sys.stderr, **kwargs)
    @staticmethod
    def error(message, **kwargs):
        print(Ansi.BRIGHT_RED + message + Ansi.RESET, file=sys.stderr, **kwargs)