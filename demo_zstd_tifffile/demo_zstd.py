from pathlib import Path
import numpy as np
from tifffile import imwrite, COMPRESSION

withzstd = False
img = np.random.rand(5, 128, 128).astype(dtype=np.float32)
pixelsize = 1.24
channelnames = ["aaa", "bbb", "dapi", "fourth channel", "eee"]
if withzstd:
    outpath = Path(Path.cwd(), "withzstd.tiff")
    compression = COMPRESSION.ZSTD
else:
    outpath = Path(Path.cwd(), "withoutzstd.tiff")
    compression = COMPRESSION.NONE
ranges = []
factors = [1.0, 2.5, 8.0, 1.0, 7.6]
for ch in range(img.shape[0]):
    img[ch, :, :] *= factors[ch]
    ranges.append(img[ch, :, :].min())
    ranges.append(img[ch, :, :].max())

imwrite(
    outpath,
    img,
    imagej=True,
    bigtiff=False,
    resolution=(1 / pixelsize, 1 / pixelsize),
    photometric="minisblack",
    compression=compression,
    metadata={
        "spacing": pixelsize,
        "unit": "um",
        "axes": "CYX",
        "Labels": channelnames,
        "Ranges": [ranges],
    },
)
