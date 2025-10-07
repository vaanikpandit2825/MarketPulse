# marketpulse_part1.py
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QScrollArea
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QCandlestickSeries, QCandlestickSet

# ----------------- Dummy Data -----------------
def get_key_metrics():
    return {
        "Market Cap": "1,23,456 Cr",
        "Current Price": "1,234",
        "P/E": "25.3",
        "ROCE": "18%",
        "ROE": "15%",
        "Dividend Yield": "1.2%",
        "Book Value": "450"
    }

# Additional dummy data for chart
def get_stock_data():
    # returns list of tuples: (open, high, low, close)
    return [
        (100, 110, 95, 105),
        (105, 115, 100, 110),
        (110, 120, 105, 115),
        (115, 125, 110, 120),
        (120, 130, 115, 125),
        (125, 140, 120, 135),
        (135, 150, 130, 145),
        (140, 155, 135, 150)
    ]

def get_line_chart_data():
    return [100, 120, 115, 130, 125, 140, 150, 160]

# ----------------- Main Application -----------------
class MarketPulseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Market Pulse")
        self.setGeometry(100, 100, 1300, 900)
        self.is_dark = False  # Light mode by default
        self.initUI()

    # ----------------- UI Initialization -----------------
    def initUI(self):
        # Scrollable central widget
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        self.main_layout = QVBoxLayout(container)
        self.main_layout.setContentsMargins(15,15,15,15)
        self.main_layout.setSpacing(20)
        scroll_area.setWidget(container)
        self.setCentralWidget(scroll_area)

        # Header
        self.header_widget = self.create_header()
        self.main_layout.addWidget(self.header_widget)

        # Key Metrics
        self.metrics_layout = self.create_key_metrics()
        self.main_layout.addLayout(self.metrics_layout)

        # Stock Chart
        self.chart_view = self.create_stock_chart()
        self.main_layout.addWidget(self.chart_view)

        # Apply initial theme
        self.apply_theme()

    # ----------------- Header -----------------
    def create_header(self):
        header = QFrame()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10,5,10,5)
        header_layout.setSpacing(10)

        self.title_lbl = QLabel("MarketPulse")
        self.title_lbl.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header_layout.addWidget(self.title_lbl)

        header_layout.addStretch()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search Stocks")
        self.search_box.setFixedWidth(250)
        header_layout.addWidget(self.search_box)

        self.follow_btn = QPushButton("Follow")
        self.export_btn = QPushButton("Export")
        self.watchlist_btn = QPushButton("Watchlist")
        self.mode_btn = QPushButton("Dark Mode")
        self.mode_btn.clicked.connect(self.toggle_mode)

        for btn in [self.follow_btn, self.export_btn, self.watchlist_btn, self.mode_btn]:
            header_layout.addWidget(btn)

        header.setLayout(header_layout)
        header.setStyleSheet("border-bottom:1px solid gray; padding:5px;")
        return header

    # ----------------- Key Metrics -----------------
    def create_key_metrics(self):
        layout = QHBoxLayout()
        layout.setSpacing(15)
        data = get_key_metrics()
        self.metric_cards = []
        for key, value in data.items():
            card = QFrame()
            card.setFrameShape(QFrame.Shape.Box)
            card.setStyleSheet(
                "background-color:white; border:1px solid #ccc; border-radius:5px; padding:12px;"
            )
            card_layout = QVBoxLayout()
            lbl_key = QLabel(key)
            lbl_key.setFont(QFont("Arial",10))
            lbl_value = QLabel(value)
            lbl_value.setFont(QFont("Arial",12,QFont.Weight.Bold))
            lbl_value.setStyleSheet("color:#007bff;")
            card_layout.addWidget(lbl_key)
            card_layout.addWidget(lbl_value)
            card.setLayout(card_layout)
            layout.addWidget(card)
            self.metric_cards.append(card)
        return layout

    # ----------------- Stock Chart -----------------
    def create_stock_chart(self):
        # Line series
        line_series = QLineSeries()
        for i, val in enumerate(get_line_chart_data()):
            line_series.append(i, val)

        # Candlestick series
        candle_series = QCandlestickSeries()
        candle_series.setName("Candlestick")
        candle_series.setIncreasingColor(QColor("#007bff"))
        candle_series.setDecreasingColor(QColor("#ff4d4d"))

        for o,h,l,c in get_stock_data():
            candle_series.append(QCandlestickSet(o,c,l,h))

        chart = QChart()
        chart.addSeries(line_series)
        chart.addSeries(candle_series)
        chart.createDefaultAxes()
        chart.setBackgroundBrush(QColor("white") if not self.is_dark else QColor("#2c2c2c"))
        chart.legend().hide()
        chart.setTitle("Stock Price Chart")
        chart_view = QChartView(chart)
        chart_view.setMinimumHeight(320)
        self.chart = chart
        return chart_view

    # ----------------- Theme Switching -----------------
    def toggle_mode(self):
        self.is_dark = not self.is_dark
        self.mode_btn.setText("Light Mode" if self.is_dark else "Dark Mode")
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark:
            self.setStyleSheet("background-color:#2c2c2c; color:white;")
            self.title_lbl.setStyleSheet("color:#00bfff;")
            self.search_box.setStyleSheet("background-color:#444; color:white; border:1px solid #666;")
            for btn in [self.follow_btn,self.export_btn,self.watchlist_btn,self.mode_btn]:
                btn.setStyleSheet("background-color:#444; color:white; border:1px solid #666;")
            for card in self.metric_cards:
                card.setStyleSheet("background-color:#3c3c3c; border:1px solid #666; border-radius:5px; padding:12px;")
            self.chart.setBackgroundBrush(QColor("#2c2c2c"))
        else:
            self.setStyleSheet("background-color:#f8f8f8; color:black;")
            self.title_lbl.setStyleSheet("color:#007bff;")
            self.search_box.setStyleSheet("background-color:white; color:black; border:1px solid #ccc;")
            for btn in [self.follow_btn,self.export_btn,self.watchlist_btn,self.mode_btn]:
                btn.setStyleSheet("background-color:white; color:black; border:1px solid #ccc;")
            for card in self.metric_cards:
                card.setStyleSheet("background-color:white; border:1px solid #ccc; border-radius:5px; padding:12px;")
            self.chart.setBackgroundBrush(QColor("white"))

