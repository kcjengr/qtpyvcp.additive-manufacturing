import os
import sys

from xml.dom import minidom

from qtpy.QtCore import Slot
from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout
from qtpy.QtSvg import QSvgWidget, QSvgRenderer

from qtpyvcp import hal
from qtpyvcp.widgets import HALWidget
from qtpyvcp.plugins import getPlugin, LOG

STATUS = getPlugin('status')


IN_DESIGNER = os.getenv('DESIGNER', False)


class SvgSlicer(QSvgWidget, HALWidget):
    """HAL Connections for SvgSlicer

    SvgSlicer will display layers according to `u32` and `s32` HAL pin values.

    .. table:: HAL Pins

        =============================== ========= =========
        HAL Pin Name                    Type      Direction
        =============================== ========= =========
        qtpyvcp.svgslicer.enable        bool      in
        qtpyvcp.svgslicer.layer.in      s32       in
        qtpyvcp.svgslicer.layer.count   s32       out
        =============================== ========= =========

    Notes:
        ...
    """

    def __init__(self, parent=None):
        super(SvgSlicer, self).__init__(parent)

        self.status = STATUS

        self._enabled_pin = None
        self._layer_in_pin = None
        self._layer_count_pin = None

        self._svg_header = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.0//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
<svg width="23.838" height="23.838" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:slic3r="http://slic3r.org/namespaces/slic3r">
"""
        self._svg_end = "</svg>"

        self._current_layer = 0
        self._num_layers = 0

        self._file_name = ""
        self._layers = None

        self.status.file.notify(self.load)

    def initialize(self):
        comp = hal.getComponent()
        obj_name = self.getPinBaseName()

        # enable HAL pin
        _pin_name = ".".join([obj_name, "enable"])
        self._enabled_pin = comp.addPin(_pin_name, "bit", "in")
        self._enabled_pin.value = self.isEnabled()
        self._enabled_pin.valueChanged.connect(self.setEnabled)

        # layer in HAL pin
        _pin_name = ".".join([obj_name, "layer", "in"])
        self._layer_in_pin = comp.addPin(_pin_name, "s32", "in")
        self._layer_in_pin.valueChanged.connect(self.selectLayer)

        # layer count out HAL pin
        _pin_name = ".".join([obj_name, "layer", "count"])
        self._layer_count_pin = comp.addPin(_pin_name, "s32", "out")
        self._layer_count_pin.value = self._num_layers

    def get_layers(self):
        xmldoc = minidom.parse(self._file_name)

        assert isinstance(xmldoc, minidom.Document)

        _layers = []
        for node in xmldoc.getElementsByTagName('g'):
            _layers.append(node)

        return _layers

    def select_layers(self):
        xmldoc = minidom.parse(self._file_name)

        assert isinstance(xmldoc, minidom.Document)

        svg_data = None

        # for all group nodes...
        for node in xmldoc.getElementsByTagName('g'):
            if int(node.attributes['id'].value.lstrip('layer')) == self._current_layer:
                svg_data = node.toxml()
                break

        return svg_data

    def draw(self):
        layer = self.select_layers()
        svg_file = "{}{}\n{}".format(self._svg_header, layer, self._svg_end)
        svg_bytes = bytearray(svg_file, encoding='utf-8')
        
        self.renderer().load(svg_bytes)

    def load(self, file_name):
        self._file_name = file_name
        self._layers = self.get_layers()
        self._num_layers = len(self._layers)
        self._layer_count_pin.value = self._num_layers

        self.draw()

    def selectLayer(self, layer):
        self._current_layer = layer

        self.draw()

