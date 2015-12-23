#MenuTitle: Make HTML Web Glyphtable v1.1
# encoding: utf-8

#Version 1.0
__doc__="""
This script generates html/css-files for using your font in web
"""

#  updated v.1.1 (06-27-2015)
#  -make it possible to scale the font-size
#  -changes 'icon_x' to 'icon-x' names


import re
import os
import os.path
import GlyphsApp
from time import *
from vanilla import dialogs
from robofab.interface.all.dialogs import *

Glyphs.clearLog()


### use this to set your icon-size compared to text -- try out in fonts.css | class .icons | line xy
myIconSize = str('20px') # f.e. 'initial', '12px', '1em', etc.

### set the text-sizes
myTextSize = str('12px')

### use this to set your view-size in icon-panels -- unlock and try out in styles.css | class .icon-box | line xy
myViewSize = str('50px') # f.e. 'initial', '12px', '1em', etc.

myLayers = Glyphs.font.selectedLayers
lt = localtime()

myGoodReportlist = []
myBadReportlist = []
myFontCssList = []
myHtmlList = []

myHtmlOut = ""
myCssOut = ""
myFontCssOut = ""


#LOOKING WETHER THE GLYPHS_FILE IS SAVED (NEED IT FOR GENERATING FILES)

try:
	myGFilePath = Glyphs.font.filepath
except:
	myGFilePath = ""
	
myPath = os.path.dirname(myGFilePath)+'/'

#SET UP DIRECTORY- AND FILE-SPECS

myDir = myPath+Glyphs.font.familyName+'_glyphtable'
myDirStyles = myDir+'/styles'
myDirFonts = myDir+'/fonts'

myHtmlFileName = myDir+'/'+Glyphs.font.familyName+'_glyphtable.html'
myCssFileName = myDirStyles+'/style.css'
myFontCssFileName = myDirStyles+'/fonts.css'


#IF THERE IS AN INSTANCE A CUSTOM-PARAMETER-NAME, USE IT

if len(Glyphs.font.instances) > 0:
	if bool(Glyphs.font.instances[0].customParameters['fileName']) == True:
		myFontExportName = str(Glyphs.font.instances[0].customParameters['fileName'])
	else:
		myFontExportName = (str(Glyphs.font.familyName+'-'+Glyphs.font.instances[0].name)).replace(' ', '')
else:
	myFontExportName = str(Glyphs.font.familyName).replace(' ', '')+'-'+str(Glyphs.font.masters[0].name)

Glyphs.font.disableUpdateInterface()

#IF THERE IS PATH TO SAVE AND A VALID SELECTION RUN 