# ----------------- Run Application -----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarketPulseApp()
    window.show()
    sys.exit(app.exec())

# marketpulse_part2.py
from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtGui import QFont, QColor

# ----------------- Dummy Data -----------------
def get_pros_cons():
    return {
        "Pros": [
            "Strong balance sheet", "High ROE", "Consistent dividend",
            "Good management", "Strong growth in past years",
            "Efficient cost management", "Low debt-to-equity ratio",
            "High operating margin", "Expanding market share", "Stable cash flows"
        ],
        "Cons": [
            "High debt", "Cyclical industry", "Limited growth",
            "Vulnerable to regulation changes", "Low liquidity",
            "Dependence on single product", "Exposure to currency fluctuations",
            "High competition", "Slow innovation", "Geopolitical risks"
        ]
    }

def get_peers():
    return [
        ["Company A", "1200", "24", "17%"], ["Company B", "980", "22", "14%"],
        ["Company C", "1500", "28", "19%"], ["Company D", "1350", "26", "16%"],
        ["Company E", "900", "21", "13%"], ["Company F", "1100", "23", "15%"],
        ["Company G", "1400", "27", "18%"], ["Company H", "1250", "25", "16%"],
        ["Company I", "1450", "29", "20%"], ["Company J", "1300", "24", "17%"],
        ["Company K", "1150", "22", "15%"], ["Company L", "1050", "23", "14%"],
        ["Company M", "950", "21", "13%"], ["Company N", "1250", "25", "16%"],
        ["Company O", "1400", "28", "18%"], ["Company P", "1500", "30", "19%"]
    ]

