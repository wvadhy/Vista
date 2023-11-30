from abc import ABC
import PyQt5.QtWidgets as widgets
import PyQt5.QtCore as core
import PyQt5.QtGui as gui
from typing import *


class Utilities(ABC):

    """A list of complementary methods compartmentalised for brevity"""

    @staticmethod
    def wdg_builder(width: int, height: int,
                    x: int = 0, y: int = 0, **kwargs) -> widgets.QWidget:

        """
        Creates a new QWidget

        width -> Width of widget
        height -> Height of widget
        x -> Dimensional horizontal geometry
        y -> Dimensional vertical geometry
        **kwargs -> Any valid property attributes for widgets.QWidgets
        """

        obj = widgets.QWidget()
        obj.setGeometry(x, y, width, height)

        return Utilities.gen_args(obj, kwargs)


    @staticmethod
    def lbl_builder(name: str, width: int, height: int,
                    pix: str = "", font: str = "Arial", f_size: int = 10,
                    x: int = 0, y: int = 0, **kwargs) -> widgets.QLabel:

        """
        Creates a new QLabel

        name -> Name of label
        width -> Width of label
        height -> Height of label
        x -> Dimensional horizontal geometry
        y -> Dimensional vertical geometry
        font -> Selected font for label
        f_size -> Text size
        pix -> Image path, used to super-impose image over label, leave blank for just text
        **kwargs -> Any valid property attributes for widgets.QLabel
        """

        obj = widgets.QLabel(name)
        obj.setGeometry(x, y, width, height)
        obj.setFont(gui.QFont(font, f_size, obj.font().Bold)) \
            if kwargs.get("bold") \
            else obj.setFont(gui.QFont(font, f_size))

        if pix: obj.setPixmap(gui.QPixmap(pix))

        return Utilities.gen_args(obj, kwargs)

    @staticmethod
    def lne_builder(name: str, width: int, height: int,
                    x: int = 0, y: int = 0,
                    holder: str = "...", **kwargs) -> widgets.QLineEdit:

        """
        Creates a new QLineEdit

        name -> Name of textbox
        width -> Width of textbox
        height -> Height of textbox
        x -> Dimensional horizontal geometry
        y -> Dimensional vertical geometry
        holder -> Placeholder text
        **kwargs -> Any valid property attributes for widgets.QLineEdit
        """

        obj = widgets.QLineEdit(name)
        obj.setGeometry(x, y, width, height)
        obj.setAttribute(core.Qt.WA_MacShowFocusRect, 0)
        obj.setPlaceholderText(holder)

        return Utilities.gen_args(obj, kwargs)

    @staticmethod
    def btn_builder(name: str, width: int, height: int,
                    x: int = 0, y: int = 0,
                    font: str = "Arial", f_size: int = 10, **kwargs) -> widgets.QPushButton:

        """
        Creates a new QPushButton

        name -> Name of button
        width -> Width of button
        height -> Height of button
        x -> Dimensional horizontal geometry
        y -> Dimensional vertical geometry
        font -> Selected font for text
        f_size -> Text size
        **kwargs -> Any valid property attributes for widgets.QPushButoon
        """

        obj = widgets.QPushButton(name)
        obj.setGeometry(x, y, width, height)
        obj.setFont(gui.QFont(font, f_size, obj.font().Bold)) \
            if kwargs.get("bold") \
            else obj.setFont(gui.QFont(font, f_size))

        return Utilities.gen_args(obj, kwargs)

    @staticmethod
    def change_ss(obj: widgets, bg_color: AnyStr, border: int = 5, color: AnyStr = 'FFFFFF',
                  bg_color2: AnyStr = "", **kwargs: Any) -> None:

        """
        Changes the background color of passed in object:

        obj -> Any applicable object from QtWidgets
        bg_color -> Any valid hex color used for background
        color -> Any valid hex color used for text
        border -> Integer value used for curvature
        gradient -> Creates a gradient from bg_color and kwargs if True else flat
        **kwargs -> Any valid arguments where key=valid_css_property
        """

        if bg_color2:
            obj.setStyleSheet(f"""background-color: 
                                  qlineargradient(x1: 0, x2: 1, stop: 0 #{bg_color}, 
                                  stop: 1 #{bg_color2});
                                  border-radius: {border}px;
                                  color: #{color}""")
        else:
            obj.setStyleSheet(f'background-color: #{bg_color}; border-radius: {border}px; color: #{color}')

    @staticmethod
    def setup_effects(p, vc: Callable) -> Tuple:

        """Setup graphics effects to be declared in main Window"""

        o_fx = widgets.QGraphicsOpacityEffect()
        s_fx = widgets.QGraphicsDropShadowEffect()
        g_fx = widgets.QGraphicsDropShadowEffect()
        r_fx = core.QVariantAnimation(p, startValue=0.0, endValue=900.0, duration=3000, valueChanged=vc)
        o_anime = core.QPropertyAnimation(o_fx, b"opacity")
        s_fx.setOffset(0, 0)
        s_fx.setBlurRadius(10)
        s_fx.setColor(gui.QColor(255, 255, 255))
        g_fx.setOffset(0, 0)
        g_fx.setBlurRadius(50)
        g_fx.setColor(gui.QColor(0, 0, 0))
        return o_fx, s_fx, g_fx, r_fx, o_anime

    @staticmethod
    def fade_out(widget: widgets, o_fx: widgets.QGraphicsOpacityEffect,
                 a: core.QPropertyAnimation, dur: int = 1000) -> None:

        """
        Fade out selected widget

        widget -> Applicable QtWidgets object
        o_fx -> Opacity graphics effect
        a -> Animation specification
        dur -> Duration
        """

        widget.setGraphicsEffect(o_fx)
        a.setDuration(dur)
        a.setStartValue(1)
        a.setEndValue(0)
        a.start()

    @staticmethod
    def fade_in(widget: widgets, o_fx: widgets.QGraphicsOpacityEffect,
                 a: core.QPropertyAnimation, dur: int = 1000) -> None:

        """
        Fade in selected widget

        widget -> Applicable QtWidgets object
        o_fx -> Opacity graphics effect
        a -> Animation specification
        dur -> Duration
        """

        widget.setGraphicsEffect(o_fx)
        a.setDuration(dur)
        a.setStartValue(0)
        a.setEndValue(1)
        a.start()

    @staticmethod
    def gen_args(obj: widgets, vals: Dict) -> widgets:

        """
        Compartmentalises generic builder predicates into one function

        obj -> Widget object passed from any _builder function
        vals -> **kwargs values
        """

        if align := vals.get("align"): obj.setAlignment(align)

        if conn := vals.get("conn"): obj.clicked.connect(conn)

        if parent := vals.get("p"): obj.setParent(parent)

        if graphic := vals.get("fx"): obj.setGraphicsEffect(graphic)

        if vals.get("hide"): obj.setHidden(True)

        if efilter := vals.get("filter"): obj.installEventFilter(efilter)

        if mov := vals.get("move"): obj.move(*mov)

        if vals := vals.get("style"): Utilities.change_ss(obj, *vals)

        return obj

    @staticmethod
    def hide(*args: widgets) -> None:
        for obj in args: obj.setHidden(True)

    @staticmethod
    def show(*args: widgets) -> None:
        for obj in args: obj.setHidden(False)