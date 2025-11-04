import argparse

from deep_trader.utils.agent_runner import AgentRunner


def main():
    parser = argparse.ArgumentParser(description="Run the Deep Trader top-level agent (crypto trading)")
    parser.add_argument(
        "-m",
        "--message",
        dest="message",
        help="Prompt to give the Trader agent. If omitted, you will be prompted interactively.",
    )
    args = parser.parse_args()

    runner = AgentRunner()
    user_message = args.message or input("Enter a trading prompt: ").strip()
    full_content = runner.run_agent(user_message)
    runner.save_report(user_message, full_content)


if __name__ == "__main__":
    main()
