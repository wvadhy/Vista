import PyQt5.QtWidgets as widgets
import PyQt5.QtCore as core
import PyQt5.QtGui as gui
from Utilities import Utilities as utl
from Factory import Factory as fct

from dataclasses import (
    dataclass,
    field
)

from typing import (
    List,
    Dict,
    Tuple,
    Any,
    Callable,
    Optional
)

from time import sleep
import multiprocessing as multi
import requests as req
import sys

@dataclass
class Window(widgets.QWidget):

    Offset: float
    Store: List[Any] = field(default_factory=list)

    def __init__(self, width: int = 300, height: int = 400):

        """Sets up main Window"""

        super(Window, self).__init__(None)

        self.o_fx, self.s_fx, self.g_fx, self.r_fx, self.o_anime = utl.setup_effects(self, self.ovc)

        self.setWindowTitle("vista")
        self.setFixedSize(width, height)
        self.setWindowFlags(core.Qt.CustomizeWindowHint | core.Qt.FramelessWindowHint)
        self.pressing = False
        utl.change_ss(self, "2B2A4C", bg_color2="4E3636")
        self.round_corners()

        self.lw = utl.wdg_builder(200, 300, p=self, move=(width // 6, height // 6 - 20), style=("212A3E", 10))

        self.logo_lbl = utl.lbl_builder("", 75, 75, "vista.png", p=self.lw, move=(65, 15))
        utl.fade_in(self.logo_lbl, self.o_fx, self.o_anime, dur=1000)

        self.login_box = utl.lne_builder("", 150, 30, align=core.Qt.AlignHCenter, p=self.lw, filter=self, move=(28, 100), style=('F8F6F4', 15, '000000'))

        self.login_btn = utl.btn_builder("login", 125, 30, p=self.lw, filter=self, conn=self.__check_details, move=(40, 155), style=('4F4557', 10, 'FFFFFF', "6D5D6E"))

        self.register_btn = utl.btn_builder("register", 125, 30, p=self.lw, filter=self, move=(40, 195), style=('4F4557', 10, 'FFFFFF', "6D5D6E"))

        self.misc_btn = utl.btn_builder('', 125, 30, p=self.lw, filter=self, move=(40, 235), style=('FFFFFF', 10, '000000'))

        self.settings = utl.btn_builder("⛭", 32, 32, f_size=28, bold=True, p=self, fx=self.s_fx, filter=self, move=(width - 40, 10), style=('212A3E', 15))

        self.load_widget = utl.wdg_builder(self.width(), 0, p=self, style=("212A3E", 10))

        self.load_lbl = utl.lbl_builder("", 90, 90, "loading.png", align=core.Qt.AlignCenter, p=self, move=(width // 2 - 44, height // 2 - 44), hide=True)

        self.load_pix = gui.QPixmap("loading.png")

        self.menu_wdg = utl.wdg_builder(0, self.height(), p=self, fx=self.g_fx, style=("06283D", 0))

        f_btn = fct('btn', {'width': 75, 'height': 30, 'p': self.menu_wdg, 'filter': self, 'style': ('2B4865', 2, 'E7F6F2')})

        self.menu_btn1 = f_btn("data", move=(90, 50))
        self.menu_btn2 = f_btn("model", move=(90, 110))
        self.menu_btn3 = f_btn("resolve", move=(90, 170))
        self.menu_btn4 = f_btn("analyse", move=(90, 230))
        self.menu_btn5 = f_btn("import", move=(90, 290))

        self.prog_label = utl.lbl_builder("Loading", 0, 0, bold=True, align=core.Qt.AlignCenter, p=self, move=(width // 2 + 2, height // 2 + 70), style=("212A3E",))

        self.min_btn = utl.btn_builder("", 15, 15, p=self, filter=self, conn=self.showMinimized, move=(0 + 35, 10), style=('9BA4B5', 5))

        self.close_btn = utl.btn_builder("", 15, 15, p=self, filter=self, conn=widgets.qApp.quit, move=(0 + 10, 10), style=('9BA4B5', 5))

        self.expand_btn = utl.btn_builder("", 15, 15, p=self, filter=self, conn=self.showMaximized, move=(0 + 60, 10), style=('9BA4B5', 5))

        self.oldPos = self.pos()

        self.show()

    def mousePressEvent(self, event) -> None:

        """
        Override mousePressEvent to switch self Pos to Generic Pos:

        event -> Generic for events
        """

        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event) -> None:

        """
        Override mouseMoveEvent in order to enable dragging of main Window:

        event -> Generic for events
        """

        delta = core.QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def round_corners(self) -> None:

        """Rounds the corner of main Window"""

        path = gui.QPainterPath()
        path.addRoundedRect(core.QRectF(self.rect()), 9.0, 9.0)
        mask = gui.QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)

    def eventFilter(self, obj: widgets, event: core.QEvent) -> Optional[int]:

        """
        Detects generic events and filters them

        obj -> Object which on which an event has occurred
        event -> Any valid QEvent
        """

        if event.type() == core.QEvent.Enter:
            self.on_hover(obj)

        elif event.type() == core.QEvent.Leave:
            self.on_leave(obj)

        elif event.type() == core.QEvent.MouseButtonPress:
            self.default_click(obj)

        elif event.type() == core.QEvent.MouseButtonRelease:
            self.default_release(obj)

        return super(Window, self).eventFilter(obj, event)

    def default_click(self, obj: widgets) -> None:

        """
        Detects mouse click event

        obj -> Object which mouse has clicked on
        """

        if obj in (self.login_btn, self.register_btn, self.misc_btn):
            self.animate(obj, 20, 115, 25)
            obj.setFont(gui.QFont('Arial', 8))

        elif obj in (self.min_btn, self.close_btn, self.expand_btn):
            self.animate(obj, x=13, y=13)

        elif obj in (self.menu_btn1, self.menu_btn2, self.menu_btn3, self.menu_btn4, self.menu_btn5):
            self.animate(obj, 20, 65, 25)
            obj.setFont(gui.QFont('Arial', 8))

        elif obj == self.login_box:
            utl.change_ss(obj, "F8F6F4", 15, color="000000")

    def default_release(self, obj: widgets) -> None:

        """
        Detects mouse release event

        obj -> Object which mouse has released key press on
        """

        if obj in (self.login_btn, self.register_btn, self.misc_btn):
            self.animate(obj, 20, 125, 30)
            obj.setFont(gui.QFont('Arial', 10))

        elif obj in (self.menu_btn1, self.menu_btn2, self.menu_btn3, self.menu_btn4, self.menu_btn5):
            self.animate(obj, 20, 75, 30)
            self.setFont(gui.QFont('Arial', 10))

        elif obj in (self.min_btn, self.close_btn, self.expand_btn):
            self.animate(obj, x=15, y=15)

    def on_hover(self, obj: widgets) -> None:

        """
        Events triggered upon the mouse cursor entering obj:

        obj -> Any object from QtWidgets which implements eventFilter(...)
        """

        if obj == self.min_btn:
            utl.change_ss(obj, "FFE569", 5)
            self.animate(obj)

        elif obj == self.close_btn:
            utl.change_ss(obj, "DB005B", 5)
            self.animate(obj)

        elif obj == self.expand_btn:
            utl.change_ss(obj, "00DFA2", 5)
            self.animate(obj)

        elif obj == self.settings:
            self.animate(obj, 50, 36, 36)

        elif obj in (self.login_btn, self.register_btn):
            utl.change_ss(obj, "393646", 10)
            self.animate(obj, 50, 135, 35)

        elif obj == self.misc_btn:
            utl.change_ss(obj, "DDE6ED", 10, '000000')
            self.animate(obj, 50, 130, 35)

        elif obj in (self.menu_btn1, self.menu_btn2, self.menu_btn3, self.menu_btn4, self.menu_btn5):
            utl.change_ss(obj, "395B64", 2, 'E7F6F2')
            self.animate(obj, 50, 85, 35)

        elif obj == self.login_box:
            self.animate(obj, 100, 170, 30)

    def on_leave(self, obj: Any) -> None:

        """
        Events triggered upon the mouse cursor leaving obj:

        obj -> Any object from QtWidgets which implements eventFilter(...)
        """

        if obj in (self.min_btn, self.close_btn, self.expand_btn):
            utl.change_ss(obj, "9BA4B5", 5)
            self.animate(obj, x=15, y=15)

        elif obj == self.settings:
            self.animate(obj, 50, 32, 32)

        elif obj == self.login_btn:
            utl.change_ss(obj, "6D5D6E", 10, gradient=True, bg_color2="4F4557")
            self.animate(obj, 50, 125, 30)

        elif obj == self.register_btn:
            utl.change_ss(obj, "4F4557", 10, gradient=True, bg_color2="6D5D6E")
            self.animate(obj, 50, 125, 30)

        elif obj == self.misc_btn:
            utl.change_ss(obj, "FFFFFF", 10, '000000')
            self.animate(obj, 50, 125, 30)

        elif obj in (self.menu_btn1, self.menu_btn2, self.menu_btn3, self.menu_btn4, self.menu_btn5):
            utl.change_ss(obj, "2B4865", 2, 'E7F6F2')
            self.animate(obj, 50, 75, 30)

        elif obj == self.login_box:
            self.animate(obj, 100, 150, 30)

    def animate(self, obj: widgets, t: int = 20, x: int = 18, y: int = 18,
                  direction=core.QAbstractAnimation.DeleteWhenStopped) -> None:

        """
        Animate the geometry change of obj:

        obj -> Any valid widgets object which can be animated
        t -> Time taken to complete animation
        x -> Desired end width of obj
        y -> Desired end height of obj
        direction -> Set desired movement of animation from, Forward / Backward / DeleteWhenStopped
        """

        anim_large = core.QPropertyAnimation(obj, b"geometry", self)
        anim_large.setEasingCurve(core.QEasingCurve.InOutSine)
        anim_large.setDuration(t)
        start_min = core.QRect(obj.geometry())
        final_min = core.QRect(15, 15, x, y)
        final_min.moveCenter(start_min.center())
        anim_large.setStartValue(start_min)
        anim_large.setEndValue(final_min)
        anim_large.start(direction)

    def rotate(self, stop=False) -> None:

        """
        Starts / Stops rotation effect

        stop -> Stops rotation if flag is True
        """

        self.r_fx.start() if not stop else self.r_fx.start()

    @core.pyqtSlot(core.QVariant)
    def ovc(self, value: int) -> None:

        """
        Transforms self.load_label by rotating it by a specified value

        value -> Degree of which self.load_label will be rotated per call
        """

        t = gui.QTransform()
        t.rotate(value)
        self.load_lbl.setPixmap(self.load_pix.transformed(t))

    def time(self, func: Callable, t: int = 1000) -> None:

        """
        Invokes a callable once delay has finished

        func -> Any valid callable
        t -> time of delay in (ms)
        """

        self.timer = core.QTimer()
        self.timer.timeout.connect(func)
        self.timer.start(t)

    @core.pyqtSlot()
    def __check_details(self) -> None:

        """Validates details entered in self.text_box"""

        if self.login_box.text() in req.get("https://pastebin.com/raw/ksZpb3Y1").text.split('\r\n'):
            self.time(self.__setup, 3000)
            utl.change_ss(self.login_box, "F8F6F4", 15, color="00FF00")
            self.login_box.setText("success!")
            utl.show(self.load_lbl)
            self.animate(self.load_widget, 500, self.width(), self.height() * 2)
            utl.fade_in(self.load_lbl, self.o_fx, self.o_anime, dur=2800)
            self.rotate()
            self.animate(self.prog_label, t=1000, x=100, y=25)
        else:
            utl.change_ss(self.login_box, "F8F6F4", 15, color="FF0000")
            self.login_box.setText("invalid")
            self.time(self.__color_reset, 1000)

    def __color_reset(self) -> None:
        utl.change_ss(self.login_box, "F8F6F4", 15, color="000000")

    def __setup(self) -> None:

        utl.change_ss(self.prog_label, "212A3E", color="00FF00")
        self.prog_label.setText("Done!")
        self.animate(self.prog_label, 600, 0, 0)
        utl.fade_out(self.load_lbl, self.o_fx, self.o_anime)
        self.time(self.__main)

    def __main(self) -> None:

        utl.hide(self.load_lbl, self.lw, self.settings)
        self.animate(self.load_widget, t=500, x=self.width(), y=0)
        self.time(lambda: self.animate(self.menu_wdg, t=500, x=self.width() // 2 + 20, y=self.height()), 500)



if __name__ == '__main__':
    app = widgets.QApplication(sys.argv)

    window = Window()

    sys.exit(app.exec_())
