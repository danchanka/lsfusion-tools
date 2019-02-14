SyntaxHighlighter.brushes.Custom = function()
{
  var keywords    =    'INTEGER DOUBLE LONG BOOLEAN DATE DATETIME TEXT STRING ISTRING VARISTRING VARSTRING TIME RICHTEXT ' +
                       'ABSTRACT ACTION ADD ADDFORM ADDOBJ ADDSESSIONFORM AFTER ' + 
                       'AGGR AGGPROP ALL AND APPLY AS ASC ASONCHANGE ASONCHANGEWYS ASONEDIT ASSIGN ASYNCUPDATE ATTACH '+
                       'AUTO AUTOAPPLY AUTOREFRESH AUTOSET BACKGROUND BCC BEFORE BOTTOM BREAK BY CANCEL CASCADE ' +
                       'CASE CC CENTER CHANGE CHANGECLASS CHANGED CHANGEWYS CHECK ' + 
                       'CHECKED CLASS CLOSE COLOR COLUMNS CONCAT CONFIRM CONSTRAINT ' + 
                       'CONTAINERH CONTAINERV CONTEXTFILTER CUSTOM CUSTOMFILE CYCLES DATA DEFAULT DELETE ' +
                       'DELETESESSION DESC DESIGN DIALOG DO DOCKED DOCKEDMODAL DOCX DRAWROOT ' +
                       'DROP DROPCHANGED DROPSET ECHO EDIT EDITABLE EDITFORM EDITKEY ' +
                       'EDITSESSIONFORM ELSE EMAIL END EQUAL EVAL EVENTID EVENTS EXCELFILE ' +
                       'EXCEPTLAST EXCLUSIVE EXEC EXTEND FALSE FILTER FILTERGROUP ' + 
                       'FILTERS FIRST FIXED FIXEDCHARWIDTH FOOTER FOR FORCE FOREGROUND ' +
                       'FORM FORMS FORMULA FROM FULLSCREEN GOAFTER GRID GROUP HALIGN HEADER ' +
                       'HIDE HIDESCROLLBARS HIDETITLE HINTNOUPDATE HINTTABLE HORIZONTAL ' + 
                       'HTML IF IMAGE IMAGEFILE IMPOSSIBLE IN INCREMENT INDEX ' + 
                       'INDEXED INIT INITFILTER INLINE INPUT IS JOIN LAST LEADING LEFT LENGTH LIMIT ' +
                       'LIST LOADFILE LOCAL LOGGABLE MANAGESESSION MAX MAXCHARWIDTH ' + 
                       'MESSAGE META MIN MINCHARWIDTH MODAL MODULE MULTI NAGGR NAME NAMESPACE ' +
                       'NAVIGATOR NEW NEWSESSION NEWTHREAD NO NOT NOTHING NULL NUMERIC OBJECT ' +
                       'OBJECTS OBJVALUE OK ON OPENFILE OPTIMISTICASYNC OR ORDER OVERRIDE PAGESIZE ' +
                       'PANEL PARENT PARTITION PDF PDFFILE PERSISTENT POSITION ' + 
                       'PREFCHARWIDTH PREV PRINT PRIORITY PROPERTIES PROPERTY ' + 
                       'PROPORTION QUERYOK QUERYCLOSE QUICKFILTER READONLY READONLYIF RECURSION REGEXP REMOVE ' +
                       'REPORTFILE REQUEST REQUIRE RESOLVE RETURN RGB RIGHT ' + 
                       'ROUND RTF SELECTOR SESSION SET SETCHANGED SHORTCUT SHOW SHOWDROP ' +
                       'SHOWIF SINGLE SPLITH SPLITV STEP STRETCH STRICT STRUCT SUBJECT ' +
                       'SUM TABBED TABLE TEXTHALIGN TEXTVALIGN THEN TIME TITLE TO TODRAW ' +
                       'TOOLBAR TOP TRAILING TREE TRUE UNGROUP UPDATE VALIGN ' +
                       'VERTICAL WHEN WHERE WHILE WINDOW WORDFILE XLS XOR YES';

  this.regexList = [
      { regex: SyntaxHighlighter.regexLib.singleLineCComments, css: 'color1' }, 
      { regex: /#{2,3}/gi, css: 'color2' },             
      { regex: /@[a-zA-Z]\w*\b/gi, css: 'color2' },
      { regex: SyntaxHighlighter.regexLib.singleQuotedString, css: 'value' },
      { regex: /\b\d+l?\b/gi, css: 'value' }, 
      { regex: /\b\d+\.\d*d?\b/gi, css: 'value' }, 
      { regex: /\b\d{4}_\d\d_\d\d(_\d\d:\d\d)?\b/gi, css: 'value' }, 
      { regex: /\b\d\d:\d\d\b/gi, css: 'value' }, 
      { regex: /#[0-9a-fA-F]{6}/gi, css: 'value' },
      { regex: new RegExp(this.getKeywords(keywords), 'gm'), css: 'keyword' }
      ];	
};
 
SyntaxHighlighter.brushes.Custom.prototype = new SyntaxHighlighter.Highlighter();
SyntaxHighlighter.brushes.Custom.aliases = ['custom', 'lsf', 'ls'];
