# qgis-hillshaderenderer
QGIS plugin offering on the fly hillshading of DEM data

*Note: This is by no means a functional plugin yet!*

The code is more like a proof of concept. It works on my data. Most of the time.

To run the proof of concept code:

1. Open QGIS and load DEM raster data
2. Make the DEM layer active (click it in the legend). Apply any styling options you want to work for the hillshade (like transparency and resampling options)
3. Run the [python code](hillshaderenderer.py) either by copy/pasting into the python console or using the built in editor.

## Limitations

There is nu GUI for setting options. They must be set in the code.

The hillshading algorithm uses the relationship between z units and xy units. At the moment it is assumed they are 1:1. This could probably be calculated. 

The shading does not look good when QGIS is resampling the DEM data. This is very pronounced when qgis is upsampling, where the hillshade will then look jagged or terraced. This can be solved by forcing QGIS to not use nearest neighbor. I havn't figured a way to get the Renderer to do this..

Nodata is not handled. At all.

Changing the layer style (like transparency, blending mode etc) using the layer styling dialog doesnt work. But it seems that reattaching the renderer after the change may lead to the desired result.

## Improvements

My conversion between QgsRasterBlock and numpy array is outright dumb and extremely slow. I loop over all the pixels and copy them one by one... I think it could be done a lot faster using [QgsRasterBlock::bits	(		)](https://qgis.org/api/classQgsRasterBlock.html#a8b1799304477d0f01643891f5ee6395e), but unfortunately according to the docs it is not available from Python.