if len(myGFilePath) > 0:
	if myLayers != None:
	
	
	##############################################
	
	#			VALIDATION, GET SNIPPETS FOR SELECTION
	
	##############################################
	
	
	# VALIDATE HTML, WRITE HTML-LIST
	
		for thisLayer in myLayers:
			thisGlyph = thisLayer.parent
	
			if len(thisLayer.components) > 0 or len(thisLayer.paths) > 0:
				if thisGlyph.export == True\
				and not thisGlyph.unicode == True\
				and not thisGlyph.unicode == None\
				and not thisGlyph.unicode == '00AD':
	
					myDeci = int(str(thisGlyph.unicode), 16)
					myHtmlList.append(str(
"""
				<div class='icon-panel'>
					<p class='icon-box icons article' data-icon='&#%s;'></p>
					<div class='description_box'>
					<strong>%s</strong><br>&amp;#%s; &mdash; i-%s</div>
				</div>
""" 
					% (myDeci, thisGlyph.name, myDeci, thisGlyph.name.lower())
					))
	
	
	# VALIDATE FONTCSS, WRITE FONTCSS-LIST
	
		for thisLayer in myLayers:
			thisGlyph = thisLayer.parent
			if len(thisLayer.components) > 0 or len(thisLayer.paths) > 0\
			and thisGlyph.export == True\
			and thisGlyph.unicode != None\
			and thisGlyph.unicode != '': 
				
				myFontCssList.append(str(
"""
	.i-%s:before {
	content: '\%s';
	}
"""\
				% (thisGlyph.name.lower(),str(thisLayer.parent.unicode))
				))
	
	
	##############################################
	
	#			GET REPORT LISTS
	
	##############################################
	
	
		for thisLayer in myLayers:
			thisGlyph = thisLayer.parent
	
			if len(thisLayer.components) > 0 or len(thisLayer.paths) > 0:
				if thisGlyph.export == True\
				and not thisGlyph.unicode == True\
				and not thisGlyph.unicode == None\
				and not thisGlyph.unicode == '00AD':
	
					myGoodReportlist.append(str('glyph name:	\''+thisGlyph.name+'\''))
	
				else:
	
					if len(thisLayer.components) > 0 or len(thisLayer.paths) > 0:
						myNodes = '----------' 
					else:
						myNodes = 'no content'		
	
					if thisGlyph.export == True:
						myExport = '---------'
					else:
						myExport = 'no export'
	
					if not thisGlyph.unicode == True\
					and not thisGlyph.unicode == None:
						myHex = '----------'
					else:
						myHex = 'no unicode'
	
	# LOOKING FOR EXCEPTION
	
					if thisGlyph.unicode == '00AD':
						myNodes = 'exception!'
	
					myBadReportlist.append(str(myNodes+' '+myExport+' '+myHex+' in: \''+thisGlyph.name+'\''))
	
	
	
	##############################################
	
	#			HTML FILE
	
	##############################################
		
	# GET LEAD-GLYPH
	
		for thisLayer in myLayers:
			thisGlyph = thisLayer.parent
	
			if len(thisLayer.components) > 0 or len(thisLayer.paths) > 0:
				if thisGlyph.export == True\
				and not thisGlyph.unicode == True\
				and not thisGlyph.unicode == None\
				and not thisGlyph.unicode == '00AD':
				
					myLeadDeci = int(str(thisGlyph.unicode), 16)
					break
	
				else:
					myLeadDeci = '0000'
	
	# WRITE HTML
	
		myHtmlOut +=\
