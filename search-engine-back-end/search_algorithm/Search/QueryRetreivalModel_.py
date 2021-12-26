# import QUERY as query
# from DOCUMENT import Document
# import Search.DOCUMENT  as Document
from collections import defaultdict
from Search.DOCUMENT import Document 

#import Indexing.MyIndexReader as ixReader
import gc



class QueryRetrievalModel:

    indexReader=[]

    def __init__(self, ixReader):
        self.indexReader = ixReader
        self.num_terms = self.indexReader.total_term()

        return


    # query:  The query to be searched for.
    # topN: The maximum number of returned documents.
    # The returned results (retrieved documents) should be ranked by the score (from the most relevant to the least).
    # You will find our IndexingLucene.Myindexreader provides method: docLength().
    # Returned documents should be a list of Document.
    def retrieveQuery(self, query, topN):
        res = []
        Q = query.getQueryContent()
        mu =2000
        d = defaultdict(lambda: 1)
        for token in Q:
            # Dirichlet = [count(w,D)+ mu*p(w|C)] / [len(D)+mu]
            cf = self.indexReader.CollectionFreq(token)

            if cf>0: # the token exist in the collection.
                posting = self.indexReader.getPostingList1(token)

                for j  in posting:
                    s = (posting[j] + mu * (cf /self.num_terms))/(self.indexReader.doc_len(j)+mu)
                    #print(j,'word count',posting[j],'cf',cf,'doc_len:',self.indexReader.getDocLength(j))
                    d[j] = d[j]*s

        sorted_dict = sorted(d.items(), key = lambda item: item[1], reverse = True)

        for i in range (min(topN,len(sorted_dict))):
            D = Document()
            D.setDocId(sorted_dict[i][0])
            D.setDocNo(self.indexReader.getDocNo(sorted_dict[i][0]))
            D.setScore(sorted_dict[i][1])

            res.append(D)


        return res