from .model import Especialidade
from .html_generator import HTMLGenerator

import webbrowser

class PDFGenerator:
    def __init__(self, especialidade: Especialidade) -> None:
        self.especialidade = especialidade

    def generate_pdf(self) -> None:
        output_path = HTMLGenerator(self.especialidade).generate_html()
        webbrowser.open(output_path.as_uri())