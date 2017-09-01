# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VDLNetwork
                                 A QGIS plugin for the Ville de Lausanne
                              -------------------
        begin                : 2016-06-20
        git sha              : $Format:%H$
        copyright            : (C) 2016 Ville de Lausanne
        author               : Christophe Gusthiot
        email                : christophe.gusthiot@lausanne.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from future.builtins import range
from future.builtins import object

from ..ui.show_settings_dialog import ShowSettingsDialog
from PyQt4.QtCore import (QCoreApplication,
                          QVariant)
from qgis.core import (QgsProject,
                       QgsMapLayerRegistry,
                       edit,
                       QgsField,
                       QGis,
                       QgsMapLayer)
from ..core.db_connector import DBConnector


class ShowSettings(object):
    """
    Class to manage plugin settings
    """

    def __init__(self, iface):
        """
        Constructor
        :param iface: interface
        """
        self.__iface = iface
        self.icon_path = ':/plugins/VDLNetwork/icons/settings_icon.png'
        self.text = QCoreApplication.translate("VDLNetwork", "Settings")
        self.__showDlg = None
        self.__configTable = None
        self.__uriDb = None
        self.__schemaDb = None
        self.__project_loaded()
        QgsProject.instance().readProject.connect(self.__project_loaded)

    def __project_loaded(self):
        """
        Get saved settings on load
        """

        """ Config table in Database for importing new Lausanne data """
        self.__configTable = QgsProject.instance().readEntry("VDLNetwork", "config_table", None)[0]

        """ Database used for importing new Lausanne data """
        dbName = QgsProject.instance().readEntry("VDLNetwork", "db_name", None)[0]

        """ Schema of the Database used for importing new Lausanne data """
        self.__schemaDb = QgsProject.instance().readEntry("VDLNetwork", "schema_db", None)[0]

        if dbName != "":
            usedDbs = DBConnector.getUsedDatabases()
            if dbName in list(usedDbs.keys()):
                self.__uriDb = usedDbs[dbName]

    def start(self):
        """
        To start the show settings, meaning display a Show Settings Dialog
        """
        self.__showDlg = ShowSettingsDialog(self.__iface, self.__configTable, self.__uriDb, self.__schemaDb)
        self.__showDlg.okButton().clicked.connect(self.__onOk)
        self.__showDlg.cancelButton().clicked.connect(self.__onCancel)
        self.__showDlg.show()

    def __onOk(self):
        """
        When the Ok button in Show Settings Dialog is pushed
        """
        self.__showDlg.accept()
        #self.linesLayer = self.__showDlg.linesLayer()
        #self.pointsLayer = self.__showDlg.pointsLayer()
        self.configTable = self.__showDlg.configTable()
        self.uriDb = self.__showDlg.uriDb()
        #self.ctlDb = self.__showDlg.ctlDb()
        self.schemaDb = self.__showDlg.schemaDb()
        #self.mntUrl = self.__showDlg.mntUrl()

    def __onCancel(self):
        """
        When the Cancel button in Show Settings Dialog is pushed
        """
        self.__showDlg.reject()

    @property
    def configTable(self):
        """
        To get the saved config table (for import tool)
        :return: saved config table
        """
        return self.__configTable

    @property
    def uriDb(self):
        """
        To get the saved uri import database
        :return: saved uri import database
        """
        return self.__uriDb

    @property
    def schemaDb(self):
        """
        To get the saved schema import database
        :return: saved schema import database
        """
        return self.__schemaDb

    @configTable.setter
    def configTable(self, configTable):
        """
        To set the saved config table
        :param configTable: config table to save
        """
        self.__configTable = configTable
        if configTable is not None:
            QgsProject.instance().writeEntry("VDLNetwork", "config_table", configTable)

    @uriDb.setter
    def uriDb(self, uriDb):
        """
        To set the saved uri import database
        :param uriDb: saved uri import database
        """
        self.__uriDb = uriDb
        if uriDb is not None:
            QgsProject.instance().writeEntry("VDLNetwork", "db_name", uriDb.database())

    @schemaDb.setter
    def schemaDb(self, schemaDb):
        """
        To set the saved schema import database
        :param schemaDb: saved schema import database
        """
        self.__schemaDb = schemaDb
        if schemaDb is not None:
            QgsProject.instance().writeEntry("VDLNetwork", "schema_db", schemaDb)