# ----------------- Pros & Cons Section -----------------
def create_pros_cons_section():
    layout = QHBoxLayout()
    layout.setSpacing(20)
    data = get_pros_cons()
    pros_cons_cards = []

    for section, items in data.items():
        frame = QFrame()
        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(10,10,10,10)
        frame_layout.setSpacing(5)

        lbl_title = QLabel(section)
        lbl_title.setFont(QFont("Arial",12,QFont.Weight.Bold))
        frame_layout.addWidget(lbl_title)

        for item in items:
            lbl_item = QLabel(f"• {item}")
            lbl_item.setFont(QFont("Arial",10))
            frame_layout.addWidget(lbl_item)

        frame.setLayout(frame_layout)
        frame.setStyleSheet(
            "background-color:white; border:1px solid #ccc; border-radius:5px; padding:10px;"
        )
        layout.addWidget(frame)
        pros_cons_cards.append(frame)

    return layout, pros_cons_cards

# ----------------- Peers Table -----------------
def create_peers_table():
    table = QTableWidget()
    peers = get_peers()
    table.setRowCount(len(peers))
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels(["Company", "Price", "P/E", "ROE"])
    table.horizontalHeader().setStretchLastSection(True)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    table.verticalHeader().setVisible(False)
    table.setAlternatingRowColors(True)

    for i, row in enumerate(peers):
        for j, val in enumerate(row):
            table.setItem(i, j, QTableWidgetItem(val))

    table.setMinimumHeight(300)
    table.setStyleSheet(
        "QTableWidget { background-color:white; alternate-background-color:#f8f8f8; color:black; }"
        "QHeaderView::section { background-color:white; font-weight:bold; color:black; }"
    )
    return table

# ----------------- Dark/Light Mode Adjustments -----------------
def apply_theme_pros_peers(pros_cards, peers_table, is_dark):
    if is_dark:
        for card in pros_cards:
            card.setStyleSheet("background-color:#3c3c3c; border:1px solid #666; border-radius:5px; padding:10px; color:white;")
        peers_table.setStyleSheet(
            "QTableWidget { background-color:#3c3c3c; alternate-background-color:#2c2c2c; color:white; }"
            "QHeaderView::section { background-color:#3c3c3c; font-weight:bold; color:white; }"
        )
    else:
        for card in pros_cards:
            card.setStyleSheet("background-color:white; border:1px solid #ccc; border-radius:5px; padding:10px; color:black;")
        peers_table.setStyleSheet(
            "QTableWidget { background-color:white; alternate-background-color:#f8f8f8; color:black; }"
            "QHeaderView::section { background-color:white; font-weight:bold; color:black; }"
        )

# ----------------- Example Usage in Main Window -----------------
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

    app = QApplication(sys.argv)

    main_window = QMainWindow()
    main_window.setWindowTitle("MarketPulse - Chunk2 Test")
    main_window.setGeometry(100,100,1300,900)

    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setSpacing(20)
    layout.setContentsMargins(15,15,15,15)

    # Pros & Cons
    pros_layout, pros_cards = create_pros_cons_section()
    layout.addLayout(pros_layout)

    # Peers Table
    peers_table_widget = create_peers_table()
    layout.addWidget(peers_table_widget)

    # Apply light/dark theme example
    apply_theme_pros_peers(pros_cards, peers_table_widget, is_dark=False)

    main_window.setCentralWidget(container)
    main_window.show()
    sys.exit(app.exec())

# marketpulse_part3.py
from PyQt6.QtWidgets import (
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout, QLabel, QFrame
)
from PyQt6.QtGui import QFont

