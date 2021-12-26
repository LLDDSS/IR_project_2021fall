

input = './data/results.trectext'

class PreprocessedCorpusReader:

    def __init__(self):

        self.f = open(input, 'r', encoding='latin-1')
        return

    # Read a line for docNo from the corpus, read another line for the content, and return them in [docNo, content].
    def nextDocument(self):
        className = self.f.readline()
        if  className == '':  # Determine if reach the end of the document
            self.f.close()
            return None
        else:
            className=className.strip('\n')
            class_T = []
            for i in className.split(' '):
                if i.isdigit():
                    continue
                else:
                    class_T.append(i.lower())
            class_T = ' '.join(class_T)

        describe = self.f.readline()
        # except UnicodeDecodeError:
        #     print(className)
        if describe == 'na \n':
            return [className,class_T]

        else :
            describe = describe.strip('\n')
            describe = describe.strip()


        return [className,class_T+' '+describe]



# a = PreprocessedCorpusReader()
#
# print (a.nextDocument())
