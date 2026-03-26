import json
import os
from datetime import date, timedelta
from pathlib import Path


def stats_file_path() -> Path:
    """Путь к JSON со статистикой: %APPDATA%\\KeySound\\stats.json.

    Не каталог рядом с exe и не _MEIPASS: после --onefile туда писать нельзя / данные пропадут.
    """
    appdata = os.environ.get('APPDATA')
    if not appdata:
        return Path.home() / 'KeySound' / 'stats.json'
    return Path(appdata) / 'KeySound' / 'stats.json'


class KeyStats:
    """Счётчики за день и за всё время; хранятся в JSON."""

    def __init__(self) -> None:
        self.total: int = 0
        self._daily: dict[str, int] = {}

    def load(self) -> None:
        path = stats_file_path()
        if not path.is_file():
            return
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, OSError):
            return
        self.total = int(data.get('total', 0))
        raw = data.get('daily', {})
        self._daily = {}
        for k, v in raw.items():
            try:
                self._daily[str(k)] = int(v)
            except (TypeError, ValueError):
                continue

    def save(self) -> None:
        path = stats_file_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {'total': self.total, 'daily': self._daily}
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )

    def record_keypress(self) -> None:
        self.total += 1
        day = date.today().isoformat()
        self._daily[day] = self._daily.get(day, 0) + 1

    def today_count(self) -> int:
        return self._daily.get(date.today().isoformat(), 0)

    def yesterday_count(self) -> int:
        y = (date.today() - timedelta(days=1)).isoformat()
        return self._daily.get(y, 0)
