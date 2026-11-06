import json
import socket
import sys
import urllib.request
import psutil
from PyQt6.QtCore import QThread, Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class PortScannerWorker(QThread):
  """Background thread to scan targeted network ports asynchronously."""

  update_signal = pyqtSignal(str)

  def __init__(self, target_host):
    super().__init__()
    self.target_host = target_host

  def run(self):
    target_ports = [21, 22, 80, 443, 8080, 3306, 5432]
    self.update_signal.emit(
        f"[~] Initiating Port Audit on host: {self.target_host}..."
    )
    open_ports = 0

    for port in target_ports:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.settimeout(0.5)
      result = sock.connect_ex((self.target_host, port))
      if result == 0:
        self.update_signal.emit(
            f"    [!] PORT OPEN: {port} (Service active/listening)"
        )
        open_ports += 1
      else:
        self.update_signal.emit(f"    [-] Port Closed/Filtered: {port}")
      sock.close()

    self.update_signal.emit(
        f"[+] Audit Complete: Found {open_ports} open ports on"
        f" {self.target_host}."
    )


class GitHubWorker(QThread):
  """Background thread to fetch live GitHub stats from public API."""

  update_signal = pyqtSignal(str)

  def run(self):
    try:
      url = "https://api.github.com/users/HACKERpgx"
      req = urllib.request.Request(
          url, headers={"User-Agent": "CyberSec-Talent-HUD"}
      )
      with urllib.request.urlopen(req, timeout=5) as response:
        data = json.loads(response.read().decode())
        public_repos = data.get("public_repos", "N/A")
        followers = data.get("followers", "N/A")
        name = data.get("name", "HACKERpgx")
        self.update_signal.emit(
            f"[+] GitHub API Connected Successfully!\n"
            f"    • User: {name} (@HACKERpgx)\n"
            f"    • Public Repositories: {public_repos}\n"
            f"    • Followers: {followers}"
        )
    except Exception as e:
      self.update_signal.emit(
          f"[!] GitHub API Warning: Could not fetch live stats ({str(e)})"
      )


class TelemetryWorker(QThread):
  """Background thread to fetch live system metrics without blocking the UI."""

  update_signal = pyqtSignal(str)

  def run(self):
    try:
      connections = psutil.net_connections(kind="inet")
      active_count = sum(1 for c in connections if c.status == "ESTABLISHED")
      self.update_signal.emit(
          f"[+] Active Established Connections: {active_count}"
      )

      cpu_usage = psutil.cpu_percent(interval=1)
      mem_usage = psutil.virtual_memory().percent
      self.update_signal.emit(
          f"[+] System Health -> CPU: {cpu_usage}% | RAM: {mem_usage}%"
      )
    except Exception as e:
      self.update_signal.emit(f"[!] Telemetry Warning: {str(e)}")


