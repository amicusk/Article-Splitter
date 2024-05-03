from nltk import word_tokenize, pos_tag, FreqDist
from nltk.corpus import stopwords, wordnet, words
from nltk.stem import WordNetLemmatizer

class Parser:
    isInit : bool = False
    __wordList : list[tuple[str, int]] = []

    def __init__(self, article : str, bookName : str) -> None:
        self.__article : str = article
        self.__bookName : str = bookName
        self.__wnl = WordNetLemmatizer()
        self.isInit = True

    def Parse(self) -> None:
        if not self.isInit:
            return
        
        if not self.__article:
            return
        
        myWords = word_tokenize(self.__article)
        # 去除标点，去除停止词，并小写化
        filteredWords = self.__filterWords(myWords)
        # 还原形变
        originWords = self.__lemmatizeWords(filteredWords)

        # 清除错误单词以及字母
        wordSet = set(words.words())
        newList = [word for word in originWords if word in wordSet and len(word) != 1]

        # 获取词频并排序
        self.__wordList = sorted(FreqDist(newList).items(), key=lambda x: x[1], reverse=True)
        print(f"处理完毕，共{len(self.__wordList)}个单词")

    def PrintWordsAndFreq(self) -> None:
        for i in self.__wordList:
            print(f"{i[0]} {i[1]}")

    def GetOrderedWords(self) -> list[str]:
        return [w[0] for w in self.__wordList]
    
    def Save(self, printFreq : bool = False):
        if not self.isInit:
            return
        
        filename = f"Word List\\word List - {self.__bookName}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            if printFreq:
                for item in self.__wordList:
                    file.write(f"{str(item[0])} {str(item[1])}\n")
            else:
                for item in self.GetOrderedWords():
                    file.write(str(item) + "\n")

            print(f"保存完毕，保存到 {filename}")
    
    def __filterWords(self, words : list[str]) -> list[str]:
        stopWords = set(stopwords.words("english"))
        filteredWords = [w.lower() for w in words if w.lower() not in stopWords and w.isalpha()]
        return filteredWords
    
    def __lemmatizeWords(self, filteredWords : list[str]) -> list[str]:
        wordTags = pos_tag(filteredWords)
        originWords = []

        for tag in wordTags:
            wordnetPos = self.__getWordnetPos(tag[1]) or wordnet.NOUN
            originWords.append(self.__wnl.lemmatize(tag[0], pos=wordnetPos)) # 词形还原
        
        return originWords

    # 获取单词词性
    def __getWordnetPos(self, tag : str):
        if tag.startswith("J"):
            return wordnet.ADJ
        elif tag.startswith("V"):
            return wordnet.VERB
        elif tag.startswith("N"):
            return wordnet.NOUN
        elif tag.startswith("R"):
            return wordnet.ADV
        else:
            return None