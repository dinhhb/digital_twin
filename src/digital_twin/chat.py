import gradio as gr
from digital_twin.styles import CSS, JS, EXAMPLES
from digital_twin.crew import DigitalTwin
from digital_twin.main import linkedin


def respond(message, history):
    inputs = {"linkedin": linkedin, "message": message}
    return DigitalTwin().crew().kickoff(inputs=inputs).raw


def chat():
    gr.ChatInterface(respond, title="Digital Twin", examples=EXAMPLES).launch(css=CSS, js=JS, theme=gr.themes.Base())

if __name__ == "__main__":
    chat()
