from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from .tools.push_tool import send_push_notification

@CrewBase
class DigitalTwin():
    """DigitalTwin crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def digital_twin(self) -> Agent:
        return Agent(
            config=self.agents_config['digital_twin'], # type: ignore[index]
            tools=[send_push_notification]
        )

    @task
    def answer_task(self) -> Task:
        return Task(
            config=self.tasks_config['answer_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the DigitalTwin crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, 
        )
