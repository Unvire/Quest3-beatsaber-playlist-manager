import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QRect, QPoint


class ImageWithOverlay(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.image = QPixmap(image_path)
        self.square_rect = QRect(100, 100, 200, 200)  # Początkowy prostokąt
        self.dragging = None
        self.drag_offset = QPoint()

    def paintEvent(self, event):
        painter = QPainter(self)
        # Rysowanie obrazu
        painter.drawPixmap(0, 0, self.image)

        # Rysowanie półprzezroczystej warstwy na zewnątrz kwadratu
        overlay_color = QColor(0, 0, 0, 150)  # Czerń z przezroczystością
        painter.setBrush(overlay_color)
        painter.setPen(Qt.NoPen)

        # Rysowanie czterech obszarów poza kwadratem
        painter.drawRect(0, 0, self.width(), self.square_rect.top())  # Góra
        painter.drawRect(0, self.square_rect.bottom(), self.width(), self.height() - self.square_rect.bottom())  # Dół
        painter.drawRect(0, self.square_rect.top(), self.square_rect.left(), self.square_rect.height())  # Lewo
        painter.drawRect(self.square_rect.right(), self.square_rect.top(), self.width() - self.square_rect.right(), self.square_rect.height())  # Prawo

        # Rysowanie obramowania kwadratu
        pen = QPen(Qt.red, 2)
        painter.setPen(pen)
        painter.setBrush(Qt.transparent)
        painter.drawRect(self.square_rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.is_near_corner(event.pos()):
                self.dragging = "corner"
            elif self.square_rect.contains(event.pos()):
                self.dragging = "move"
                self.drag_offset = event.pos() - self.square_rect.topLeft()

    def mouseMoveEvent(self, event):
        if self.dragging == "move":
            new_top_left = event.pos() - self.drag_offset
            self.square_rect.moveTopLeft(new_top_left)
            self.update()
        elif self.dragging == "corner":
            new_bottom_right = event.pos()
            self.square_rect.setBottomRight(new_bottom_right)
            self.update()

    def mouseReleaseEvent(self, event):
        self.dragging = None

    def is_near_corner(self, pos):
        corner_size = 10
        bottom_right_corner = QRect(
            self.square_rect.bottomRight() - QPoint(corner_size, corner_size),
            self.square_rect.bottomRight() + QPoint(corner_size, corner_size),
        )
        return bottom_right_corner.contains(pos)

    def sizeHint(self):
        return self.image.size()


class MainWindow(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle("Aplikacja PyQt5 z przyciemnieniem na zewnątrz kwadratu")

        self.image_widget = ImageWithOverlay(image_path)
        self.setCentralWidget(self.image_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    image_path = "image.png"  # Zmień na ścieżkę do swojego obrazu
    window = MainWindow(image_path)
    window.show()
    sys.exit(app.exec_())