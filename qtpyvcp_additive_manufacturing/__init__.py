from qtpyvcp.widgets.qtdesigner import _DesignerPlugin

from svg_slicer.svg_slicer import SvgSlicer
class SvgWidget_Plugin(_DesignerPlugin):
    def pluginClass(self):
        return SvgSlicer
