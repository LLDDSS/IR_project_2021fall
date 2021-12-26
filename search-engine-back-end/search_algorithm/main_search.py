# import IndexingWithWhoosh.MyIndexReader as MyIndexReader
import Search.QueryRetreivalModel as QueryRetreivalModel
import Search.ExtractQuery as ExtractQuery
import datetime
import Indexing.MyIndexReader as MyIndexReader
import collections
import sys
import json

# startTime = datetime.datetime.now()


categories = ['CMPINF', 'CS', 'INFSCI', 'ISSP', 'LIS', 'TELCOM']
course_list = collections.defaultdict(str)

for c in categories:
    file = open('./search_algorithm/' + c, 'r')
    for line in file.readlines():
        l = line.strip().split(':')
        if l[2]:
            course_list[l[0]] = l[2]
        else:
            course_list[l[0]] = 'NA'

    file.close()

index = MyIndexReader.MyIndexReader()
search = QueryRetreivalModel.QueryRetrievalModel(index)


def main(argv):
    s = argv[1].strip().lower()
    extractor = ExtractQuery.ExtractQuery(s)
    queries = extractor.getQuries()

    try:
        for query in queries:
            results = search.retrieveQuery(query, 10)
            if not results:
                print("error No available infomation related to the query!")
            else:
                for r in results:
                    info = r.getDocNo().split(' ')
                    reformed_info = {"department": info[0], "courseNumber": info[1], \
                        "courseTitle": " ".join(info[2:]), "courseDescription": course_list["".join(info[:2])]}
                    app_json = json.dumps(reformed_info)
                    print(app_json)
    except:
        print("error Incorrect information!")
            
    

    

if __name__ == "__main__":
   main(sys.argv)

# print("--------- Welcome to Our Course Search System ----------- \n")
# s = input("Please type in any keywords you want to search or quit() to quit: ").strip().lower()
# while s != "quit()":
#     print("The query you just type in: {}".format(s))
#     extractor = ExtractQuery.ExtractQuery(s)

#     queries= extractor.getQuries()
#     for query in queries:
#         ##print(query.topicId,"\t",query.queryContent)
#         results = search.retrieveQuery(query, 10)
#         rank = 1
#         for result in results:
#             docNo = result.getDocNo()
#             print('Rank {}: '.format(rank), docNo)
#             print('Description: ', course_list["".join(docNo.split(' ')[:2])], '\n')
#             rank = rank +1
    
#     s = input("Type a new query for another search or quit() to quit: ").lower()

# print("Goodbye!")

# endTime = datetime.datetime.now()
# print ("load index & retrieve the token running time: ", endTime - startTime)
