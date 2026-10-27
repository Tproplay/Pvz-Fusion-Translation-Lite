"""Level Creator Help Node Translations - Part 2 (Nodes 50 - 99)."""

NODES_50_99 = [
    {
        "type": "CompareZombieTypeNode",
        "purpose": "Checks if two zombie types are identical.",
        "usage": "Connect two zombie types to inputs; connect comparison result to branch condition.",
        "example": "Zombie Split Type vs Constant Zombie Type; Event triggers branch.",
        "warning": "Outputs a boolean value only; does not execute True branch on its own."
    },
    {
        "type": "SinglePlantTypeListNode",
        "purpose": "Wraps a single plant type into a list.",
        "usage": "Connect plant type to input; use list output for merging, random selection, or iteration.",
        "example": "Plant Type → Single Plant Type List → Merge Plant Type Lists.",
        "warning": "Produces a list of plant types, not active plant entities on the lawn."
    },
    {
        "type": "MultiPlantTypeListNode",
        "purpose": "Configures multiple plant types within a single node.",
        "usage": "Edit list within node; connect output to random selector or iteration loop.",
        "example": "Multi Plant Type List → Get Random Plant Type → Add Plant Card.",
        "warning": "If list is empty, subsequent random selection will not return a valid type."
    },
    {
        "type": "MergePlantTypeListsNode",
        "purpose": "Combines two plant type lists into one.",
        "usage": "Connect two lists to inputs; use merged result list or length output.",
        "example": "Two Single Plant Type Lists → Merge → Get Random Plant Type.",
        "warning": "Merging does not execute actions automatically; check for duplicate types if needed."
    },
    {
        "type": "PlantTypeListStorageNode",
        "purpose": "Saves and modifies a plant type list within the current match.",
        "usage": "Send list to storage node; select action (Set, Add, Remove) and trigger.",
        "example": "Set reward pool at start; remove chosen type after reward selection, then read remaining list.",
        "warning": "Unlike primitive variables, runtime modifications do not write back to initial editor lists."
    },
    {
        "type": "GetRandomPlantTypeNode",
        "purpose": "Draws a random plant type from an input list.",
        "usage": "Provide non-empty type list; connect output to card or plant spawn type input.",
        "example": "Multi Plant Type List → Get Random Plant Type → Create Plant Card; trigger spawn on event.",
        "warning": "Draws randomly on read; multiple reads may return different types; avoid empty lists."
    },
    {
        "type": "RemovePlantTypeNode",
        "purpose": "Removes a specified plant type from a plant type list.",
        "usage": "Connect source list and target type; use result list and success output.",
        "example": "Reward Pool List + Selected Type → Remove Plant Type → Follow-up list processing.",
        "warning": "Must use result list output; does not remove plants on lawn or cards in seed bank."
    },
    {
        "type": "ShowTextNode",
        "purpose": "Displays a prompt message on the game screen.",
        "usage": "Enter text and duration (seconds); connect execution trigger.",
        "example": "Wave 5 True Branch → Show Text: 'The Boss has arrived!'.",
        "warning": "Connecting text alone does not display it; duration is specified in seconds."
    },
    {
        "type": "PlaySoundNode",
        "purpose": "Plays an existing game sound effect.",
        "usage": "Select or enter valid SFX ID; connect execution trigger.",
        "example": "Reward Option Clicked → Play Sound.",
        "warning": "Sound IDs correspond to game assets, not local file paths; invalid IDs produce no sound."
    },
    {
        "type": "PlayZombieAnimNode",
        "purpose": "Switches the animation of a specified zombie.",
        "usage": "Connect zombie object; enter valid animation state name on that entity.",
        "example": "Create Zombie Success → Play Zombie Animation: 'walk'.",
        "warning": "Animation names must match entity assets; visual only, does not deal attack damage."
    },
    {
        "type": "GetSunNode",
        "purpose": "Grants a specified amount of Sun to the player.",
        "usage": "Enter integer amount; connect execution trigger.",
        "example": "Reward Option Clicked → Gain Sun (Amount = 50).",
        "warning": "Amount is an integer; triggers repeatedly if called multiple times; precede with 'Do Once' for one-time rewards."
    },
    {
        "type": "GetMoneyNode",
        "purpose": "Grants a specified amount of Coins to the player.",
        "usage": "Enter integer amount; connect execution trigger.",
        "example": "Reward Option Clicked → Gain Coins (Amount = 50).",
        "warning": "Amount is an integer; triggers repeatedly if called multiple times; precede with 'Do Once' for one-time rewards."
    },
    {
        "type": "UseSunNode",
        "purpose": "Attempts to deduct a specified amount of Sun from the player.",
        "usage": "Enter cost; Success output connects to purchased effect, Failure output connects to insufficient sun prompt.",
        "example": "Interact Event → Use Sun; Success grants reward, Failure shows insufficient warning.",
        "warning": "Do not connect rewards parallel to this node, otherwise reward may be granted even if deduction fails."
    },
    {
        "type": "UseMoneyNode",
        "purpose": "Attempts to deduct a specified amount of Coins from the player.",
        "usage": "Enter cost; Success output connects to purchased effect, Failure output connects to insufficient coins prompt.",
        "example": "Interact Event → Use Coins; Success grants reward, Failure shows insufficient warning.",
        "warning": "Do not connect rewards parallel to this node, otherwise reward may be granted even if deduction fails."
    },
    {
        "type": "GetSunAmountNode",
        "purpose": "Reads player's current Sun count.",
        "usage": "Connect integer output to comparison or arithmetic nodes.",
        "example": "Current Sun Compare (≥ 100) → Branch Condition; interact event triggers branch.",
        "warning": "Query only; does not add or deduct Sun; use 'Use Sun' for transactions."
    },
    {
        "type": "GetTravelBuffNode",
        "purpose": "Grants a specified Odyssey Modifier to the match.",
        "usage": "Select modifier category and entry in node; connect trigger to apply.",
        "example": "Reward Choice → Gain Odyssey Modifier, select desired buff.",
        "warning": "Legacy node kept for backwards compatibility; prefer 'Gain Travel Entry' in newer rules."
    },
    {
        "type": "GetTravelEntryNode",
        "purpose": "Grants a specified Odyssey Modifier to the match.",
        "usage": "Select modifier category and entry in node; connect trigger to apply.",
        "example": "Reward Choice → Gain Odyssey Modifier, select desired buff.",
        "warning": "Legacy node kept for backwards compatibility; prefer 'Gain Travel Entry' in newer rules."
    },
    {
        "type": "GameOverNode",
        "purpose": "Manually triggers a Game Over defeat for this match.",
        "usage": "Connect trigger to defeat condition branch; enter defeat reason.",
        "example": "Defense Objective Destroyed → Game Over (Reason: 'Target Destroyed').",
        "warning": "Do not connect to unconditional start events; defeat sequence terminates current combat."
    },
    {
        "type": "GameWinNode",
        "purpose": "Manually triggers victory settlement for this match.",
        "usage": "Connect trigger to mission completed branch.",
        "example": "Target Count Reached → Branch True → Game Win.",
        "warning": "Comparison result alone will not finish level; requires execution trigger signal."
    },
    {
        "type": "CreateGraveNode",
        "purpose": "Spawns a tombstone at the specified grid tile.",
        "usage": "Enter row and col along with optional parameters; connect trigger.",
        "example": "Target Wave → Create Grave at specified tile.",
        "warning": "Rows and cols are 0-indexed; obstacles alter plantable space."
    },
    {
        "type": "CreateParticleNode",
        "purpose": "Spawns white smoke visual particle effect at specified grid tile.",
        "usage": "Enter row and col along with optional parameters; connect trigger.",
        "example": "Target Wave → Create Particle Effect at specified tile.",
        "warning": "Rows and cols are 0-indexed; smoke is visual only and does not affect gameplay mechanics."
    },
    {
        "type": "CreateLadderNode",
        "purpose": "Spawns a ladder obstacle at the specified grid tile.",
        "usage": "Enter row and col along with optional parameters; connect trigger.",
        "example": "Target Wave → Create Ladder at specified tile.",
        "warning": "Rows and cols are 0-indexed; obstacles alter plantable space."
    },
    {
        "type": "CreateCraterNode",
        "purpose": "Spawns a crater obstacle at the specified grid tile.",
        "usage": "Enter row and col along with optional parameters; connect trigger.",
        "example": "Target Wave → Create Crater at specified tile.",
        "warning": "Rows and cols are 0-indexed; craters temporarily prevent planting."
    },
    {
        "type": "CreateIceBlockNode",
        "purpose": "Spawns an ice block obstacle at the specified grid tile.",
        "usage": "Enter row and col along with optional parameters; connect trigger.",
        "example": "Target Wave → Create Ice Block at specified tile.",
        "warning": "Rows and cols are 0-indexed; encased plants must be configured separately."
    },
    {
        "type": "CreateIceShroomEffectNode",
        "purpose": "Directly triggers Ice-shroom freeze effect across the entire lawn.",
        "usage": "Configure duration/damage parameters; triggers screen-wide freeze.",
        "example": "Skill Key Event → Ice-shroom Freeze Effect.",
        "warning": "Direct effect that does not plant an entity; test freeze duration in sandbox first."
    },
    {
        "type": "CreateJalapenoEffectNode",
        "purpose": "Directly triggers Jalapeño fire effect along a specified lane.",
        "usage": "Configure target row and damage parameters; triggers lane-wide burn.",
        "example": "Skill Key Event → Jalapeño Fire Effect.",
        "warning": "Direct effect that does not plant an entity; verifies target row before dealing damage."
    },
    {
        "type": "CreateDoomShroomEffectNode",
        "purpose": "Directly triggers Doom-shroom explosion effect around specified tile.",
        "usage": "Configure row, column, and damage parameters; triggers 3x3 blast.",
        "example": "Skill Key Event → Doom-shroom Explosion Effect.",
        "warning": "Direct effect that does not plant an entity; check crater creation settings."
    },
    {
        "type": "CreateCherryExplodeNode",
        "purpose": "Directly triggers Cherry Bomb explosion effect around specified tile.",
        "usage": "Configure row, column, and damage parameters; triggers 3x3 blast.",
        "example": "Skill Key Event → Cherry Bomb Explosion Effect.",
        "warning": "Direct effect that does not plant an entity; deals standard explosive damage."
    },
    {
        "type": "CreateZombieExplodeNode",
        "purpose": "Directly triggers Jack-in-the-Box zombie explosion effect at specified location.",
        "usage": "Configure row, column, and damage parameters; triggers explosion.",
        "example": "Skill Key Event → Jack-in-the-Box Explosion Effect.",
        "warning": "Direct effect that does not spawn a zombie entity; damages surrounding plants."
    },
    {
        "type": "TypedChoiceOptionNode",
        "purpose": "Adds a selectable card option to a reward choice menu.",
        "usage": "Enter title, description, and display content; chain list output to next option or menu; Click output triggers reward.",
        "example": "Chain three options into Show Menu; Click outputs connect to Sun, Coins, and Cards respectively.",
        "warning": "Options are constructed when menu reads the list; use with 'Typed Choice Menu'."
    },
    {
        "type": "AddMultipleChoiceOptionNode",
        "purpose": "Adds a selectable card option to a reward choice menu.",
        "usage": "Enter title, description, and display content; chain list output to next option or menu; Click output triggers reward.",
        "example": "Chain three options into Show Menu; Click outputs connect to Sun, Coins, and Cards respectively.",
        "warning": "Legacy GameObject option port; pair with legacy Multi-Choice Menu."
    },
    {
        "type": "TypedChoiceMenuNode",
        "purpose": "Opens a multi-choice menu letting player choose a reward.",
        "usage": "Connect option list input; trigger with event signal; configure display count, reroll, and cancel options.",
        "example": "Wave Cleared → Show Choice Menu; connect 3 chained options, set window count to 3.",
        "warning": "Window count limited to 1-5; pauses game while active; resumes on select or cancel."
    },
    {
        "type": "ShowMultipleChoiceMenuNode",
        "purpose": "Opens a multi-choice menu letting player choose a reward.",
        "usage": "Connect option list input; trigger with event signal; configure display count, reroll, and cancel options.",
        "example": "Wave Cleared → Show Choice Menu; connect 3 chained options, set window count to 3.",
        "warning": "Window count limited to 1-5; pauses game while active; resumes on select or cancel."
    },
    {
        "type": "TypedChoiceMergeNode",
        "purpose": "Merges two reward option lists into a single list.",
        "usage": "Connect lists A and B to inputs; use output for menu or further merging.",
        "example": "Two independent option lists → Merge Options → Show Choice Menu.",
        "warning": "Do not mix typed options with legacy GameObject options; merging does not open the menu by itself."
    },
    {
        "type": "MergeMultipleChoiceOptionListsNode",
        "purpose": "Merges two reward option lists into a single list.",
        "usage": "Connect lists A and B to inputs; use output for menu or further merging.",
        "example": "Two independent option lists → Merge Options → Show Choice Menu.",
        "warning": "Do not mix typed options with legacy GameObject options; merging does not open the menu by itself."
    },
    {
        "type": "CreateInfoCardNode",
        "purpose": "Creates an information card in seed bank that responds to player clicks.",
        "usage": "Configure display contents; connect trigger; Click output connects to interactive actions.",
        "example": "Game Start → Create Info Card; Card Clicked → Show Mission Objectives.",
        "warning": "Used for informational prompts, not plantable cards; click callback expires when event graph terminates."
    },
    {
        "type": "BranchNode",
        "purpose": "Directs execution flow along True or False path based on condition.",
        "usage": "Connect execution trigger; connect comparison result to Condition; True and False outputs connect to follow-up actions.",
        "example": "Current Sun ≥ 100 → Condition; Key Press triggers Branch; True and False display different text.",
        "warning": "Defaults to False if Condition is unconnected. 'False (Stop)' still executes False branch."
    },
    {
        "type": "WaitNode",
        "purpose": "Delays execution by specified number of seconds before continuing.",
        "usage": "Enter delay duration (seconds); connect execution trigger; output connects to follow-up actions.",
        "example": "Game Start → Wait (5s) → Display Text.",
        "warning": "Each trigger instance waits independently; timer pauses during game pause; exiting match cancels waiting."
    },
    {
        "type": "ForLoopNode",
        "purpose": "Repeats execution of loop body synchronously within the same frame.",
        "usage": "Specify loop count; Loop Body connects to actions; Index output is 0-indexed.",
        "example": "Loop 3 Times → Create Plant; Index connects to Column (0, 1, 2).",
        "warning": "Executes synchronously in one frame, does not wait for asynchronous tasks; excessive counts trigger safety limit."
    },
    {
        "type": "ToggleCycleNode",
        "purpose": "Toggles a periodic repeating timer on and off.",
        "usage": "First trigger turns on, second trigger turns off; Cycle Event output triggers periodic action.",
        "example": "Game Start → Toggle Cycle (Interval = 5s) → Gain 25 Sun.",
        "warning": "First cycle executes after one full interval; minimum interval is 0.1s; timer pauses during game pause."
    },
    {
        "type": "RandomTriggerNode",
        "purpose": "Randomly triggers a specified number of downstream actions from candidates.",
        "usage": "Connect candidate actions to output; configure pick count and allow repeats.",
        "example": "Key Press → Random Trigger → Three different prompt nodes.",
        "warning": "Without repeats, pick count cannot exceed number of candidates; selects execution branches, not random numbers."
    },
    {
        "type": "CounterNode",
        "purpose": "Tracks trigger counts for objective progress and condition checks.",
        "usage": "Connect event to trigger; Count output connects to Integer Compare; configure initial value and reset input.",
        "example": "Zombie Dies → Counter; Count == 10 → Branch → Mission Complete.",
        "warning": "First execution loads initial value before incrementing; Reset sets count to 0, not initial value."
    },
    {
        "type": "ToggleNode",
        "purpose": "Toggles boolean state between ON and OFF on each trigger.",
        "usage": "Trigger input flips state; State output provides boolean; State Changed output triggers follow-up actions.",
        "example": "Key Press → Toggle; State connects to Branch Condition, State Changed triggers branch.",
        "warning": "Reading state does not toggle it; runtime state resets each match."
    },
    {
        "type": "PulseNode",
        "purpose": "Outputs True only during synchronous execution of downstream nodes.",
        "usage": "Trigger pulse, passing boolean output to synchronous downstream conditions.",
        "example": "Event → Pulse; Execution connects to Branch, Boolean output connects to Condition.",
        "warning": "Resets immediately after synchronous execution in the same frame, not on next frame."
    },
    {
        "type": "NotNode",
        "purpose": "Inverts a boolean value (NOT logic).",
        "usage": "Connect boolean input; connect inverted output to condition branch.",
        "example": "True input outputs False; use separate event signal to trigger branch.",
        "warning": "Logical operation only; does not trigger actions on its own."
    },
    {
        "type": "AndNode",
        "purpose": "Checks if both boolean conditions are true (AND logic).",
        "usage": "Connect two boolean inputs; connect result output to condition branch.",
        "example": "Has Enough Sun AND Target Wave Reached → Branch Condition.",
        "warning": "Logical operation only; does not trigger actions on its own."
    },
    {
        "type": "OrNode",
        "purpose": "Checks if at least one boolean condition is true (OR logic).",
        "usage": "Connect two boolean inputs; connect result output to condition branch.",
        "example": "Boss Defeated OR Target Count Reached → Branch Condition.",
        "warning": "Logical operation only; does not trigger actions on its own."
    },
    {
        "type": "CompareIntNode",
        "purpose": "Compares two integers and outputs boolean comparison results.",
        "usage": "Connect two integer values; connect desired comparison output (Equal, Greater, etc.) to condition branch.",
        "example": "Compare Wave and 5; connect Equal output to Branch Condition.",
        "warning": "Types must match; inputs require integer values."
    },
    {
        "type": "CompareFloatNode",
        "purpose": "Compares two floating-point numbers and outputs boolean comparison results.",
        "usage": "Connect two float values; connect desired comparison output (Equal, Greater, etc.) to condition branch.",
        "example": "Compare HP Ratio and 0.5; connect Less Than output to Branch Condition.",
        "warning": "Types must match; inputs require float values."
    },
    {
        "type": "CompareGameObjectNode",
        "purpose": "Compares two game objects to check if they refer to the exact same instance.",
        "usage": "Connect two object inputs; connect Equal output to condition branch.",
        "example": "Compare Held Item with Target Object; connect Equal to Condition.",
        "warning": "Compares instance references, not matching names or entity types."
    }
]
