# import QUERY as Query
from Search.QUERY import Query
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import string

class ExtractQuery:

    def __init__(self,input):
        # get self.Q containing tokenized query

        self.Q = []
        stop = stopwords.words('english')

        stemmer = SnowballStemmer('english', ignore_stopwords=False)

        if input:
            input = input.translate(str.maketrans("","", string.punctuation))
            input = input.strip('\n')
            l = input.split(' ')

            l = [x.lower() for x in l]
            ll = []
            for i in l:
                if i not in stop:
                    ll.append(stemmer.stem(i))

            self.Q.append(ll)


        return

    # Return extracted queries with class Query in a list.
    def getQuries(self):
        res = []

        for i, j in enumerate(self.Q):
            query = Query()
            query.setTopicId(i+1)
            query.setQueryContent(j)
            res.append(query)


        return res



# test = ExtractQuery()
# test = test.getQuries()
# for i in test:
#     print(i.getTopicId())