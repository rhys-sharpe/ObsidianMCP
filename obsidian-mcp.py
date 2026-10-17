import httpx2
import os
import sys
import json
from pathlib import Path
from mcp.server import MCPServer

mcp = MCPServer("obsidian")


OBSIDIAN_DIR = sys.argv[1]


@mcp.tool()
def walk_vault():
    dir_dict = {OBSIDIAN_DIR: {}}
    stack = [OBSIDIAN_DIR]
    while len(stack) != 0:
        current_dir = stack.pop()
        for f in Path(current_dir).iterdir():
            fstr = str(f)
            if os.path.isdir(fstr):
                dir_dict[current_dir][fstr] = []
                stack.append(fstr)
            else:
                dir_dict[current_dir][fstr] = os.system(f"cat {fstr}")
    return json.dumps(dir_dict)


if __name__ == "__main__":
    # print("os walk: ", [(root, dirs, files) for (root, dirs, files) in os.walk(OBSIDIAN_DIR)])
    print("Serialized JSON: ", walk_vault())
    
