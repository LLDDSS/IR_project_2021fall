import Indexing.PreProcessedCorpusReader as PreprocessedCorpusReader
import Indexing.MyIndexWriter as MyIndexWriter
import Indexing.MyIndexReader as MyIndexReader
import datetime



def WriteIndex():
    count = 0
    # Initiate pre-processed collection file reader.
    corpus =PreprocessedCorpusReader.PreprocessedCorpusReader()
    # Initiate the index writer.
    indexWriter = MyIndexWriter.MyIndexWriter()
    # Build index of corpus document by document.
    while True:
        doc = corpus.nextDocument()
        if doc == None:
            break
        indexWriter.index(doc[0], doc[1])
        count+=1
        if count%1000==0:
            print("finish ", count," docs")
    print("totally finish ", count, " docs")
    indexWriter.close()
    return

def ReadIndex( token):
    # Initiate the index file reader.
    index =MyIndexReader.MyIndexReader()
    # retrieve the token.
    df = index.DocFreq(token)
    ctf = index.CollectionFreq(token)
    print(" >> the token \""+token+"\" appeared in "+ str(df) +" documents and "+ str(ctf) +" times in total")
    if df>0:
        posting = index.getPostingList(token)
        for docId in posting:
            docNo = index.getDocNo(docId)
            print(docNo+"\t"+str(docId)+"\t"+str(posting[docId]))

startTime = datetime.datetime.now()
WriteIndex()
endTime = datetime.datetime.now()
print ("index web corpus running time: ", endTime - startTime)
startTime = datetime.datetime.now()
ReadIndex("data")
endTime = datetime.datetime.now()
print ("load index & retrieve the token running time: ", endTime - startTime)


