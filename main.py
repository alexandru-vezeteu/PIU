import sys
from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5.QtCore import Qt
from src.ImageEditor import ImageEditor


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("Image Editor")
    app.setOrganizationName("PIU")
    app.setApplicationVersion("1.0.0")

    available_styles = QStyleFactory.keys()
    if 'Fusion' in available_styles:
        app.setStyle('Fusion')

    editor = ImageEditor()
    editor.show()

    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())