"""<!DOCTYPE html>
	<html xmlns='http://www.w3.org/1999/xhtml'> 
		<head profile='http://www.w3.org/2005/10/profile'>

			<title>%s - Glyphtable</title>
			<meta http-equiv='Content-Type' content='text/html'>
			<link rel='stylesheet' media='screen' href='styles/fonts.css'>
			<link rel='stylesheet' media='screen' href='styles/style.css'>


			<script type="text/javascript">

//  dw_event.js version date Oct 2009
//  basic event handling file from dyn-web.com

var dw_Event = {
  
	add: function(obj, etype, fp, cap) {
		cap = cap || false;
		if (obj.addEventListener) obj.addEventListener(etype, fp, cap);
		else if (obj.attachEvent) obj.attachEvent("on" + etype, fp);
	}, 

	remove: function(obj, etype, fp, cap) {
		cap = cap || false;
		if (obj.removeEventListener) obj.removeEventListener(etype, fp, cap);
		else if (obj.detachEvent) obj.detachEvent("on" + etype, fp);
	}, 
	
	DOMit: function(e) { 
		e = e? e: window.event; // e IS passed when using attachEvent though ...
		if (!e.target) e.target = e.srcElement;
		if (!e.preventDefault) e.preventDefault = function () { e.returnValue = false; return false; }
		if (!e.stopPropagation) e.stopPropagation = function () { e.cancelBubble = true; }
		return e;
	},
	
	getTarget: function(e) {
		e = dw_Event.DOMit(e); var tgt = e.target; 
		if (tgt.nodeType != 1) tgt = tgt.parentNode; // safari...
		return tgt;
	}
	
}



/*********************************************************************************
  dw_cookies.js - cookie functions for dyn-web.com
  version date: Nov 2009
**********************************************************************************/

var dw_Cookie = {

	set: function(name, value, days, path, domain, secure) {
		var date, expires;
		if (typeof days == "number") {
			date = new Date();
			date.setTime( date.getTime() + (days*24*60*60*1000) );
			expires = date.toGMTString();
		}
		document.cookie = name + "=" + encodeURI(value) +
			((expires) ? "; expires=" + expires : "") +
			((path) ? "; path=" + path : "") +
			((domain) ? "; domain=" + domain : "") +
			((secure) ? "; secure" : "");
	},
	
	get: function(name) {
		var c, cookies = document.cookie.split( /;\s/g );
		for (var i=0; cookies[i]; i++) {
			c = cookies[i];
			if ( c.indexOf(name + '=') === 0 ) {
				return decodeURI( c.slice(name.length + 1, c.length) );
			}
		}
		return null;
	},
	
	del: function(name, path, domain) {
		if ( dw_Cookie.get(name) ) {
			document.cookie = name + "=" +
				((path) ? "; path=" + path : "") +
				((domain) ? "; domain=" + domain : "") +
				"; expires=Thu, 01-Jan-70 00:00:01 GMT";
		}
	}
}



/*************************************************************************
  This code is from Dynamic Web Coding at dyn-web.com
  Copyright 2004-10 by Sharon Paine 
  See Terms of Use at www.dyn-web.com/business/terms.php
  regarding conditions under which you may use this code.
  This notice must be retained in the code as is!
*************************************************************************/

/*  dw_sizerdx.js version date: April 2010
	requires dw_cookies.js (Nov 2009 version) and dw_event.js 
*/

var dw_fontSizerDX = {
	sizeUnit: "px",
	defaultSize: 12,
	maxSize: 26,
	minSize: 9,
	sizerDivId: 'sizer', // div id for sizer controls
	queryName: "dw_fsz", // name to check query string for when passing size in URL
	cookieLifetime: 180, // how long to keep cookie
	
	adjustList: [],  // set method populates

	setDefaults: function(unit, dflt, mn, mx, sels) {
		this.sizeUnit = unit; this.defaultSize = dflt;
		this.maxSize = mx;	this.minSize = mn;
		if (sels) this.set(dflt, mn, mx, sels);
	},

	set: function (dflt, mn, mx, sels) { 
		var ln = this.adjustList.length;		
		for (var i=0; sels[i]; i++) {
			this.adjustList[ln+i] = [];
			this.adjustList[ln+i]["sel"]  = sels[i];
			this.adjustList[ln+i]["dflt"] = dflt;
			this.adjustList[ln+i]["min"]   = mn || this.minSize;
			this.adjustList[ln+i]["max"]   = mx || this.maxSize;
			// hold ratio of this selector's default size to this.defaultSize for calcs in adjust fn 
			this.adjustList[ln+i]["ratio"] = this.adjustList[ln+i]["dflt"] / this.defaultSize;
		}
	},

	addHandlers: function () {
		var sizerEl = document.getElementById( dw_fontSizerDX.sizerDivId );
		if ( !dw_fontSizerDX.sizeIncrement ) { dw_fontSizerDX.getSizeIncrement(); }
		var links = sizerEl.getElementsByTagName('a');
		for (var i=0; links[i]; i++) {
			if ( dw_Util.hasClass( links[i], 'increase') ) {
				links[i].onclick = function () { dw_fontSizerDX.adjust( dw_fontSizerDX.sizeIncrement ); return false }
			} else if ( dw_Util.hasClass( links[i], 'decrease') ) {
				links[i].onclick = function () { dw_fontSizerDX.adjust( -dw_fontSizerDX.sizeIncrement ); return false }
			} else if ( dw_Util.hasClass( links[i], 'reset')  ) {
				links[i].onclick = function () { dw_fontSizerDX.reset(); return false }
			}
		}
		if (sizerEl) sizerEl.style.display = "block";
	},

	getSizeIncrement: function () {
		var val = 2;
		switch ( dw_fontSizerDX.sizeUnit ) {
			case 'px' : val = 5; break;
			case 'em' : val = .5; break;
			case '%%' : val = 5; break;
		}
		dw_fontSizerDX.sizeIncrement = val;
	},
	
	init: function() {
		if ( !document.getElementById || !document.getElementsByTagName || !document.createElement ) return;
		var _this = dw_fontSizerDX;
		if ( !_this.doControlsSetup ) {
			_this.addHandlers();
		} else {
			_this.setupControls();
		}
		var size;
		// check query string and cookie for fontSize
		// check size (in case default unit changed or size passed in url out of range)
		size = dw_Util.getValueFromQueryString( _this.queryName );
		if ( isNaN( parseFloat(size) ) || size > _this.maxSize || size < _this.minSize ) {
			size = dw_Cookie.get("fontSize");
			if ( isNaN( parseFloat(size) ) || size > _this.maxSize || size < _this.minSize ) {
				size = _this.defaultSize;
			}
		} 
		// if neither set nor setDefaults populates adjustList, apply sizes to body and td's
		if (_this.adjustList.length == 0) _this.set(  _this.defaultSize, _this.minSize, _this.maxSize, ['body', 'td'] ); 
		_this.curSize = _this.defaultSize;  // create curSize property to use in calculations 
		if ( size != _this.defaultSize ) _this.adjust( size - _this.defaultSize );
	},

	adjust: function(n) {
		if ( !this.curSize ) return; 
		var alist, size, list, i, j;
		// check against max/minSize
		if ( n > 0 ) {
			if ( this.curSize + n > this.maxSize ) n = this.maxSize - this.curSize;
		} else if ( n < 0 ) {
			if ( this.curSize + n < this.minSize ) n = this.minSize - this.curSize;
		}
		if ( n == 0 ) return;
		this.curSize += n;
		// loop through adjustList, calculating size, checking max/min
		alist = this.adjustList;
		for (i=0; alist[i]; i++) {
			size = this.curSize * alist[i]['ratio']; // maintain proportion 
			size = Math.max(alist[i]['min'], size); size = Math.min(alist[i]['max'], size);
			list = dw_Util.getElementsBySelector( alist[i]['sel'] );
			for (j=0; list[j]; j++) { list[j].style.fontSize = size + this.sizeUnit; }
		}
		dw_Cookie.set( "fontSize", this.curSize, this.cookieLifetime, "/" );
	},

	reset: function() {
		if ( !this.curSize ) return; 
		var alist = this.adjustList, list, i, j;
		for (i=0; alist[i]; i++) {
			list = dw_Util.getElementsBySelector( alist[i]['sel'] );
			for (j=0; list[j]; j++) { 
				// Reset adjustList elements to their default sizes
				//list[j].style.fontSize = alist[i]['dflt'] + this.sizeUnit;
				list[j].style.fontSize = '';  // restores original font size (unless set inline!)
			} 
		}
		this.curSize = this.defaultSize;
		dw_Cookie.del("fontSize", "/");
	}

};

/////////////////////////////////////////////////////////////////////

var dw_Util; 
if (!dw_Util) dw_Util = {};

// removes space characters from start and end of string
dw_Util.trimString = function (str) {
	var re = /^\s+|\s+$/g;
	return str.replace(re, "");
}

// removes extra space characters
dw_Util.normalizeString = function (str) {
	var re = /\s\s+/g;
	return dw_Util.trimString(str).replace(re, " ");
}

dw_Util.hasClass = function (el, cl) {
	var re = new RegExp("\\\\b" + cl + "\\\\b", "i");
	if ( re.test( el.className ) ) {
		return true;
	}
	return false;
}

// what className attached to what element type in what container element (default: document)
dw_Util.getElementsByClassName = function (sClass, sTag, oCont) {
	var result = [], list, i;
	var re = new RegExp("\\\\b" + sClass + "\\\\b", "i");
	oCont = oCont? oCont: document;
	if ( document.getElementsByTagName ) {
		if ( !sTag || sTag == "*" ) { // for ie5
			list = oCont.all? oCont.all: oCont.getElementsByTagName("*");
		} else {
			list = oCont.getElementsByTagName(sTag);
		}
		for (i=0; list[i]; i++) 
			if ( re.test( list[i].className ) ) result.push( list[i] );
	}
	return result;
}

// resource: simon.incutio.com/archive/2003/03/25/getElementsBySelector
dw_Util.getElementsBySelector = function (selector) {
	if (!document.getElementsByTagName) return [];
	var nodeList = [document], tokens, bits, list, col, els, i, j, k;
	selector = dw_Util.normalizeString(selector);
	tokens = selector.split(' ');
	for (i=0; tokens[i]; i++) {
		if ( tokens[i].indexOf('#') != -1 ) {  // id
			bits = tokens[i].split('#'); 
			var el = document.getElementById( bits[1] );
			if (!el) return []; 
			if ( bits[0] ) {  // check tag
				if ( el.tagName.toLowerCase() != bits[0].toLowerCase() ) return [];
			}
			for (j=0; nodeList[j]; j++) {  // check containment
				if ( nodeList[j] == document || dw_Util.contained(el, nodeList[j]) ) 
					nodeList = [el];
				else return [];
			}
		} else if ( tokens[i].indexOf('.') != -1 ) {  // class
			bits = tokens[i].split('.'); col = [];
			for (j=0; nodeList[j]; j++) {
				els = dw_Util.getElementsByClassName( bits[1], bits[0], nodeList[j] );
				for (k=0; els[k]; k++) { col[col.length] = els[k]; }
			}
			nodeList = [];
			for (j=0; col[j]; j++) { nodeList.push(col[j]); }
		} else {  // element 
			els = []; 
			for (j = 0; nodeList[j]; j++) {
				list = nodeList[j].getElementsByTagName(tokens[i]);
				for (k = 0; list[k]; k++) { els.push(list[k]); }
			}
			nodeList = els;
		}
	}
	return nodeList;
}

// obj: link or window.location
dw_Util.getValueFromQueryString = function (name, obj) {
	obj = obj? obj: window.location; 
	if (obj.search && obj.search.indexOf(name != -1) ) {
		var pairs = obj.search.slice(1).split("&"); // name/value pairs
		var set;
		for (var i=0; pairs[i]; i++) {
			set = pairs[i].split("="); // Check each pair for match on name 
			if ( set[0] == name && set[1] ) {
				return set[1];
			}
		}
	}
	return '';
}

// returns true of oNode is contained by oCont (container)
dw_Util.contained = function (oNode, oCont) {
	if (!oNode) return null; // in case alt-tab away while hovering (prevent error)
	while ( (oNode = oNode.parentNode) ) if ( oNode == oCont ) return true;
	return false;
}

				// setDefaults arguments: size unit, default size, minimum, maximum
				// optional array of elements or selectors to apply these defaults to

				dw_fontSizerDX.setDefaults("px", 20, 6, 150, ['div#main p.article'] );

				// set arguments: default size, minimum, maximum
				// array of elements or selectors to apply these settings to
				dw_fontSizerDX.set(20, 6, 150, ['div#main h2'] );

				dw_Event.add( window, 'load', dw_fontSizerDX.init );

			</script>

		</head>

		<body>

		<div class='header foreground'>
			<strong>%s - glyphtable</strong> &mdash; glyphs %s &mdash; date %s
			<span id='sizer' class='btn_wrap'>
				<a class='increase text btn' href='#' title='Increase text size'>+</a>
				<a class='decrease text btn' href='#' title='Decrease text size'>
				&ndash;</a>
				<a class='reset text btn' href='#' title='Restore default font-sizes'>R</a>
			</span>
			
		</div>

		<div class='footer foreground'>
			<span class='icons' data-icon='&#%s;'>
			</span>
			<span> icon-size at %s to text-size at %s &mdash; set in fonts.css
			</span>
		</div>

		<div id='wrapper'>

			<div id='main'>

"""\
		% (Glyphs.font.familyName, Glyphs.font.familyName, str(len(myHtmlList)), strftime('%m-%d-%Y', lt), str(myLeadDeci), myIconSize, myTextSize)
		
		for x in myHtmlList:
			myHtmlOut += x
	
		myHtmlOut+=\
