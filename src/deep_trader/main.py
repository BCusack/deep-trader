import argparse

from deep_trader.utils.agent_runner import AgentRunner


def main():
    parser = argparse.ArgumentParser(description="Run the Deep Trader top-level agent (crypto trading)")
    parser.add_argument(
        "-m",
        "--message",
        dest="message",
        help="Prompt to give the Trader agent. If omitted, a default autonomous task is used.",
    )
    args = parser.parse_args()

    runner = AgentRunner()
    # Run autonomously without requiring user input. Provide a default task prompt.
    default_prompt = (
        "Identify today's strongest Bybit USDT perpetual on the daily timeframe using breakout criteria, "
        "then produce a concise trade plan with entry, invalidation, targets, and risk notes."
    )
    user_message = (args.message or default_prompt).strip()
    full_content = runner.run_agent(user_message)
    runner.save_report(user_message, full_content)


if __name__ == "__main__":
    main()
