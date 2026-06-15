from collectors.github_collector import collect_ai_tools

tools = collect_ai_tools()

for tool in tools:
    print(tool)