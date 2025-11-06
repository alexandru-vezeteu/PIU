import sys
from PyQt5.QtWidgets import QApplication
from src.ImageEditor import ImageEditor

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = ImageEditor()
    editor.show()
    sys.exit(app.exec_())