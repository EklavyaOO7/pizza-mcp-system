import yaml, json

def generate():
    with open("openapi/pizza.yaml") as f:
        spec = yaml.safe_load(f)

    tools = []

    for path, methods in spec["paths"].items():
        for method, meta in methods.items():
            tool = {
                "name": f"{method}_{path.replace('/', '_').strip('_')}",
                "description": meta.get("summary", ""),
                "input_schema": {}
            }

            if "parameters" in meta:
                for p in meta["parameters"]:
                    tool["input_schema"][p["name"]] = p["schema"]["type"]

            if "requestBody" in meta:
                props = meta["requestBody"]["content"]["application/json"]["schema"]["properties"]
                for k, v in props.items():
                    tool["input_schema"][k] = v["type"]

            tools.append(tool)

    with open("mcp_server/tools.json", "w") as f:
        json.dump(tools, f, indent=2)

    print("✅ MCP tools generated")

if __name__ == "__main__":
    generate()
