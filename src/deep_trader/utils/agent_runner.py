from datetime import datetime
from pathlib import Path

from deep_trader.agents.research_agent import create_research_agent


class AgentRunner:
    def __init__(self):
        self.agent = create_research_agent()
        self.outputs_dir = Path(__file__).resolve().parents[2] / "outputs"
        self.outputs_dir.mkdir(exist_ok=True)

    def run_agent(self, user_message: str):
        print(f"Running research agent with prompt: {user_message}")
        if not user_message:
            raise SystemExit("No prompt provided. Aborting.")

        print("\nAgent Response:\n")
        result = self.agent.invoke({"messages": [{"role": "user", "content": user_message}]})
        full_content = result["messages"][-1].content
        print(full_content)
        return full_content

    def save_report(self, user_message: str, content: str):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.outputs_dir / f"research_{timestamp}.md"
        with output_file.open("w", encoding="utf-8") as file:
            file.write(f"# Research Report\n\n")
            file.write(f"**Prompt:** {user_message}\n\n")
            file.write(content)
        print(f"Report saved to {output_file}")