"""

			</div>
		</div>
		</body>
	</html>
"""
	
	##############################################
	
	#			STYLE CSS FILE
	
	##############################################
	
	
		myCssOut +=\
"""@charset 'UTF-8';
	/* CSS Document */

	body {
		margin: 0;
		font-family: "Helvetica Neue", Helvetica, sans-serif;
	}

	.foreground {
		-webkit-font-smoothing: antialiased;
		width: 100%%;
		color: #888;
		box-shadow: 0 1px 0 rgba(255, 255, 255, 0.7) inset, 0 0 2px 0 rgba(0, 0, 0, 0.4);
		background-color: rgba(242, 242, 242, 0.95);
		-webkit-box-sizing: border-box;
		box-sizing: border-box;
		position: fixed;
		line-height: inherit;
		margin: 0;
		overflow-x: hidden;
		padding: 5px 12px 5px 12px;
		text-overflow: ellipsis;
		white-space: nowrap;
		border: none;
		z-index: 10;
	}

		.text {
			font-size: 0.9em;
			color: #aaa;
			-webkit-font-smoothing: antialiased;
			-moz-osx-font-smoothing: grayscale;
			word-wrap: break-word;
			text-decoration: none;
			text-align: center;
			font-weight: bold;
		}

		.btn_wrap {
			margin-top: 0px;
			margin-bottom: 0px;
			overflow: hidden;
			float:right;
		}

		.btn {
			background-color: #fff;
			width: 27px;
			margin-right: 2px;
			padding-bottom: 1.5px;
			padding-left: 7px;
			padding-right: 7px;
			-webkit-box-sizing: border-box;
			box-sizing: border-box;
			border: 1px solid;
			border-radius: 20px;
			float: left;
		}

		.btn:hover {
			background-color: #ddd !important;
		}

		.btn a {
			color: #888;
		}

	.header {
		font-size: %s;
	}
	
	.footer {
		font-size: %s;
		bottom: 0;
		padding-top: 0px;
		padding-bottom: 5px;
	}
	
	#wrapper {
		padding-bottom: 40px;
		top: 40px;
		left: 4px;
		position: absolute;
		width: 100%%;
		margin-left: 10px;
	}

	/* Glyphtable Styles */

	.icon-panel {
		border: 1px solid #fff;
		float: left;
		min-width: 50px;
		max-width: 150px;
		width: 100%%;
		color: #000;
		background-color: #fafafa;
		white-space: nowrap;
	}

	.icon-box { 
		padding-top: 10px;
		padding-right: 10px;
		padding-bottom: 5px;
		padding-left: 8px;
		margin: 0px;
		/*font-size: %s;*/ /* specific icon-setup only for the icon-view in this table */
		text-align: center;
		border-bottom: #eee;
		border-bottom-style: dotted;
		border-bottom-width: thin;
	}

	.description_box {
		float: left;
		padding: 0.5em 1em;
		font-size: 10px;
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
		color: #999;
	}

	strong {
		color: #999;
	}
"""\
		% (myTextSize, myTextSize, myViewSize)
	
	
	
	##############################################
	
	#			FONT CSS FILE
	
	##############################################
	
		myFontCssOut +=\
