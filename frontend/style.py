from enum import StrEnum, Enum

class Color(StrEnum):
    APP_BACKGROUND = "#034C8C"
    LIST_BACKGROUND = "#89B8E0"
    OPTION_MENU_COLOR = "#BACEDB"
    BUTTON_COLOR = "#1A1A1A"
    BUTTON_HOVER_COLOR = "#1DF3F3"
    RED = "#FF0000"
    YELLOW = "#F2B705"
    GOLD = "#967001"
    ORANGE = "#F28705"
    BLACK = "#0D0D0D"
    WHITE = "#F0F0F0"
    GRAY = "#808080"
    LIGHT_GRAY = "#D3D3D3"
    GRAPHITE = "#1A1A1A"


class FontStyle(StrEnum):
    BOLD = "bold"
    ITALIC = "italic"
    UNDERLINE = "underline"
    OVERSTRIKE = "overstrike"
    BOLD_ITALIC = "bold italic"
    BOLD_UNDERLINE = "bold underline"
    BOLD_OVERSTRIKE = "bold overstrike"
    ITALIC_UNDERLINE = "italic underline"
    ITALIC_OVERSTRIKE = "italic overstrike"


class Font(Enum):
    DEFAULT_8 = ("Arial", 8)
    DEFAULT_9 = ("Arial", 9)
    DEFAULT_10 = ("Arial", 10)
    DEFAULT_11 = ("Arial", 11)
    DEFAULT_12 = ("Arial", 12)
    DEFAULT_13 = ("Arial", 13)
    DEFAULT_14 = ("Arial", 14)
    DEFAULT_15 = ("Arial", 15)
    DEFAULT_16 = ("Arial", 16)

    TITLE_SMALL = ("Helvetica", 12, FontStyle.BOLD_ITALIC)
    TITLE_MEDIUM = ("Helvetica", 14, FontStyle.BOLD_ITALIC)
    TITLE_LARGE = ("Helvetica", 16, FontStyle.BOLD_ITALIC)

    SUBTITLE_SMALL = ("Helvetica", 8, FontStyle.BOLD)
    SUBTITLE_MEDIUM = ("Helvetica", 10, FontStyle.BOLD)
    SUBTITLE_LARGE = ("Helvetica", 12, FontStyle.BOLD)


class AnchorPosition(StrEnum):
    NW = "nw"
    N = "n"
    NE = "ne"
    W = "w"
    CENTER = "center"
    E = "e"
    SW = "sw"
    S = "s"
    SE = "se"


class JustifyPosition(StrEnum):
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"