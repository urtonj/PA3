import nltk
from nltk.corpus import treebank

class parser():
    
    tree = None; node_list = []; sequences = []; matches = []; position = 0
    
    def parse(self, tree, grammar):
        parser.tree = tree; parser.sequences = []
        parser.node_list = []
        print "\n\nInput tree: " 
        print tree
        for rule in grammar:
            parser.test_all_sequences(rule)   
    
    def test_all_sequences(self, rule):
        parser.node_list = []; updated_sequence_list = False; parser.position = 0
        parser.generate_subsequences(parser.tagged_list_from_tree(parser.tree, rule))
        for sequence in parser.sequences:
            if updated_sequence_list == True: continue
            parser.matches = []
            parser.test_sequence(sequence, rule)
            if parser.matches != []:
                updated_sequence_list = True
                parser.tree = parser.update_tree(parser.tree, parser.matches, rule[0], parser.position)
                parser.sequences = []; parser.node_list = []
                parser.generate_subsequences(parser.tagged_list_from_tree(parser.tree, rule))
                parser.test_all_sequences(rule)                
                #parser.position += len(parser.matches)
            else: parser.position += 1
                
    def test_sequence(self, sequence, rule):
        index = 0; sequence_rejected = False; index_array = []
        #print "\n\nTesting sequence: " + parser.print_sequence(sequence) + " with rule: " + str(rule[1]) + "\n\n"
        for entity in rule[1]:
            if sequence_rejected: continue
            entity_rejected = False; tag = entity[0]; type = entity[1]
            while not entity_rejected:
                if index >= len(sequence):
                    continue 
                elif index > 0 and (sequence[index].tag == ","):
                    index_array.append(index); index += 1
                elif type == "+":
                    if sequence[index].tag == tag:
                        index_array.append(index); index += 1
                        type = "*"    
                    else:
                        sequence_rejected = True
                        entity_rejected = True
                elif isinstance(type, int):
                    if sequence[index].tag == tag:
                        index_array.append(index); index += 1
                        entity_rejected = True
                    else:
                        sequence_rejected = True
                        entity_rejected = True
                elif type == "?":
                    if sequence[index].tag == tag:
                        index_array.append(index); index += 1
                    entity_rejected = True
                elif type == "*":
                    if sequence[index].tag == tag:
                        index_array.append(index); index += 1
                    else: 
                        entity_rejected = True
                else:
                    print "Unsupported operator found!"
        if index_array != []: parser.matches = index_array
    
    def update_tree(self, original_tree, nodes_to_chunk, chunk_name, offset):
        array = []; 
        updated_tree = original_tree.copy()
        nodes_to_chunk.reverse()
        for n in range(len(nodes_to_chunk)): 
            nodes_to_chunk[n] = nodes_to_chunk[n] + offset
        for index in nodes_to_chunk:
            array.insert(0, original_tree[index])
            updated_tree.pop(index)
        updated_tree.insert(offset, nltk.tree.Tree(chunk_name, array))
        print "Updated tree: \n" + str(updated_tree); return updated_tree
        
    def tagged_list_from_tree(self, tree, rule):
        for n in range(len(tree)):
            if isinstance(tree[n], tuple):
                parser.node_list.append(node(tree[n][1], tree[n], n))
            else:
                if tree[n].node == "CHUNK":
                    parser.node_list.append(node('CHUNK', tree[n], n))
                else:
                    parser.node_list.append(node(rule[0], tree[n], n))
                #elif tree[n].node == 'SUPERCHUNK':
                #    parser.node_list.append(node('SUPERCHUNK', tree[n], n))
                #else: 
                #    print tree[n]
                #    print "Unrecognized tree character..."


    def generate_subsequences(self, list):
        for index in range(len(parser.node_list)):
            parser.sequences = parser.sequences + [parser.node_list[index:]]
    
    def print_sequence(self, sequence):
        str = ""
        for item in sequence: str = str + " " + item.tag
        return str
    
class node():
    def __init__(self, tag, word, index): 
        self.tag = tag; self.word = word; self.index = index  
    def print_node(self):
        print "TAG: %s || Body: %s || Index: %s" % (self.tag, self.word, self.index) 
                         
def chunker(files):
    parser = nltk.RegexpParser(original_grammar)
    test_tree = treebank.tagged_sents(files)
    return parser.parse(test_tree)

def get_chunked_trees(trees = []):
    original_parser = nltk.RegexpParser(original_grammar) 
    corpus = treebank.tagged_sents(test_set)
    for tree in corpus: trees += [original_parser.parse(tree)]
    return trees
     
def start(parser):
    trees = get_chunked_trees()
    for tree in trees:
        parser.parse(tree, grammar)
      
original_grammar = r"""
CHUNK: {<DT>?<NN.*>+<VBG><NN.*>+}
       {<DT><CD>?<VBN><NN.*>*}
       {<DT><CD><VBG>?<NN.*>+}
       {<PDT>?<DT|WDT|PR.*>?<\$>?<CD>*<JJ.*>*<NN.*>*<POS>?<NN.*>*<\$>?<CD>*}
       {<WP.*>}
       {<EX>}  
"""

grammar = [ 
           
( "SUPERCHUNK", [[("CHUNK"), ("+")], [("IN"), ("?")], [("MD"), ("?")]] ),
( "SUPERCHUNK-VB", [[("VB"), (1)]] )

]

test_set = ['wsj_0001.mrg']

parser = parser()
start(parser)

#result = chunker(test_set)
#parser = parser()
#for sentence in test_set:
#    print sentence
#parser.parse(result, grammar)
