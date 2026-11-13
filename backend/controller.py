from typing import Optional

from .service import AreaService, EspecialidadeService
from .model import *
from .database import Database
from .reader import FileType


class AreaController:
    def __init__(self, reader_type: FileType, version: int | None = None, is_test: bool = False) -> None:
        db = Database(reader_type)
        if version is None:
            version = db.get_latest_version()
            if version == 0:
                version = db.save_new_version()
        data_file = db.get_version_file(version)
        self.reader_type = reader_type
        self.area_service = AreaService(reader_type, data_file, version, is_test=is_test) #type: ignore

    def update_version(self, version: int) -> None:
        db = Database(self.reader_type) #type: ignore
        data_file = db.get_version_file(version)
        self.area_service = AreaService(self.reader_type, data_file, version, is_test=self.area_service.is_test) #type: ignore

    def list_areas(self, sort_by: str = "codigo") -> list[Area]:
        return self.area_service.list_areas(sort_by=sort_by)

    def get_area_by_codigo(self, codigo: str) -> Area:
        return self.area_service.get_area_by_codigo(codigo)

    def add_area(self, *, nome: str, codigo: str) -> bool:
        area = Area(nome=nome, codigo=codigo) 
        return self.area_service.add_area(area) #type: ignore

    def update_area(self, *, codigo: str, new_nome: Optional[str] = None, new_codigo: Optional[str] = None) -> bool:
        area = self.get_area_by_codigo(codigo)
        new_nome = new_nome or area.nome
        new_codigo = new_codigo or area.codigo
        area = Area(nome=new_nome, codigo=new_codigo)
        return self.area_service.update_area(codigo, area) #type: ignore

    def delete_area(self, codigo: str) -> bool:
        return self.area_service.remove_area(codigo) #type: ignore



class EspecialidadeController:
    def __init__(self, reader_type: FileType, version: int | None = None, is_test: bool = False) -> None:
        self.reader_type = reader_type
        if version is None:
            version = Database(reader_type).get_latest_version() #type: ignore
        data_file = Database(reader_type).get_version_file(version) #type: ignore
        self.especialidade_service = EspecialidadeService(reader_type, data_file, version, is_test=is_test) #type: ignore


    def update_version(self, version: int) -> None:
        data_file = Database(self.reader_type).get_version_file(version) #type: ignore
        self.especialidade_service = EspecialidadeService(self.reader_type, data_file, version, is_test=self.especialidade_service.is_test) #type: ignore

    def list_especialidades(self, area: str, sort_by: str = "codigo") -> list[Especialidade]:
        return self.especialidade_service.list_especialidades(area, sort_by=sort_by)

    def get_especialidade(self, area: str, codigo: int) -> Especialidade | None:
        return self.especialidade_service.get_especialidade(area, codigo)


    def add_especialidade(self, body: dict) -> bool:
        try:
            especialidade = Especialidade.from_json(body)
            return self.especialidade_service.add_especialidade(especialidade.area, especialidade) #type: ignore
        except:
            return False


    def update_especialidade(self, *, area: str, codigo: int, body: dict) -> bool:
        try:
            especialidade = Especialidade.from_json(body)
            return self.especialidade_service.update_especialidade(area, codigo, especialidade) #type: ignore
        except:
            return False


    def add_questao(self, *, area: str, codigo: int, body: dict) -> bool:
        try:
            especialidade = self.get_especialidade(area, codigo)
            if especialidade is None:
                return False
            questao = (
                QuestaoResposta.from_json(body) if "numero_linhas" in body 
                else QuestaoGrid.from_json(body) if "linhas" in body and "colunas" in body 
                else QuestaoDesenho.from_json(body) if "dimensoes" in body 
                else QuestaoAlternativa.from_json(body)
            )
            return self.especialidade_service.update_especialidade_add_questao(area, codigo, questao) #type: ignore
        except:
            return False


    def update_questao(self, *, area: str, codigo: int, questao_id: int, body: dict) -> bool:
        
        try:
            especialidade = self.get_especialidade(area, codigo)
            if especialidade is None:
                return False
            questao = (
                QuestaoResposta.from_json(body) if "numero_linhas" in body 
                else QuestaoGrid.from_json(body) if "linhas" in body and "colunas" in body 
                else QuestaoDesenho.from_json(body) if "dimensoes" in body 
                else QuestaoAlternativa.from_json(body)
            )
            return self.especialidade_service.update_especialidade_update_questao(area, codigo, questao_id, questao) #type: ignore
        except:
            return False


    def delete_questao(self, *, area: str, codigo: int, questao_id: int) -> bool:
        return self.especialidade_service.update_especialidade_remove_questao(area, codigo, questao_id) #type: ignore

    def delete_especialidade(self, *, area: str, codigo: int) -> bool:
        return self.especialidade_service.remove_especialidade(area, codigo) #type: ignore