# ----------------- Dummy Data for Financials -----------------
def get_financials(tab_name):
    if tab_name == "Quarterly":
        return [[f"Q{i} 2025", str(1000+i*50), str(150+i*5), str(120+i*5)] for i in range(12)]
    elif tab_name == "Profit & Loss":
        return [[f"{2025-i}", str(5000-i*100), str(700-i*10), str(600-i*10)] for i in range(12)]
    elif tab_name == "Balance Sheet":
        return [[f"{2025-i}", str(20000-i*500), str(5000-i*50), str(15000-i*450)] for i in range(12)]
    elif tab_name == "Cashflows":
        return [[f"{2025-i}", str(600-i*10), str(400-i*5), str(200-i*5)] for i in range(12)]
    elif tab_name == "Ratios":
        return [[f"{2025-i}", str(25-i), f"{18-i}%", f"{15-i}%"] for i in range(12)]
    elif tab_name == "Shareholding":
        return [
            ["Promoters", "50%"], ["Institutional", "30%"], ["Retail", "20%"]
        ]
    return []

# ----------------- Financial Tabs -----------------
def create_financial_tabs():
    tabs = QTabWidget()
    tabs.setStyleSheet(
        "QTabBar::tab { padding:10px; }"
        "QTabBar::tab:selected { border-bottom:2px solid #007bff; }"
    )
    tab_names = ["Quarterly","Profit & Loss","Balance Sheet","Cashflows","Ratios","Shareholding"]
    financial_tables = {}

    for name in tab_names:
        table = create_financial_table(name)
        tabs.addTab(table,name)
        financial_tables[name] = table

    return tabs, financial_tables

def create_financial_table(tab_name):
    data = get_financials(tab_name)
    if not data:
        return QLabel("No data available")

    cols = len(data[0])
    table = QTableWidget()
    table.setRowCount(len(data))
    table.setColumnCount(cols)
    table.setHorizontalHeaderLabels([f"Col {i+1}" for i in range(cols)])
    table.horizontalHeader().setStretchLastSection(True)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    table.verticalHeader().setVisible(False)
    table.setAlternatingRowColors(True)
    table.setMinimumHeight(250)

    for i,row in enumerate(data):
        for j,val in enumerate(row):
            table.setItem(i,j,QTableWidgetItem(val))
            table.item(i,j).setFont(QFont("Arial",10))

    table.setStyleSheet(
        "QTableWidget { background-color:white; alternate-background-color:#f8f8f8; color:black; }"
        "QHeaderView::section { background-color:white; font-weight:bold; color:black; }"
    )

    return table

# ----------------- Dark/Light Mode for Financials -----------------
def apply_theme_financials(fin_tables, is_dark):
    for table in fin_tables.values():
        if is_dark:
            table.setStyleSheet(
                "QTableWidget { background-color:#3c3c3c; alternate-background-color:#2c2c2c; color:white; }"
                "QHeaderView::section { background-color:#3c3c3c; font-weight:bold; color:white; }"
            )
        else:
            table.setStyleSheet(
                "QTableWidget { background-color:white; alternate-background-color:#f8f8f8; color:black; }"
                "QHeaderView::section { background-color:white; font-weight:bold; color:black; }"
            )

# ----------------- Example Usage in Main Window -----------------
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

    app = QApplication([])

    main_window = QMainWindow()
    main_window.setWindowTitle("MarketPulse - Chunk3 Test")
    main_window.setGeometry(100,100,1300,900)

    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setSpacing(20)
    layout.setContentsMargins(15,15,15,15)

    # Financial Tabs
    fin_tabs, fin_tables = create_financial_tabs()
    layout.addWidget(fin_tabs)

    # Apply light/dark theme example
    apply_theme_financials(fin_tables, is_dark=False)

    main_window.setCentralWidget(container)
    main_window.show()
    app.exec()

# marketpulse_final.py
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QScrollArea, QTabWidget, QTableWidget,
    QTableWidgetItem, QHeaderView
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QCandlestickSeries, QCandlestickSet

# ----------------- DUMMY DATA -----------------
def get_key_metrics():
    return {
        "Market Cap": "1,23,456 Cr",
        "Current Price": "1,234",
        "P/E": "25.3",
        "ROCE": "18%",
        "ROE": "15%",
        "Dividend Yield": "1.2%",
        "Book Value": "450"
    }

