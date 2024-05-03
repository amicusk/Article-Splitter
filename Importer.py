import fitz
from os.path import splitext, basename, exists
from abc import ABC, abstractclassmethod

class Importer(ABC):
    def __init__(self, path : str) -> None:
        self._filePath : str = path
        self._text : str = ""

    @abstractclassmethod
    def _parse(self) -> bool:
        pass
        
    def Import(self):
        self._parse()

    def GetTxt(self):
        return self._text
    
class PdfImporter(Importer):
    def _parse(self) -> bool:
        with fitz.open(self._filePath) as doc:
            for page in doc.pages():
                self._text += page.get_text()
            
            return self._text != ""
        
class TxtImporter(Importer):
    def _parse(self) -> bool:
        with open(self._filePath, "r", encoding="utf-8") as f:
            self._text = f.read()
            return self._text != ""


class ImporterFactory:
    def __init__(self, path : str) -> None:
        self.ifSupport = False
        self.__filePath : str = path
        self.__bookName, self.__bookFormat = splitext(basename(self.__filePath))

    def GetBookName(self) -> str:
        return self.__bookName;

    def __checkFileExist(self) -> bool:
        return exists(self.__filePath)

    def CreateImporter(self) -> Importer:
        if not self.__checkFileExist():
            self.ifSupport = False
            print("文件不存在")
            return None
    
        if self.__bookFormat == ".txt":
            print("读取到 txt 文件")
            self.ifSupport = True
            return TxtImporter(self.__filePath)
        elif self.__bookFormat == ".pdf":
            print("读取到 pdf 文件")
            self.ifSupport = True
            return PdfImporter(self.__filePath)
        else:
            print(f"暂不支持 {self.__bookFormat} 文件")
            self.ifSupport = False
            return None