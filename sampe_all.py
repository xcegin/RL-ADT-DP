import pickle

from Environment.enviroment import Enviroment
from Environment.enviromentWalkerRedLabel import enviromentWalkerContext
from Vectorizer.Sample import SampleVisitor
from Vectorizer.train import learn_vectors

# Creates the embeddings for the given dataset we specified in the Enviroment class

env = Enviroment()
m = 0
Samples = []
while m < len(env.listOfFiles):
    env.prepareNextFile()
    for table in env.listOfTables:
        tableRows = []
        # Extract values for each column according to one row
        for row in table:
            dictForRow = env.mergeDictsInRow(row)
            sampleVisitor = SampleVisitor(enviromentWalkerContext(), dictForRow, env.expressions, env.rootTreeAdtNode.name)
            lists = sampleVisitor.traverse_tree(env.rootTreeAdtNode)
            lists = [x for x in lists if x != []]
            Samples += lists
    m += 1
embed_file = open('vectors_nextDate.pkl', 'wb')
lists = learn_vectors(Samples, 'Vectorizer/logs')
pickle.dump(lists, embed_file)
embed_file.close()