"""Level Creator Help Node Translations - Part 3 (Nodes 100 - 149)."""

NODES_100_149 = [
    {
        "type": "IntValueNode",
        "purpose": "Provides a constant integer to multiple nodes.",
        "usage": "Enter the value in the node, then connect the output to inputs of the same type.",
        "example": "Enter 25, connect to an action input requiring this value; use an event to trigger the action.",
        "warning": "Constants do not require a trigger. If only setting an unconnected input, you can also use 'Set Input Value' on the toolbar directly."
    },
    {
        "type": "FloatValueNode",
        "purpose": "Provides a constant float to multiple nodes.",
        "usage": "Enter the value in the node, then connect the output to inputs of the same type.",
        "example": "Enter 0.5, connect to an action input requiring this value; use an event to trigger the action.",
        "warning": "Constants do not require a trigger. If only setting an unconnected input, you can also use 'Set Input Value' on the toolbar directly."
    },
    {
        "type": "BoolValueNode",
        "purpose": "Provides a constant boolean to multiple nodes.",
        "usage": "Enter the value in the node, then connect the output to inputs of the same type.",
        "example": "Enter true, connect to an action input requiring this value; use an event to trigger the action.",
        "warning": "Constants do not require a trigger. If only setting an unconnected input, you can also use 'Set Input Value' on the toolbar directly."
    },
    {
        "type": "StringValueNode",
        "purpose": "Provides a constant string to multiple nodes.",
        "usage": "Enter the value in the node, then connect the output to inputs of the same type.",
        "example": "Enter 'Boss Incoming!', connect to an action input requiring this value; use an event to trigger the action.",
        "warning": "Constants do not require a trigger. If only setting an unconnected input, you can also use 'Set Input Value' on the toolbar directly."
    },
    {
        "type": "AddNode",
        "purpose": "Calculates the addition of two numbers.",
        "usage": "Connect two numbers of the same type; connect the result to an action, comparison, or variable setting input.",
        "example": "Inputs 2 and 3 yield addition result 5; use an event to trigger actions reading the result.",
        "warning": "Do not mix integer and float ports. Avoid division or modulo by 0. Integer division truncates decimals."
    },
    {
        "type": "SubtractNode",
        "purpose": "Calculates the subtraction of two numbers.",
        "usage": "Connect two numbers of the same type; connect the result to an action, comparison, or variable setting input.",
        "example": "Inputs 5 and 2 yield subtraction result 3; use an event to trigger actions reading the result.",
        "warning": "Do not mix integer and float ports. Avoid division or modulo by 0. Integer division truncates decimals."
    },
    {
        "type": "MultiplyNode",
        "purpose": "Calculates the multiplication of two numbers.",
        "usage": "Connect two numbers of the same type; connect the result to an action, comparison, or variable setting input.",
        "example": "Inputs 2 and 3 yield multiplication result 6; use an event to trigger actions reading the result.",
        "warning": "Do not mix integer and float ports. Avoid division or modulo by 0. Integer division truncates decimals."
    },
    {
        "type": "DivideNode",
        "purpose": "Calculates the division of two numbers.",
        "usage": "Connect two numbers of the same type; connect the result to an action, comparison, or variable setting input.",
        "example": "Inputs 6 and 2 yield division result 3; use an event to trigger actions reading the result.",
        "warning": "Do not mix integer and float ports. Avoid division or modulo by 0. Integer division truncates decimals."
    },
    {
        "type": "IntAddNode",
        "purpose": "Calculates the addition of two integers.",
        "usage": "Connect two integers; connect the result to an action, comparison, or variable setting input.",
        "example": "Inputs 2 and 3 yield integer addition result 5; use an event to trigger actions reading the result.",
        "warning": "Do not mix integer and float ports. Avoid division or modulo by 0. Integer division truncates decimals."
    },
    {
        "type": "IntSubtractNode",
        "purpose": "Calculates the subtraction of two integers.",
        "usage": "Connect two integers; connect the result to an action, comparison, or variable setting input.",
        "example": "Inputs 5 and 2 yield integer subtraction result 3; use an event to trigger actions reading the result.",
        "warning": "Do not mix integer and float ports. Avoid division or modulo by 0. Integer division truncates decimals."
    },
    {
        "type": "IntMultiplyNode",
        "purpose": "Calculates the multiplication of two integers.",
        "usage": "Connect two integers; connect the result to an action, comparison, or variable setting input.",
        "example": "Inputs 2 and 3 yield integer multiplication result 6; use an event to trigger actions reading the result.",
        "warning": "Do not mix integer and float ports. Avoid division or modulo by 0. Integer division truncates decimals."
    },
    {
        "type": "IntDivideNode",
        "purpose": "Calculates the division of two integers.",
        "usage": "Connect two integers; connect the result to an action, comparison, or variable setting input.",
        "example": "Inputs 7 and 2 yield integer division result 3; use an event to trigger actions reading the result.",
        "warning": "Do not mix integer and float ports. Avoid division or modulo by 0. Integer division truncates decimals."
    },
    {
        "type": "IntModuloNode",
        "purpose": "Calculates the modulo (remainder) of two integers.",
        "usage": "Connect two integers; connect the result to an action, comparison, or variable setting input.",
        "example": "Inputs 7 and 2 yield integer modulo result 1; use an event to trigger actions reading the result.",
        "warning": "Do not mix integer and float ports. Avoid division or modulo by 0. Integer division truncates decimals."
    },
    {
        "type": "StringConcatNode",
        "purpose": "Concatenates two text strings in order.",
        "usage": "Connect two strings to inputs; connect the output to Display Text.",
        "example": "Concatenate 'Current Reward: ' and 'Sun', then trigger display.",
        "warning": "Numbers must be converted to strings first. Concatenation does not automatically insert spaces or line breaks."
    },
    {
        "type": "RandomIntNode",
        "purpose": "Picks a random integer within a range.",
        "usage": "Enter minimum and maximum values; connect output to reward amount or other numeric input.",
        "example": "Range set to 10 - 50 -> Sun amount gained; floats should be converted to integers as needed.",
        "warning": "May re-randomize every time it is read. If multiple actions need the same value, store it in a variable first. Range is inclusive of both bounds."
    },
    {
        "type": "RandomFloatNode",
        "purpose": "Picks a random float within a range.",
        "usage": "Enter minimum and maximum values; connect output to duration or other numeric input.",
        "example": "Range set to 1.5 - 5.0 -> Timer duration or multiplier.",
        "warning": "May re-randomize every time it is read. If multiple actions need the same value, store it in a variable first."
    },
    {
        "type": "IntVariableNode",
        "purpose": "References a shared integer variable from the Level Variables panel.",
        "usage": "Drag in from the Level Variables panel; connect the variable port to the corresponding Get or Set node.",
        "example": "Variable Reference -> Get Integer -> Compare or Calculate.",
        "warning": "Dragging the same variable in multiple times still shares the same value. Normal copy shares original variable; template insertion copies an independent variable."
    },
    {
        "type": "GetIntVariableValueNode",
        "purpose": "Reads the current value stored in an integer variable.",
        "usage": "Connect variable input to the variable reference dragged from Level Variables panel; output provides the raw value.",
        "example": "Variable Reference -> Get Value -> Add / Compare -> Subsequent Action.",
        "warning": "Has no trigger port; only reads the current value. Reading does not automatically execute upstream set actions."
    },
    {
        "type": "SetIntVariableValueNode",
        "purpose": "Stores a new value into a shared integer variable.",
        "usage": "Connect variable reference, new value, and trigger; connect completion output to subsequent actions that depend on the new value.",
        "example": "Event -> Set Variable; Completed -> Display or check updated result.",
        "warning": "Connecting a new value without triggering will not write to the variable. Variable output can daisy-chain to other Set nodes, but action sequence still requires execution flow lines."
    },
    {
        "type": "FloatVariableNode",
        "purpose": "References a shared float variable from the Level Variables panel.",
        "usage": "Drag in from the Level Variables panel; connect the variable port to the corresponding Get or Set node.",
        "example": "Variable Reference -> Get Float -> Compare or Calculate.",
        "warning": "Dragging the same variable in multiple times still shares the same value. Normal copy shares original variable; template insertion copies an independent variable."
    },
    {
        "type": "GetFloatVariableValueNode",
        "purpose": "Reads the current value stored in a float variable.",
        "usage": "Connect variable input to the variable reference dragged from Level Variables panel; output provides the raw value.",
        "example": "Variable Reference -> Get Value -> Add / Compare -> Subsequent Action.",
        "warning": "Has no trigger port; only reads the current value. Reading does not automatically execute upstream set actions."
    },
    {
        "type": "SetFloatVariableValueNode",
        "purpose": "Stores a new value into a shared float variable.",
        "usage": "Connect variable reference, new value, and trigger; connect completion output to subsequent actions that depend on the new value.",
        "example": "Event -> Set Variable; Completed -> Display or check updated result.",
        "warning": "Connecting a new value without triggering will not write to the variable. Variable output can daisy-chain to other Set nodes, but action sequence still requires execution flow lines."
    },
    {
        "type": "BoolVariableNode",
        "purpose": "References a shared boolean variable from the Level Variables panel.",
        "usage": "Drag in from the Level Variables panel; connect the variable port to the corresponding Get or Set node.",
        "example": "Variable Reference -> Get Bool -> Compare or Branch.",
        "warning": "Dragging the same variable in multiple times still shares the same value. Normal copy shares original variable; template insertion copies an independent variable."
    },
    {
        "type": "GetBoolVariableValueNode",
        "purpose": "Reads the current value stored in a boolean variable.",
        "usage": "Connect variable input to the variable reference dragged from Level Variables panel; output provides the raw boolean.",
        "example": "Variable Reference -> Get Value -> Branch Condition -> Subsequent Action.",
        "warning": "Has no trigger port; only reads the current value. Reading does not automatically execute upstream set actions."
    },
    {
        "type": "SetBoolVariableValueNode",
        "purpose": "Stores a new value into a shared boolean variable.",
        "usage": "Connect variable reference, new value, and trigger; connect completion output to subsequent actions that depend on the new value.",
        "example": "Event -> Set Variable; Completed -> Display or check updated result.",
        "warning": "Connecting a new value without triggering will not write to the variable."
    },
    {
        "type": "IntToFloatNode",
        "purpose": "Converts an integer to a float type.",
        "usage": "Integer input, float output connects to ports requiring floats.",
        "example": "Integer 5 -> Int to Float -> Wait Duration.",
        "warning": "Value 5 becomes 5.0; it will not scale to 0.05."
    },
    {
        "type": "FloatToIntNode",
        "purpose": "Converts a float to an integer, truncating decimal digits.",
        "usage": "Float input, integer output connects to counters, Sun amount, etc.",
        "example": "2.9 converts to 2, then passed to inputs requiring integers.",
        "warning": "Truncates towards zero, does not round. Negative numbers also truncate towards zero."
    },
    {
        "type": "FloatToStringNode",
        "purpose": "Converts a number to text for display.",
        "usage": "Input float; set number of decimal places to keep in the node.",
        "example": "Numeric Value -> Float to String -> Display Text port.",
        "warning": "Output is text and cannot be used in arithmetic calculations directly. Decimal places range from 0 to 6."
    },
    {
        "type": "VariableNode",
        "purpose": "Base implementation of variable references, used internally by specific variable nodes.",
        "usage": "Create Int, Float, or Bool variables from the Level Variables panel; do not create this base node directly.",
        "example": "Use Integer Variable Reference -> Get Integer.",
        "warning": "Not present in the right-click create menu; not intended as an independent user node."
    },
    {
        "type": "GetStringVariableValueNode",
        "purpose": "Reads the current text stored in a shared string variable.",
        "usage": "Connect variable input to a string variable reference; output provides the stored text.",
        "example": "String Variable Reference -> Get String -> Display Text content.",
        "warning": "Returns an empty string if unconnected. Reading does not execute write operations."
    },
    {
        "type": "SetStringVariableValueNode",
        "purpose": "Modifies a shared string variable upon trigger.",
        "usage": "Connect variable reference, new text, and trigger input.",
        "example": "On Game Start -> Set String; variable connected to 'Objective Text', new value set to 'Defend the Boss'.",
        "warning": "If object is null, type mismatches, or input is out of bounds, failure output/default value is used."
    },
    {
        "type": "IntVariableArithmeticNode",
        "purpose": "Performs add, subtract, multiply, divide, or modulo directly on a shared integer variable in one trigger.",
        "usage": "Connect variable reference and trigger; select operation in node dropdown.",
        "example": "Zombie Dies -> Int Variable Arithmetic; select 'Add', operand set to 1 to increment counter.",
        "warning": "Division by zero or overflow routes to failure output, leaving original value unchanged. Integer division truncates towards 0. Default operand is 1 if empty."
    },
    {
        "type": "FloatVariableArithmeticNode",
        "purpose": "Performs add, subtract, multiply, divide, or modulo directly on a shared float variable in one trigger.",
        "usage": "Connect variable reference and trigger; select operation in node dropdown.",
        "example": "Zombie Dies -> Float Variable Arithmetic; select 'Add', operand set to 1.0 to increment counter.",
        "warning": "Division by zero or overflow routes to failure output, leaving original value unchanged. Default operand is 1.0 if empty."
    },
    {
        "type": "PowerNode",
        "purpose": "Calculates power of a number.",
        "usage": "Connect base value and exponent; output provides power result.",
        "example": "Base 2, Exponent 3 -> Power result 8.",
        "warning": "For logarithmic operations use the Logarithm node. Unrepresentable results return 0 with Valid=False."
    },
    {
        "type": "LogarithmNode",
        "purpose": "Calculates logarithm with a specified base for finite floats.",
        "usage": "Connect value and base; output provides logarithm result.",
        "example": "Value 8, Base 2 -> Logarithm result 3.",
        "warning": "Logarithm requires value and base > 0, base != 1. Unrepresentable results return 0 with Valid=False."
    },
    {
        "type": "IntToBoolNode",
        "purpose": "Evaluates 0 as False, and any other non-zero integer as True.",
        "usage": "Connect integer to input; output boolean connects to branch conditions.",
        "example": "Integer Count -> Int to Bool -> Branch Condition.",
        "warning": "Negative numbers also evaluate to True."
    },
    {
        "type": "FloatToBoolNode",
        "purpose": "Evaluates 0.0 as False, and other finite non-zero floats as True.",
        "usage": "Connect float to input; output boolean connects to branch conditions.",
        "example": "Float Value -> Float to Bool -> Branch Condition.",
        "warning": "Float NaN and Infinity both evaluate to False. Negative numbers evaluate to True."
    },
    {
        "type": "IntToStringNode",
        "purpose": "Converts an integer to readable text.",
        "usage": "Connect integer to input; string output connects to text display nodes.",
        "example": "Integer -> Int to String -> Set String.",
        "warning": "Numbers use fixed-point decimal format."
    },
    {
        "type": "StringToIntNode",
        "purpose": "Parses a string into an integer, outputting the result and whether parsing succeeded.",
        "usage": "Connect string input; output provides integer value and IsValid boolean.",
        "example": "String '25' -> String to Int -> Sun Amount; check Valid output first.",
        "warning": "Empty, invalid, or out-of-range strings return default 0 with Valid=False. For ASCII conversion use String to ASCII node."
    },
    {
        "type": "StringToFloatNode",
        "purpose": "Parses a string into a float, outputting the result and whether parsing succeeded.",
        "usage": "Connect string input; output provides float value and IsValid boolean.",
        "example": "String '1.5' -> String to Float -> Timer Duration; check Valid output first.",
        "warning": "Empty or non-numeric strings return default 0.0 with Valid=False."
    },
    {
        "type": "PlantTypeToStringNode",
        "purpose": "Converts a plant type enum to readable text.",
        "usage": "Connect plant type input; output string provides enum identifier name.",
        "example": "Plant Type -> Plant Type to String -> Set String.",
        "warning": "Outputs internal enum member name (e.g., 'Peashooter'), not localized display name."
    },
    {
        "type": "StringToPlantTypeNode",
        "purpose": "Parses a string or enum name into a plant type, outputting the type and validity.",
        "usage": "Connect string to input; output provides Plant Type and IsValid boolean.",
        "example": "String 'Peashooter' -> String to Plant Type -> Spawn Plant; check Valid output first.",
        "warning": "Blank, invalid names, or unrecognized IDs return default with Valid=False."
    },
    {
        "type": "ZombieTypeToStringNode",
        "purpose": "Converts a zombie type enum to readable text.",
        "usage": "Connect zombie type input; output string provides enum identifier name.",
        "example": "Zombie Type -> Zombie Type to String -> Set String.",
        "warning": "Outputs internal enum member name (e.g., 'Zombie'), not localized display name."
    },
    {
        "type": "StringToZombieTypeNode",
        "purpose": "Parses a string or enum name into a zombie type, outputting the type and validity.",
        "usage": "Connect string to input; output provides Zombie Type and IsValid boolean.",
        "example": "String 'Zombie' -> String to Zombie Type -> Spawn Zombie; check Valid output first.",
        "warning": "Blank, invalid names, or unrecognized IDs return default with Valid=False."
    },
    {
        "type": "StringToAsciiNode",
        "purpose": "Reads the ASCII code of a character at the specified index in a string (0-indexed).",
        "usage": "Connect string and index; output provides integer ASCII code.",
        "example": "String 'A', Index 0 -> ASCII 65.",
        "warning": "Only accepts ASCII characters 0 - 127. Non-ASCII characters return Valid=False."
    },
    {
        "type": "AsciiToStringNode",
        "purpose": "Converts an ASCII code (0 - 127) into a single-character string.",
        "usage": "Connect integer ASCII code; output provides single-character string.",
        "example": "ASCII 65 -> 'A'.",
        "warning": "Out-of-range values return empty string. Control characters may be invisible."
    },
    {
        "type": "AppendIntListNode",
        "purpose": "Appends an integer value to a shared list.",
        "usage": "Create an integer list in Level Variables and drag to canvas; connect list port to this node and trigger to append.",
        "example": "On Game Start -> Append Int List; list connected to 'Reward Pool', value connected to constant or calculated int.",
        "warning": "0-indexed. Maximum 512 items. Type mismatch or out of bounds triggers failure output without modifying the list."
    },
    {
        "type": "InsertIntListNode",
        "purpose": "Inserts an integer value into a shared list at the specified index.",
        "usage": "Create an integer list in Level Variables and drag to canvas; connect list port, index, value, and trigger.",
        "example": "On Game Start -> Insert Int List; list connected to 'Reward Pool', index 0, value connected to int.",
        "warning": "0-indexed. Insert allows index equal to length (appends to end). Maximum 512 items. Type mismatch or out of bounds triggers failure without modifying the list."
    },
    {
        "type": "ReplaceIntListNode",
        "purpose": "Replaces an integer value at the specified index in a shared list.",
        "usage": "Create an integer list in Level Variables and drag to canvas; connect list port, index, value, and trigger.",
        "example": "On Game Start -> Replace Int List; list connected to 'Reward Pool', index 0, new value.",
        "warning": "0-indexed. The index must already exist. Maximum 512 items. Type mismatch or out of bounds triggers failure without modifying the list."
    },
    {
        "type": "GetIntListItemNode",
        "purpose": "Reads the value at the specified index in a shared integer list.",
        "usage": "Connect list and index inputs; output provides the integer value and IsValid boolean.",
        "example": "List 'Reward Amounts' -> Get Int List Item (Index 0) -> Gain Sun.",
        "warning": "0-indexed. If type mismatches or index is out of bounds, Valid is False."
    }
]
