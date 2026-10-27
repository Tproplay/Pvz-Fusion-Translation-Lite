import json
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.level_creator_nodes_1 import NODES_0_49
from scripts.level_creator_nodes_2 import NODES_50_99
from scripts.level_creator_nodes_3 import NODES_100_149
from scripts.level_creator_nodes_4 import NODES_150_199
from scripts.level_creator_nodes_5 import NODES_200_240

all_nodes = NODES_0_49 + NODES_50_99 + NODES_100_149 + NODES_150_199 + NODES_200_240
print(f'Total translated nodes: {len(all_nodes)}')

orig = json.load(open('translation-data/Dumps/LevelCreatorHelp.json', encoding='utf-8'))
orig_nodes = orig['nodes']
print(f'Total orig nodes: {len(orig_nodes)}')

assert len(all_nodes) == len(orig_nodes), f"{len(all_nodes)} != {len(orig_nodes)}"

cjk_pattern = re.compile(r'[\u4e00-\u9fff]')
cjk_found = 0

for i, (tr, og) in enumerate(zip(all_nodes, orig_nodes)):
    assert tr['type'] == og['type'], f"Mismatch at {i}: {tr['type']} != {og['type']}"
    for field in ['purpose', 'usage', 'example', 'warning']:
        assert field in tr, f"Missing {field} in node {i}"
        if cjk_pattern.search(tr[field]):
            print(f"CJK found in node {i} ({tr['type']}) field {field}: {tr[field]}")
            cjk_found += 1

print(f"Verification passed! CJK issues: {cjk_found}")
