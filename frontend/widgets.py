from typing import Any, Callable

from .config import DimensionConfig, StyleConfig, TagConfig
from .style import Color

from tkinter import Scrollbar, StringVar, Button, Frame, Label, font, OptionMenu
from tkinter.ttk import Combobox, Treeview, Style


class BaseConfigGenerator:
    @staticmethod
    def get(*, dimensions: DimensionConfig | None = None, style: StyleConfig | None = None) -> tuple[DimensionConfig, StyleConfig]:
        if dimensions is None:
            dimensions = DimensionConfig()
        if style is None:
            style = StyleConfig()
        return dimensions, style


class DinamicWidthHeightGetter:
    @staticmethod
    def get_width(text: str, font_config: Any, min_width: int = 0, max_width: int = 500) -> int:
        """
        Calcula a largura dinâmica baseada no tamanho do texto.
        
        Args:
            text: Texto do botão
            font_config: Configuração de fonte
            min_width: Largura mínima em pixels (padrão: 0)
            max_width: Largura máxima em pixels (padrão: 500)
        
        Returns:
            Largura calculada respeitando min e max width
        """
        try:
            tkinter_font = font.Font(font=font_config)
            text_width = tkinter_font.measure(text)
            # Adiciona padding (espaço extra ao redor do texto)
            padding = 20
            calculated_width = text_width + padding
        except Exception:
            # Se houver erro, usa width padrão do botão Tkinter
            calculated_width = 50
        
        # Respeita os limites de min e max width
        return max(min_width, min(calculated_width, max_width))

    @staticmethod
    def get_height(text: str, font_config: Any, min_height: int = 0, max_height: int = 100) -> int:
        """
        Calcula a altura dinâmica baseada no tamanho do texto.
        
        Args:
            text: Texto do botão
            font_config: Configuração de fonte
            min_height: Altura mínima em pixels (padrão: 0)
            max_height: Altura máxima em pixels (padrão: 100)
        
        Returns:
            Altura calculada respeitando min e max height
        """
        try:
            tkinter_font = font.Font(font=font_config)
            text_height = tkinter_font.metrics("linespace")
            padding = 20
            calculated_height = text_height + padding
        except Exception:
            calculated_height = 30
        return max(min_height, min(calculated_height, max_height))
    

class LabelGenerator:
    @staticmethod
    def generate(
        parent,
        *,
        dimensions: DimensionConfig,
        style: StyleConfig | None = None,
        text: str
    ) -> Label:

        dimensions, style = BaseConfigGenerator.get(dimensions=dimensions, style=style)

        label = Label(
            parent,
            text=text,
            background=style.background,  #type: ignore
            foreground=style.foreground,  #type: ignore
            font=style.font.value,        #type: ignore
        )

        label.place(
            relx=dimensions.relx,           #type: ignore
            rely=dimensions.rely,           #type: ignore
            relwidth=dimensions.relwidth,   #type: ignore
            relheight=dimensions.relheight  #type: ignore
        )

        label.configure(
            anchor=style.anchor,  #type: ignore
            justify=style.justify  #type: ignore
        )

        return label


class FrameGenerator:
    @staticmethod
    def generate(
        parent,
        *,
        dimensions: DimensionConfig,
        style: StyleConfig | None = None
    ) -> Frame:

        dimensions, style = BaseConfigGenerator.get(dimensions=dimensions, style=style)
                
        frame = Frame(
            parent, 
            background=style.background,                    #type: ignore
            bd=style.bd,                                    #type: ignore
            highlightbackground=style.highlightbackground,  #type: ignore
            highlightthickness=style.highlightthickness     #type: ignore
        )           
            
        frame.place(            
            relx=dimensions.relx,           #type: ignore
            rely=dimensions.rely,           #type: ignore
            relwidth=dimensions.relwidth,   #type: ignore
            relheight=dimensions.relheight  #type: ignore
        )
        return frame


class ButtonGenerator:
    @staticmethod
    def generate(
        parent,
        *,
        dimensions: DimensionConfig,
        style: StyleConfig | None = None,
        text: str,
        command: Callable[..., Any]
    ) -> Button:

        dimensions, style = BaseConfigGenerator.get(dimensions=dimensions, style=style)

        button = Button(
            parent, 
            text=text, 
            command=command, 
            background=style.background, #type: ignore 
            foreground=style.foreground, #type: ignore
            font=style.font.value        #type: ignore
        )  


        button.place(
            relx=dimensions.relx,           #type: ignore
            rely=dimensions.rely,           #type: ignore
            relwidth=dimensions.relwidth,   #type: ignore
            relheight=dimensions.relheight, #type: ignore
        )  

        return button


