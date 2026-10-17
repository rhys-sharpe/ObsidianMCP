import httpx2
import os
import sys
import json
from pathlib import Path
from mcp.server import MCPServer

mcp = MCPServer("obsidian")


OBSIDIAN_DIR = sys.argv[1]

def walk_vault_helper(path):
    result = {'name': path, 'type': 'folder', 'children': []}
    for f in Path(path).iterdir():
        fstr = str(f)
        if os.path.isdir(fstr):
            result['children'].append(walk_vault_helper(fstr))
        else:
            contents = []
            with open(fstr, "r") as file:
                contents = file.readlines()
            result['children'].append({'name': fstr, 'type': 'file', 'content': " ".join(contents)})

    return result





@mcp.tool()
def walk_vault():
    result = walk_vault_helper(OBSIDIAN_DIR)
    return json.dumps(result)


if __name__ == "__main__":
    # print("os walk: ", [(root, dirs, files) for (root, dirs, files) in os.walk(OBSIDIAN_DIR)])
    print("Serialized JSON: ", walk_vault())
    
