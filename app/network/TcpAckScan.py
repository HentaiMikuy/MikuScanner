from time import sleep

import nmap
from PySide6.QtCore import QThread, Signal


class TcpAckScan(QThread):

    updateList = Signal(list)
    stopSignal = Signal()
    endReady = Signal()

    def __init__(self, hosts: str, widget_ring):
        super().__init__()
        self.hosts = hosts
        self.ring = widget_ring
        self.ipList = []

    def run(self):
        self._scan(self.hosts)

    def _scan(self, hosts: str):

        nmapScanner = nmap.PortScanner()
        self.ring.setValue(5)
        sleep(1)
        nmapScanner.scan(hosts=hosts, arguments='-sA')
        self.ring.setValue(10)
        sleep(1)

        if self.isInterruptionRequested():
            self.quit()
            self.stopSignal.emit()
            return
        self.ring.setValue(20)
        sleep(1)

        for host in nmapScanner.all_hosts():
            if nmapScanner[host].state() == 'up':
                self.ipList.append(host)

        self.ring.setValue(100)
        self.updateList.emit(self.ipList)
        self.endReady.emit()