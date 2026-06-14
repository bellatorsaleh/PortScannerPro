"""
Scanner Engine - Core port scanning logic with threading and service detection.
"""

import socket
import threading
import time
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed

# Well-known service names
SERVICE_MAP = {
    20: "FTP-Data", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 67: "DHCP", 68: "DHCP", 69: "TFTP", 80: "HTTP",
    110: "POP3", 111: "RPC", 119: "NNTP", 123: "NTP", 135: "MSRPC",
    137: "NetBIOS", 138: "NetBIOS", 139: "NetBIOS", 143: "IMAP",
    161: "SNMP", 162: "SNMP-Trap", 179: "BGP", 194: "IRC",
    389: "LDAP", 443: "HTTPS", 445: "SMB", 465: "SMTPS",
    514: "Syslog", 515: "LPD", 587: "SMTP-Sub", 631: "IPP",
    636: "LDAPS", 873: "rsync", 993: "IMAPS", 995: "POP3S",
    1080: "SOCKS", 1194: "OpenVPN", 1433: "MSSQL", 1521: "Oracle",
    1723: "PPTP", 2049: "NFS", 2082: "cPanel", 2083: "cPanel-SSL",
    2181: "Zookeeper", 2375: "Docker", 2376: "Docker-TLS",
    3000: "Dev-Server", 3306: "MySQL", 3389: "RDP", 3690: "SVN",
    4000: "Dev-Alt", 4444: "Metasploit", 5000: "Flask/UPnP",
    5432: "PostgreSQL", 5672: "RabbitMQ", 5900: "VNC", 5901: "VNC-1",
    6379: "Redis", 6443: "Kubernetes", 6667: "IRC",
    7001: "WebLogic", 8000: "HTTP-Alt", 8008: "HTTP-Alt",
    8080: "HTTP-Proxy", 8081: "HTTP-Alt", 8443: "HTTPS-Alt",
    8888: "Jupyter", 9000: "PHP-FPM", 9092: "Kafka",
    9200: "Elasticsearch", 9300: "Elasticsearch", 10000: "Webmin",
    11211: "Memcached", 27017: "MongoDB", 27018: "MongoDB",
    50000: "SAP", 50070: "Hadoop"
}

# Banner grabbing probes
BANNER_PROBES = {
    21: b"",
    22: b"",
    23: b"",
    25: b"EHLO scanner\r\n",
    80: b"HEAD / HTTP/1.0\r\n\r\n",
    110: b"",
    143: b"",
    443: b"",
}

RISK_LEVELS = {
    "critical": [21, 23, 135, 137, 138, 139, 445, 1433, 3389, 4444, 5900],
    "high":     [22, 25, 53, 80, 110, 143, 3306, 5432, 6379, 27017, 11211],
    "medium":   [443, 993, 995, 8080, 8443, 9200, 27018],
    "low":      []
}

def get_risk_level(port):
    for level, ports in RISK_LEVELS.items():
        if port in ports:
            return level
    return "info"

def get_service(port):
    try:
        return socket.getservbyport(port)
    except Exception:
        return SERVICE_MAP.get(port, "unknown")

def grab_banner(host, port, timeout=2.0):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        probe = BANNER_PROBES.get(port, b"")
        if probe:
            s.send(probe)
        banner = s.recv(1024).decode("utf-8", errors="ignore").strip()
        s.close()
        return banner[:120] if banner else ""
    except Exception:
        return ""

def scan_port(host, port, timeout=1.0, grab_banners=True):
    result = {
        "port": port,
        "state": "closed",
        "service": get_service(port),
        "banner": "",
        "response_time": 0,
        "risk": get_risk_level(port)
    }
    try:
        start = time.time()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        code = s.connect_ex((host, port))
        elapsed = round((time.time() - start) * 1000, 2)
        s.close()

        if code == 0:
            result["state"] = "open"
            result["response_time"] = elapsed
            if grab_banners:
                result["banner"] = grab_banner(host, port, timeout)
        else:
            result["state"] = "closed"
    except socket.timeout:
        result["state"] = "filtered"
    except Exception:
        result["state"] = "error"
    return result


class PortScanner:
    def __init__(self, host, port_start, port_end, timeout=1.0,
                 max_threads=100, grab_banners=True,
                 on_result=None, on_progress=None, on_complete=None):
        self.host = host
        self.port_start = port_start
        self.port_end = port_end
        self.timeout = timeout
        self.max_threads = max_threads
        self.grab_banners = grab_banners
        self.on_result = on_result
        self.on_progress = on_progress
        self.on_complete = on_complete
        self._stop_event = threading.Event()
        self.results = []

    def stop(self):
        self._stop_event.set()

    def is_running(self):
        return not self._stop_event.is_set()

    def resolve_host(self):
        try:
            ip = socket.gethostbyname(self.host)
            return ip
        except socket.gaierror:
            return None

    def run(self):
        ip = self.resolve_host()
        if not ip:
            if self.on_complete:
                self.on_complete([], error=f"Cannot resolve host: {self.host}")
            return

        ports = list(range(self.port_start, self.port_end + 1))
        total = len(ports)
        scanned = 0
        open_results = []
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = {
                executor.submit(scan_port, ip, p, self.timeout, self.grab_banners): p
                for p in ports
            }
            for future in as_completed(futures):
                if self._stop_event.is_set():
                    executor.shutdown(wait=False, cancel_futures=True)
                    break
                result = future.result()
                scanned += 1
                if result["state"] == "open":
                    open_results.append(result)
                    if self.on_result:
                        self.on_result(result)
                if self.on_progress:
                    self.on_progress(scanned, total, len(open_results))

        elapsed = round(time.time() - start_time, 2)
        self.results = open_results
        if self.on_complete:
            self.on_complete(open_results, scan_time=elapsed,
                             total_scanned=scanned, ip=ip)
