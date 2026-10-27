"""Level Creator Help Node Translations - Part 1 (Nodes 0 - 49)."""

NODES_0_49 = [
    {
        "type": "OnBoardStartNode",
        "purpose": "Executes initialization rules when the lawn board is ready.",
        "usage": "Connect trigger output to initialization actions; pre-placed plants are already placed.",
        "example": "Board Start → Display Text to show a welcome message.",
        "warning": "Triggers before the game officially starts. To time from active combat, use 'On Game Start'."
    },
    {
        "type": "OnGameStartNode",
        "purpose": "Executes rules after the game officially starts.",
        "usage": "Connect trigger output to timers, prompts, or initial rewards.",
        "example": "Game Start → Periodic Timer → Gain Sun.",
        "warning": "Also triggers when skipping the intro. The timer's first action occurs after one interval."
    },
    {
        "type": "WaveEventNode",
        "purpose": "Executes rules whenever the wave increases, providing the current wave number.",
        "usage": "Connect trigger output to actions or branches, and wave data to Integer Compare.",
        "example": "Wave → Value A of Integer Compare (Value B = 5); Equal → Branch Condition; True → Display Text.",
        "warning": "Triggers on every wave; does not automatically filter for a specific wave."
    },
    {
        "type": "OnMouseClickNode",
        "purpose": "Reads clicked grid tile, held item, and mouse button (left/right).",
        "usage": "Execution output starts rules; row/column outputs connect to spawn or query nodes.",
        "example": "Click → Branch; 'Is Left Click' → Condition; True → Display Prompt.",
        "warning": "Can trigger on both left and right clicks. Rows and columns are 0-indexed."
    },
    {
        "type": "OnKeyPressNode",
        "purpose": "Executes rules when a specified key is pressed.",
        "usage": "Assign a key in the node, then connect the trigger output.",
        "example": "Select Key → Display Text for in-level interactive prompts.",
        "warning": "Will not trigger if no key is assigned. Avoid conflicting with existing game hotkeys."
    },
    {
        "type": "OnPlantCreateNode",
        "purpose": "Executes rules when a plant is planted, providing that plant.",
        "usage": "Trigger output starts actions; plant output reads attributes or modifies that target.",
        "example": "Event Trigger → Gain Sun (Amount = 25); filter types with Plant Split and Type Compare.",
        "warning": "Does not trigger for pre-placed plants at the start of the level."
    },
    {
        "type": "OnPlantClickNode",
        "purpose": "Executes rules when the player clicks a plant, providing that plant.",
        "usage": "Trigger output starts actions; plant output reads attributes or modifies that target.",
        "example": "Event Trigger → Gain Sun (Amount = 25); filter types with Plant Split and Type Compare.",
        "warning": "Different from mouse click events on empty lawn tiles."
    },
    {
        "type": "OnPlantDieNode",
        "purpose": "Executes rules when a plant's health reaches zero, providing that plant.",
        "usage": "Trigger output starts actions; plant output reads attributes or modifies that target.",
        "example": "Event Trigger → Gain Sun (Amount = 25); filter types with Plant Split and Type Compare.",
        "warning": "Does not cover all removal causes like fusions or manual shoveling."
    },
    {
        "type": "OnPlantDeathCompleteNode",
        "purpose": "Executes rules when a plant finishes its death sequence, providing that plant.",
        "usage": "Trigger output starts actions; plant output reads attributes or modifies that target.",
        "example": "Event Trigger → Gain Sun (Amount = 25); filter types with Plant Split and Type Compare.",
        "warning": "Object may be destroyed shortly after; verify existence after waiting. Death cause output is an integer."
    },
    {
        "type": "OnPlantMixedNode",
        "purpose": "Executes rules when plant fusion completes, providing the resulting plant.",
        "usage": "Trigger output starts actions; plant output reads attributes or modifies that target.",
        "example": "Event Trigger → Gain Sun (Amount = 25); filter types with Plant Split and Type Compare.",
        "warning": "Only listens to fusion events; regular planting will not trigger this."
    },
    {
        "type": "OnZombieSpawnNode",
        "purpose": "Executes rules when a zombie spawns, providing that zombie.",
        "usage": "Trigger output connects to actions; zombie output connects to split attributes or target processing.",
        "example": "Event → Display Text; Zombie Split → Type Compare → Branch to filter specific types.",
        "warning": "Triggers for both normal spawns and hypnotized spawns; filter targets as needed."
    },
    {
        "type": "OnZombieDieNode",
        "purpose": "Executes rules when a zombie dies, providing that zombie.",
        "usage": "Trigger output connects to actions; zombie output connects to split attributes or target processing.",
        "example": "Event → Display Text; Zombie Split → Type Compare → Branch to filter specific types.",
        "warning": "Target may be destroyed shortly after; actions after a delay should not assume target is alive."
    },
    {
        "type": "OnWaveClearedNode",
        "purpose": "Executes rules once when all enemies from a normal wave are cleared.",
        "usage": "Recorded per wave; trigger output grants rewards or switches stages; wave output gives the cleared wave.",
        "example": "Clearing Wave 1 enemies during Wave 2 still outputs Wave 1; Wave 2 enemies don't need to be cleared together.",
        "warning": "Spawned/summoned enemies belong to current wave; death/exit/hypnosis unblocks. Max once per wave. Depends on normal spawn completion; special spawn modes might not trigger; final victory may end combat first."
    },
    {
        "type": "OnZombieHealthBelowNode",
        "purpose": "Triggers when specified zombie's base HP reaches a threshold.",
        "usage": "Zombie input connects to boss object; HP ratio 0.5 represents half health.",
        "example": "Create Boss → Bind Zombie; Get Bound Zombie → HP Below Threshold Event → Change Stage.",
        "warning": "Does not count armor. Monitoring the same target only triggers once; switching targets resets check; dead targets do not trigger."
    },
    {
        "type": "OnStageEnterNode",
        "purpose": "Executes rules when entering a specified gameplay stage.",
        "usage": "Enter stage name in node, matching the name used in Change Stage.",
        "example": "Change Stage to 'Reward'; Enter Stage 'Reward' → Show Reward Selection.",
        "warning": "Initial stage is empty; consecutively switching to the same stage will not trigger repeatedly; names must match exactly."
    },
    {
        "type": "ChangeStageNode",
        "purpose": "Switches current level event graph to specified gameplay stage.",
        "usage": "Connect trigger input and enter stage name; completion output continues follow-up actions.",
        "example": "Boss Half HP → Change Stage, name 'Phase 2'.",
        "warning": "Cancels waits and timers from the previous stage; stage name does not automatically change zombie spawns or pause the game."
    },
    {
        "type": "GetStageNode",
        "purpose": "Reads current gameplay stage name.",
        "usage": "Connect text output to text inputs requiring stage name.",
        "example": "Get Current Stage → Text input of Display Text; trigger with key press.",
        "warning": "This is a query node without execution trigger; will not switch stages by itself."
    },
    {
        "type": "DoOnceNode",
        "purpose": "Ensures an action or reward executes only the first time a signal is received.",
        "usage": "First trigger output connects to one-time action; trigger again with Reset=true to re-enable.",
        "example": "Repeated Event → Do Once → Gain Sun.",
        "warning": "Calling with Reset=true only resets state without executing action; must be triggered again afterward."
    },
    {
        "type": "BindPlantNode",
        "purpose": "Assigns a custom name to a plant on the lawn for easy lookup elsewhere.",
        "usage": "Input plant object, enter name, and connect trigger signal.",
        "example": "Create Plant Success → Bind Plant, name 'Target'; connect object output to Bind Plant.",
        "warning": "Binding same name replaces previous target; valid only within current match's event graph."
    },
    {
        "type": "GetBoundPlantNode",
        "purpose": "Finds previously bound plant by name.",
        "usage": "Enter exact name used in Bind Plant; use Object and Exists outputs.",
        "example": "Get Bound Plant 'Exists' → Branch Condition; True branch operates on Object output.",
        "warning": "Returns null if not found or destroyed; always check 'Exists' first."
    },
    {
        "type": "BindZombieNode",
        "purpose": "Assigns a custom name to a zombie on the lawn for easy lookup elsewhere.",
        "usage": "Input zombie object, enter name, and connect trigger signal.",
        "example": "Create Zombie Success → Bind Zombie, name 'Boss'; connect object output to Bind Zombie.",
        "warning": "Binding same name replaces previous target; valid only within current match's event graph."
    },
    {
        "type": "GetBoundZombieNode",
        "purpose": "Finds previously bound zombie by name.",
        "usage": "Enter exact name used in Bind Zombie; use Object and Exists outputs.",
        "example": "Get Bound Zombie 'Exists' → Branch Condition; True branch operates on Object output.",
        "warning": "Returns null if not found or destroyed; always check 'Exists' first."
    },
    {
        "type": "SetPlantNode",
        "purpose": "Spawns a plant on a specified grid tile.",
        "usage": "Provide plant type, row, and column; connect trigger; Success output connects to follow-up actions.",
        "example": "Game Start → Set Plant: Row 0, Col 0, Peashooter; Failure output connects to Display Text.",
        "warning": "Non-forced by default; water, roof, carrier, or existing plants may cause failure; rows and cols are 0-indexed."
    },
    {
        "type": "CreateZombieNode",
        "purpose": "Spawns a specified zombie type at a given location.",
        "usage": "Set row, col, zombie type, and hypnotized; use spawned zombie object after triggering.",
        "example": "Key Press → Create Zombie; Success output passes object to Bind Zombie.",
        "warning": "Data outputs do not spawn entities on their own; must execute the trigger; verify spawn position."
    },
    {
        "type": "MovePlantNode",
        "purpose": "Moves an existing plant to a specified grid tile.",
        "usage": "Connect lawn plant object and target coordinates, then connect trigger.",
        "example": "Create Plant → Move Plant to shift target column to another tile.",
        "warning": "Plant Type cannot substitute for Object; out-of-bounds, occupied, or invalid targets may fail; handle failure branch."
    },
    {
        "type": "MoveZombieNode",
        "purpose": "Moves an existing zombie to a specified grid tile.",
        "usage": "Connect lawn zombie object and target coordinates, then connect trigger.",
        "example": "Create Zombie → Move Zombie to shift target column to another tile.",
        "warning": "Zombie Type cannot substitute for Object; out-of-bounds, occupied, or invalid targets may fail; handle failure branch."
    },
    {
        "type": "CreatePlantCardNode",
        "purpose": "Spawns a collectible plant card on the lawn.",
        "usage": "Specify plant type and spawn coordinates, then connect trigger.",
        "example": "Zombie Dies → Create Plant Card, select dropped plant type.",
        "warning": "Spawns card on lawn, does not add directly to seed bank; use 'Add Plant Card' for seed bank."
    },
    {
        "type": "AddPlantCardNode",
        "purpose": "Adds a plant card to player's seed bank.",
        "usage": "Choose plant type; toggle default data off to customize cost and cooldown.",
        "example": "Reward Clicked → Add Plant Card, select Peashooter.",
        "warning": "May fail if seed bank is full; Planted trigger output tracks the plant placed from this card."
    },
    {
        "type": "DeleteCardByTypeNode",
        "purpose": "Removes plant cards of a specified type from seed bank.",
        "usage": "Connect trigger and provide plant type.",
        "example": "Enter Stage → Remove Plant Card from seed bank, then add new cards.",
        "warning": "Only removes cards from seed bank; does not remove plants already planted on lawn."
    },
    {
        "type": "HealPlantNode",
        "purpose": "Restores health to specified plant.",
        "usage": "Connect plant object, enter heal amount, and connect trigger.",
        "example": "Plant Event Output → Object; Trigger Event → Heal Plant, enter desired amount.",
        "warning": "Verify target validity; healing and shields do not modify maximum health."
    },
    {
        "type": "DamagePlantNode",
        "purpose": "Inflicts damage on specified plant.",
        "usage": "Connect plant object, enter damage amount, and connect trigger.",
        "example": "Plant Event Output → Object; Trigger Event → Damage Plant, enter desired amount.",
        "warning": "Verify target validity; does not bypass invulnerability unless specified."
    },
    {
        "type": "DamageZombieNode",
        "purpose": "Inflicts damage on specified zombie.",
        "usage": "Connect zombie object, enter damage amount, and connect trigger.",
        "example": "Zombie Event Output → Object; Trigger Event → Damage Zombie, enter desired amount.",
        "warning": "Verify target validity; damage respects zombie armor rules."
    },
    {
        "type": "GivePlantShieldNode",
        "purpose": "Adds a protective shield to specified plant.",
        "usage": "Connect plant object, enter shield amount, and connect trigger.",
        "example": "Plant Event Output → Object; Trigger Event → Give Shield, enter desired amount.",
        "warning": "Verify target validity; shields absorb damage before plant health."
    },
    {
        "type": "DiePlantNode",
        "purpose": "Directly removes specified plant and executes death handling.",
        "usage": "Connect plant object and trigger signal.",
        "example": "Click Plant → Condition Branch → Kill Plant, passing clicked plant object.",
        "warning": "Unlike dealing damage, may bypass HP reduction events; avoid connecting to all planting events."
    },
    {
        "type": "SetZombieMindControlledNode",
        "purpose": "Hypnotizes specified zombie to fight for the player.",
        "usage": "Connect zombie object and trigger signal.",
        "example": "Zombie Spawned → Set Zombie Mind Controlled, passing spawned zombie object.",
        "warning": "Requires a specific zombie object, not a zombie type; ensure target is valid."
    },
    {
        "type": "ModifyPlantAttackNode",
        "purpose": "Modifies attack bonus multiplier of specified plant.",
        "usage": "Connect plant object and trigger; set desired multiplier in float input.",
        "example": "Create Plant Success → Modify Plant Attack; pass object and observe values.",
        "warning": "Input is a bonus multiplier (default 1.0), not a flat stat override; setting repeatedly does not compound."
    },
    {
        "type": "ModifyPlantHealthNode",
        "purpose": "Modifies health bonus multiplier of specified plant.",
        "usage": "Connect plant object and trigger; set desired multiplier in float input.",
        "example": "Create Plant Success → Modify Plant Health; pass object and observe values.",
        "warning": "Input is a bonus multiplier (default 1.0), not a flat stat override; setting repeatedly does not compound."
    },
    {
        "type": "ModifyZombieHealthNode",
        "purpose": "Modifies health multiplier of specified zombie.",
        "usage": "Connect zombie object and trigger; set desired multiplier in float input.",
        "example": "Create Zombie Success → Modify Zombie Health; pass object and observe values.",
        "warning": "Input is a multiplier (default 1.0), not a flat stat override; setting repeatedly does not compound."
    },
    {
        "type": "PlantSplitNode",
        "purpose": "Reads row, column, and plant type from a specific plant.",
        "usage": "Input plant object; connect coordinate or type outputs to query/compare nodes.",
        "example": "Plant Event → Plant Split → Plant Type Compare → Condition Branch.",
        "warning": "Does not trigger actions on its own; if object is null, default coordinates should not be treated as actual position."
    },
    {
        "type": "ZombieSplitNode",
        "purpose": "Reads row, column, and zombie type from a specific zombie.",
        "usage": "Input zombie object; connect coordinate or type outputs to query/compare nodes.",
        "example": "Zombie Event → Zombie Split → Zombie Type Compare → Condition Branch.",
        "warning": "Does not trigger actions on its own; if object is null, default coordinates should not be treated as actual position."
    },
    {
        "type": "GetPlantsInCellNode",
        "purpose": "Retrieves all registered plants in a specified grid tile.",
        "usage": "Enter row and col; connect list output to For Each Plant.",
        "example": "Mouse Row/Col → Get Plants in Cell → For Each Plant; Mouse Click triggers loop.",
        "warning": "Includes all layers (Lily Pad, Flower Pot, Flying, Shell), not just main plant."
    },
    {
        "type": "GetPlantsOnLayerNode",
        "purpose": "Queries plants on a specific layer in a grid tile.",
        "usage": "Enter row and col; choose layer: Main, Flower Pot, Lily Pad, Pumpkin, or Flying.",
        "example": "Mouse Row/Col → Get Plants on Layer (Main) → For Each Plant.",
        "warning": "Position layer is not combat class; returns empty list if out of bounds or empty."
    },
    {
        "type": "GetAllPlantsNode",
        "purpose": "Retrieves list of all registered plants on the lawn.",
        "usage": "Connect list output to For Each Plant; start loop from another event.",
        "example": "Level Start → For Each Plant; connect list from GetAllPlants.",
        "warning": "Connecting list alone does not execute loop; targets may die during subsequent actions."
    },
    {
        "type": "GetNearestZombieNode",
        "purpose": "Finds zombie closest to specified coordinates.",
        "usage": "Provide coordinates; connect object output to damage, hypnotize, or split nodes.",
        "example": "Key Press → Damage Zombie; connect nearest zombie output to target.",
        "warning": "Returns null if no valid targets on lawn; query itself does not inflict damage."
    },
    {
        "type": "GetEventPositionNode",
        "purpose": "Reads most recent mouse or entity position recorded in execution chain.",
        "usage": "Enable retain trigger data; check Has Position before using row/column outputs. Coordinates persist after delays.",
        "example": "Click Lawn → Wait 1s → Spawn Plant at original clicked tile using row/column outputs.",
        "warning": "Coordinates remain readable after entity dies, but entity may no longer exist; returns false and (0,0) if no position recorded."
    },
    {
        "type": "ForEachPlantNode",
        "purpose": "Processes each plant in a list sequentially.",
        "usage": "Connect list to input and event to trigger; loop body connects to actions using current item.",
        "example": "Get All Plants → For Each Plant; loop body performs action on each plant.",
        "warning": "Executes synchronously in the same frame; does not wait for Wait nodes inside loop body."
    },
    {
        "type": "ForEachPlantTypeNode",
        "purpose": "Processes each plant type in a list sequentially.",
        "usage": "Connect list to input and event to trigger; loop body connects to actions using current item.",
        "example": "Get Plant Type List → For Each Plant Type; loop body performs action for each type.",
        "warning": "Executes synchronously in the same frame; does not wait for Wait nodes inside loop body."
    },
    {
        "type": "PlantTypeValueNode",
        "purpose": "Provides a constant plant type.",
        "usage": "Select plant type in node; connect output to spawn or type comparison nodes.",
        "example": "Plant Type → Set Plant Type input; Game Start triggers spawn.",
        "warning": "Type is not an active entity on lawn; does not require trigger signal."
    },
    {
        "type": "ZombieTypeValueNode",
        "purpose": "Provides a constant zombie type.",
        "usage": "Select zombie type in node; connect output to spawn or type comparison nodes.",
        "example": "Zombie Type → Create Zombie Type input; Game Start triggers spawn.",
        "warning": "Type is not an active entity on lawn; does not require trigger signal."
    },
    {
        "type": "ComparePlantTypeNode",
        "purpose": "Checks if two plant types are identical.",
        "usage": "Connect two plant types to inputs; connect comparison result to branch condition.",
        "example": "Plant Split Type vs Constant Plant Type; Event triggers branch.",
        "warning": "Outputs a boolean value only; does not execute True branch on its own."
    }
]
