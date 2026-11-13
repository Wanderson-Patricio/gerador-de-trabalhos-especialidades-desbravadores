from dataclasses import dataclass
from typing import Union
from dataclasses import field

@dataclass
class Area:
    nome: str
    codigo: str

    def __post_init__(self) -> None:
        if not self.nome or self.nome.strip() == "":
            raise ValueError("O nome da área não pode ser vazio.")
        if not self.codigo or self.codigo.strip() == "" or len(self.codigo) != 2:
            raise ValueError("O código da área não pode ser vazio e deve ter exatamente 2 caracteres.")

    @classmethod
    def from_json(cls, data: dict) -> "Area":
        return cls(
            nome=data["nome"],
            codigo=data["codigo"]
        )

    def to_json(self) -> dict:
        return {
            "nome": self.nome,
            "codigo": self.codigo
        }


@dataclass
class QuestaoResposta:
    texto: str
    numero_linhas: int
    numero_linhas_transparentes: int | None = None

    @classmethod
    def from_json(cls, data: dict) -> "QuestaoResposta":
        return cls(
            texto=data["texto"],
            numero_linhas=data["numero_linhas"],
            numero_linhas_transparentes=data.get("numero_linhas_transparentes")
        )

    def to_json(self) -> dict:
        return {
            "texto": self.texto,
            "numero_linhas": self.numero_linhas,
            "numero_linhas_transparentes": self.numero_linhas_transparentes
        }


@dataclass
class Dimensoes:
    largura: float
    altura: float

    @classmethod
    def from_json(cls, data: dict) -> "Dimensoes":
        return cls(
            largura=data["largura"],
            altura=data["altura"]
        )

    def to_json(self) -> dict:
        return {
            "largura": self.largura,
            "altura": self.altura
        }

@dataclass
class QuestaoDesenho:
    texto: str
    dimensoes: Dimensoes
    numero_linhas_transparentes: int | None = None

    @classmethod
    def from_json(cls, data: dict) -> "QuestaoDesenho":
        return cls(
            texto=data["texto"],
            dimensoes=Dimensoes.from_json(data["dimensoes"]),
            numero_linhas_transparentes=data.get("numero_linhas_transparentes")
        )

    def to_json(self) -> dict:
        return {
            "texto": self.texto,
            "dimensoes": self.dimensoes.to_json(),
            "numero_linhas_transparentes": self.numero_linhas_transparentes
        }


@dataclass
class QuestaoGrid:
    texto: str
    linhas: int
    colunas: int
    dimensoes: Dimensoes
    numero_linhas_transparentes: int | None = None

    @classmethod
    def from_json(cls, data: dict) -> "QuestaoGrid":
        return cls(
            texto=data["texto"],
            linhas=data["linhas"],
            colunas=data["colunas"],
            dimensoes=Dimensoes.from_json(data["dimensoes"]),
            numero_linhas_transparentes=data.get("numero_linhas_transparentes")
        )

    def to_json(self) -> dict:
        return {
            "texto": self.texto,
            "linhas": self.linhas,
            "colunas": self.colunas,
            "dimensoes": self.dimensoes.to_json(),
            "numero_linhas_transparentes": self.numero_linhas_transparentes
        }

type QuestaoParaAlternativa = Union[QuestaoResposta, QuestaoDesenho, QuestaoGrid]


@dataclass
class QuestaoAlternativa:
    texto: str
    alternativas: list[QuestaoParaAlternativa] = field(default_factory=list)
    numero_linhas_transparentes: int | None = None

    @classmethod
    def from_json(cls, data: dict) -> "QuestaoAlternativa":
        return cls(
            texto=data["texto"],
            alternativas=[
                QuestaoResposta.from_json(a)
                if "numero_linhas" in a 
                else QuestaoGrid.from_json(a) if "linhas" in a and "colunas" in a
                else QuestaoDesenho.from_json(a) for a in data.get("alternativas", [])
            ],
            numero_linhas_transparentes=data.get("numero_linhas_transparentes")
        )

    def to_json(self) -> dict:
        return {
            "texto": self.texto,
            "alternativas": [a.to_json() for a in self.alternativas],
            "numero_linhas_transparentes": self.numero_linhas_transparentes
        }



type Questao = Union[QuestaoResposta, QuestaoAlternativa, QuestaoDesenho, QuestaoGrid]


@dataclass
class Especialidade:
    nome: str
    area: str
    codigo: int

    questoes: list[Questao] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.nome or self.nome.strip() == "":
            raise ValueError("O nome da especialidade não pode ser vazio.")
        if not isinstance(self.area, str):
            raise ValueError("A área deve ser uma string.")
        if not isinstance(self.codigo, int) or self.codigo < 1:
            raise ValueError("O número da especialidade deve ser um número inteiro maior ou igual a 1.")

    @classmethod
    def from_json(cls, data: dict) -> "Especialidade":
        return cls(
            nome=data["nome"],
            area=data["area"],
            codigo=data["codigo"],
            questoes=[
                QuestaoResposta.from_json(q)
                if "numero_linhas" in q 
                else QuestaoGrid.from_json(q) if "linhas" in q and "colunas" in q
                else QuestaoDesenho.from_json(q) if "dimensoes" in q 
                else QuestaoAlternativa.from_json(q) for q in data.get("questoes", [])
            ]
        )

    def to_json(self) -> dict:
        return {
            "nome": self.nome,
            "area": self.area,
            "codigo": self.codigo,
            "questoes": [q.to_json() for q in self.questoes]
        }