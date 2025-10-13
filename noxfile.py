from __future__ import annotations
import enum
import sys

import nox
import shutil
from pathlib import Path


ROOT = Path(__file__).parent.resolve()
SRC = ROOT / "src"
PKG = SRC / "btrvol"
GUI_DIR = PKG / "gui"
UI_FILE = GUI_DIR / "main.ui"
GUI_ASSETS = GUI_DIR / "assets"
ICON_ICO = GUI_ASSETS / "icons" / "icon.16.ico"
BUILD_DIR = ROOT / "build"


def rm(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)
    elif path.exists():
        path.unlink(missing_ok=True)


def rglob_remove(patterns: list[str]) -> None:
    for pat in patterns:
        for p in ROOT.rglob(pat):
            try:
                if p.is_dir():
                    shutil.rmtree(p, ignore_errors=True)
                else:
                    p.unlink(missing_ok=True)
            except Exception:
                # best-effort; keep going
                pass


@nox.session(venv_backend='none')
def clean(session: nox.Session) -> None:
    """Clean up build artifacts and caches."""
    for d in [
        ROOT / "dist",
        ROOT / "build",
        ROOT / ".nuitka",
        ROOT / ".nuitka-build",
        ROOT / ".pytest_cache",
        ROOT / ".mypy_cache",
    ]:
        rm(d)

    rglob_remove([
        "__pycache__",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        "*.spec",
        "*.build",
        "*.dist",
        "*.o",
        "*.obj",
        "*.dll",
        "*.so",
        "*.a",
        "*.lib",
    ])

    session.log("Clean done.")


def _build(
    session: nox.Session, mode: BuildMode, build_bootloader: bool = False
) -> None:
    session.install("-e", ".[gui]")
    session.run("uv", "pip", "freeze", external=True)
    if build_bootloader:
        session.install(
            "--verbose",
            "--no-binary", ":all:",
            "pyinstaller",
            "--reinstall",
            "git+https://github.com/pyinstaller/pyinstaller.git",
            env={**session.env, "PYINSTALLER_COMPILE_BOOTLOADER": "1"},
            silent=False,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
    else:
        session.install("pyinstaller")

    match mode:
        case BuildMode.ONEDIR:
            sub_build_folder = "ONEDIR"
            args = [
                "--onedir",
                "--console",
            ]
        case BuildMode.ONEFILE:
            sub_build_folder = "ONEFILE"
            args = [
                "--onefile",
                "--windowed",
            ]

    build_path = BUILD_DIR / sub_build_folder
    build_path.mkdir(exist_ok=True, parents=True)

    common_args = [
        "--noconfirm",
        "--clean",
        "--distpath", f"{build_path}",
        "--workpath", f"{build_path}/pyi",
        "--name=Btrvol",
        "--icon", "./resources/icon.ico",
        "--add-data", "./src/btrvol/gui/main.ui;btrvol/gui/.",
        "--add-data", "./src/btrvol/gui/assets;btrvol/gui/assets/",
        "--collect-all", "pygubu",
        "--collect-all", "awthemes",
        "--collect-all", "ttkwidgets",
    ]

    session.run(
        "pyinstaller",
        *args, *common_args,
        "./src/btrvol/gui/__main__.py",
        external=True,
    )


class BuildMode(enum.StrEnum):
    ONEDIR = enum.auto()
    ONEFILE = enum.auto()


@nox.session(reuse_venv=True, venv_backend="uv")
def build(session: nox.Session) -> None:
    _build(session, BuildMode.ONEDIR)


@nox.session(reuse_venv=True, venv_backend="uv")
def build_onefile(session: nox.Session) -> None:
    _build(session, BuildMode.ONEFILE)
