from qtpy.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QCheckBox, 
    QLabel, QProgressBar, QFileDialog, QGroupBox, QListWidgetItem
)
from qtpy.QtCore import Qt, Signal, QThread
import os
import os.path as osp

class BatchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Batch Processing")
        self.resize(600, 500)
        self.setModal(True)
        self.files = []
        
        layout = QVBoxLayout(self)

        # File List Section
        file_group = QGroupBox("Files to Process")
        file_layout = QVBoxLayout()
        
        btn_layout = QHBoxLayout()
        self.btn_add_files = QPushButton("Add Files")
        self.btn_add_folder = QPushButton("Add Folder")
        self.btn_clear = QPushButton("Clear List")
        btn_layout.addWidget(self.btn_add_files)
        btn_layout.addWidget(self.btn_add_folder)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addStretch()

        self.file_list_widget = QListWidget()
        
        file_layout.addLayout(btn_layout)
        file_layout.addWidget(self.file_list_widget)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)

        # Options Section
        options_group = QGroupBox("Processing Options")
        options_layout = QVBoxLayout()
        
        self.check_detect = QCheckBox("Auto-Detect Text (Use Detection Model)")
        self.check_ocr = QCheckBox("Run OCR (Read Text)")
        self.check_translate = QCheckBox("Translate Text (Use current Translator)")
        self.check_inpaint = QCheckBox("Inpaint (Remove Original Text)")
        self.check_export = QCheckBox("Export Result Images")

        self.check_detect.setChecked(True)
        self.check_ocr.setChecked(True)
        self.check_translate.setChecked(True)
        self.check_inpaint.setChecked(True)
        self.check_export.setChecked(True)

        options_layout.addWidget(self.check_detect)
        options_layout.addWidget(self.check_ocr)
        options_layout.addWidget(self.check_translate)
        options_layout.addWidget(self.check_inpaint)
        options_layout.addWidget(self.check_export)
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)

        # Action Buttons
        action_layout = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.btn_start = QPushButton("Start Batch Process")
        self.btn_cancel = QPushButton("Cancel / Close")

        action_layout.addWidget(self.progress_bar)
        action_layout.addStretch() 
        action_layout.addWidget(self.btn_start)
        action_layout.addWidget(self.btn_cancel)
        layout.addLayout(action_layout)

        # Connections
        self.btn_add_files.clicked.connect(self.add_files)
        self.btn_add_folder.clicked.connect(self.add_folder)
        self.btn_clear.clicked.connect(self.clear_list)
        self.btn_cancel.clicked.connect(self.close)
        # Start logic to be implemented later via signal or simple loop
        self.btn_start.clicked.connect(self.start_processing)
    
    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Images (*.png *.jpg *.jpeg *.bmp *.webp)")
        if files:
            self.files.extend(files)
            self.update_list()

    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp')):
                        self.files.append(osp.join(root, file))
            self.update_list()

    def clear_list(self):
        self.files = []
        self.update_list()

    def update_list(self):
        self.file_list_widget.clear()
        for f in self.files:
            self.file_list_widget.addItem(QListWidgetItem(f))

    def start_processing(self):
        # Placeholder for actual logic
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, len(self.files))
        self.btn_start.setEnabled(False)
        # In real implementation, emit signal to main window to start threaded processing
        # checking options
        options = {
            'detect': self.check_detect.isChecked(),
            'ocr': self.check_ocr.isChecked(),
            'translate': self.check_translate.isChecked(),
            'inpaint': self.check_inpaint.isChecked(),
            'export': self.check_export.isChecked()
        }
        # Signal emission or direct logic can be placed here
        # self.start_batch_signal.emit(self.files, options)
        pass

