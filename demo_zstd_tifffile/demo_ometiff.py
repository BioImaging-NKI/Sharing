from pathlib import Path
import numpy as np
from tifffile import imwrite, COMPRESSION, TiffWriter

withzstd = False
img = np.random.rand(5, 128, 128).astype(dtype=np.float32)
pixelsize = 1.24
channelnames = ["aaa", "bbb", "dapi", "fourth channel", "eee"]
outpath = Path(Path.cwd(), "newfile.ome.tif")
ranges = []
factors = [1.0, 2.5, 8.0, 1.0, 7.6]
for ch in range(img.shape[0]):
    img[ch, :, :] *= factors[ch]
    ranges.append(0.0)
    ranges.append(factors[ch]/2)

with TiffWriter(outpath, bigtiff=True) as tif:
    metadata = {
        "PhysicalSizeX": pixelsize,
        "PhysicalSizeXUnit": "µm",
        "PhysicalSizeY": pixelsize,
        "PhysicalSizeYUnit": "µm",
        "axes": "CYX",
        "Channel": {"Name": channelnames},
        "Ranges": [ranges],
    }
    options = dict(
        compression=COMPRESSION.ZSTD,
    )
    tif.write(img, metadata=metadata, **options)