"""@charset 'UTF-8';
	/* FontCSS Document */

	/* get Fonts & Icon */

	@font-face {
		font-family: '%s';
		src: url(../fonts/%s.eot),
			url(../fonts/%s.eot?#iefix) format('embedded-opentype'),
			url(../fonts/%s.woff2) format('woff2'),
			url(../fonts/%s.woff) format('woff'),
			url(../fonts/%s.ttf) format('truetype');
	}

	/* Fonts & Icon Setup *//* global icon-setup for basic usage */

	.icons {
		font-family: '%s',consolas, monaco, verdana;

		font-size: %s;	/* setup for global - optimized - icon-size */
		font-style: normal;
		font-weight: normal;
		font-variant: normal;
		text-transform: none;
		line-height: 1;
		vertical-align: 0px;
		speak: none;

		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
	}

	/* method: data-icon */

	[data-icon]:before {
		content: attr(data-icon);
	}

	/* method: icon-classes */
"""\
		% (myFontExportName, myFontExportName, myFontExportName, myFontExportName, myFontExportName, myFontExportName, myFontExportName, myIconSize)
	
		for x in myFontCssList:
			myFontCssOut += x
	
	
	
	##############################################
	
	#			WRITE DATA
	
	##############################################
	
	
		if bool(myGoodReportlist) == True:
	
	# WRITE DIRECTORIES
		
			if os.path.isfile(myDir) == False and os.path.isdir(myDir) == False:
				os.mkdir(myDir)
				os.mkdir(myDirStyles)
				os.mkdir(myDirFonts)
				myDirResult ='(glyphtable-folder & sub-folders created)\n\t'+str(myDir)
			else:
				myDirResult ='(the directories already exist)\n\t'+str(myDir) 
	
	
	# WRITE HTML
	
			myHtmlFile = open(myHtmlFileName,'w')
			myHtmlFile.write(myHtmlOut)
			myHtmlFile.close()
	
	
	# WRITE STYLES.CSS
	
			if os.path.isfile(myCssFileName) == True:
	
				myAwnser = dialogs.askYesNo(\
				messageText='\nstyles.css already exist',\
				informativeText='want to overwrite?')
	
				if myAwnser == 1:
					myCssFile = open(myCssFileName,'w')
					myCssFile.write(myCssOut)
					myCssFile.close()
					myCssResult = 'styles.css - new created'
	
				elif myAwnser == 0 or myAwnser == -1:
					myCssResult = 'styles.css - leave at it is'
	
			else:
				myCssResult = 'styles.css - new created'
	
				myCssFile = open(myCssFileName,'w')
				myCssFile.write(myCssOut)
				myCssFile.close()
	
			myFontCssFile = open(myFontCssFileName,'w')
			myFontCssFile.write(myFontCssOut)
			myFontCssFile.close()		
	
	
	##############################################
	
	#			WRITING OUTPUT
	
	##############################################
	
	
	# PRINT OUTPUT: REPORT-LISTS
	
			if bool(myBadReportlist) == True:
				print\
