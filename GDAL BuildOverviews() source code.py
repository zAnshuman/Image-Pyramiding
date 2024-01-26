# -*- coding: utf-8 -*-
"""The Answer

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1A2liLZc4z7UUq3ek7a78foPmlu2ee1KG
"""

from osgeo import gdal, gdalconst

def create_overviews(input_raster, output_raster, overview_levels):
    # Open the input raster dataset
    ds = gdal.Open(input_raster, gdalconst.GA_ReadOnly)
    if ds is None:
        print(f"Failed to open {input_raster}")
        return

    # Get the original raster's geotransform and projection
    geotransform = ds.GetGeoTransform()
    projection = ds.GetProjection()

    # Create a new raster dataset for the overviews
    driver = gdal.GetDriverByName('GTiff')
    overview_ds = driver.Create(output_raster, ds.RasterXSize, ds.RasterYSize, ds.RasterCount, ds.GetRasterBand(1).DataType)
    overview_ds.SetGeoTransform(geotransform)
    overview_ds.SetProjection(projection)

    # Generate overviews at specified levels
    for level in overview_levels:
        # Calculate the size of the overview
        overview_width = ds.RasterXSize // level
        overview_height = ds.RasterYSize // level

        # Create a buffer to read data from the original raster
        buffer = ds.ReadRaster(0, 0, ds.RasterXSize, ds.RasterYSize, buf_xsize=overview_width, buf_ysize=overview_height)

        # Write the buffer to the overview dataset
        overview_ds.WriteRaster(0, 0, overview_width, overview_height, buffer)

    # Close datasets
    ds = None
    overview_ds = None

# Input and output raster filenames
input_raster = 'input_image.tif'
output_raster = 'output_image_with_overviews.tif'

# Specify overview levels
overview_levels = [2, 4, 8]

# Create overviews manually using GDAL
create_overviews(input_raster, output_raster, overview_levels)