class CyberSecHUD(QMainWindow):

  def __init__(self):
    super().__init__()
    self.alarm_active = False
    self.initUI()
    self.load_github_stats()

  def initUI(self):
    self.setWindowTitle("CyberSec-Talent HUD | Ops Center")
    self.setGeometry(100, 100, 1100, 750)

    self.setStyleSheet(
        """
            QMainWindow { background-color: #0F172A; }
            QLabel { color: #E2E8F0; font-family: 'Segoe UI', sans-serif; }
            QWidget#Card { 
                background-color: #1E293B; 
                border: 1px solid #334155; 
                border-radius: 8px; 
            }
            QPushButton { 
                background-color: #3B82F6; color: white; 
                border-radius: 4px; padding: 8px 12px; font-weight: bold;
            }
            QPushButton:hover { background-color: #2563EB; }
            QLineEdit {
                background-color: #090D16; color: #38BDF8;
                border: 1px solid #334155; border-radius: 4px; padding: 6px;
                font-family: 'Consolas', monospace;
            }
            QTextEdit { 
                background-color: #090D16; color: #38BDF8; 
                border: 1px solid #334155; font-family: 'Consolas', monospace; 
            }
        """
    )

    central_widget = QWidget()
    self.setCentralWidget(central_widget)
    grid_layout = QGridLayout(central_widget)
    grid_layout.setContentsMargins(15, 15, 15, 15)
    grid_layout.setHorizontalSpacing(15)
    grid_layout.setVerticalSpacing(15)

    # --- TILE 1: Security Telemetry (Top Left) ---
    sec_card = QWidget()
    sec_card.setObjectName("Card")
    sec_layout = QVBoxLayout(sec_card)
    sec_title = QLabel("🛡️ Active Security Telemetry")
    sec_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))

    self.sec_log = QTextEdit()
    self.sec_log.setReadOnly(True)
    self.sec_log.append("[+] Port Watchdog: Initialized")
    self.sec_log.append("[+] Intrusion Detection: Armed & Ready")

    sec_layout.addWidget(sec_title)
    sec_layout.addWidget(self.sec_log)
    grid_layout.addWidget(sec_card, 0, 0)

    # --- TILE 2: Talent & Portfolio Panel (Top Right) ---
    talent_card = QWidget()
    talent_card.setObjectName("Card")
    talent_layout = QVBoxLayout(talent_card)
    talent_title = QLabel("📊 Talent & Skill Metrics (Live GitHub)")
    talent_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))

    self.talent_log = QTextEdit()
    self.talent_log.setReadOnly(True)
    self.talent_log.append("[~] Connecting to GitHub API for HACKERpgx...")

    talent_layout.addWidget(talent_title)
    talent_layout.addWidget(self.talent_log)
    grid_layout.addWidget(talent_card, 0, 1)

    # --- TILE 3: Operations & Port Audit Panel (Bottom) ---
    control_card = QWidget()
    control_card.setObjectName("Card")
    control_layout = QVBoxLayout(control_card)
    control_title = QLabel("⚙️ Operations & Port Audit Console")
    control_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))

    # Port Scan Controls Row
    scan_row = QHBoxLayout()
    self.host_input = QLineEdit()
    self.host_input.setText("127.0.0.1")
    self.host_input.setPlaceholderText("Target IP/Host (e.g. 127.0.0.1)")

    self.btn_port_scan = QPushButton("Run Port Audit")
    self.btn_port_scan.clicked.connect(self.run_port_scan)

    scan_row.addWidget(self.host_input)
    scan_row.addWidget(self.btn_port_scan)

    # Global Buttons Row
    btn_row = QHBoxLayout()
    self.btn_scan = QPushButton("Run Telemetry Scan")
    self.btn_scan.clicked.connect(self.run_telemetry_scan)

    self.btn_alert = QPushButton("Toggle Intrusion Alarm")
    self.btn_alert.clicked.connect(self.toggle_alarm)

    btn_row.addWidget(self.btn_scan)
    btn_row.addWidget(self.btn_alert)

    control_layout.addWidget(control_title)
    control_layout.addLayout(scan_row)
    control_layout.addLayout(btn_row)
    grid_layout.addWidget(control_card, 1, 0, 1, 2)

    grid_layout.setColumnStretch(0, 1)
    grid_layout.setColumnStretch(1, 1)

  def load_github_stats(self):
    self.gh_worker = GitHubWorker()
    self.gh_worker.update_signal.connect(self.append_talent_log)
    self.gh_worker.start()

  def append_talent_log(self, text):
    self.talent_log.append(text)

  def run_telemetry_scan(self):
    self.sec_log.append("\n[~] Scanning system telemetry...")
    self.worker = TelemetryWorker()
    self.worker.update_signal.connect(self.append_sec_log)
    self.worker.start()

  def run_port_scan(self):
    target = self.host_input.text().strip() or "127.0.0.1"
    self.port_worker = PortScannerWorker(target)
    self.port_worker.update_signal.connect(self.append_sec_log)
    self.port_worker.start()

  def append_sec_log(self, text):
    self.sec_log.append(text)

  def toggle_alarm(self):
    self.alarm_active = not self.alarm_active
    if self.alarm_active:
      self.btn_alert.setStyleSheet(
          "background-color: #EF4444; color: white; border-radius: 4px; padding:"
          " 8px 12px; font-weight: bold;"
      )
      self.sec_log.append("[!] WARNING: Intrusion Alarm State ACTIVATED!")
    else:
      self.btn_alert.setStyleSheet(
          "background-color: #3B82F6; color: white; border-radius: 4px; padding:"
          " 8px 12px; font-weight: bold;"
      )
      self.sec_log.append(
          "[+] Intrusion Alarm Disarmed. System in normal monitor mode."
      )


if __name__ == "__main__":
  app = QApplication(sys.argv)
  hud = CyberSecHUD()
  hud.show()
  sys.exit(app.exec())
