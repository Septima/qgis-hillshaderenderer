# Inspired from http://osdir.com/ml/qgis-user-gis/2013-10/msg00420.html

from qgis.core import *
from qgis.utils import iface
import numpy as np
from PyQt4.QtGui import QImage
    
class HillshadeRenderer ( QgsRasterRenderer ):
    def __init__( self ):
        QgsRasterRenderer.__init__(self)
        self.zfactor = 4           # Vertical exaggeration
        self.azimuth = -45      # in degrees
        self.altitude = 45        # in degrees

    def block ( self, bandNo, extent, width, height ):
        #self._log("block() called")
        
        resolution = extent.width() / float(width)

        #self._log("Resolution: " + str(resolution))
        block = self.input().block ( 1, extent, width, height )
        data = self._block2numpy(block)
        #self._log(data)
        shaded = self._hillshade(data, self.azimuth, self.altitude, resolution, self.zfactor)
        #self._log(shaded)
        output = self._numpy2block(shaded)
        #self._log(output)
        return output
        
    def clone(self):
        return HillshadeRenderer()

    def _block2numpy(self, block):
        shape = (block.height(), block.width())
        nparr = np.zeros(shape, dtype=np.float)
        for r in xrange(shape[0]):
            for c in xrange(shape[1]):
                nparr[r,c] = block.value(r, c)
        return nparr
        
    def _numpy2block(self, nparray):
        height, width = nparray.shape
        bgra = np.empty((height, width, 4) ,np.uint8, 'C')
        bgra[:,:,0] = nparray
        bgra[:,:,1] = nparray
        bgra[:,:,2] = nparray
        bgra[:,:,3] = 255
        img = QImage(bgra.data, width, height, QImage.Format_ARGB32_Premultiplied)
        img.ndarray = bgra # Need to carry reference or python will GC the memory 
        block = QgsRasterBlock ( QGis.ARGB32_Premultiplied, width, height, 0 )
        block.setImage(img)
        return block
        
    # http://geoexamples.blogspot.dk/2014/03/shaded-relief-images-using-gdal-python.html
    def _hillshade(self, array, azimuth, angle_altitude, resolution = 1, zfactor = 1):  
        #self._log( "hillshade called")
        f = float(resolution) / zfactor
        x, y = np.gradient(array, f, f)
        slope = np.pi/2. - np.arctan(np.sqrt(x*x + y*y) )  
        aspect = np.arctan2(-x, y)  

        azimuthrad = azimuth * np.pi / 180.  
        altituderad = angle_altitude * np.pi / 180.  
           
        shaded = np.sin(altituderad) * np.sin(slope)\
               + np.cos(altituderad) * np.cos(slope)\
               * np.cos(azimuthrad - aspect)  
        return (255*(shaded + 1)/2).astype(np.uint8)
        
    def _log(self, message):
        QgsMessageLog.logMessage(str(message), 'HillshadeRenderer', QgsMessageLog.INFO)

renderer = HillshadeRenderer()
layer = iface.activeLayer()
layer.pipe().set( renderer )

if hasattr(layer, "setCacheImage"):
  layer.setCacheImage(None)
layer.triggerRepaint()