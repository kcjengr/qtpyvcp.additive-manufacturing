from qtpyvcp.widgets.qtdesigner import _DesignerPlugin

from custom_line_edit import CustomLineEdit
class CustomLineEdit_Plugin(_DesignerPlugin):
    def pluginClass(self):
        return CustomLineEdit
