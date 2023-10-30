from pathlib import Path
import h5py

imarisfile = Path(Path.cwd(), "demofile.ims")
hdffile = h5py.File(str(imarisfile))
channels = [x for x in hdffile['DataSetInfo'].keys() if x.startswith("Channel ")]
for channel in channels:
    channel_name = hdffile['DataSetInfo'][channel].attrs['Name'].tobytes().decode('UTF-8')
    print(f"{channel} is {channel_name}")
