#MenuTitle: Name Guidelines
# -*- coding: utf-8 -*-
__doc__="""
Name selected Guidelines via input. Just leave input empty to delete names.
"""

from robofab.interface.all.dialogs import AskString

count = 0
arrayOfValids = []
myLayer = Glyphs.font.selectedLayers[0]
myGuides = myLayer.guides

## looking for selected guidline
for x in myGuides:
	if myGuides[count].selected:
		mySelGuide = myGuides[count]
		arrayOfValids.append(count)
	count = count + 1
 
## if a guideline is selected
if mySelGuide:	
	myName = AskString("Type a Name for this Guideline: ")
	for x in arrayOfValids:
		x = x - 1
		y = arrayOfValids[x]
		myGuides[y].name = myName
else:
	Message('Message','Please make sure you have select a Guideline')