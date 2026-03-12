import sys
import threading
from pathlib import Path

import keyboard
import pystray
from PIL import Image, ImageDraw

from keysound_audio import init_mixer, load_sound, play_sound, shutdown_mixer
from keysound_sounds import SoundFiles


def _data_base_dir() -> Path:
    base_dir = getattr(sys, '_MEIPASS', None)
    return Path(base_dir) if base_dir is not None else Path(__file__).resolve().parent


def _make_tray_image() -> Image.Image:
    """Создать простую иконку белой клавиши."""
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    outer_pad = 6
    outer_rect = (outer_pad, outer_pad, size - outer_pad, size - outer_pad)
    draw.rounded_rectangle(
        outer_rect,
        radius=10,
        fill=(245, 245, 245, 255),
        outline=(180, 180, 180, 255),
        width=2,
    )

    inner_pad = 10
    inner_rect = (inner_pad, inner_pad, size - inner_pad, size - inner_pad)
    draw.rounded_rectangle(
        inner_rect,
        radius=7,
        fill=(255, 255, 255, 255),
        outline=None,
    )

    return img


class SoundPlayer:
    """Проигрывает звуки клавиш с кешированием загруженных файлов."""

    def __init__(self, sound_files: SoundFiles) -> None:
        self._sound_files = sound_files
        self._lock = threading.Lock()
        self._cache: dict[Path, object] = {}

    def play_for_key(self, key_name: str) -> None:
        path = self._sound_files.resolve(key_name)
        if path is None:
            return

        with self._lock:
            sound = self._cache.get(path)
            if sound is None:
                sound = load_sound(path)
                self._cache[path] = sound

        play_sound(sound)


class KeySoundApp:
    """Основное приложение: иконка в трее и обработка клавиатуры."""

    def __init__(self) -> None:
        init_mixer()
        data_dir = _data_base_dir()
        sounds_dir = data_dir / 'sounds'

        self._player = SoundPlayer(SoundFiles(sounds_dir=sounds_dir))
        self._pressed: set[str] = set()
        self._key_count: int = 0

        self._icon = pystray.Icon(
            'keysound',
            _make_tray_image(),
            title=self._title,
            menu=pystray.Menu(pystray.MenuItem('Закрыть программу', self._quit)),
        )

    @property
    def _title(self) -> str:
        return f'Прожмакал клавиш: {self._key_count}'

    def _quit(self, icon: pystray.Icon) -> None:
        # Лёгкое уведомление в трее с итоговым числом нажатий.
        try:
            icon.notify(
                f'За время работы программы ты нажал: {self._key_count} клавиш',
                'KeySound',
            )
        except Exception:
            pass
        shutdown_mixer()
        icon.stop()

    def _on_keyboard_event(self, event: keyboard.KeyboardEvent) -> None:
        name = event.name
        if not name:
            return

        if event.event_type == keyboard.KEY_DOWN:
            if name in self._pressed:
                return
            self._pressed.add(name)
            self._key_count += 1
            self._icon.title = self._title
            self._player.play_for_key(name)
            return

        if event.event_type == keyboard.KEY_UP:
            self._pressed.discard(name)

    def run(self) -> int:
        keyboard.hook(self._on_keyboard_event)
        self._icon.run()
        return 0
