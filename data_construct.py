import numpy as np
import pandas as pd
import os
from os import listdir

book_dir = "Books"

booknames = [b for b in listdir(bookdir) if b != '.DS_Store']
booknames
r = np.random.RandomState(1234)

def data_construct(booknames):
    df = pd.DataFrame(columns=["BookName", "TextVector", "CharVec", "Response"])
    for bn in booknames:
        book = Book(bn)
        title = book.bookname
        charVec = book.getCharactersMatrix
        bookVec = book.getMainTextVector()
        temp = pd.DataFrame({"BookName": title, "TextVector": bookVec, "CharVec": charVec, "Response": 1})
        df = df.append(temp)

    return df


###################
# Fake Book class #
###################

class Book():
    def __init__(self, bookname):
        self.bookdir = "Books/" + bookname + "/"
        self.meta_data = pd.read_csv(self.bookdir + "meta_data.csv")
        self.bookname = bookname.replace('_', ' ')


    def getTitle(self):
        return self.bookname

    def getMainTextVector(self):
        textvector = r.uniform(0,10,100)
        return textvector

    def getCharactersMatrix(self):
        charMat = {charName:r.uniform(10,20,50) for charName in self.meta_data.characterName}
        return charMat


a = Book('The_Color_of_Water')
a.bookdir
a.getTitle()
a.getMainTextVector()
a.getCharactersMatrix()
