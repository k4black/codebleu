from setuptools import setup
import subprocess
from pathlib import Path
from setuptools.dist import Distribution


ROOT = Path(__file__).parent


subprocess.check_call(
    ['bash', 'build.sh'],
    cwd=ROOT / 'codebleu' / 'parser'
)


class PlatformSpecificDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""
    def has_ext_modules(self):
        return True


setup(distclass=PlatformSpecificDistribution)
