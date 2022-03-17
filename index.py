import pandas as pd
import numpy as np
from typing import List
from jpype import JClass, JString, getDefaultJVMPath, shutdownJVM, startJVM, java

data = pd.read_csv("test.csv",sep=",")
# zemberek-full jar dosyasını C:/Users/kullanici-adi dosya yoluna koyun
ZEMBEREK_PATH = r'C:\Users\Kivanc\zemberek-full.jar' # alttakina göre uyarla
#ZEMBEREK_PATH = r'C:\Users\<your-user-name>\zemberek-full.jar'
startJVM(getDefaultJVMPath(), '-ea', '-Djava.class.path=%s' % (ZEMBEREK_PATH))

TurkishMorphology = JClass('zemberek.morphology.TurkishMorphology')
morphology = TurkishMorphology.createWithDefaults()

# rastgele yazılan kelimeler
kelimeler = 'kalem ilişkilendiremediklerimiz gözlük gözlem'

analysis: java.util.ArrayList = (
    morphology.analyzeAndDisambiguate(kelimeler).bestAnalysis()
    )
    
pos: List[str] = []
for i, analysis in enumerate(analysis, start=1):
    f'\nAnalysis {i}: {analysis}',
    f'\nPrimary POS {i}: {analysis.getPos()}'
    f'\nPrimary POS (Short Form) {i}: {analysis.getPos().shortForm}'
       
    pos.append(
        f'{str(analysis.getLemmas()[0])}'
        )
print(f'\n Kelime Kökleri: {" ".join(pos)}')

print("\n çekilen veriii -------------------")
# boş olan(nan) yerlere "bilinmiyor" yazdırlıyor
for col in data.columns:
    if data[col].isnull().any():
        data[col] = data[col].fillna("Bilinmiyor")

def findElements(data):
    result = dict()
    for col in data.columns:
        temp = []
        if col != "Id":
            for i in data[col]:
                #print(i)
                if i != "Bilinmiyor":
                    temp.append(i)
            result[col] = temp
    return result


myDic = findElements(data)

#print(myDic["Key"])

allWords = " ".join(myDic["Key"])

#print(allWords)

print("\n çekilen verilerin zemberekten geçmiş hali -------------- \n")

analysis: java.util.ArrayList = (
    morphology.analyzeAndDisambiguate(allWords).bestAnalysis()
    )
    
pos: List[str] = []
for i, analysis in enumerate(analysis, start=1):
    f'\nAnalysis {i}: {analysis}',
    f'\nPrimary POS {i}: {analysis.getPos()}'
    f'\nPrimary POS (Short Form) {i}: {analysis.getPos().shortForm}'
       
    pos.append(
        f'{str(analysis.getLemmas()[0])}'
        )
print(f'\n Kelime Kökleri: {" ".join(pos)}')