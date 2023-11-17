# -*- coding: utf-8 -*-
import re
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep

from PySide6.QtCore import QThread, Signal
from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sr1


def _generate_ip(start_ip, end_ip):
    """
    生成给定范围内的IP地址
    :param start_ip: 起始IP
    :param end_ip:  结束IP
    :return: 通过for-in进行取值
    """
    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)

    current_ip = start
    while current_ip <= end:
        yield str(current_ip)
        current_ip += 1


class TcpConnectScan(QThread):
    """
    TCP全连接扫描类
    """
    resultReady = Signal(list)
    updateList = Signal(list)
    stopSignal = Signal()
    endReady = Signal()

    def __init__(self, threadNum: int, hosts: str, ports: str, widget_ring):
        super().__init__()
        self.executor = None
        self.threadNum = threadNum
        self.hosts = hosts
        self.ports = ports
        self.ring = widget_ring
        self.futures = []
        self.ipList = []

    def run(self):
        self.ring.setValue(1)
        sleep(0.1)
        self._scan(self.hosts, self.ports)
        self.ring.setValue(100)

    def _pack_send(self, ip: str, ports: list) -> str | None:
        """
        构造数据包发送
        :param ip: 单个点分十进制IP地址
        :param ports: 端口号列表
        :return: 字符串信息是否存活，异常返回None
        """
        ports = list(map(int, ports))
        try:
            for port in ports if len(ports) == 1 or ports[1] != '-' else range(ports[0], ports[2] + 1):
                resp = sr1(IP(dst=ip) / TCP(dport=port, flags="S"), timeout=1, verbose=0)
                if resp and resp.haslayer(TCP) and resp.getlayer(TCP).flags == 0x12:
                    self.ipList.append(ip)
                    return "{} is alive!".format(ip)
                return None
        except:
            return None

    def __scan_deal(self):
        all_result = []
        for future in as_completed(self.futures):
            result = future.result()
            if result is not None:
                all_result.append(result)

        if self.isInterruptionRequested():
            self.quit()
            self.stopSignal.emit()
            return

        self.ring.setValue(75)
        sleep(1)
        self.resultReady.emit(all_result)
        self.updateList.emit(self.ipList)
        self.executor.shutdown()
        self.endReady.emit()

    def _scan(self, hosts: str, ports: str):
        """
        进行TCP全连接扫描，对于单端口目标只需输入start_port即可
        :param hosts: 目标IP，点分十进制和CIDR记法，一定范围用”-“进行分隔，多个目标用”,“隔开
        :param ports: 端口号
        """
        if "-" in ports:
            ports = ports.split("-")
            ports.insert(1, "-")
        elif "," in ports:
            ports = ports.split(",")
        else:
            ports = ports.split()

        if '/' in hosts or ',' in hosts:
            # 正则匹配：xxx.xxx.xxx.
            prefix = re.search(r"^(\d{1,3}\.){3}", hosts).group() if '/' in hosts else hosts.split(',')
            self.executor = ThreadPoolExecutor(max_workers=self.threadNum)
            self.ring.setValue(5)
            sleep(0.1)
            for i in range(1, 255) if '/' in hosts else prefix:
                ip = prefix+str(i) if '/' in hosts else i
                future = self.executor.submit(self._pack_send, ip, ports)
                self.futures.append(future)
            self.ring.setValue(50)
            sleep(0.1)
            self.__scan_deal()

        else:
            ip_range = hosts.split('-')
            self.executor = ThreadPoolExecutor(max_workers=self.threadNum)
            self.ring.setValue(5)
            sleep(0.1)
            for ip in _generate_ip(ip_range[0], ip_range[1]):
                future = self.executor.submit(self._pack_send, ip, ports)
                self.futures.append(future)
            self.ring.setValue(50)
            sleep(0.1)
            self.__scan_deal()
