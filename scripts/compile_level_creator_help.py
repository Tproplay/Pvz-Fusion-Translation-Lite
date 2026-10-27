import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.level_creator_nodes_1 import NODES_0_49
from scripts.level_creator_nodes_2 import NODES_50_99
from scripts.level_creator_nodes_3 import NODES_100_149
from scripts.level_creator_nodes_4 import NODES_150_199
from scripts.level_creator_nodes_5 import NODES_200_240

def main():
    target_path = Path("translation-data/Almanac/LevelCreatorHelpTranslate.json")
    with open(target_path, "r", encoding="utf-8") as f:
        existing = json.load(f)
    
    topics = existing.get("topics", [])
    all_nodes = (
        NODES_0_49 +
        NODES_50_99 +
        NODES_100_149 +
        NODES_150_199 +
        NODES_200_240
    )
    
    assert len(all_nodes) == 241, f"Expected 241 nodes, got {len(all_nodes)}"
    
    data = {
        "topics": topics,
        "nodes": all_nodes
    }
    
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully compiled {len(topics)} topics and {len(all_nodes)} nodes to {target_path}")

if __name__ == "__main__":
    main()
