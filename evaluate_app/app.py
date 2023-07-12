import importlib
import subprocess
import sys

import evaluate
from evaluate.utils import launch_gradio_widget


# hotfix: somehow codebleu is not installed in the docker image
subprocess.run([sys.executable, "-m", "pip", "install", "codebleu"], check=True)
globals()["codebleu"] = importlib.import_module("codebleu")


module = evaluate.load("k4black/codebleu")
launch_gradio_widget(module)
