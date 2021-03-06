# editor.py

from PyQt4 import QtGui
import syntax

app = QtGui.QApplication([])
editor = QtGui.QPlainTextEdit()
highlight = syntax.PythonHighlighter(editor.document())
editor.show()

# Load syntax.py into the editor for demo purposes
#infile = open('syntax.py', 'r')
infile = open('../../samples/missionxyz.cfs', 'r')
editor.setPlainText(infile.read())

app.exec_()
