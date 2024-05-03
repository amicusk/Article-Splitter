from Importer import ImporterFactory
from Parser import Parser

bookPath : str = "Books\\Nuclear Weapons.pdf"

class Application:
    def __init__(self) -> None:
        factory = ImporterFactory(bookPath)
        self.__importer = factory.CreateImporter()
        if factory.ifSupport:
            self.__importer.Import()

        txt = self.__importer.GetTxt() if self.__importer else ""
        self.__parser = Parser(txt, factory.GetBookName()) if txt else None

    def Run(self):
        if self.__parser is not None:
            self.__parser.Parse()
            self.__parser.Save()

def Main():
    Application().Run()

if __name__ == "__main__": 
    Main()
    