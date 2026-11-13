from math import isfinite
from pathlib import Path

from .model import *


class LineGenerator:
    @staticmethod
    def generate_line(comprimento_cm: float = 10, transparente: bool = False) -> str:
        if not isfinite(comprimento_cm) or comprimento_cm <= 0:
            raise ValueError("O comprimento da linha deve ser um número positivo e finito.")
        return f"<span class='filler-line{'-transparent' if transparente else ''}' style='width: {comprimento_cm}cm;'></span>"
        


class QuestaoRespostaHTMLGenerator:
    def __init__(self, indice: int | str, questao: QuestaoResposta) -> None:
        self.indice = indice
        self.questao = questao

    def generate_html(self) -> str:
        return f"""
        <div class="questao-resposta">
            <p>{f"Questão {self.indice}".strip() if isinstance(self.indice, int) else self.indice}. {self.questao.texto}</p>
            {"".join([f"<p>{LineGenerator.generate_line(20)}</p>"] * self.questao.numero_linhas)}
            {"".join([f"<p>{LineGenerator.generate_line(20, transparente=True)}</p>"] * (self.questao.numero_linhas_transparentes or 0))}
        </div>
        """


class RectangleHTMLGenerator:
    def __init__(self, largura: float, altura: float) -> None:
        self.largura = largura
        self.altura = altura

    def generate_html(self) -> str:
        return f"<div class='rectangle' style='width: {self.largura}cm; height: {self.altura}cm;'></div>"

class QuestaoDesenhoHTMLGenerator:
    def __init__(self, indice: int | str, questao: QuestaoDesenho) -> None:
        self.indice = indice
        self.questao = questao

    def generate_html(self) -> str:
        return f"""
        <div class="questao-desenho">
            <p>{f"Questão {self.indice}".strip() if isinstance(self.indice, int) else self.indice}. {self.questao.texto}</p>
            <div class="center">
                {RectangleHTMLGenerator(self.questao.dimensoes.largura, self.questao.dimensoes.altura).generate_html()}
            </div>
            {"".join([f"<p>{LineGenerator.generate_line(20, transparente=True)}</p>"] * (self.questao.numero_linhas_transparentes or 0))}
        </div>
        """


class QuestaoGridHTMLGenerator:
    def __init__(self, indice: int | str, questao: QuestaoGrid) -> None:
        self.indice = indice
        self.questao = questao

    def generate_html(self) -> str:
        return f"""
        <div class="questao-grid">
            <p>{f"Questão {self.indice}".strip() if isinstance(self.indice, int) else self.indice}. {self.questao.texto}</p>
            <div class="center">
                <table>
                    {"".join([
                        f"<tr>{''.join([
                            f'<td>{RectangleHTMLGenerator(self.questao.dimensoes.largura, self.questao.dimensoes.altura).generate_html()}</td>' 
                        for _ in range(self.questao.colunas)])}</tr>" for _ in range(self.questao.linhas)
                    ])}
                </table>
            </div>
            {"".join([f"<p>{LineGenerator.generate_line(20, transparente=True)}</p>"] * (self.questao.numero_linhas_transparentes or 0))}
        </div>
        """


class QuestaoAlternativaHTMLGenerator:
    def __init__(self, indice: int | str, questao: QuestaoAlternativa) -> None:
        self.indice = indice
        self.questao = questao

    def generate_html(self) -> str:
        alternativas_html = ""
        for index, alternativa in enumerate(self.questao.alternativas):
            match alternativa:
                case QuestaoResposta():
                    alternativas_html += QuestaoRespostaHTMLGenerator(chr(97 + index), alternativa).generate_html()
                case QuestaoDesenho():
                    alternativas_html += QuestaoDesenhoHTMLGenerator(chr(97 + index), alternativa).generate_html()
                case QuestaoGrid():
                    alternativas_html += QuestaoGridHTMLGenerator(chr(97 + index), alternativa).generate_html()
                case _:
                    alternativas_html += ""
        
        html = f"""
        <div class="questao-alternativa">
            <p>{f"Questão {self.indice}".strip() if isinstance(self.indice, int) else self.indice}. {self.questao.texto}</p>
            <ul>
                {alternativas_html}
            </ul>
            {"".join([f"<p>{LineGenerator.generate_line(20, transparente=True)}</p>"] * (self.questao.numero_linhas_transparentes or 0))}
        </div>
        """
        return html







class HTMLGenerator:
    def __init__(self, especialidade: Especialidade):
        self.especialidade = especialidade

    def generate_title(self) -> str:
        return f"<h1 class='mb-4 text-center'>{self.especialidade.nome}</h1>"

    

    def generate_info_filler(self) -> str:
        date_line_width = 0.74
        return f"""
        <div class="border-bottom mb-3">
            <p>Nome: {LineGenerator.generate_line(13.1)} Data: {LineGenerator.generate_line(date_line_width)} /{LineGenerator.generate_line(date_line_width)} /{LineGenerator.generate_line(date_line_width * 2)}</p>
            <p>Clube: {LineGenerator.generate_line(17.9)}</p>
            <p>Unidade: {LineGenerator.generate_line(17.4)}</p>
        </div>
        """


    def generate_questoes_respostas(self) -> str:
        questoes_html = ""
        
        for index, questao in enumerate(self.especialidade.questoes):
            match questao:
                case QuestaoResposta():
                    texto_html = QuestaoRespostaHTMLGenerator(index + 1, questao).generate_html()
                case QuestaoDesenho():
                    texto_html = QuestaoDesenhoHTMLGenerator(index + 1, questao).generate_html()
                case QuestaoGrid():
                    texto_html = QuestaoGridHTMLGenerator(index + 1, questao).generate_html()
                case QuestaoAlternativa():
                    texto_html = QuestaoAlternativaHTMLGenerator(index + 1, questao).generate_html()
                case _:
                    texto_html = ""

            questoes_html += texto_html
        
        return questoes_html
    

    def generate_body(self) -> str:
        body_content = "".join([
            self.generate_title(),
            self.generate_info_filler(),
            self.generate_questoes_respostas()
        ])
        return body_content

    def generate_html(self) -> Path:

        output_file = Path(__file__).parent / "template" / "output.html"

        output_file.parent.mkdir(parents=True, exist_ok=True)
        html = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link rel="stylesheet" href="style.css">
            <title>{self.especialidade.nome}</title>
        </head>
        <body>
            <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
                <div class="container-fluid">
                    <span class="navbar-brand mb-0 h1">Gerador de Especialidades - Desbravadores</span>
                </div>
            </nav>

            <div style="margin-top: 20px;" class="d-flex gap-2 justify-content-center no-print">
                <button class="box-shadow btn btn-primary" onclick="window.print()">
                    <i class="bi bi-printer"></i> Imprimir
                </button>
            </div>

            <main class="container mt-5">
                <div class="row">
                    <div class="col-lg-8 mx-auto">
                        <div class="card shadow-sm mb-4">
                            <div class="card-body">
                                {self.generate_body()}
                            </div>
                        </div>
                    </div>
                </div>
            </main>

            <footer class="bg-dark text-light text-center py-4 mt-5 no-print">
                <p class="mb-0">&copy; 2026 Wanderson Patricio</p>
            </footer>

            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        """

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)

        output_path = output_file

        return output_path