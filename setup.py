from __future__ import annotations

import io
import shutil
import zipfile
from pathlib import Path

import requests
from setuptools import setup
from setuptools.dist import Distribution
from tree_sitter import Language

ROOT = Path(__file__).parent


tree_sitter_languages = {
    "go": "https://github.com/tree-sitter/tree-sitter-go/archive/refs/tags/v0.20.0.zip",
    "javascript": "https://github.com/tree-sitter/tree-sitter-javascript/archive/refs/tags/v0.20.1.zip",
    "python": "https://github.com/tree-sitter/tree-sitter-python/archive/refs/tags/v0.20.4.zip",
    "ruby": "https://github.com/tree-sitter/tree-sitter-ruby/archive/refs/tags/v0.19.0.zip",
    "php": "https://github.com/tree-sitter/tree-sitter-php/archive/refs/tags/v0.19.0.zip",
    "java": "https://github.com/tree-sitter/tree-sitter-java/archive/refs/tags/v0.20.2.zip",
    "c-sharp": "https://github.com/tree-sitter/tree-sitter-c-sharp/archive/refs/tags/v0.20.0.zip",
    "c": "https://github.com/tree-sitter/tree-sitter-c/archive/refs/tags/v0.20.6.zip",
    "cpp": "https://github.com/tree-sitter/tree-sitter-cpp/archive/refs/tags/v0.20.3.zip",
}


def download_tree_sitter_languages(languages: dict[str, str], languages_folder: Path) -> list[str]:
    if languages_folder.exists():
        shutil.rmtree(languages_folder)
    languages_folder.mkdir(parents=True)

    extracted_folders: list[str] = []
    for lang, url in languages.items():
        # Download the ZIP file
        response = requests.get(url)
        response.raise_for_status()

        # Extract the ZIP file
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_f:
            zip_f.extractall(languages_folder)
            extracted_folders.append(zip_f.namelist()[0])  # get the name of the extracted folder

    return extracted_folders


def build_tree_sitter_languages(languages: dict[str, str], languages_folder: Path, target_lib_file: Path) -> str:
    extracted_folders = download_tree_sitter_languages(languages, languages_folder)

    Language.build_library(
        str(target_lib_file),
        [str(languages_folder / lang_folder) for lang_folder in extracted_folders],
    )

    return str(target_lib_file)


build_tree_sitter_languages(
    tree_sitter_languages,
    ROOT / "tree_sitter_languages",
    ROOT / "codebleu" / "my-languages.so",
)


# tree_sitter_extension = Extension(
#     'codebleu.tree_sitter',
#     sources=[],
#     include_dirs=[],
#     libraries=[],
#     extra_objects=[
#
#     ],
# )


class PlatformSpecificDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""

    def has_ext_modules(self):
        return True


setup(
    distclass=PlatformSpecificDistribution,
)