"""

	=============================================
	these glyphs were not exported, check report:
"""
				for x in myBadReportlist:
					print '\t'+x
	
	
			if bool(myGoodReportlist) == True:
				print\
"""

	===========================
	these glyphs were exported:
"""
				for x in myGoodReportlist:
					print '\t'+x
	
	
	# CHECK FOR WEB-FONT-FILES
	
			if os.path.isfile(myDirFonts+'/'+myFontExportName+'.eot') == True\
			and os.path.isfile(myDirFonts+'/'+myFontExportName+'.woff') == True:
				myFontsResult = '> all fonts in the right directory'
	
			elif os.path.isfile(myDirFonts+'/'+myFontExportName+'.eot') != True\
			and os.path.isfile(myDirFonts+'/'+myFontExportName+'.woff') == True:
				myFontsResult = '> export .eot-file to fonts-directory'
	
			elif os.path.isfile(myDirFonts+'/'+myFontExportName+'.eot') == True\
			and os.path.isfile(myDirFonts+'/'+myFontExportName+'.woff') != True:
				myFontsResult = '> export .woff-files to fonts-directory'
	
			elif os.path.isfile(myDirFonts+'/'+myFontExportName+'.eot') != True\
			and os.path.isfile(myDirFonts+'/'+myFontExportName+'.woff') != True:
				myFontsResult = '> export actual web-font-files to fonts-directory'
	
	
	# SET "FONTS"-FOLDER AS EXPORT DEFAULT
	
			Glyphs.defaults["WebfontPluginExportPath"] = myDirFonts
	
	#
	# PRINT OUTPUT: FILES AND DIRECTORIES
	
			print\
"""

	================
	files generated:

	html - new created
	%s
	fonts.css - new created

	generated in:

	%s

	> done! maybe have a look at report above
	%s
	
"""\
		% (myCssResult, myDirResult, myFontsResult)
		
	
		else:
			print\
"""
	====================================
	no valid glyphs in selection, 
	no directories created, check report:
"""
			for x in myBadReportlist:
				print '\t'+x
	
	
			print\
"""		
> please select some "valid" glyphs
"""
	
		Glyphs.font.enableUpdateInterface()
		Glyphs.showMacroWindow()
	
	else:
		Message('\nplease select some "valid" glyphs')
		print\
"""
> please select some "valid" glyphs
"""
else:
	Message('\nplease be sure you have saved your glyphs-file')
	print\
"""
> please be sure you have saved your glyphs-file
"""
	
	
	
#CLEAN UP STRING BLOCKS