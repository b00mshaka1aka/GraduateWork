# Copyright (C) 2023 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

"""PySide6 port of the Qt DataVisualization graphgallery example from Qt v6.x"""

import os
import sys

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow

from scattergraph import ScatterGraph

if __name__ == "__main__":
    os.environ["QSG_RHI_BACKEND"] = "opengl"

    app = QApplication(sys.argv)

    # Create a tab widget for creating own tabs for Q3DBars, Q3DScatter, and Q3DSurface
    main_window = QMainWindow()
    main_window.setWindowTitle("CloudView")

    screen_size = main_window.screen().size()
    minimum_graph_size = QSize(screen_size.width() / 2, screen_size.height() / 1.75)

    scatter = ScatterGraph()

    if not scatter.initialize(minimum_graph_size, screen_size):
        QMessageBox.warning(None, "Graph Gallery", "Couldn't initialize the OpenGL context.")
        sys.exit(-1)

    # Add scatter widget
    main_window.setCentralWidget(scatter.scatterWidget())

    main_window.show()
    sys.exit(app.exec())
