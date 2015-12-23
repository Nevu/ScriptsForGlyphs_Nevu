#MenuTitle: Delete Guideline Names
# -*- coding: utf-8 -*-
__doc__="""
Deletes all Guideline Names
"""
count = 0
myLayer = Glyphs.font.selectedLayers[0]
myGuides = myLayer.guides

for x in myGuides:
	myGuides[count].name = None
	count = count + 1
