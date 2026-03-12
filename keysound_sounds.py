from dataclasses import dataclass
from pathlib import Path

KEY_TO_SOUND: dict[str, str] = {
    'a': 'a',
    'b': 'b',
    'c': 'c',
    'd': 'd',
    'e': '3e',
    'f': 'f',
    'g': 'g',
    'h': 'h',
    'i': '8i',
    'j': 'j',
    'k': 'k',
    'l': 'l',
    'm': 'm',
    'n': 'n',
    'o': '-[9o',
    'p': 'p',
    'q': '8i',
    'r': '45rt',
    's': 's',
    't': '45rt',
    'u': '7u',
    'v': 'v',
    'w': '2w',
    'x': 'x',
    'y': '6y',
    'z': 'z',
    '0': ']=0',
    '1': '8i',
    '2': '2w',
    '3': '3e',
    '4': '45rt',
    '5': '45rt',
    '6': '6y',
    '7': '7u',
    '8': '8i',
    '9': '-[9o',
    '`': '8i',
    '-': '-[9o',
    '=': ']=0',
    '[': '-[9o',
    ']': ']=0',
    '\\': ']=0',
    ';': 'k',
    "'": 'l',
    ',': 'b',
    '.': 'n',
    '/': 'm',
    'space': 'space',
    'enter': 'downentershiftlshiftrupwin',
    'tab': 'alt_rlcapsctlr_lrtablr',
    'backspace': 'esc_backspace',
    'shift': 'downentershiftlshiftrupwin',
    'shift left': 'downentershiftlshiftrupwin',
    'shift right': 'downentershiftlshiftrupwin',
    'ctrl': 'alt_rlcapsctlr_lrtablr',
    'ctrl left': 'alt_rlcapsctlr_lrtablr',
    'ctrl right': 'alt_rlcapsctlr_lrtablr',
    'alt': 'alt_rlcapsctlr_lrtablr',
    'alt left': 'alt_rlcapsctlr_lrtablr',
    'alt right': 'alt_rlcapsctlr_lrtablr',
    'caps lock': 'alt_rlcapsctlr_lrtablr',
    'win': 'downentershiftlshiftrupwin',
    'esc': 'esc_backspace',
    'print screen': ']=0',
    'up': 'u',
    'down': 'n',
    'left': 'j',
    'right': 'k',
    'home': 'j',
    'end': 'k',
    'page up': 'u',
    'page down': 'n',
    'insert': 'f',
    'delete': 'g',
    'f1': '8i',
    'f2': '2w',
    'f3': '3e',
    'f4': '45rt',
    'f5': '45rt',
    'f6': '6y',
    'f7': '7u',
    'f8': '8i',
    'f9': '-[9o',
    'f10': ']=0',
    'f11': 'v',
    'f12': 'b',
    'play/pause': '8i',
    'play pause': '8i',
    'media play pause': '8i',
    'stop': '2w',
    'media stop': '2w',
    'next track': '3e',
    'media next': '3e',
    'previous track': '2w',
    'prev track': '2w',
    'media previous': '2w',
    'fn': 'alt_rlcapsctlr_lrtablr',
    'num lock': '8i',
    'num 0': 'downentershiftlshiftrupwin',
    'num 1': 'z',
    'num 2': 'x',
    'num 3': 'c',
    'num 4': 'a',
    'num 5': 's',
    'num 6': 'd',
    'num 7': '8i',
    'num 8': '2w',
    'num 9': '3e',
    'num /': '2w',
    'num *': '3e',
    'num -': '8i',
    'num +': 'space',
    'num enter': 'esc_backspace',
    'num .': 'n',
}


@dataclass(frozen=True)
class SoundFiles:
    """Поиск wav-файлов для клавиш с учётом групп звуков и fallback-а."""

    sounds_dir: Path
    fallback_sound: str = '-[9o.wav'

    def resolve(self, key_name: str) -> Path | None:
        """Вернуть путь к звуку для клавиши или fallback/None."""
        for filename in _candidate_filenames(key_name):
            path = self.sounds_dir / filename
            if path.is_file():
                return path

        fallback = self.sounds_dir / self.fallback_sound
        return fallback if fallback.is_file() else None


def _candidate_filenames(key_name: str) -> list[str]:
    name = key_name.strip().lower()
    if not name:
        return []
    sound_name = KEY_TO_SOUND.get(name, name)
    return [f'{sound_name}.wav']
