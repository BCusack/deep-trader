import argparse
from datetime import datetime
from pathlib import Path

from deep_trader.agents.research_agent import create_research_agent


def main():
    parser = argparse.ArgumentParser(description="Run the Deep Trader research agent")
    parser.add_argument(
        "-m",
        "--message",
        dest="message",
        help="Prompt to give the research agent. If omitted, you will be prompted interactively.",
    )
    args = parser.parse_args()

    agent = create_research_agent()
    user_message = args.message or input("Enter a research prompt: ").strip()
    print(f"Running research agent with prompt: {user_message}")
    if not user_message:
        raise SystemExit("No prompt provided. Aborting.")

    result = agent.invoke({"messages": [{"role": "user", "content": user_message}]})
    content = result["messages"][-1].content

    outputs_dir = Path(__file__).resolve().parents[1] / "outputs"
    outputs_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = outputs_dir / f"research_{timestamp}.md"
    with output_file.open("w", encoding="utf-8") as file:
        file.write(f"# Research Report\n\n")
        file.write(content)

    print(f"Report saved to {output_file}")


if __name__ == "__main__":
    main()
