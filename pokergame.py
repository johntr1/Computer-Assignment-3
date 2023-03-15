# Author:
# John Tran
# Martin Diderholm
# Date: 05/03/2023
# Group 19

from pokerview import *
import sys

app = QApplication(sys.argv)

game = TexasHoldEm()

window = MainWindow(app, game)
window.show()
app.exec_()

