import os
import requests

from backend.reader import YAMLReader

class GitHubDBUpdater:

    def __init__(self, usuario: str, repositorio: str, pasta: str):
        self.usuario = usuario
        self.repositorio = repositorio
        self.pasta = pasta
        self.base_url = (
            f"https://api.github.com/repos/{usuario}/{repositorio}/contents"
        )

    def get_remote_versions(self) -> list[str]:
        """Busca as pastas de versão disponíveis no repositório remoto."""
        response = requests.get(f"{self.base_url}/{self.pasta}")
        if response.status_code == 200:
            return [item["name"] for item in response.json()]
        print(f"Erro ao acessar o repositório remoto: {response.status_code}")
        return []

    def get_remote_files(self, version: str) -> list[dict[str, str]]:
        """Busca a lista de arquivos de uma versão específica."""
        response = requests.get(f"{self.base_url}/{self.pasta}/{version}")
        if response.status_code == 200:
            return [
                {"name": item["name"], "download_url": item["download_url"]}
                for item in response.json()
            ]
        print(f"Erro ao buscar arquivos da versão {version}: {response.status_code}")
        return []

    def get_local_versions(self) -> list[str]:
        """Retorna as versões já existentes na pasta local."""
        if not os.path.exists(self.pasta):
            os.makedirs(self.pasta, exist_ok=True)
            return []
        return os.listdir(self.pasta)

    def is_outdated(self) -> bool:
        return self.get_remote_versions() != self.get_local_versions()

    def sync(self) -> None:
        """Executa o processo completo de verificação e download das novas versões."""
        print("Analisando versões disponíveis...")
        remote_versions = self.get_remote_versions()

        if not remote_versions:
            print(
                "O repositório remoto está vazio ou inacessível. Entre em contato com"
                " o desenvolvedor."
            )
            return

        local_versions = self.get_local_versions()
        missing_versions = set(remote_versions) - set(local_versions)

        if not missing_versions:
            print("Repositório local já está atualizado.")
            return

        print(f"Versões novas encontradas: {', '.join(missing_versions)}")
        print("Atualizando versões...")

        for version in missing_versions:
            version_dir = os.path.join(self.pasta, version)
            os.makedirs(version_dir, exist_ok=True)
            print(f"Baixando versão {version}...")

            files = self.get_remote_files(version)
            for file in files:
                res = requests.get(file["download_url"])
                if res.status_code == 200:
                    file_path = os.path.join(version_dir, file["name"])
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(res.text)
                else:
                    print(
                        f"Erro ao baixar o arquivo '{file['name']}' da versão {version}."
                    )
                    return

        print("Repositório atualizado com sucesso!")


def default_updater() -> GitHubDBUpdater:
    properties = YAMLReader("properties.yaml").read().get("remote_repository", {}) #type: ignore
    updater = GitHubDBUpdater(
        properties.get("user"),
        properties.get("repository_name"),
        properties.get("folder")
    )
    return updater



if __name__ == "__main__":
    updater = default_updater()
    updater.sync()
    input("Pressione Enter para sair...")