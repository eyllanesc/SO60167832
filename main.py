import subprocess
import threading

from PyQt5 import QtCore


class Worker(QtCore.QObject):
    outSignal = QtCore.pyqtSignal(str)
    errSignal = QtCore.pyqtSignal(str)

    def run_command(self, cmd, **kwargs):
        threading.Thread(
            target=self._execute_command, args=(cmd,), kwargs=kwargs, daemon=True
        ).start()

    def _execute_command(self, cmd, **kwargs):
        with subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs
        ) as proc:
            out, err = proc.communicate()
            if out:
                self.outSignal.emit(out.decode())
            if err:
                self.errSignal.emit(err.decode())


if __name__ == "__main__":
    import os
    import sys

    app = QtCore.QCoreApplication(sys.argv)
    w = Worker()

    def printer(data):
        print(data)

    w.outSignal.connect(print)
    w.errSignal.connect(print)

    w.run_command("test.bat", cwd="./", shell=True)
    w.run_command("cd", cwd="./", shell=True)
    w.run_command("whoami", cwd="./", shell=True)
    w.run_command("dir", cwd="./", shell=True)

    QtCore.QTimer.singleShot(60 * 1000, QtCore.QCoreApplication.quit)

    sys.exit(app.exec_())
