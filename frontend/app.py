from backend.database import Database
from backend.controller import AreaController, EspecialidadeController
from backend.pdf_generator import PDFGenerator

from .style import Color, Font, AnchorPosition, JustifyPosition
from .config import DimensionConfig, StyleConfig, TagConfig
from .widgets import *

from typing import Any
from tkinter import Button, Tk



class App(Tk):
    def __init__(self, db: Database, is_test: bool = False) -> None:
        self.is_test = is_test

        self._db = db
        self._db_version = self._db.get_latest_version()

        self._selected_area = None
        self._especialidades = None

        self._sort_by: str = "nome"
        self._sort_reverse: bool = False

        self._area_controller = AreaController(db.extension, self._db_version, is_test=self.is_test)
        self._especialidade_controller = EspecialidadeController(db.extension, self._db_version, is_test=self.is_test)

        super().__init__()
        self.configure_app()
        

    def configure_app(self) -> None:
        self.title("Gerador de Especialidades")
        self.configure(
            background=Color.APP_BACKGROUND
        )
        self.geometry("800x600")
        self.resizable(False, False)


        self.option_frame = FrameGenerator.generate(
            self,
            dimensions=DimensionConfig(relx=0.0, rely=0.0, relwidth=1.0, relheight=0.2),
            style=StyleConfig(background=Color.APP_BACKGROUND)
        )


        self.title_label = LabelGenerator.generate(
            self.option_frame,
            dimensions=DimensionConfig(relwidth=1.0),
            style=StyleConfig(background=Color.APP_BACKGROUND, foreground=Color.YELLOW, font=Font.TITLE_LARGE),
            text="Gerador de Especialidades"
        )

        self.db_version_label = LabelGenerator.generate(
            self.option_frame,
            dimensions=DimensionConfig(relx=0.0, rely=0.3, relwidth=0.5, relheight=0.3),
            style=StyleConfig(font=Font.SUBTITLE_LARGE, foreground=Color.YELLOW, anchor=AnchorPosition.W, justify=JustifyPosition.LEFT),
            text=f"Versão do Banco de Dados:"
        )

        self.db_version_selector = OptionMenuGenerator.generate(
            self.option_frame,
            dimensions=DimensionConfig(relx=0.5, rely=0.3, relwidth=0.15, relheight=0.3),
            style=StyleConfig(
                background=Color.OPTION_MENU_COLOR, 
                highlightbackground=Color.APP_BACKGROUND, 
                highlightthickness=4, 
                bd=4, 
                font=Font.SUBTITLE_SMALL
            ),
            text=f"Versão {self._db_version}",
            options=self.get_all_versions(),
            command=lambda value: self.set_db_version(int(value.split(" ")[1]))
        )

        self.area_label = LabelGenerator.generate(
            self.option_frame,
            dimensions=DimensionConfig(relx=0.0, rely=0.65, relwidth=0.5, relheight=0.3),
            style=StyleConfig(font=Font.SUBTITLE_LARGE, foreground=Color.YELLOW, anchor=AnchorPosition.W, justify=JustifyPosition.LEFT),
            text=f"Área:"
        )

        self.area_selector = OptionMenuGenerator.generate(
            self.option_frame,
            dimensions=DimensionConfig(relx=0.5, rely=0.65, relwidth=0.48, relheight=0.3),
            style=StyleConfig(
                background=Color.OPTION_MENU_COLOR, 
                highlightbackground=Color.APP_BACKGROUND, 
                highlightthickness=4, 
                bd=4, 
                font=Font.SUBTITLE_SMALL,
                anchor=AnchorPosition.W,
                justify=JustifyPosition.LEFT
            ),
            text="Selecione a Área de Especialidades",
            options=[f"{area.nome} - {area.codigo}" for area in self.area_controller.list_areas()],
            command=lambda value: self.set_selected_area(value)
        )


        self.especialidade_frame = FrameGenerator.generate(
            self,
            dimensions=DimensionConfig(relx=0.0, rely=0.2, relwidth=1.0, relheight=0.8),
            style=StyleConfig(background=Color.LIST_BACKGROUND)
        )


        self._pdf_buttons: dict[str, Button] = {}
        self.especialidade_treeview = TreeViewGenerator.generate(
            self.especialidade_frame,
            dimensions=DimensionConfig(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0),
            heading_style=StyleConfig(font=Font.SUBTITLE_MEDIUM, background=Color.OPTION_MENU_COLOR, foreground=Color.GRAPHITE),
            body_style=StyleConfig(font=Font.SUBTITLE_MEDIUM, background=Color.WHITE, foreground=Color.GRAPHITE, row_height=30),
            columns=[("Código", 100), ("Nome", 580), ("Gerar PDF", 100)],
            on_scroll=self._position_pdf_buttons,
        )
        self.especialidade_treeview.bind(
            "<Configure>", self._schedule_pdf_button_positions, add="+"
        )
        self.especialidade_treeview.bind(
            "<B1-Motion>", self._schedule_pdf_button_positions, add="+"
        )
        self.especialidade_treeview.bind(
            "<Button-1>", self._on_treeview_header_click, add="+"
        )
        self.especialidade_treeview.bind(
            "<Motion>", self._on_treeview_motion, add="+"
        )
        
        self._update_header_indicators()


    @property
    def db(self) -> Database:
        return self._db

    @db.setter
    def db(self, value: Any) -> None:
        raise AttributeError("Cannot modify the database instance.")

    @property
    def db_version(self) -> int:
        return self._db_version

    @db_version.setter
    def db_version(self, value: int) -> None:
        raise AttributeError("Cannot modify the database version directly. Use the set_db_version method.")

    @property
    def area_controller(self) -> AreaController:
        return self._area_controller

    @area_controller.setter
    def area_controller(self, value: Any) -> None:
        raise AttributeError("Cannot modify the area controller instance without using the proper method (set_db_version).")

    @property
    def especialidade_controller(self) -> EspecialidadeController:
        return self._especialidade_controller

    @especialidade_controller.setter
    def especialidade_controller(self, value: Any) -> None:
        raise AttributeError("Cannot modify the especialidade controller instance without using the proper method (set_db_version).")

    def get_all_versions(self) -> list[str]:
        latest_version = self._db.get_latest_version()
        return [f"Versão {i}" for i in range(1, latest_version + 1)]

    def set_db_version(self, version: int) -> None:
        self._db_version = version
        self._area_controller.update_version(version)
        self._especialidade_controller.update_version(version)

    def set_selected_area(self, value: str) -> None:
        self._selected_area = next((area for area in self._area_controller.list_areas() if f"{area.nome} - {area.codigo}" == value), None)
        if self._selected_area is not None:
            self.set_especialidades(self._selected_area.codigo)


    def set_especialidades(self, codigo: str) -> None:
        especialidades = self._especialidade_controller.list_especialidades(codigo, sort_by=self._sort_by)
        
        if self._sort_reverse:
            especialidades = list(reversed(especialidades))
        
        self._especialidades = especialidades

        for button in self._pdf_buttons.values():
            button.destroy()
        self._pdf_buttons.clear()

        for item in self.especialidade_treeview.get_children():
            self.especialidade_treeview.delete(item)

        for i, especialidade in enumerate(self._especialidades):
            tag = TagConfig.ODD_ROW if i % 2 == 0 else TagConfig.EVEN_ROW
            item = self.especialidade_treeview.insert(
                "",
                "end",
                values=(especialidade.codigo, especialidade.nome),
                tags=(tag,)
            )

            button = Button(
                self.especialidade_treeview,
                text="Gerar PDF",
                command=lambda e=especialidade: PDFGenerator(e).generate_pdf(),
            )

            button.configure(
                background=Color.BUTTON_COLOR,
                foreground=Color.WHITE,
                font=Font.SUBTITLE_MEDIUM.value
            )

            button.bind(
                "<MouseWheel>",
                lambda event: self.especialidade_treeview.event_generate(
                    "<MouseWheel>", delta=event.delta
                ),
            )
            button.bind(
                "<Enter>",
                lambda event, btn=button: self._on_button_enter(btn)
            )
            button.bind(
                "<Leave>",
                lambda event, btn=button: self._on_button_leave(btn)
            )
            self._pdf_buttons[item] = button

        self.especialidade_treeview.after_idle(self._position_pdf_buttons)

    def _schedule_pdf_button_positions(self, event: Any) -> None:
        self.especialidade_treeview.after_idle(self._position_pdf_buttons)

    def _position_pdf_buttons(self) -> None:
        for item, button in self._pdf_buttons.items():
            bounds = self.especialidade_treeview.bbox(item, "Gerar PDF")
            if bounds:
                x, y, width, height = bounds
                button.place(x=x + 2, y=y + 1, width=width - 4, height=height - 2)
            else:
                button.place_forget()

    def _on_treeview_header_click(self, event: Any) -> None:
        region = self.especialidade_treeview.identify_region(event.x, event.y)
        if region != "heading":
            return

        col = self.especialidade_treeview.identify_column(event.x)
        col_index = int(col[1:]) - 1
        
        columns = ["Código", "Nome", "Gerar PDF"]
        if col_index >= len(columns):
            return

        column_name = columns[col_index]
        
        if column_name == "Gerar PDF":
            return

        sort_key = "codigo" if column_name == "Código" else "nome"
        
        if self._sort_by == sort_key:
            self._sort_reverse = not self._sort_reverse
        else:
            self._sort_by = sort_key
            self._sort_reverse = False

        self._update_header_indicators()
        if self._selected_area is not None:
            self.set_especialidades(self._selected_area.codigo)

    def _update_header_indicators(self) -> None:
        columns = ["Código", "Nome", "Gerar PDF"]
        for col_name in columns:
            if col_name == "Gerar PDF":
                self.especialidade_treeview.heading(col_name, text=col_name)
            elif col_name == "Código" and self._sort_by == "codigo":
                indicator = " ↓" if self._sort_reverse else " ↑"
                self.especialidade_treeview.heading("Código", text=f"Código{indicator}")
            elif col_name == "Nome" and self._sort_by == "nome":
                indicator = " ↓" if self._sort_reverse else " ↑"
                self.especialidade_treeview.heading("Nome", text=f"Nome{indicator}")
            else:
                self.especialidade_treeview.heading(col_name, text=col_name)

    def _on_treeview_motion(self, event: Any) -> None:
        region = self.especialidade_treeview.identify_region(event.x, event.y)
        if region == "heading":
            col = self.especialidade_treeview.identify_column(event.x)
            col_index = int(col[1:]) - 1
            columns = ["Código", "Nome", "Gerar PDF"]
            if col_index < len(columns) and columns[col_index] != "Gerar PDF":
                self.especialidade_treeview.config(cursor="hand2")
            else:
                self.especialidade_treeview.config(cursor="arrow")
        else:
            self.especialidade_treeview.config(cursor="arrow")

    def _on_button_enter(self, button: Button) -> None:
        button.config(background=Color.BUTTON_HOVER_COLOR, foreground=Color.GRAPHITE, cursor="hand2")

    def _on_button_leave(self, button: Button) -> None:
        button.config(background=Color.BUTTON_COLOR, foreground=Color.WHITE, cursor="arrow")

    