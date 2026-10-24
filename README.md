# Digital Twin Agent

Welcome to my Digital Twin Agent, powered by [crewAI](https://crewai.com) (framework for orchestrating autonomous AI agents), [gradio](https://gradio.app/) (quick web interface), and [render](https://render.com/) (deploy web services). You can ask questions about my background and experience. 

TRY IT OUT [HERE](https://digital-twin-a2k1.onrender.com/).

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, download the dependencies:
```bash
uv add -r requirements.txt
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/digital_twin/config/agents.yaml` to define your agents
- Modify `src/digital_twin/config/tasks.yaml` to define your tasks
- Modify `src/digital_twin/crew.py` to add your own logic, tools and specific args
- Modify `src/digital_twin/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
uv run python -m digital_twin.chat
```

This command initializes the digital_twin Crew, assembling the agents and assigning them tasks as defined in your configuration.


## Understanding Your Crew

The digital_twin Crew is composed of one AI agent `digital_twin`, with unique role, goal, and tool. This agent collaborate on a series of tasks, defined in `config/tasks.yaml`. The `config/agents.yaml` file outlines the capabilities and configurations of the agent in your crew.
