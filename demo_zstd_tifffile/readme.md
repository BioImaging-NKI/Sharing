# Channelnames and ranges disappear
This happens when writing images with [tifffile](https://pypi.org/project/tifffile/) and reading with [FIJI](https://fiji.sc/).

When enabeling zstd the file is opened with bioformats, but the channelnames are suddenly ignored.

Two small tifffiles in this repository are generated with [demo_zstd.py](demo_zstd.py).
