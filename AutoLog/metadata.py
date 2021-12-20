#--cofing:utf-8--
import exiftool

class Metadata:
    def __init__(self):
        pass

    def extract(self,filePath):
        with exiftool.ExifTool() as et:
            return et.get_metadata_batch(filePath)
