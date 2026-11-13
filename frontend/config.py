from dataclasses import dataclass
from enum import StrEnum

from .style import Font, JustifyPosition, AnchorPosition, Color


@dataclass
class DimensionConfig:
    relx: float | None = None
    rely: float | None = None
    relwidth: float | None = None
    maxwidth: float | None = None
    minwidth: float | None = None
    maxheight: float | None = None
    minheight: float | None = None
    relheight: float | None = None
    padx: float | None = None
    pady: float | None = None


@dataclass
class StyleConfig:
    background: Color = Color.APP_BACKGROUND
    foreground: Color = Color.BLACK
    highlightbackground: Color = Color.APP_BACKGROUND
    highlightthickness: int | None = None
    bd: int | None = None
    font: Font = Font.DEFAULT_12
    anchor: AnchorPosition = AnchorPosition.CENTER
    justify: JustifyPosition = JustifyPosition.CENTER
    row_height: float | None = None
    row_width: float | None = None


class TagConfig(StrEnum):
    ODD_ROW = "oddrow"
    EVEN_ROW = "evenrow"