"""Level Creator Help Node Translations - Part 5 (Nodes 200 - 240)."""

NODES_200_240 = [
    {
        "type": "AddZombieCardNode",
        "purpose": "Adds a zombie card to the current card slot, with optional price and cooldown.",
        "usage": "Enter price, cooldown seconds, and IsReady flag; connect trigger input.",
        "example": "Regular Zombie, Cost 50, Cooldown 5s, IsReady=True.",
        "warning": "Cost/Cooldown -1 reads level zombie defaults. Routes to failure if card slots are full or unavailable."
    },
    {
        "type": "DeleteZombieCardsNode",
        "purpose": "Deletes all zombie cards of the specified type from the current card slot.",
        "usage": "Select zombie type and trigger to delete.",
        "example": "Delete all Conehead Zombie cards.",
        "warning": "Supports regular card bar and I, Zombie card bar. Gallery cards not selected into card bar are not deleted. Completes normally even if 0 cards are deleted."
    },
    {
        "type": "DeleteInfoCardsNode",
        "purpose": "Deletes all info cards, or a single info card corresponding to the input object.",
        "usage": "Delete all info cards or connect card object with All=False.",
        "example": "Connect created info card object to this node with All=False.",
        "warning": "If no object is connected and All is False, 0 cards are deleted to prevent accidental deletion."
    },
    {
        "type": "SetZombieCardCooldownNode",
        "purpose": "Modifies the total cooldown and remaining cooldown of matching zombie cards in the current card slot.",
        "usage": "Select zombie type; enter total seconds and remaining seconds.",
        "example": "Total 10s, Remaining 0s -> Instantly ready, then 10s cooldown on each subsequent use.",
        "warning": "Remaining seconds cannot exceed total seconds. Only affects existing cards in the slot."
    },
    {
        "type": "ToolTypeValueNode",
        "purpose": "Selects a tool type for queries, cooldowns, and comparison nodes.",
        "usage": "Select tool type from dropdown; connect output to tool-related nodes.",
        "example": "Select Glove, connect to Set Tool Cooldown.",
        "warning": "Plant preview, zombie preview, coffee bean, etc., can be recognized as held types, but do not have tool cooldowns."
    },
    {
        "type": "GetHeldToolNode",
        "purpose": "Gets the item object and tool type currently held by the mouse cursor.",
        "usage": "Identifies shovel, glove, hammer, bucket, cannon crosshair, etc., outputting item object and tool type.",
        "example": "Tool Type output connects to Compare Tool Type to check if holding Glove.",
        "warning": "Returns 'None' and null object if empty-handed."
    },
    {
        "type": "CompareToolTypeNode",
        "purpose": "Checks whether two tool types are identical.",
        "usage": "Connect two tool types to inputs; output boolean connects to branch conditions.",
        "example": "Held Tool Type compares with 'Glove' constant.",
        "warning": "Null or invalid inputs return False."
    },
    {
        "type": "SetToolCooldownNode",
        "purpose": "Modifies the cooldown of shovel, glove, hammer, or lawnmower in this match.",
        "usage": "Select tool type, enter total cooldown and remaining cooldown seconds.",
        "example": "Glove, Total 5s, Remaining 0s -> Instantly available.",
        "warning": "Total seconds setting lasts until the tool is destroyed; remaining seconds only changes the current cooldown cycle. No Cooldown mode or IZ free cooldown rules take priority."
    },
    {
        "type": "GetToolCooldownNode",
        "purpose": "Reads the total cooldown, remaining cooldown, and existence of the specified tool.",
        "usage": "Select tool type; output provides total seconds, remaining seconds, and Exists boolean.",
        "example": "Read Glove remaining seconds and convert to text for display.",
        "warning": "Returns 0 and Exists=False if tool does not exist."
    },
    {
        "type": "WaitUntilNode",
        "purpose": "Checks condition at specified intervals, continuing execution flow once condition becomes true.",
        "usage": "Checks immediately once, then checks at each interval; True triggers Completed, False continues waiting. Reaching max check count routes to Timeout. Re-triggering replaces previous wait.",
        "example": "Int Variable >= 10 connects to Condition, Interval 0.2s; continues when variable reaches 10.",
        "warning": "Failed output indicates invalid parameters (e.g. interval < 0.1s); False condition does not trigger Failed. Exiting level or changing stage cancels waiting."
    },
    {
        "type": "RepeatUntilNode",
        "purpose": "Repeatedly executes an action until condition becomes true, then continues subsequent flow.",
        "usage": "Checks immediately once; False triggers 'Loop', then waits specified interval before checking again; True triggers 'Completed'. Reaching max checks routes to Timeout.",
        "example": "Condition connects to Int Variable >= 10; Loop connects to Variable + 1, interval 0.2s; Completed once 10 is reached.",
        "warning": "Failed indicates invalid parameters (e.g. interval < 0.1s). Exiting level or changing phase cancels loop."
    },
    {
        "type": "OnZombieClickNode",
        "purpose": "Triggers when an alive zombie is left-clicked on the lawn board.",
        "usage": "Trigger output starts actions; zombie output provides the clicked target zombie.",
        "example": "Trigger -> Damage Zombie; target zombie connects to Zombie input to create click-to-damage gameplay.",
        "warning": "Only queries colliders on valid battlefield clicks; selects nearest zombie if overlapping. Does not intercept normal card or tool placement."
    },
    {
        "type": "OnWorldPlantEffectNode",
        "purpose": "Listens for full-screen Ice-shroom or single-row Jalapeno effects.",
        "usage": "Select effect from dropdown; Row output indicates row of effect (-1 for full-screen).",
        "example": "Select Jalapeno; Row output connects to spawn or cleanup nodes.",
        "warning": "Ice-shroom is full-screen, returning Row=-1. Listens to both plant actions and node calls; avoid triggering the same effect recursively."
    },
    {
        "type": "SetZombieHouseRuleNode",
        "purpose": "Controls whether zombies entering the house trigger the default defeat game-over.",
        "usage": "Connect trigger and set Defeat On House flag.",
        "example": "Level Start -> Set Zombie House Rule (Defeat = False); customize win/loss via visual scripting.",
        "warning": "Only modifies the house breach trigger; other defeat sources (e.g., protected plant dies, manual quit) remain unchanged. Disabled zombies keep walking and despawn past the left border."
    },
    {
        "type": "SetWaveCountdownPausedNode",
        "purpose": "Pauses automatic countdown to the next wave; already spawned zombies continue acting.",
        "usage": "Connect trigger and set Paused flag.",
        "example": "Dialogue starts -> Set Wave Countdown Paused (True); Dialogue ends -> Set Paused (False).",
        "warning": "Pauses wave timer and low-health early spawns; does not stop zombies already spawning in current wave. Auto-resumes when event graph stops."
    },
    {
        "type": "DeleteGridItemsNode",
        "purpose": "Deletes graves, craters, ladders, or ice blocks from the specified grid tile.",
        "usage": "Select obstacle type; enter row and column coordinates.",
        "example": "Select Crater, Row 2, Column 3 -> Removes crater at that tile.",
        "warning": "Calls Die logic and clears grid occupation. 'Ice Block' refers to tile ice blocks, not Zomboni ice trails. 0-indexed rows and columns."
    },
    {
        "type": "ChangeEventMusicNode",
        "purpose": "Plays selected in-game background music.",
        "usage": "Select music track from dropdown and connect trigger.",
        "example": "Phase Enter event -> Change Event Music; selects battle BGM for that phase.",
        "warning": "Only uses loaded in-game tracks. Do not call every frame to avoid restarting track repeatedly."
    },
    {
        "type": "RemoveTravelEntryNode",
        "purpose": "Removes a specified Travel modifier in this match, stopping ongoing effects and refreshing synergies.",
        "usage": "Select modifier category; enter internal name, ID, or localized display title.",
        "example": "Select Zombie Modifier, enter 'Unstoppable' to remove the modifier.",
        "warning": "Unregisters listener and stops continuous cycles. Synergies and buffs update dynamically. Handed-out resources or cards are not revoked."
    },
    {
        "type": "GetPlantBasicComponentsNode",
        "purpose": "Recursively unpacks a fusion plant formula, outputting a list of basic component plant types.",
        "usage": "Connect plant type input; output provides list of base plant types.",
        "example": "Input Fusion Plant -> For Each Plant Type to inspect ingredients; duplicate components are preserved.",
        "warning": "Uses static fusion recipes, not randomized mutation history. Returns self if plant has no fusion recipe."
    },
    {
        "type": "MakeVector3Node",
        "purpose": "Combines three floats into a 3D world coordinate vector.",
        "usage": "Connect X, Y, Z float values; output connects to position inputs.",
        "example": "X=0, Y=1, Z=0 -> Position port of Create Event Object.",
        "warning": "Invalid numbers return default Vector3.zero."
    },
    {
        "type": "GetMouseWorldPositionNode",
        "purpose": "Reads the mouse cursor's world position and corresponding grid tile on the lawn board.",
        "usage": "Output provides Vector3 position, Row, and Column.",
        "example": "Position connects to Create Event Object; Row/Column connect to grid actions.",
        "warning": "Row and Column may be out of bounds if mouse is outside the lawn board."
    },
    {
        "type": "CreateEventObjectNode",
        "purpose": "Creates a lightweight empty object managed by the event graph, with optional plant icon decoration.",
        "usage": "Select decorative plant icon and enter world position; output provides object reference.",
        "example": "Select Peashooter icon, create decorative marker at mouse position.",
        "warning": "Scene marker only; does not perform attacks or occupy grid tiles. Maximum 256 alive objects per graph; cleaned up when graph exits."
    },
    {
        "type": "BindObjectNode",
        "purpose": "Saves an object reference by name for later event retrieval.",
        "usage": "Connect object reference, enter name string, and trigger.",
        "example": "Name 'Marker1' -> Retrieve later via String to Object.",
        "warning": "Reusing existing name overwrites previous binding. Name is only valid within current graph run. Pooled bullets cannot be bound as persistent objects."
    },
    {
        "type": "ObjectToStringNode",
        "purpose": "Generates a unique runtime reference token string for an object.",
        "usage": "Connect object; output string provides runtime reference token.",
        "example": "Store object reference string in a String List, then resolve later with String to Object.",
        "warning": "Token is a runtime reference, not an object name or persistent save ID. Returns empty string for invalid/destroyed objects."
    },
    {
        "type": "StringToObjectNode",
        "purpose": "Resolves an object from its runtime reference string or bound object name.",
        "usage": "Enter reference string or bound name; output provides object reference.",
        "example": "String 'Marker1' -> Resolves object saved with Bind Object.",
        "warning": "Returns null if expired, destroyed, or from a different match."
    },
    {
        "type": "PlantToObjectNode",
        "purpose": "Converts a plant instance into a generic scene object reference.",
        "usage": "Connect plant input; output provides object reference.",
        "example": "Use for object binding, object lists, or reading transform coordinates.",
        "warning": "Returns null if plant is null or destroyed."
    },
    {
        "type": "ObjectToPlantNode",
        "purpose": "Retrieves the Plant component from a scene object.",
        "usage": "Connect object input; output provides plant instance.",
        "example": "Retrieve item from Object List -> Object to Plant -> Combat Action.",
        "warning": "Returns null if object has no plant component or is invalid."
    },
    {
        "type": "ZombieToObjectNode",
        "purpose": "Converts a zombie instance into a generic scene object reference.",
        "usage": "Connect zombie input; output provides object reference.",
        "example": "Use for object binding, object lists, or reading transform coordinates.",
        "warning": "Returns null if zombie is null or destroyed."
    },
    {
        "type": "ObjectToZombieNode",
        "purpose": "Retrieves the Zombie component from a scene object.",
        "usage": "Connect object input; output provides zombie instance.",
        "example": "Retrieve item from Object List -> Object to Zombie -> Combat Action.",
        "warning": "Returns null if object has no zombie component or is invalid."
    },
    {
        "type": "GetObjectTransformNode",
        "purpose": "Reads the world position, scale, and existence state of an object.",
        "usage": "Connect object input; output provides Position Vector3, Scale Vector3, and Exists boolean.",
        "example": "Read plant position as spawn coordinate for decorative markers.",
        "warning": "Returns default zero vectors and Exists=False if object is null."
    },
    {
        "type": "SetEventObjectTransformNode",
        "purpose": "Moves and scales decorative marker objects created by Create Event Object.",
        "usage": "Connect event object, enter new Position and Scale multiplier.",
        "example": "Move marker to mouse position with Scale 0.5.",
        "warning": "Only affects decorative objects created by the event graph. For plants/zombies use dedicated move nodes."
    },
    {
        "type": "DestroyEventObjectNode",
        "purpose": "Destroys a scene marker object created by the current event graph.",
        "usage": "Connect event object and trigger to destroy.",
        "example": "Destroy temporary bound marker when phase completes.",
        "warning": "Only allowed for event graph-owned objects. For plants/zombies/cards use their native removal nodes."
    },
    {
        "type": "BulletTypeValueNode",
        "purpose": "Selects an in-game bullet type.",
        "usage": "Select bullet type from dropdown; output connects to bullet nodes.",
        "example": "Bullet_pea is regular pea; same bullet type can be fired by plants or custom sources.",
        "warning": "Fails to shoot if resources are unloaded. Projectiles fly in straight lines at specified angles."
    },
    {
        "type": "ShootEventBulletNode",
        "purpose": "Fires a bullet in a given direction from a specified grid tile or mouse position.",
        "usage": "Connect bullet type; enter row, column, damage, speed, angle, and scale.",
        "example": "Row 2, Col 3.5, Damage 20, Speed 6, Angle 0 (Right), Scale 1.",
        "warning": "0-indexed rows/columns. Angle 0 is Right, 90 Up, 180 Left, 270 Down. Recycled when leaving screen or after 20s."
    },
    {
        "type": "ModifyEventBulletNode",
        "purpose": "Modifies scale, speed, damage, or direction of an active event bullet.",
        "usage": "Select property to modify, connect bullet handle and enter new value.",
        "example": "Select Angle, Value 90 -> Turns bullet upward.",
        "warning": "Routes to failure if bullet has already despawned or been recycled."
    },
    {
        "type": "ChangeEventMapNode",
        "purpose": "Switches Day/Night background within compatible terrain, preserving board entities and ice trails.",
        "usage": "Select target map stage; triggers background transition.",
        "example": "Phase event in Day map -> Select Night -> Transitions map to Night.",
        "warning": "Supports Day/Night, Day_6/Night_6, Pool/NightPool, Roof/NightRoof, Travel Roof phases, Travel Pool phases, SnowPool Day/Night. At least 1s cooldown. Does not alter sun, entities, waves, or speed."
    },
    {
        "type": "ForEachAllZombiesNode",
        "purpose": "Sequentially processes every alive zombie currently on the lawn board.",
        "usage": "Connect trigger; 'Loop' output triggers for each zombie, providing current zombie object.",
        "example": "Loop -> Apply Zombie Status; Target Zombie connects to Zombie input.",
        "warning": "Takes snapshot upon trigger; zombies spawned during loop are processed in next trigger. Dead zombies are skipped. Includes charmed zombies."
    },
    {
        "type": "SetPlantAttackIntervalNode",
        "purpose": "Sets the base attack interval of a designated plant.",
        "usage": "Connect plant and enter interval in seconds.",
        "example": "Enter 0.5s -> Plant base delay between attacks becomes 0.5 seconds.",
        "warning": "Allowed range: 0.05 to 3600 seconds. Attack speed buffs still scale on top. Only affects plants using base attack interval."
    },
    {
        "type": "FeedGoldenBeanNode",
        "purpose": "Invokes the native Golden Coffee Bean feeding sequence on a plant.",
        "usage": "Connect plant and trigger; 'Success' output indicates whether feeding succeeded.",
        "example": "Trigger -> Feed Golden Bean; checks Success output to confirm.",
        "warning": "Does not require player to pick up bean. Honors coin cost, upgradeable types, and super skill conditions."
    },
    {
        "type": "StringVariableNode",
        "purpose": "References a shared string variable from the Level Variables panel.",
        "usage": "Create string variable in Level Variables panel and drag to canvas; connects to Get or Set String Variable.",
        "example": "String Variable -> Get String -> Display Text.",
        "warning": "Dragging same variable multiple times shares value. Template insertion creates independent copy."
    },
    {
        "type": "ListVariableNode",
        "purpose": "References a shared typed list from the Level Variables panel.",
        "usage": "Create list in Level Variables panel, choose element type, fill initial values, then drag to canvas.",
        "example": "Integer List -> List Length; Trigger -> Append to list -> Read length again.",
        "warning": "0-indexed, max 512 items. Element type must match operating node."
    }
]
