from demo_ims_channelname import ImarisFile
from pathlib import Path

imarisfile = ImarisFile(Path(Path.cwd(), "demofile.ims"))
imarisfile.setchannels(["DAPI", "CD3e", "CD20"])
imarisfile.write()
