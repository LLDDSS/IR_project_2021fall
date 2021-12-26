import json
import ast
import gc


index_Result="search_algorithm/data/index_result/"
#index_Result = ""
# Efficiency and memory cost should be paid with extra attention.
class MyIndexReader:

    def __init__(self):
        self.path = index_Result
        #print("finish reading the index")
        self.post= -1

    # Return the integer DocumentID of input string DocumentNo.
    def getDocId(self, docNo):
        with open(self.path+'DocID') as f:
            dict = f.read()

        dict_id = json.loads(dict)
        ID = dict_id.get(docNo,-1)
        return ID

    # Return the string DocumentNo of the input integer DocumentID.
    def getDocNo(self, docId):
        with open(self.path+'DocID') as f:
            dict = f.read()

        dict_no = json.loads(dict)
        dict_no = list(dict_no.keys())
        try:
            No  = dict_no[docId-1]
        except IndexError:
            No = -1

        return No

    # Return DF.
    def DocFreq(self, token):
        post = self.getPostingList1(token)
        #print(post)
        return len(post)

    # Return the frequency of the token in whole collection/corpus.
    def CollectionFreq(self, token):
        with open(self.path+'Term_dict','r') as f:
            ele = f.readline()
            while ele != '':
                if ele.split(',')[0] == token:
                    return int(ele.split(',')[1])
                if ele.split(',')[0]> token:
                    break
                ele = f.readline()
        return 0

    # Return posting list in form of {documentID:frequency}.
    def getPostingList1(self, token):
        with open(self.path+'index') as f:
            ele = f.readline()
            while ele != '':
                if ele.split(',')[0] < token:
                    ele = f.readline()
                    continue

                elif ele.split(',')[0]==token:
                    self.post = ele.split(',')[1]
                    break
                else:
                    break

        if self.post != -1:
            self.post = self.post.strip('\n')
            self.post = ast.literal_eval('{'+self.post.replace(' ',',')+"}")
        return self.post

    def getPostingList(self, token):
        post = self.post
        return post



    def doc_len(self,doc_id):
        file_path = 'search_algorithm/data/results.trectext'
        with open(file_path,'r',encoding='latin-1') as f:
            line = f.readline()
            counts = 1
            while line:
                if counts == 2*doc_id-1:
                    className = line
                    describe = f.readline()
                    break
                line = f.readline()
                counts += 1
        class_T = []
        for i in className.split(' '):
            if i.isdigit():
                continue
            else:
                class_T.append(i)


        if describe == 'na \n':
            return len(class_T)

        else :
            describe = describe.strip('\n')
            describe = describe.strip().split(' ')
            tot_len = len(class_T)+len(describe)


        return tot_len


        return

    def total_term(self):
        count = len(open(index_Result+'index', 'r').readlines())
        gc.collect()
        return count
