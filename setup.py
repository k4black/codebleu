from setuptools import setup
import subprocess


subprocess.check_call(
    ['bash', 'build.sh'],
    cwd='codebleu/parser'
)


setup()
