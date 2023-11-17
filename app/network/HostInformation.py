from PySide6.QtCore import QThread, Signal
from nmap import nmap


class HostInformation(QThread):
    results = Signal(str, str, list)

    def __init__(self, host: str):
        super().__init__()
        self.host = host

    def run(self):
        self._info(self.host)

    def _info(self, host):
        nmapScanner = nmap.PortScanner()
        scan_result = nmapScanner.scan(host, arguments='-O')

        OS_info = scan_result['scan'][host]['osmatch'][0]['name']
        Port_info = []

        open_ports = scan_result['scan'][host]['tcp']
        for port in open_ports:
            Port_info.append([str(port), 'Open', open_ports[port]['name']])

        self.results.emit(host, OS_info, Port_info)