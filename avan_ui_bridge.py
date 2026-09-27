from PySide6.QtCore import QObject, Signal


class AvanUIBridge(QObject):

    # Main status
    status_changed = Signal(str)

    # Last command
    command_changed = Signal(str)

    # Module status
    module_changed = Signal(str, bool)

    def set_status(self, status):
        status = status.upper()

        print(f"[AVAN UI] STATUS: {status}")

        self.status_changed.emit(status)

    def set_command(self, command):
        print(f"[AVAN UI] COMMAND: {command}")

        self.command_changed.emit(command)

    def set_module(self, module, online=True):
        state = bool(online)

        print(
            f"[AVAN UI] MODULE: {module} = "
            f"{'ONLINE' if state else 'OFFLINE'}"
        )

        self.module_changed.emit(
            module.upper(),
            state
        )


ui_bridge = AvanUIBridge()