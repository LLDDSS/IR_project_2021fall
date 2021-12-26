#import Class.Path as Path
import gc #（garbage collector）
import json
import collections
import os


index_Result="data/index_result//"
#index_Result = ""

# Efficiency and memory cost should be paid with extra attention.
class MyIndexWriter:

    def __init__(self):
        self.douc_count = 0
        self.indexing = collections.defaultdict(dict)
        self.DocID = {}
        self.block_count = 1
        #self.termID = 1
        self.path =  index_Result

        return

    # This method build index for each document.
 # NT: in your implementation of the index, you should transform your string docno into non-negative integer docids,
    # and in MyIndexReader, you should be able to request the integer docid for each docno.
    def index(self, docNo, content):
        self.douc_count += 1
        self.DocID[docNo]=self.douc_count         # each doc get one integer ID,saving in a dict
        cons = content.split(' ')
        #cons.sort()

        for term in cons:  # construct indexing----{term:{docID:TF}} from one doc
            if not term.isalpha():
                continue
            if self.douc_count not in self.indexing[term]:
                self.indexing[term][self.douc_count] = 1
            else:
                self.indexing[term][self.douc_count] += 1
        #
        # if self.douc_count % 100 == 0:       #save after each 2w docs
        #     self.save_index()
        #     self.block_count += 1

        #self.save_index()
        return




    def save_index(self):          # save index coming from each 2w docs

        with open(self.path + 'index', 'w') as f:
           for term in sorted(self.indexing.keys()):
             tf = [ "{}:{}".format(key, value) for key, value in self.indexing[term].items()]
             f.write("{},{}\n".format(term, " ".join(tf)))
        self.indexing.clear()

        return



    def merge(self):       # merge block for final index
        for i in range(2, self.block_count + 1):    # for_loop, merge all of block
            if i == 2:
                merge_c = open(self.path + "index_block_{}".format(i - 1), 'r')
            else:
                merge_c = open(self.path + "posting_merge_{}".format(i - 1), 'r')

            cur_block = open(self.path + "index_block_{}".format(i), 'r')
            if i== self.block_count:
                write_merge = open(self.path + 'posting_merge', 'w')
            else:
                write_merge = open(self.path + "posting_merge_{}".format(i), 'w')

            mc = merge_c.readline().strip().split(',')
            cb = cur_block.readline().strip().split(',')

            ## 2 by 2 sorted-merge
            try:
                while mc != [''] and cb != ['']:
                    if mc[0] < cb[0]:
                        write_merge.write("{},{}\n".format(mc[0], mc[1]))
                        tem = mc
                        mc = merge_c.readline().strip().split(',')
                    elif mc[0] > cb[0]:
                        write_merge.write("{},{}\n".format(cb[0], cb[1]))
                        tem = cb
                        cb = cur_block.readline().strip().split(',')
                    else:
                        write_merge.write("{},{}\n".format(mc[0], mc[1] + ' ' + cb[1]))
                        mc = merge_c.readline().strip().split(',')
                        cb = cur_block.readline().strip().split(',')
                while mc != ['']:
                    write_merge.write("{},{}\n".format(mc[0], mc[1]))
                    mc = merge_c.readline().strip().split(',')

                while cb != ['']:
                    write_merge.write("{},{}\n".format(cb[0], cb[1]))
                    cb = cur_block.readline().strip().split(',')
            except IndexError:
                print('mc\n', mc)
                print(merge_c.name + '\n')
                print('cb\n', cb)
                print(tem)
                print(cur_block.name + '\n')

            merge_c.close()
            cur_block.close()
            write_merge.close()


            if i == 2:
                os.remove(self.path + "index_block_{}".format(i - 1))
                os.remove(self.path + "index_block_{}".format(i))
            else:
                os.remove(self.path + "posting_merge_{}".format(i - 1))
                os.remove(self.path + "index_block_{}".format(i))

        return




    # Close the index writer, and you should output all the buffered content (if any).
    def close(self):
        self.save_index()  # save final block

        with open(self.path + 'DocID', 'w') as f:  # save DocNo2DocID
            jsObj = json.dumps(self.DocID)
            f.write(jsObj)
        gc.collect()

        # self.merge()  # merge all of block--be a final posting

        # construct term_dict     {term, CF}
        with open(self.path+'Term_dict','w') as f:
            with open(self.path+'index') as merge_index:
                ele = merge_index.readline()
                while ele !='':
                    term = ele.split(',')[0]
                    cf = sum([int(i.split(':')[1]) for i in ele.split(',')[1].split(' ')])
                    f.write("{},{}\n".format(term, cf))
                    ele = merge_index.readline()
        gc.collect()

        return