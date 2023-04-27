# Copyright (C) 2023 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

from PySide6.QtCore import QObject, QSize, Qt
from PySide6.QtWidgets import (QCheckBox, QComboBox, QCommandLinkButton,
                               QLabel, QHBoxLayout, QSizePolicy,
                               QVBoxLayout, QWidget, QMessageBox)
from PySide6.QtDataVisualization import (QAbstract3DSeries, Q3DScatter)

from scatterdatamodifier import ScatterDataModifier


class ScatterGraph(QObject):

    def __init__(self):
        super().__init__()
        self._scatterGraph = Q3DScatter()
        self._container = None
        self._scatterWidget = None

    def initialize(self, minimum_graph_size, maximum_graph_size):
        if not self._scatterGraph.hasContext():
            return -1

        self._scatterWidget = QWidget()
        hLayout = QHBoxLayout(self._scatterWidget)
        self._container = QWidget.createWindowContainer(self._scatterGraph, self._scatterWidget)
        self._container.setMinimumSize(minimum_graph_size)
        self._container.setMaximumSize(maximum_graph_size)
        self._container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._container.setFocusPolicy(Qt.StrongFocus)
        hLayout.addWidget(self._container, 1)

        vLayout = QVBoxLayout()
        hLayout.addLayout(vLayout)

        backgroundCheckBox = QCheckBox(self._scatterWidget)
        backgroundCheckBox.setText("Задний фон")
        backgroundCheckBox.setChecked(True)

        gridCheckBox = QCheckBox(self._scatterWidget)
        gridCheckBox.setText("Сетка")
        gridCheckBox.setChecked(True)

        smoothCheckBox = QCheckBox(self._scatterWidget)
        smoothCheckBox.setText("Качественные текстуры")
        smoothCheckBox.setChecked(True)

        itemStyleList = QComboBox(self._scatterWidget)
        itemStyleList.addItem("Сфера", QAbstract3DSeries.MeshSphere)
        itemStyleList.addItem("Куб", QAbstract3DSeries.MeshCube)
        itemStyleList.addItem("Минимал", QAbstract3DSeries.MeshMinimal)
        itemStyleList.addItem("Точка", QAbstract3DSeries.MeshPoint)
        itemStyleList.setCurrentIndex(0)

        d_list = QComboBox(self._scatterWidget)
        d_list.addItem("0.125", 0.125)
        d_list.addItem("0.25", 0.25)
        d_list.addItem("0.5", 0.5)
        d_list.addItem("1", 1.)
        d_list.setCurrentIndex(1)

        themeList = QComboBox(self._scatterWidget)
        themeList.addItem("Qt")
        themeList.addItem("Primary Colors")
        themeList.addItem("Digia")
        themeList.addItem("Stone Moss")
        themeList.addItem("Army Blue")
        themeList.addItem("Retro")
        themeList.addItem("Ebony")
        themeList.addItem("Isabelle")
        themeList.setCurrentIndex(3)

        shadowQuality = QComboBox(self._scatterWidget)
        shadowQuality.addItem("Отсутствует")
        shadowQuality.addItem("Низкое")
        shadowQuality.addItem("Среднее")
        shadowQuality.addItem("Высокое")
        shadowQuality.addItem("Низкое с сглаживанием")
        shadowQuality.addItem("Среднее с сглаживанием")
        shadowQuality.addItem("Высокое с сглаживанием")
        shadowQuality.setCurrentIndex(6)

        vLayout.addWidget(backgroundCheckBox)
        vLayout.addWidget(gridCheckBox)
        vLayout.addWidget(smoothCheckBox)
        vLayout.addWidget(QLabel("Коэффициент разбиения"))
        vLayout.addWidget(d_list)
        vLayout.addWidget(QLabel("Стиль вектора"))
        vLayout.addWidget(itemStyleList)
        vLayout.addWidget(QLabel("Тема"))
        vLayout.addWidget(themeList)
        vLayout.addWidget(QLabel("Качество тени"))
        vLayout.addWidget(shadowQuality, 1, Qt.AlignTop)

        self._modifier = ScatterDataModifier(self._scatterGraph, self)

        backgroundCheckBox.stateChanged.connect(self._modifier.setBackgroundEnabled)
        gridCheckBox.stateChanged.connect(self._modifier.setGridEnabled)
        smoothCheckBox.stateChanged.connect(self._modifier.setSmoothDots)

        d_list.currentIndexChanged.connect(self._modifier.change_d)

        self._modifier.backgroundEnabledChanged.connect(backgroundCheckBox.setChecked)
        self._modifier.gridEnabledChanged.connect(gridCheckBox.setChecked)
        itemStyleList.currentIndexChanged.connect(self._modifier.changeStyle)

        themeList.currentIndexChanged.connect(self._modifier.changeTheme)

        shadowQuality.currentIndexChanged.connect(self._modifier.changeShadowQuality)

        self._modifier.shadowQualityChanged.connect(shadowQuality.setCurrentIndex)
        self._scatterGraph.shadowQualityChanged.connect(self._modifier.shadowQualityUpdatedByVisual)
        return True

    def scatterWidget(self):
        return self._scatterWidget
