import subprocess
import sys

import evaluate
from evaluate.utils import launch_gradio_widget

# hotfix: somehow codebleu is not installed in the docker image
subprocess.check_call([sys.executable, "-m", "pip", "install", "codebleu"])

module = evaluate.load("k4black/codebleu")
launch_gradio_widget(module)
