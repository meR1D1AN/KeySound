from pathlib import Path

import pygame


def init_mixer() -> None:
    """Инициализировать микшер, если он ещё не активен."""
    if pygame.mixer.get_init() is not None:
        return
    pygame.mixer.init()


def shutdown_mixer() -> None:
    """Корректно завершить работу микшера, если он уже инициализирован."""
    if pygame.mixer.get_init() is None:
        return
    pygame.mixer.quit()


def load_sound(path: Path) -> pygame.mixer.Sound:
    """Загрузить звук из файла."""
    init_mixer()
    return pygame.mixer.Sound(str(path))


def play_sound(sound: pygame.mixer.Sound) -> None:
    """Проиграть звук на максимальной громкости."""
    init_mixer()
    sound.set_volume(1.0)
    sound.play()