def get_stock_data():
    return [
        (100,110,95,105),(105,115,100,110),(110,120,105,115),
        (115,125,110,120),(120,130,115,125),(125,140,120,135),
        (135,150,130,145),(140,155,135,150)
    ]

def get_line_chart_data():
    return [100,120,115,130,125,140,150,160]

def get_pros_cons():
    return {
        "Pros":[
            "Strong balance sheet","High ROE","Consistent dividend",
            "Good management","Strong growth in past years",
            "Efficient cost management","Low debt-to-equity ratio",
            "High operating margin","Expanding market share","Stable cash flows"
        ],
        "Cons":[
            "High debt","Cyclical industry","Limited growth",
            "Vulnerable to regulation changes","Low liquidity",
            "Dependence on single product","Exposure to currency fluctuations",
            "High competition","Slow innovation","Geopolitical risks"
        ]
    }

def get_peers():
    return [
        ["Company A","1200","24","17%"],["Company B","980","22","14%"],
        ["Company C","1500","28","19%"],["Company D","1350","26","16%"],
        ["Company E","900","21","13%"],["Company F","1100","23","15%"],
        ["Company G","1400","27","18%"],["Company H","1250","25","16%"],
        ["Company I","1450","29","20%"],["Company J","1300","24","17%"],
        ["Company K","1150","22","15%"],["Company L","1050","23","14%"],
        ["Company M","950","21","13%"],["Company N","1250","25","16%"],
        ["Company O","1400","28","18%"],["Company P","1500","30","19%"]
    ]

def get_financials(tab_name):
    if tab_name=="Quarterly":
        return [[f"Q{i} 2025", str(1000+i*50), str(150+i*5), str(120+i*5)] for i in range(12)]
    elif tab_name=="Profit & Loss":
        return [[f"{2025-i}", str(5000-i*100), str(700-i*10), str(600-i*10)] for i in range(12)]
    elif tab_name=="Balance Sheet":
        return [[f"{2025-i}", str(20000-i*500), str(5000-i*50), str(15000-i*450)] for i in range(12)]
    elif tab_name=="Cashflows":
        return [[f"{2025-i}", str(600-i*10), str(400-i*5), str(200-i*5)] for i in range(12)]
    elif tab_name=="Ratios":
        return [[f"{2025-i}", str(25-i), f"{18-i}%", f"{15-i}%"] for i in range(12)]
    elif tab_name=="Shareholding":
        return [["Promoters","50%"],["Institutional","30%"],["Retail","20%"]]
    return []

