from qtpy.QtWidgets import QLineEdit


class CustomLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(CustomLineEdit, self).__init__(parent)

        self.setText('CustomLineEdit')
