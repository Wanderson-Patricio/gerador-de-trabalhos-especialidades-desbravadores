from pathlib import Path

from .model import *
from .reader import reader_by_file_type, FileType
from .database import Database


####################################################################################
####################################################################################
####################################################################################
####################################################################################

class Service:
    def __init__(self, reader_type: FileType, data_file: str | Path, version: int, is_test: bool = False) -> None:
        self.reader = reader_by_file_type[reader_type]
        self.reader_type = reader_type
        self._data_file = data_file
        self._version = version
        self._is_test = is_test


class AreaService(Service):
    def __init__(self, reader_type: FileType, data_file: str | Path, version: int, is_test: bool = False) -> None:
        super().__init__(reader_type, data_file, version, is_test)
        self._instance_cache: dict[str, dict] = {}
    
    def _get_areas_data(self) -> dict:
        if self._instance_cache and not self._is_test:
            return self._instance_cache

        areas_data = self.reader(self._data_file).read()

        self._instance_cache = {area["codigo"]: area for area in areas_data.get("areas", [])}
        return self._instance_cache


    
    def list_areas(self, sort_by: str = "codigo") -> list[Area]:
        areas_data = self._get_areas_data()
        return [Area.from_json(area) for area in sorted(areas_data.values(), key=lambda x: x.get(sort_by))]


    
    def get_area_by_codigo(self, codigo: str) -> Area:
        areas_data = self._get_areas_data()
        area = areas_data.get(codigo)
        if area is None:
            raise ValueError(f"Area with codigo {codigo} not found")
        return Area.from_json(area)


    @Database.update_date   #type: ignore
    def add_area(self, area: Area) -> bool:
        self._get_areas_data()  # Ensure the cache is populated before adding a new area
        if area.codigo in self._instance_cache:
            raise ValueError(f"Area with codigo {area.codigo} already exists")

        data = area.to_json()
        try:
            self.reader(self._data_file).append("areas", data)
        except:
            return False
        self._instance_cache[area.codigo] = area.to_json()
        return True

    
    @Database.update_date   #type: ignore
    def update_area(self, codigo: str, area: Area) -> bool:
        if area.codigo != codigo and area.codigo in self._instance_cache:
            raise ValueError(f"Area with codigo {area.codigo} already exists")
        data = area.to_json()
        try:
            self.reader(self._data_file).update("areas", data, codigo=codigo)
        except:
            return False
        self._instance_cache.pop(codigo, None)
        self._instance_cache[area.codigo] = area.to_json()
        return True

    @Database.update_date   #type: ignore
    def remove_area(self, codigo: str) -> bool:
        try:
            self.reader(self._data_file).remove("areas", codigo=codigo)
        except:
            return False
        if codigo in self._instance_cache:
            self._instance_cache.pop(codigo, None)
        return True




####################################################################################
####################################################################################
####################################################################################
####################################################################################
class QuestaoService(Service):
    
    def get_tipo_questao(self, data: dict) -> type:
        if "numero_linhas" in data:
            return QuestaoResposta
        elif "linhas" in data and "colunas" in data:
            return QuestaoGrid
        elif "dimensoes" in data:
            return QuestaoDesenho
        return QuestaoAlternativa


    
    def generate_questoes(self, questoes_data: list[dict]) -> list[Questao]:
        questoes = []
        for data in questoes_data:
            tipo = self.get_tipo_questao(data)
            questoes.append(tipo.from_json(data))
        return questoes


####################################################################################
####################################################################################
####################################################################################
####################################################################################
class EspecialidadeService(Service):
    def __init__(self, reader_type: FileType, data_file: str | Path, version: int, is_test: bool = False) -> None:
        super().__init__(reader_type, data_file, version, is_test=is_test)
        self._instance_cache: dict[str, list[Especialidade]] = {}
    
    def get_especialidades(self, area: str) -> list[Especialidade]:
        if area in self._instance_cache and not self._is_test:
            return self._instance_cache[area]

        data = self.reader(self._data_file).read().get("especialidades", [])
        data = [e for e in data if e["area"] == area]
        especialidades = [Especialidade.from_json(e) for e in data]
        self._instance_cache[area] = especialidades
        return especialidades

    
    def list_especialidades(self, area: str, sort_by: str = "codigo") -> list[Especialidade]:
        return sorted(self.get_especialidades(area), key=lambda e: getattr(e, sort_by))


    
    def get_especialidade(self, area: str, codigo: int) -> Especialidade | None:
        especialidades = self.get_especialidades(area)
        for e in especialidades:
            if e.codigo == codigo:
                return e
        return None


    @Database.update_date   #type: ignore
    def add_especialidade(self, area: str, especialidade: Especialidade) -> bool:
        self.get_especialidades(area)  # Ensure the cache is populated before adding a new especialidade
        if self.get_especialidade(area, especialidade.codigo) is not None:
            return False

        try:
            self.reader(self._data_file).append("especialidades", especialidade.to_json())
        except:
            return False
        if area in self._instance_cache:
            self._instance_cache[area].append(especialidade)
        return True


    @Database.update_date   #type: ignore
    def update_especialidade(self, area: str, codigo: int, especialidade: Especialidade) -> bool:
        if self.get_especialidade(area, codigo) is None:
            return False

        if self.get_especialidade(area, especialidade.codigo) is not None and especialidade.codigo != codigo:
            return False
        
        try:
            self.reader(self._data_file).update("especialidades", data=especialidade.to_json(), area=area, codigo=codigo)
        except:
            return False
        
        if area in self._instance_cache:
            self._instance_cache[area] = [e for e in self._instance_cache[area] if e.codigo != codigo]
            self._instance_cache[area].append(especialidade)
        return True


    @Database.update_date   #type: ignore
    def update_especialidade_add_questao(self, area: str, codigo: int, questao: Questao) -> bool:
        especialidade = self.get_especialidade(area, codigo)
        if especialidade is None:
            return False
        especialidade.questoes.append(questao)
        return self.update_especialidade(area, codigo, especialidade) #type: ignore


    @Database.update_date   #type: ignore
    def update_especialidade_update_questao(self, area: str, codigo: int, questao_index: int, questao: Questao) -> bool:
        especialidade = self.get_especialidade(area, codigo)
        if especialidade is None:
            return False
        if 0 <= questao_index < len(especialidade.questoes):
            especialidade.questoes[questao_index] = questao
            return self.update_especialidade(area, codigo, especialidade) #type: ignore
        return False


    @Database.update_date   #type: ignore
    def update_especialidade_remove_questao(self, area: str, codigo: int, questao_index: int) -> bool:
        especialidade = self.get_especialidade(area, codigo)
        if especialidade is None:
            return False
        if 0 <= questao_index < len(especialidade.questoes):
            especialidade.questoes.pop(questao_index)
            return self.update_especialidade(area, codigo, especialidade) #type: ignore
        return False


    @Database.update_date   #type: ignore
    def remove_especialidade(self, area: str, codigo: int) -> bool:
        if self.get_especialidade(area, codigo) is None:
            return False
        try:
            self.reader(self._data_file).remove("especialidades", area=area, codigo=codigo)
        except:
            return False
        if area in self._instance_cache:
            self._instance_cache[area] = [e for e in self._instance_cache[area] if e.codigo != codigo]
        return True