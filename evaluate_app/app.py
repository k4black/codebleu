import evaluate
from evaluate.utils import launch_gradio_widget

module = evaluate.load("k4black/codebleu")
launch_gradio_widget(module)
