from pokerview import *
import sys

app = QApplication(sys.argv)

game = TexasHoldEm()

window = MainWindow(app, game)
window.show()
app.exec_()

