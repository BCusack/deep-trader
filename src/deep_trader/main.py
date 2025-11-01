

from deep_trader.agents.research_agent import create_research_agent


def main():
    agent = create_research_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": "Tell me about the Fighting Fish?"}]})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