class OptionMenuGenerator:
    @staticmethod
    def generate(
        parent,
        *,
        dimensions: DimensionConfig,
        style: StyleConfig | None = None,
        text: str,
        options: list[str],
        command: Callable[..., Any]
    ) -> OptionMenu:

        dimensions, style = BaseConfigGenerator.get(dimensions=dimensions, style=style)

        variable = StringVar(value=text)
        option_menu = OptionMenu(parent, variable, *options, command=command)

        option_menu.configure(
            background=style.background, #type: ignore
            foreground=style.foreground, #type: ignore
            font=style.font.value,       #type: ignore
            anchor=style.anchor,         #type: ignore
            justify=style.justify,       #type: ignore
        )

        option_menu.place(
            relx=dimensions.relx,           #type: ignore
            rely=dimensions.rely,           #type: ignore
            relwidth=dimensions.relwidth,   #type: ignore
            relheight=dimensions.relheight  #type: ignore
        )

        return option_menu


class ComboboxGenerator:
    @staticmethod
    def generate(
        parent,
        *,
        dimensions: DimensionConfig,
        style: StyleConfig | None = None,
        text: str,
        values: list[str],
        command: Callable[..., Any]
    ) -> Combobox:

        dimensions, style = BaseConfigGenerator.get(dimensions=dimensions, style=style)

        combobox = Combobox(
            parent,
            values=values
        )

        combobox.configure(
            background=style.background, #type: ignore
            foreground=style.foreground, #type: ignore
            font=style.font.value        #type: ignore
        )

        combobox.place(
            relx=dimensions.relx,           #type: ignore
            rely=dimensions.rely,           #type: ignore
            relwidth=dimensions.relwidth,   #type: ignore
            relheight=dimensions.relheight  #type: ignore
        )

        combobox.bind("<<ComboboxSelected>>", command)

        return combobox


class TreeViewGenerator:
    @staticmethod
    def generate(
        parent,
        *,
        dimensions: DimensionConfig,
        heading_style: StyleConfig | None = None,
        body_style: StyleConfig | None = None,
        columns: list[tuple[str, int]],
        on_scroll: Callable[[], None] | None = None,
    ) -> Treeview:

        dimensions, heading_style = BaseConfigGenerator.get(dimensions=dimensions, style=heading_style)
        _, body_style = BaseConfigGenerator.get(dimensions=dimensions, style=body_style)

        column_names = [col[0] for col in columns]

        treeview = Treeview(
            parent,
            height=10,
            columns=column_names,
            show="headings",
            selectmode="browse"
        )

        tree_style = Style(treeview)
        tree_style.theme_use("clam")
        
        tree_style.configure(
            "Treeview.Heading",
            background=heading_style.background, #type: ignore
            foreground=heading_style.foreground, #type: ignore
            font=heading_style.font.value,       #type: ignore
            relief="flat"                #type: ignore
        )

        tree_style.configure(
            "Treeview",
            background=body_style.background, #type: ignore
            foreground=body_style.foreground, #type: ignore
            font=body_style.font.value,
            fieldbackground=body_style.background, #type: ignore
        )

        if body_style.row_height is not None:
            tree_style.configure("Treeview", rowheight=body_style.row_height)

        tree_style.map(
            "Treeview",
            background=[("selected", body_style.background)], #type: ignore
            foreground=[("selected", body_style.foreground)]  #type: ignore
        )

        treeview.place(
            relx=dimensions.relx,           #type: ignore
            rely=dimensions.rely,           #type: ignore
            relwidth=dimensions.relwidth,   #type: ignore
            relheight=dimensions.relheight  #type: ignore
        )


        scroll_bar = ScrollBarGenerator.generate(
            treeview,
            dimensions=DimensionConfig(relx=0.97, rely=0.0, relwidth=0.03, relheight=1.0),
            orient="vertical"
        )

        def update_scrollbar(first: str, last: str) -> None:
            scroll_bar.set(first, last)
            if on_scroll is not None:
                treeview.after_idle(on_scroll)

        scroll_bar.config(command=treeview.yview)
        treeview.config(yscrollcommand=update_scrollbar) #type: ignore
        scroll_bar.pack(side="right", fill="y")


        for col_name, col_width in columns:
            treeview.heading(col_name, text=col_name, anchor=body_style.anchor) #type: ignore
            treeview.column(
                col_name, 
                width=col_width, 
                minwidth=col_width,
                stretch=False, 
                anchor=body_style.anchor #type: ignore
            ) 


        treeview.tag_configure(TagConfig.ODD_ROW, background=Color.WHITE) #type: ignore
        treeview.tag_configure(TagConfig.EVEN_ROW, background=Color.LIGHT_GRAY) #type: ignore

        return treeview


class ScrollBarGenerator:
    @staticmethod
    def generate(
        parent,
        *,
        dimensions: DimensionConfig,
        style: StyleConfig | None = None,
        orient: str = "vertical"
    ) -> Scrollbar:

        dimensions, style = BaseConfigGenerator.get(dimensions=dimensions, style=style)

        scrollbar = Scrollbar(
            parent,
            orient=orient #type: ignore
        )

        scrollbar.configure(
            background=style.background, #type: ignore
            highlightbackground=style.background, #type: ignore
            highlightthickness=4, #type: ignore
            bd=4 #type: ignore
        )

        scrollbar.place(
            relx=dimensions.relx,           #type: ignore
            rely=dimensions.rely,           #type: ignore
            relwidth=dimensions.relwidth,   #type: ignore
            relheight=dimensions.relheight  #type: ignore
        )

        return scrollbar