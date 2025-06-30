import requests
import time
from typing import Optional

from app.config.config import settings
from app.config.logger import logger


class MFCParserClient:
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or settings.MFC_PARSER_URL

    def search_chroma(self, query: str) -> list[dict]:
        response = requests.get(
            f"{self.base_url}/search_chroma",
            params={"q": query}
        )
        response.raise_for_status()
        return response.json()

    def get_situation_by_id(self, situation_id: str) -> dict:
        response = requests.get(f"{self.base_url}/get_situation_by_id/{situation_id}")
        response.raise_for_status()
        return response.json()

    def update_mfc_db(self):
        return requests.post(f"{self.base_url}/update_mfc_db").json()

    def update_chromadb(self):
        return requests.post(f"{self.base_url}/update_chromadb").json()

    def is_pg_filled(self) -> bool:
        r = requests.get(f"{self.base_url}/is_pg_filled")
        r.raise_for_status()
        return r.json().get("filled", False)

    def is_chroma_filled(self) -> bool:
        r = requests.get(f"{self.base_url}/is_chroma_filled")
        r.raise_for_status()
        return r.json().get("filled", False)

    def is_updating(self) -> bool:
        r = requests.get(f"{self.base_url}/is_updating")
        r.raise_for_status()
        return r.json().get("status") == "Update in progress"

    def is_chromadb_updating(self) -> bool:
        r = requests.get(f"{self.base_url}/is_chromadb_updating")
        r.raise_for_status()
        return r.json().get("status") == "Chromadb update in progress"

    def wait_until_ready(self, timeout=500, interval=10):
        start_time = time.time()

        if not self.is_pg_filled():
            logger.info("Postgres пуст. Запускаем парсинг...")
            self.update_mfc_db()
        else:
            logger.info("Данные спаршены с сайта МФЦ")

        while self.is_updating():
            logger.info("Ждём окончания парсинга...")
            time.sleep(interval)
            if time.time() - start_time > timeout:
                raise TimeoutError("Парсинг занял слишком много времени")

        if not self.is_chroma_filled():
            logger.info("ChromaDB пуста. Запускаем обновление...")
            self.update_chromadb()

        while self.is_chromadb_updating():
            logger.info("Ждём окончания обновления ChromaDB...")
            time.sleep(interval)
            if time.time() - start_time > timeout:
                raise TimeoutError("Обновление ChromaDB заняло слишком много времени")

        logger.info("Все данные готовы.")
