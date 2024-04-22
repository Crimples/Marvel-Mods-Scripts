1. Place .arc file in this folder, currently everything but 00-02 is supported, currently you cannot move skin slots from double digit slots downwards, but you can upwards. (i.e you can move skin slots from 05 to 15, but not 15 to 05)
NOTE: Keep a copy of the original .arc before modifying as it WILL be replaced at the end of the script
2. Run script
3. When it prompts for character name put EXACTLY what matches on the .arc file in the first half i.e 0040_05 would be 0040 for character's name, while Iceman_06 would be Iceman
4. Enter current skin slot This would be the second part of the .arc file after the _ i.e 0040_05 would be 05 for the sking slot, while Iceman_06 would be 06
5. Enter the requested skin slot this will be the same formatting as step 4 where you will enter the skin slot FOR THE .arc that you want. For example inputting 06 as requested sking slot will give you Slot 7 in game (due to slot 00 being first)
6. Wait for script to finish
(Optional) Remove folder and .txt file generated as part of process if not troubleshooting
7. Take modified .arc file and move it into your \ULTIMATE MARVEL VS. CAPCOM 3\nativePCx64\chr\archive\ folder
8. Enjoy

Common Problems:

-Script closed without any output?
	Incorrect CharacterName or SkinSlots specified, rarely it just happens sometimes, try again
-.arc was not modified?
	Invalid parameter provided (see list of known issues)
-Script says Python 3 required?
	Download Python 3 or later
-Game unable to pick slot?
	Ensure that the characters slots are enabled under Characters.ini or ColorExpansion.ini
-Character portraits are grey when picking character?
	Modified files changed core components (usually formatting error)
-Game crashes when picking character slot or loading game?
	-Note error message
-Game has incorrect textures loading?
	Skin Slot has uncommonly named files
-Any other issue?
	Ensure its not part of known issues

Known Issues:
-You cannot move skin slots from double digit slots downwards
-Characters with numbers in their name might break the script (STR29 i.e)
-Script only works on Python 3 and later
-Script does not work past skin slot 99 and will never work for skins 00-02
-Script has a purposeful delay that wastes time to allow script to finish making changes
-Silver and Gold Character Slots might break due to difference in naming conventions (Confirmed for Arthur and Wesker)
-Script does not account for certain variables that are rare (skinslot tied textures that require renaming) (Might have been fixed, needs more testing)
