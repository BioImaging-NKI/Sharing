from PyImarisWriter import PyImarisWriter as PW
from datetime import datetime
from pathlib import Path
import numpy as np


class ImarisFile:
    def __init__(self, path):
        self.path = Path(path)
        self.imsz = [64, 64]
        self.pixelsize = 1.0
        self.channels = ["DAPI", "CD3e"]

    def setchannels(self, channels):
        self.channels = channels

    def write(self):
        image_size = PW.ImageSize(
            x=self.imsz[1], y=self.imsz[0], z=1, c=len(self.channels), t=1
        )
        dimension_sequence = PW.DimensionSequence("x", "y", "z", "c", "t")
        block_size = PW.ImageSize(x=self.imsz[1], y=self.imsz[0], z=1, c=1, t=1)
        sample_size = PW.ImageSize(x=1, y=1, z=1, c=1, t=1)
        res = self.pixelsize
        output_filename = str(self.path)
        options = PW.Options()
        options.mNumberOfThreads = 12
        options.mCompressionAlgorithmType = PW.eCompressionAlgorithmShuffleGzipLevel2
        options.mEnableLogProgress = True
        application_name = "PyImarisWriter"
        application_version = "1.0.0"
        converter = PW.ImageConverter(
            "uint16",
            image_size,
            sample_size,
            dimension_sequence,
            block_size,
            output_filename,
            options,
            application_name,
            application_version,
            MyCallbackClass(),
        )
        num_blocks = image_size / block_size
        block_index = PW.ImageSize()
        for c in range(num_blocks.c):
            block_index.c = c
            dset = np.random.randint(low=0, high=6000, size=self.imsz, dtype=np.uint16)
            for t in range(num_blocks.t):
                block_index.t = t
                for z in range(num_blocks.z):
                    block_index.z = z
                    for y in range(num_blocks.y):
                        block_index.y = y
                        for x in range(num_blocks.x):
                            block_index.x = x
                            if converter.NeedCopyBlock(block_index):
                                converter.CopyBlock(dset, block_index)

        adjust_color_range = False
        minX = 0
        minY = 0
        minZ = 0
        maxX = res * self.imsz[0]
        maxY = res * self.imsz[1]
        maxZ = 1
        image_extents = PW.ImageExtents(minX, minY, minZ, maxX, maxY, maxZ)
        time_infos = [datetime.today()]
        color_infos = [PW.ColorInfo() for _ in range(image_size.c)]
        parameters = PW.Parameters()
        for i in range(image_size.c):
            parameters.set_channel_name(i, self.channels[i])
            r, g, b = (0.0, 1.0, 0.0)
            color_infos[i].set_base_color(PW.Color(r, g, b, 1.0))
        converter.Finish(
            image_extents, parameters, time_infos, color_infos, adjust_color_range
        )
        converter.Destroy()


class MyCallbackClass(PW.CallbackClass):
    def __init__(self):
        self.mUserDataProgress = 0

    def RecordProgress(self, progress, total_bytes_written):
        progress100 = int(progress * 100)
        if progress100 - self.mUserDataProgress >= 5:
            self.mUserDataProgress = progress100
            print(
                f"User Progress {self.mUserDataProgress}, GBytes written: {total_bytes_written / 2 ** 30 :.2f}"
            )