# ----------------- MAIN APP -----------------
class MarketPulseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MarketPulse - Final Clone")
        self.setGeometry(100,100,1300,950)
        self.is_dark=False
        self.initUI()

    def initUI(self):
        # Scrollable central widget
        scroll_area=QScrollArea()
        scroll_area.setWidgetResizable(True)
        container=QWidget()
        self.main_layout=QVBoxLayout(container)
        self.main_layout.setContentsMargins(15,15,15,15)
        self.main_layout.setSpacing(20)
        scroll_area.setWidget(container)
        self.setCentralWidget(scroll_area)

        # Header
        self.header_widget=self.create_header()
        self.main_layout.addWidget(self.header_widget)

        # Key Metrics
        self.metrics_layout=self.create_key_metrics()
        self.main_layout.addLayout(self.metrics_layout)

        # Stock Chart
        self.chart_view=self.create_stock_chart()
        self.main_layout.addWidget(self.chart_view)

        # Pros & Cons
        self.pros_layout,self.pros_cards=self.create_pros_cons()
        self.main_layout.addLayout(self.pros_layout)

        # Peers Table
        self.peers_table=self.create_peers_table()
        self.main_layout.addWidget(self.peers_table)

        # Financial Tabs
        self.financial_tabs,self.fin_tables=self.create_financial_tabs()
        self.main_layout.addWidget(self.financial_tabs)

        # Apply theme
        self.apply_theme()

    # ----------------- Header -----------------
    def create_header(self):
        header=QFrame()
        layout=QHBoxLayout()
        layout.setContentsMargins(10,5,10,5)
        layout.setSpacing(10)
        self.title_lbl=QLabel("MarketPulse")
        self.title_lbl.setFont(QFont("Arial",16,QFont.Weight.Bold))
        layout.addWidget(self.title_lbl)
        layout.addStretch()
        self.search_box=QLineEdit()
        self.search_box.setPlaceholderText("Search Stocks")
        self.search_box.setFixedWidth(250)
        layout.addWidget(self.search_box)
        self.follow_btn=QPushButton("Follow")
        self.export_btn=QPushButton("Export")
        self.watchlist_btn=QPushButton("Watchlist")
        self.mode_btn=QPushButton("Dark Mode")
        self.mode_btn.clicked.connect(self.toggle_mode)
        for btn in [self.follow_btn,self.export_btn,self.watchlist_btn,self.mode_btn]:
            layout.addWidget(btn)
        header.setLayout(layout)
        header.setStyleSheet("border-bottom:1px solid gray; padding:5px;")
        return header

    # ----------------- Key Metrics -----------------
    def create_key_metrics(self):
        layout=QHBoxLayout()
        layout.setSpacing(15)
        data=get_key_metrics()
        self.metric_cards=[]
        for key,value in data.items():
            card=QFrame()
            card.setFrameShape(QFrame.Shape.Box)
            card.setStyleSheet("background-color:white; border:1px solid #ccc; border-radius:5px; padding:12px;")
            card_layout=QVBoxLayout()
            lbl_key=QLabel(key)
            lbl_key.setFont(QFont("Arial",10))
            lbl_value=QLabel(value)
            lbl_value.setFont(QFont("Arial",12,QFont.Weight.Bold))
            lbl_value.setStyleSheet("color:#007bff;")
            card_layout.addWidget(lbl_key)
            card_layout.addWidget(lbl_value)
            card.setLayout(card_layout)
            layout.addWidget(card)
            self.metric_cards.append(card)
        return layout

    # ----------------- Stock Chart -----------------
    def create_stock_chart(self):
        line_series=QLineSeries()
        for i,val in enumerate(get_line_chart_data()):
            line_series.append(i,val)
        candle_series=QCandlestickSeries()
        candle_series.setName("Candlestick")
        candle_series.setIncreasingColor(QColor("#007bff"))
        candle_series.setDecreasingColor(QColor("#ff4d4d"))
        for o,h,l,c in get_stock_data():
            candle_series.append(QCandlestickSet(o,c,l,h))
        chart=QChart()
        chart.addSeries(line_series)
        chart.addSeries(candle_series)
        chart.createDefaultAxes()
        chart.setBackgroundBrush(QColor("white") if not self.is_dark else QColor("#2c2c2c"))
        chart.legend().hide()
        chart.setTitle("Stock Price Chart")
        chart_view=QChartView(chart)
        chart_view.setMinimumHeight(320)
        self.chart=chart
        return chart_view

    # ----------------- Pros & Cons -----------------
    def create_pros_cons(self):
        layout=QHBoxLayout()
        layout.setSpacing(20)
        data=get_pros_cons()
        pros_cards=[]
        for section,items in data.items():
            frame=QFrame()
            frame_layout=QVBoxLayout()
            frame_layout.setContentsMargins(10,10,10,10)
            frame_layout.setSpacing(5)
            lbl_title=QLabel(section)
            lbl_title.setFont(QFont("Arial",12,QFont.Weight.Bold))
            frame_layout.addWidget(lbl_title)
            for item in items:
                lbl_item=QLabel(f"• {item}")
                lbl_item.setFont(QFont("Arial",10))
                frame_layout.addWidget(lbl_item)
            frame.setLayout(frame_layout)
            frame.setStyleSheet("background-color:white; border:1px solid #ccc; border-radius:5px; padding:10px;")
            layout.addWidget(frame)
            pros_cards.append(frame)
        return layout,pros_cards

    # ----------------- Peers Table -----------------
    def create_peers_table(self):
        table=QTableWidget()
        peers=get_peers()
        table.setRowCount(len(peers))
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Company","Price","P/E","ROE"])
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        for i,row in enumerate(peers):
            for j,val in enumerate(row):
                table.setItem(i,j,QTableWidgetItem(val))
        table.setMinimumHeight(300)
        return table

    # ----------------- Financial Tabs -----------------
    def create_financial_tabs(self):
        tabs=QTabWidget()
        tabs.setStyleSheet("QTabBar::tab {padding:10px;} QTabBar::tab:selected {border-bottom:2px solid #007bff;}")
        tab_names=["Quarterly","Profit & Loss","Balance Sheet","Cashflows","Ratios","Shareholding"]
        fin_tables={}
        for name in tab_names:
            table=self.create_financial_table(name)
            tabs.addTab(table,name)
            fin_tables[name]=table
        return tabs,fin_tables

    def create_financial_table(self,tab_name):
        data=get_financials(tab_name)
        if not data:
            return QLabel("No data available")
        cols=len(data[0])
        table=QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(cols)
        table.setHorizontalHeaderLabels([f"Col {i+1}" for i in range(cols)])
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        table.setMinimumHeight(250)
        for i,row in enumerate(data):
            for j,val in enumerate(row):
                table.setItem(i,j,QTableWidgetItem(val))
        return table

    # ----------------- Theme -----------------
    def toggle_mode(self):
        self.is_dark=not self.is_dark
        self.mode_btn.setText("Light Mode" if self.is_dark else "Dark Mode")
        self.apply_theme()

    def apply_theme(self):
        # Header
        self.setStyleSheet("background-color:#2c2c2c; color:white;" if self.is_dark else "background-color:#f8f8f8; color:black;")
        self.title_lbl.setStyleSheet("color:#00bfff;" if self.is_dark else "color:#007bff;")
        self.search_box.setStyleSheet(
            "background-color:#444; color:white; border:1px solid #666;" if self.is_dark else "background-color:white; color:black; border:1px solid #ccc;")
        for btn in [self.follow_btn,self.export_btn,self.watchlist_btn,self.mode_btn]:
            btn.setStyleSheet(
                "background-color:#444; color:white; border:1px solid #666;" if self.is_dark else "background-color:white; color:black; border:1px solid #ccc;")
        # Metrics cards
        for card in self.metric_cards:
            card.setStyleSheet(
                "background-color:#3c3c3c; border:1px solid #666; border-radius:5px; padding:12px;" if self.is_dark else
                "background-color:white; border:1px solid #ccc; border-radius:5px; padding:12px;")
        # Chart
        self.chart.setBackgroundBrush(QColor("#2c2c2c") if self.is_dark else QColor("white"))
        # Pros & Cons
        for card in self.pros_cards:
            card.setStyleSheet(
                "background-color:#3c3c3c; border:1px solid #666; border-radius:5px; padding:10px; color:white;" if self.is_dark else
                "background-color:white; border:1px solid #ccc; border-radius:5px; padding:10px; color:black;")
        # Peers table
        self.peers_table.setStyleSheet(
            "QTableWidget { background-color:#3c3c3c; alternate-background-color:#2c2c2c; color:white; } QHeaderView::section { background-color:#3c3c3c; font-weight:bold; color:white; }"
            if self.is_dark else
            "QTableWidget { background-color:white; alternate-background-color:#f8f8f8; color:black; } QHeaderView::section { background-color:white; font-weight:bold; color:black; }"
        )
        # Financial tables
        for table in self.fin_tables.values():
            table.setStyleSheet(
                "QTableWidget { background-color:#3c3c3c; alternate-background-color:#2c2c2c; color:white; } QHeaderView::section { background-color:#3c3c3c; font-weight:bold; color:white; }"
                if self.is_dark else
                "QTableWidget { background-color:white; alternate-background-color:#f8f8f8; color:black; } QHeaderView::section { background-color:white; font-weight:bold; color:black; }"
            )

# ----------------- RUN -----------------
if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MarketPulseApp()
    window.show()
    sys.exit(app.exec())
