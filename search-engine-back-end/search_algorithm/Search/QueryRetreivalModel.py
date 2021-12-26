import collections
from Search.DOCUMENT import Document 


class QueryRetrievalModel:

    indexReader=[]

    def __init__(self, ixReader):
        self.indexReader = ixReader
        return


    # query:  The query to be searched for.
    # topN: The maximum number of returned documents.
    # The returned results (retrieved documents) should be ranked by the score (from the most relevant to the least).
    # You will find our IndexingLucene.Myindexreader provides method: docLength().
    # Returned documents should be a list of Document.
    def retrieveQuery(self, query, topN):
        doc_freq = collections.defaultdict(list)
        query = query.getQueryContent()
        total_words = self.indexReader.total_term()

        for i in range(len(query)):
            cur_q = query[i]
            docs = self.indexReader.getPostingList1(cur_q)
            if not docs:
                continue
            
            if docs == -1:
                return None

            for docId, fre in docs.items():
                if docId not in doc_freq:
                    doc_freq[docId] = [0] * len(query)

                doc_freq[docId][i] = fre


        for i in range(len(query)):
            cur_q = query[i]
            docs = self.indexReader.getPostingList(cur_q)

            if not docs:
                continue
            
            collection_freq = self.indexReader.CollectionFreq(cur_q)
            for key in doc_freq.keys():
                doc_freq[key][i] += 2000 * collection_freq / total_words
                doc_freq[key][i] /= (self.indexReader.doc_len(key) + 2000)

    
        
        ranked_doc = collections.defaultdict(float)
        for docId, q_list in doc_freq.items():
            prob = 1.0
            for q in q_list:
                if q != 0:
                    prob *= q

            ranked_doc[docId] = prob
        
        
        Top_ranked = sorted(ranked_doc.items(), key = lambda a: a[1], reverse=True)
        documents = []
        for item in Top_ranked[:topN]:
            result_doc = Document()
            result_doc.setDocNo(self.indexReader.getDocNo(int(item[0])))
            result_doc.setScore(item[1])
            documents.append(result_doc)
                  
        return documents
