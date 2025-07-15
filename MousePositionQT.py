import sys, os, csv
import pyautogui as pag            # pip install pyautogui
from PIL import ImageDraw         # pip install pillow
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTextEdit,
    QPushButton, QHBoxLayout, QVBoxLayout
)
from PyQt6.QtCore import Qt, QRect, QEventLoop
from PyQt6.QtGui import (
    QGuiApplication, QPainter, QPen,
    QColor, QBrush, QCursor
)

CSV_FILE = "posicoes_mouse.csv"
ICONS = {
    'posicao':      '📍',
    'clique':       '👉',
    'area':         '🔲',
    'duplo_clique': '🔖'
}

class Overlay(QWidget):
    def __init__(self, modo, geom: QRect):
        super().__init__(flags=Qt.WindowType.FramelessWindowHint |
                               Qt.WindowType.WindowStaysOnTopHint |
                               Qt.WindowType.Tool)
        self.modo  = modo
        self.begin = self.end = self.result = None
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setGeometry(geom)
        self.setWindowOpacity(0.25)
        self.setStyleSheet("background-color: rgba(0,0,0,150);")
        self.setMouseTracking(True)
        self.show()

    def mousePressEvent(self, ev):
        p = ev.globalPosition().toPoint()
        if self.modo == 'clique':
            self.result = (p.x(), p.y(), p.x(), p.y())
            self.close()
        else:
            self.begin = self.end = p
            self.update()

    def mouseMoveEvent(self, ev):
        if self.modo == 'area' and self.begin:
            self.end = ev.globalPosition().toPoint()
            self.update()

    def mouseReleaseEvent(self, ev):
        if self.modo == 'area' and self.begin:
            self.end = ev.globalPosition().toPoint()
            x1,y1 = min(self.begin.x(), self.end.x()), min(self.begin.y(), self.end.y())
            x2,y2 = max(self.begin.x(), self.end.x()), max(self.begin.y(), self.end.y())
            self.result = (x1, y1, x2, y2)
            self.close()

    def mouseDoubleClickEvent(self, ev):
        if self.modo == 'duplo_clique':
            p = ev.globalPosition().toPoint()
            self.result = (p.x(), p.y(), p.x(), p.y())
            self.close()

    def paintEvent(self, _):
        if self.modo == 'area' and self.begin and self.end:
            painter = QPainter(self)
            painter.setBrush(QBrush(QColor(255, 0, 0, 100)))
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.drawRect(QRect(self.begin, self.end))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RPA – Captura Multi-Monitor")
        self._init_csv()
        self._build_ui()

    def _init_csv(self):
        if not os.path.isfile(CSV_FILE):
            with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
                csv.writer(f).writerow(['tipo','x1','y1','x2','y2'])

    def _build_ui(self):
        central = QWidget()
        vbox    = QVBoxLayout(central)

        self.log = QTextEdit(readOnly=True)
        self.log.setPlainText("Coordenadas capturadas:\n")
        vbox.addWidget(self.log)

        hbox = QHBoxLayout()
        botoes = [
            ("Posição",         self.capture_position),
            ("Clique Tela",     lambda: self.capture_overlay('clique')),
            ("Selecionar Área", lambda: self.capture_overlay('area')),
            ("Duplo Clique",    lambda: self.capture_overlay('duplo_clique')),
            ("Limpar",          self.clear_log),
            ("Abrir CSV",       lambda: os.system(f'xdg-open {CSV_FILE}')),
            ("Sair",            self.close),
        ]
        for texto, fn in botoes:
            btn = QPushButton(texto)
            btn.clicked.connect(fn)
            hbox.addWidget(btn)

        vbox.addLayout(hbox)
        self.setCentralWidget(central)

    def keyPressEvent(self, ev):
        if ev.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.capture_position()
        elif ev.text() == '2':
            self.close()

    def register_event(self, tipo, x1, y1, x2, y2):
        icon = ICONS.get(tipo, '📌')
        linha = f"{icon} {tipo}: ({x1},{y1}) → ({x2},{y2})"
        self.log.append(linha)
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow([tipo, x1, y1, x2, y2])

    def capture_position(self):
        p = QCursor.pos()
        self.register_event('posicao', p.x(), p.y(), p.x(), p.y())

    def capture_overlay(self, modo):
        # 1) cria um Overlay para cada monitor
        telas    = QGuiApplication.screens()
        overlays = [Overlay(modo, t.geometry()) for t in telas]

        # 2) espera o primeiro overlay terminar
        loop = QEventLoop()
        for ov in overlays:
            ov.destroyed.connect(loop.quit)
        loop.exec()

        # 3) coleta resultado e fecha seguros
        resultado = None
        for ov in overlays:
            if hasattr(ov, 'result') and ov.result:
                resultado = ov.result
        for ov in overlays:
            try:
                ov.close()
            except RuntimeError:
                pass

        if not resultado:
            return
        x1, y1, x2, y2 = resultado

        # 4) screenshot da área selecionada
        if modo == 'area':
            w, h = x2 - x1, y2 - y1
            try:
                img = pag.screenshot(region=(x1, y1, w, h))
                draw = ImageDraw.Draw(img)
                draw.rectangle([(0, 0), (w-1, h-1)], outline="red", width=2)
                fname = f'captura_{x1}_{y1}_{x2}_{y2}.png'
                img.save(fname)
                self.log.append(f"💾 {fname}")
            except Exception as e:
                self.log.append(f"⚠️ Erro screenshot: {e}")

        # 5) registra o evento final
        self.register_event(modo, x1, y1, x2, y2)

    def clear_log(self):
        self.log.clear()
        self.log.setPlainText("Coordenadas capturadas:\n")

if __name__ == "__main__":
    app    = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
