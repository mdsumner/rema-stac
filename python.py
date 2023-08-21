## working through this: https://stacspec.org/en/tutorials/2-create-stac-catalog-python/
## in R.R we look at the actual REMA json for clues

# I'm using python3.8 because 3.11 is not enable-shared, and I force-installed
##  rasterio==1.3.8 because the old one didn't handle vsicurl/tif 

#reticulate::use_python("/usr/bin/python3.8")

import os
import json
import rasterio
import urllib.request
import pystac

from datetime import datetime, timezone
from shapely.geometry import Polygon, mapping
from tempfile import TemporaryDirectory

catalog = pystac.Catalog(id='rema-test', description='REMA v2 2m DEM')
print(list(catalog.get_children()))
print(list(catalog.get_items()))

print(json.dumps(catalog.to_dict(), indent=4))


datetime_utc = datetime.now(tz=timezone.utc)
def get_bbox_and_footprint(raster):
    with rasterio.open(raster) as r:
        bounds = r.bounds
        bbox = [bounds.left, bounds.bottom, bounds.right, bounds.top]
        footprint = Polygon([
            [bounds.left, bounds.bottom],
            [bounds.left, bounds.top],
            [bounds.right, bounds.top],
            [bounds.right, bounds.bottom]
        ])
        
        return (bbox, mapping(footprint))


vsi = '/vsicurl/https://pgc-opendata-dems.s3.us-west-2.amazonaws.com/rema/mosaics/v2.0/2m/41_40/41_40_2_2_2m_v2.0_dem.tif'

## these have to be in longlat (bare reprojection is fine apparently)
bbox, footprint = get_bbox_and_footprint(vsi)

item = pystac.Item(id='viscurl-tile-41_40_2_2_2m_v2.0',
                 geometry=footprint,
                 bbox=bbox,
                 datetime=datetime_utc,
                 properties={})
catalog.add_item(item)


# Add Asset and all its information to Item 
item.add_asset(
    key='image',
    asset=pystac.Asset(
        href=vsi,
        media_type=pystac.MediaType.COG
    )
)


                 
