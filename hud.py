import sys
import psutil
from PyQt6.QtCore import QThread, Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class TelemetryWorker(QThread):
  """Background thread to fetch live metrics without blocking the UI."""

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

  def initUI(self):
    self.setWindowTitle("CyberSec-Talent HUD | Ops Center")
    self.setGeometry(100, 100, 1100, 700)

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
                border-radius: 4px; padding: 10px; font-weight: bold;
            }
            QPushButton:hover { background-color: #2563EB; }
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
    talent_title = QLabel("📊 Talent & Skill Metrics")
    talent_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))

    stats_label = QLabel(
        "• GitHub Portfolio: HACKERpgx\n• Focus Areas: Cybersecurity & Python"
        " HUDs\n• Hack Club Half Life: Week 5 (Design Your Own)\n• Lab & CTF"
        " Track: Active"
    )
    stats_label.setFont(QFont("Segoe UI", 10))
    stats_label.setAlignment(Qt.AlignmentFlag.AlignTop)  # Fixed alignment call

    talent_layout.addWidget(talent_title)
    talent_layout.addWidget(stats_label)
    grid_layout.addWidget(talent_card, 0, 1)

    # --- TILE 3: Operations Command Panel (Bottom) ---
    control_card = QWidget()
    control_card.setObjectName("Card")
    control_layout = QVBoxLayout(control_card)
    control_title = QLabel("⚙️ Operations Command Console")
    control_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))

    self.btn_scan = QPushButton("Run Live System & Network Scan")
    self.btn_scan.clicked.connect(self.run_telemetry_scan)

    self.btn_alert = QPushButton("Toggle Intrusion Alarm State")
    self.btn_alert.clicked.connect(self.toggle_alarm)

    control_layout.addWidget(control_title)
    control_layout.addWidget(self.btn_scan)
    control_layout.addWidget(self.btn_alert)
    grid_layout.addWidget(control_card, 1, 0, 1, 2)

    grid_layout.setColumnStretch(0, 1)
    grid_layout.setColumnStretch(1, 1)

  def run_telemetry_scan(self):
    self.sec_log.append("\n[~] Scanning system telemetry...")
    self.worker = TelemetryWorker()
    self.worker.update_signal.connect(self.append_log)
    self.worker.start()

  def append_log(self, text):
    self.sec_log.append(text)

  def toggle_alarm(self):
    self.alarm_active = not self.alarm_active
    if self.alarm_active:
      self.btn_alert.setStyleSheet(
          "background-color: #EF4444; color: white; border-radius: 4px; padding:"
          " 10px; font-weight: bold;"
      )
      self.sec_log.append("[!] WARNING: Intrusion Alarm State ACTIVATED!")
    else:
      self.btn_alert.setStyleSheet(
          "background-color: #3B82F6; color: white; border-radius: 4px; padding:"
          " 10px; font-weight: bold;"
      )
      self.sec_log.append(
          "[+] Intrusion Alarm Disarmed. System in normal monitor mode."
      )


if __name__ == "__main__":
  app = QApplication(sys.argv)
  hud = CyberSecHUD()
  hud.show()
  sys.exit(app.exec())
