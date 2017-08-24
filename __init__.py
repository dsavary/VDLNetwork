# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VDLNetwork
                                 A QGIS plugin
 Plugin pour la gestion des réseaux souterrain
                             -------------------
        begin                : 2017-08-24
        copyright            : (C) 2017 by Savary Daniel / Commune de Lausanne
        email                : daniel.savary@lausanne.ch
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load VDLNetwork class from file VDLNetwork.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .VDLNetwork import VDLNetwork
    return VDLNetwork(iface)
