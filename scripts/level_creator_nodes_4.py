"""Level Creator Help Node Translations - Part 4 (Nodes 150 - 199)."""

NODES_150_199 = [
    {
        "type": "FindIntListValueNode",
        "purpose": "Outputs the first index of a matching value, and whether the list contains that value.",
        "usage": "Connect list and value to inputs; output provides index and Contains boolean.",
        "example": "List 'Completed Quests' and value 1 -> Find Int List Value -> Contains port connects to Branch Condition.",
        "warning": "Returns index -1 and Contains=False if not found."
    },
    {
        "type": "AppendFloatListNode",
        "purpose": "Appends a float value to a shared list.",
        "usage": "Create a float list in Level Variables and drag to canvas; connect list port to this node and trigger to append.",
        "example": "On Game Start -> Append Float List; list connected to 'Speed Multipliers', value connected to float.",
        "warning": "0-indexed. Maximum 512 items. Type mismatch or out of bounds triggers failure without modifying the list."
    },
    {
        "type": "InsertFloatListNode",
        "purpose": "Inserts a float value into a shared list at the specified index.",
        "usage": "Create a float list in Level Variables and drag to canvas; connect list port, index, value, and trigger.",
        "example": "On Game Start -> Insert Float List; list connected to 'Cooldowns', index 0, value connected to float.",
        "warning": "0-indexed. Insert allows index equal to length (appends to end). Maximum 512 items."
    },
    {
        "type": "ReplaceFloatListNode",
        "purpose": "Replaces a float value at the specified index in a shared list.",
        "usage": "Create a float list in Level Variables and drag to canvas; connect list port, index, value, and trigger.",
        "example": "On Game Start -> Replace Float List; list connected to 'Values', index 0, new value.",
        "warning": "0-indexed. The index must already exist. Maximum 512 items."
    },
    {
        "type": "GetFloatListItemNode",
        "purpose": "Reads the value at the specified index in a shared float list.",
        "usage": "Connect list and index inputs; output provides float value and IsValid boolean.",
        "example": "List 'Speeds' -> Get Float List Item (Index 0) -> Set Speed.",
        "warning": "0-indexed; Valid is False if type mismatches or index is out of bounds."
    },
    {
        "type": "FindFloatListValueNode",
        "purpose": "Outputs the first index of a matching float value, and whether the list contains that value.",
        "usage": "Connect list and float value to inputs; output provides index and Contains boolean.",
        "example": "List 'Factors' and value 1.5 -> Find Float List Value -> Contains port connects to Branch.",
        "warning": "Returns index -1 and Contains=False if not found. Floats use exact equality comparison."
    },
    {
        "type": "AppendBoolListNode",
        "purpose": "Appends a boolean value to a shared list.",
        "usage": "Create a boolean list in Level Variables and drag to canvas; connect list port to this node and trigger to append.",
        "example": "On Game Start -> Append Bool List; list connected to 'Flags', value connected to bool.",
        "warning": "0-indexed. Maximum 512 items."
    },
    {
        "type": "InsertBoolListNode",
        "purpose": "Inserts a boolean value into a shared list at the specified index.",
        "usage": "Connect list port, index, value, and trigger to insert.",
        "example": "On Game Start -> Insert Bool List; list connected to 'Flags', index 0, value true.",
        "warning": "0-indexed. Insert allows index equal to length. Maximum 512 items."
    },
    {
        "type": "ReplaceBoolListNode",
        "purpose": "Replaces a boolean value at the specified index in a shared list.",
        "usage": "Connect list port, index, value, and trigger to replace.",
        "example": "Event -> Replace Bool List; list connected to 'Flags', index 0, value false.",
        "warning": "0-indexed. Index must already exist. Maximum 512 items."
    },
    {
        "type": "GetBoolListItemNode",
        "purpose": "Reads the boolean at the specified index in a shared list.",
        "usage": "Connect list and index inputs; output provides boolean value and IsValid boolean.",
        "example": "List 'Flags' -> Get Bool List Item (Index 0) -> Branch Condition.",
        "warning": "0-indexed. Valid is False if type mismatches or index is out of bounds."
    },
    {
        "type": "FindBoolListValueNode",
        "purpose": "Outputs the first index of a matching boolean value, and whether the list contains that value.",
        "usage": "Connect list and boolean value to inputs; output provides index and Contains boolean.",
        "example": "List 'Flags' and value true -> Find Bool List Value -> Contains port connects to Branch.",
        "warning": "Returns index -1 and Contains=False if not found."
    },
    {
        "type": "AppendStringListNode",
        "purpose": "Appends a string value to a shared list.",
        "usage": "Create a string list in Level Variables and drag to canvas; connect list port to this node and trigger to append.",
        "example": "On Game Start -> Append String List; list connected to 'Quest Names', value connected to string.",
        "warning": "0-indexed. Maximum 512 items."
    },
    {
        "type": "InsertStringListNode",
        "purpose": "Inserts a string value into a shared list at the specified index.",
        "usage": "Connect list port, index, value, and trigger to insert.",
        "example": "Event -> Insert String List; list connected to 'Dialogues', index 0, value string.",
        "warning": "0-indexed. Insert allows index equal to length. Maximum 512 items."
    },
    {
        "type": "ReplaceStringListNode",
        "purpose": "Replaces a string value at the specified index in a shared list.",
        "usage": "Connect list port, index, value, and trigger to replace.",
        "example": "Event -> Replace String List; list connected to 'Dialogues', index 0, new value.",
        "warning": "0-indexed. Index must already exist. Maximum 512 items."
    },
    {
        "type": "GetStringListItemNode",
        "purpose": "Reads the string at the specified index in a shared list.",
        "usage": "Connect list and index inputs; output provides string value and IsValid boolean.",
        "example": "List 'Dialogues' -> Get String List Item (Index 0) -> Display Text.",
        "warning": "0-indexed. Valid is False if type mismatches or index is out of bounds."
    },
    {
        "type": "FindStringListValueNode",
        "purpose": "Outputs the first index of a matching string value, and whether the list contains that value.",
        "usage": "Connect list and string value to inputs; output provides index and Contains boolean.",
        "example": "List 'Completed Tasks' and value 'Boss' -> Find String List Value -> Contains connects to Branch.",
        "warning": "Returns index -1 and Contains=False if not found. String comparison is case-sensitive."
    },
    {
        "type": "AppendPlantTypeListNode",
        "purpose": "Appends a plant type value to a shared list.",
        "usage": "Create a plant type list in Level Variables and drag to canvas; connect list port to this node and trigger to append.",
        "example": "On Game Start -> Append Plant Type List; list connected to 'Seed Pool', value connected to plant type.",
        "warning": "0-indexed. Maximum 512 items."
    },
    {
        "type": "InsertPlantTypeListNode",
        "purpose": "Inserts a plant type value into a shared list at the specified index.",
        "usage": "Connect list port, index, value, and trigger to insert.",
        "example": "Event -> Insert Plant Type List; list connected to 'Seed Pool', index 0, value plant type.",
        "warning": "0-indexed. Insert allows index equal to length. Maximum 512 items."
    },
    {
        "type": "ReplacePlantTypeListNode",
        "purpose": "Replaces a plant type value at the specified index in a shared list.",
        "usage": "Connect list port, index, value, and trigger to replace.",
        "example": "Event -> Replace Plant Type List; list connected to 'Seed Pool', index 0, new value.",
        "warning": "0-indexed. Index must already exist. Maximum 512 items."
    },
    {
        "type": "GetPlantTypeListItemNode",
        "purpose": "Reads the plant type at the specified index in a shared list.",
        "usage": "Connect list and index inputs; output provides plant type and IsValid boolean.",
        "example": "List 'Seed Pool' -> Get Plant Type List Item (Index 0) -> Add Seed Card.",
        "warning": "0-indexed. Valid is False if type mismatches or index is out of bounds."
    },
    {
        "type": "FindPlantTypeListValueNode",
        "purpose": "Outputs the first index of a matching plant type value, and whether the list contains that value.",
        "usage": "Connect list and plant type to inputs; output provides index and Contains boolean.",
        "example": "List 'Banned Plants' and value Peashooter -> Find Plant Type List Value -> Contains connects to Branch.",
        "warning": "Returns index -1 and Contains=False if not found."
    },
    {
        "type": "AppendZombieTypeListNode",
        "purpose": "Appends a zombie type value to a shared list.",
        "usage": "Create a zombie type list in Level Variables and drag to canvas; connect list port to this node and trigger to append.",
        "example": "On Game Start -> Append Zombie Type List; list connected to 'Spawn Pool', value connected to zombie type.",
        "warning": "0-indexed. Maximum 512 items."
    },
    {
        "type": "InsertZombieTypeListNode",
        "purpose": "Inserts a zombie type value into a shared list at the specified index.",
        "usage": "Connect list port, index, value, and trigger to insert.",
        "example": "Event -> Insert Zombie Type List; list connected to 'Spawn Pool', index 0, value zombie type.",
        "warning": "0-indexed. Insert allows index equal to length. Maximum 512 items."
    },
    {
        "type": "ReplaceZombieTypeListNode",
        "purpose": "Replaces a zombie type value at the specified index in a shared list.",
        "usage": "Connect list port, index, value, and trigger to replace.",
        "example": "Event -> Replace Zombie Type List; list connected to 'Spawn Pool', index 0, new value.",
        "warning": "0-indexed. Index must already exist. Maximum 512 items."
    },
    {
        "type": "GetZombieTypeListItemNode",
        "purpose": "Reads the zombie type at the specified index in a shared list.",
        "usage": "Connect list and index inputs; output provides zombie type and IsValid boolean.",
        "example": "List 'Wave Zombies' -> Get Zombie Type List Item (Index 0) -> Spawn Zombie.",
        "warning": "0-indexed. Valid is False if type mismatches or index is out of bounds."
    },
    {
        "type": "FindZombieTypeListValueNode",
        "purpose": "Outputs the first index of a matching zombie type value, and whether the list contains that value.",
        "usage": "Connect list and zombie type to inputs; output provides index and Contains boolean.",
        "example": "List 'Special Zombies' and value Gargantuar -> Find Zombie Type List Value -> Contains connects to Branch.",
        "warning": "Returns index -1 and Contains=False if not found."
    },
    {
        "type": "AppendObjectListNode",
        "purpose": "Appends an object reference to a shared list.",
        "usage": "Create an object list in Level Variables and drag to canvas; connect list port to this node and trigger to append.",
        "example": "On Game Start -> Append Object List; list connected to 'Object Pool', value connected to object reference.",
        "warning": "0-indexed. Maximum 512 items."
    },
    {
        "type": "InsertObjectListNode",
        "purpose": "Inserts an object reference into a shared list at the specified index.",
        "usage": "Connect list port, index, value, and trigger to insert.",
        "example": "Event -> Insert Object List; list connected to 'Objects', index 0, value object reference.",
        "warning": "0-indexed. Insert allows index equal to length. Maximum 512 items."
    },
    {
        "type": "ReplaceObjectListNode",
        "purpose": "Replaces an object reference at the specified index in a shared list.",
        "usage": "Connect list port, index, value, and trigger to replace.",
        "example": "Event -> Replace Object List; list connected to 'Objects', index 0, new object reference.",
        "warning": "0-indexed. Index must already exist. Maximum 512 items."
    },
    {
        "type": "GetObjectListItemNode",
        "purpose": "Reads the object reference at the specified index in a shared list.",
        "usage": "Connect list and index inputs; output provides object reference and IsValid boolean.",
        "example": "List 'Spawned Markers' -> Get Object List Item (Index 0) -> Destroy Event Object.",
        "warning": "0-indexed; Valid is False if type mismatches or index is out of bounds. Returns null if object was destroyed."
    },
    {
        "type": "FindObjectListValueNode",
        "purpose": "Outputs the first index of a matching object reference, and whether the list contains that object.",
        "usage": "Connect list and object to inputs; output provides index and Contains boolean.",
        "example": "List 'Tracked Objects' and object reference -> Find Object List Value -> Contains connects to Branch.",
        "warning": "Returns index -1 and Contains=False if not found."
    },
    {
        "type": "GetListLengthNode",
        "purpose": "Reads the current number of elements in a shared list.",
        "usage": "Connect list input; output provides integer length.",
        "example": "List -> List Length -> Integer Compare (Equal to 0) -> Branch.",
        "warning": "Returns 0 if unconnected or empty."
    },
    {
        "type": "RemoveListItemNode",
        "purpose": "Removes the element at the specified index, shifting subsequent elements forward.",
        "usage": "Connect list, index, and trigger to remove item.",
        "example": "Claim Reward -> Remove List Item (Index 0); next element becomes index 0.",
        "warning": "0-indexed; routes to failure output if index is out of bounds."
    },
    {
        "type": "CopyListValuesNode",
        "purpose": "Replaces the target list's contents with the source list; both containers remain independent afterwards.",
        "usage": "Connect source list, target list, and trigger.",
        "example": "Phase Start -> Copy List: Default Reward Pool copied to Current Reward Pool.",
        "warning": "Element types must match. Copies container values; object elements still point to the same scene objects without cloning."
    },
    {
        "type": "ClearListValuesNode",
        "purpose": "Clears all elements from a shared list.",
        "usage": "Connect list and trigger to clear.",
        "example": "New Round Starts -> Clear List 'Defeated Targets This Round'.",
        "warning": "All nodes referencing the same list immediately see an empty list."
    },
    {
        "type": "GetAllZombiesNode",
        "purpose": "Captures a snapshot of all currently alive zombies on the lawn board.",
        "usage": "Connect output to For Each Zombie list to process all alive zombies.",
        "example": "All Zombies -> For Each Zombie -> Set Zombie Status (Chill).",
        "warning": "Only enumerates zombies at the moment of reading; does not continuously track. Includes both enemy and charmed zombies; filter with Zombie Split if needed."
    },
    {
        "type": "ForEachZombieNode",
        "purpose": "Outputs each alive zombie in the list sequentially, then triggers Completed when finished.",
        "usage": "Connect zombie list and trigger; 'Loop' output executes actions for each zombie; 'Completed' output triggers when done.",
        "example": "All Zombies -> Zombie List; Loop -> Modify Zombie Status; Completed -> Display Text.",
        "warning": "The input list is shallow-copied once; killing or spawning zombies during the loop will not alter the current set."
    },
    {
        "type": "SetZombieStatusNode",
        "purpose": "Sets the specified status, duration in seconds, or stacks on a zombie.",
        "usage": "Select status from dropdown. For Chill, Poison, Freeze, and Teleport, enter seconds. For Enraged/Ember, enter 0 to clear or positive to enable. For Garlic/Kelp/Freeze stacks, enter target stacks.",
        "example": "Select Chill, Value 5 -> Chills target zombie for 5 seconds upon trigger.",
        "warning": "Uses native game status logic, honoring immunities, reactions, and freeze rules. Value 0 removes status."
    },
    {
        "type": "GetZombieStatusNode",
        "purpose": "Reads remaining seconds, active flag, or stack count of a specified status on a zombie.",
        "usage": "Select status and connect zombie object input; output provides numeric value and IsActive boolean.",
        "example": "Select Freeze Stacks -> Float Compare (Greater Than or Equal to 50).",
        "warning": "Enraged/Ember returns 1 or 0; Chill/Poison/Freeze/Teleport returns remaining seconds; others return stack counts. Null object returns 0/false."
    },
    {
        "type": "CursePlantNode",
        "purpose": "Applies a specified amount of curse to a plant, or clears it with value 0.",
        "usage": "Connect target plant and trigger; enter curse value.",
        "example": "Curse Value 50 -> Adds 50 curse to the target plant.",
        "warning": "Uses native game curse mechanics; curse grows over time and can be lethal. Positive values add curse; 0 clears curse."
    },
    {
        "type": "SilencePlantNode",
        "purpose": "Pauses plant actions following standard plant silence rules.",
        "usage": "Enter duration in seconds and Force flag; connect plant and trigger.",
        "example": "Duration 3 seconds, Force False -> Attempts to silence following map and plant resistances.",
        "warning": "Outputs Completed immediately upon successful application; outputs Failed if target is null, dead, immune, or duration is invalid. Force=True bypasses resistance checks."
    },
    {
        "type": "SetPlantAttackSpeedNode",
        "purpose": "Overrides the total attack speed multiplier for the plant; 1.0 is base attack speed.",
        "usage": "Connect plant, trigger, and multiplier value.",
        "example": "Multiplier 2.0 causes attack cooldown to decrease twice as fast as base speed.",
        "warning": "Allowed range: 0.01 to 100. Overrides current total bonus; subsequent buffs or Travel entries still stack. Specific attack animations and unique skills still obey their own rules."
    },
    {
        "type": "GetPlantAttackSpeedNode",
        "purpose": "Reads the current attack speed multiplier and base attack interval of a plant.",
        "usage": "Connect plant object; outputs speed multiplier and base interval.",
        "example": "Read multiplier, multiply by 1.2, then write to Set Plant Attack Speed.",
        "warning": "If object is null or invalid, routes to failure output / default values."
    },
    {
        "type": "SetPlantAttributeCountdownNode",
        "purpose": "Sets the attribute countdown used for plant skills, growth, swallowing, etc.",
        "usage": "Remaining seconds modifies current countdown; empty is treated as 0 (completes next frame). Max seconds -1 retains current cycle; non-negative values set future countdown cycle.",
        "example": "Remaining Seconds 0, Max Seconds 5: triggers skill next frame, then uses 5 seconds for future cycles.",
        "warning": "Only affects skills that use attribute countdowns; does not change normal attack intervals."
    },
    {
        "type": "GetPlantAttributeCountdownNode",
        "purpose": "Reads current attribute countdown and maximum seconds for a plant.",
        "usage": "Connect plant object; returns current countdown and max seconds.",
        "example": "Use to create attribute cooldown UI text or trigger conditional rules.",
        "warning": "If no custom cycle was set and there is no progress bar, current countdown is returned as max seconds."
    },
    {
        "type": "TryPlantSuperSkillNode",
        "purpose": "Directly attempts to trigger a plant's Golden Coffee Bean Super Skill.",
        "usage": "Connect target plant and trigger.",
        "example": "Clicking a designated plant attempts to activate its Super Skill for free.",
        "warning": "Calls SuperSkill directly without consuming coins, upgrading silver plants, or generating coin-spending procs. Routes to failure if plant has no super skill or cannot currently activate it."
    },
    {
        "type": "UpgradeEventPlantNode",
        "purpose": "Upgrades a designated plant or grants Star Power effect.",
        "usage": "Calls native plant upgrade or plugin enhancement logic.",
        "example": "Target Tier 2, Plugin False -> Upgrades plant to Tier 2 for free.",
        "warning": "Target tier 0 - 3 must be higher than current tier. If Star Power is true, calls StarUp; only succeeds on plants supporting Star Power."
    },
    {
        "type": "SetZombieStatsNode",
        "purpose": "Sets base HP, max HP, attack power, armor HP, base speed, or scale for a zombie.",
        "usage": "Select stat to modify from dropdown, connect zombie object and enter value.",
        "example": "Select Base Speed, enter 2.0; Chill speed multipliers still apply on top.",
        "warning": "Setting base HP to 0 triggers normal death. Armor setting only affects existing armor. Scale is clamped between 0.1 and 5.0; speed is clamped between 0 and 100."
    },
    {
        "type": "GetZombieStatsNode",
        "purpose": "Reads base HP, max HP, attack power, armor HP, base speed, or scale of a zombie.",
        "usage": "Select stat and connect zombie object; base HP does not include armors.",
        "example": "Select Base HP -> Float Compare (Less Than 100).",
        "warning": "If object is null or type mismatches, outputs failure / default values."
    },
    {
        "type": "GetMoneyAmountNode",
        "purpose": "Reads the current coins in the active lawn match.",
        "usage": "Connect output to comparisons or variable setters.",
        "example": "Coins >= 1000 unlocks reward choices.",
        "warning": "Reads match coins for the current board; does not read or modify profile shop currency."
    }
]
