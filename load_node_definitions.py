import os
import json

NODE_DEFINITIONS_ROOT = "./database/n8n-node-definitions/nodes"

def load_node_definitions():
    node_map = {}

    for root, dirs, files in os.walk(NODE_DEFINITIONS_ROOT):
        for filename in files:
            if filename.endswith(".json"):
                full_path = os.path.join(root, filename)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        node_type = data.get("type")
                        node_name = data.get("name")
                        description = data.get("description", "")
                        defaults = data.get("defaults", {})

                        if node_type:
                            node_map[node_type] = {
                                "name": node_name,
                                "description": description,
                                "defaults": defaults
                            }
                except Exception as e:
                    print(f"Kļūda failā {filename}: {e}")

    print(f"Atrastie mezgli: {len(node_map)}")
    return node_map

if __name__ == "__main__":
    nodes = load_node_definitions()
    for key, val in list(nodes.items())[:10]:
        print(f"{key}: {val['name']}")

