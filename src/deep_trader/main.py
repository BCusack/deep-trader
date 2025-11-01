import argparse

from deep_trader.utils.agent_runner import AgentRunner


def main():
    parser = argparse.ArgumentParser(description="Run the Deep Trader research agent")
    parser.add_argument(
        "-m",
        "--message",
        dest="message",
        help="Prompt to give the research agent. If omitted, you will be prompted interactively.",
    )
    args = parser.parse_args()

    runner = AgentRunner()
    user_message = args.message or input("Enter a research prompt: ").strip()
    full_content = runner.run_agent(user_message)
    runner.save_report(user_message, full_content)


if __name__ == "__main__":
    main()
