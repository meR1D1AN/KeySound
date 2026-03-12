import sys

from keysound_app import KeySoundApp


def main() -> int:
    """Точка входа в приложение."""
    if sys.platform != 'win32':
        raise SystemExit('Эта программа поддерживает только Windows.')
    return KeySoundApp().run()


if __name__ == '__main__':
    raise SystemExit(main())
