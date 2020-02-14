import os
import select
import subprocess
import threading

from PyQt5 import QtCore


class Worker(QtCore.QObject):
    outSignal = QtCore.pyqtSignal(str)

    def run_command(self, cmd, **kwargs):
        threading.Thread(
            target=self._execute_command, args=(cmd,), kwargs=kwargs, daemon=True
        ).start()

    def _execute_command(self, cmd, **kwargs):
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kwargs
        )
        for line in proc.stdout:
            self.outSignal.emit(line.decode())


if __name__ == "__main__":
    import sys

    app = QtCore.QCoreApplication(sys.argv)
    w = Worker()

    def printer(data):
        print(data)

    w.outSignal.connect(lambda r: print(r, QtCore.QTime.currentTime()))

    w.run_command("test.bat", cwd="./", shell=True)
    # w.run_command("cd", cwd="./", shell=True)
    # w.run_command("whoami", cwd="./", shell=True)
    # w.run_command("dir", cwd="./", shell=True)
    w.run_command(["ping", "8.8.8.8"])

    QtCore.QTimer.singleShot(60 * 1000, QtCore.QCoreApplication.quit)

    sys.exit(app.exec_())
