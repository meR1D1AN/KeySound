"""Сборка onefile через PyInstaller на текущей ОС.

PyInstaller не собирает «чужой» формат: .exe нужно собирать на Windows,
бинарник для Linux — на Linux (или в CI с отдельным job под каждую ОС).
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent


def _dist_output_path() -> Path:
    name = 'keysound.exe' if sys.platform == 'win32' else 'keysound'
    return _ROOT / 'dist' / name


def main() -> int:
    sounds = _ROOT / 'sounds'
    entry = _ROOT / 'main.py'
    if not sounds.is_dir():
        print(f'Ожидается папка: {sounds}', file=sys.stderr)
        return 1
    if not entry.is_file():
        print(f'Ожидается файл: {entry}', file=sys.stderr)
        return 1

    add_data = f'sounds{os.pathsep}sounds'
    cmd = [
        sys.executable,
        '-m',
        'PyInstaller',
        '--onefile',
        '--noconsole',
        '--name',
        'keysound',
        '--add-data',
        add_data,
        str(entry),
    ]
    proc = subprocess.run(cmd, cwd=_ROOT, check=False)
    if proc.returncode != 0:
        return proc.returncode

    out = _dist_output_path()
    print(f'Готово: {out}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
