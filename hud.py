import sys
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
    # Placeholder for psutil / socket telemetry checks
    # e.g., checking active connections or system stats
    self.update_signal.emit("[INFO] Security HUD monitoring initialized...")


class CyberSecHUD(QMainWindow):

  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    self.setWindowTitle("CyberSec-Talent HUD")
    self.setGeometry(100, 100, 1100, 700)

    # Dark Theme Palette Styling
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
                border-radius: 4px; padding: 8px; font-weight: bold;
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
    self.sec_log.append("[+] Port Watchdog: Active")
    self.sec_log.append("[+] Intrusion Detection: Standby")
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
        "• GitHub Repos: Active\n• CTF Labs Completed: Verified\n• Hack Club"
        " Half Life: Week 5 in Progress"
    )
    stats_label.setFont(QFont("Segoe UI", 10))
    stats_label.setAlignment(Qt.AlignmentFlag.AlignTop)
    talent_layout.addWidget(talent_title)
    talent_layout.addWidget(stats_label)
    grid_layout.addWidget(talent_card, 0, 1)

    # --- TILE 3: Quick Controls / Actions (Bottom Left/Right spanning) ---
    control_card = QWidget()
    control_card.setObjectName("Card")
    control_layout = QVBoxLayout(control_card)
    control_title = QLabel("⚙️ Operations Command Panel")
    control_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))

    self.btn_scan = QPushButton("Run Quick Network Check")
    self.btn_alert = QPushButton("Toggle Intrusion Alarm State")

    control_layout.addWidget(control_title)
    control_layout.addWidget(self.btn_scan)
    control_layout.addWidget(self.btn_alert)
    grid_layout.addWidget(control_card, 1, 0, 1, 2)

    # Set column stretch for a balanced side-by-side view
    grid_layout.setColumnStretch(0, 1)
    grid_layout.setColumnStretch(1, 1)


if __name__ == "__main__":
  app = QApplication(sys.argv)
  hud = CyberSecHUD()
  hud.show()
  sys.exit(app.exec())
