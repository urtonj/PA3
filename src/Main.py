import nltk
from nltk.corpus import treebank

## Possible problem in traversal function with tree type?
## Algo should parse and output a new tree if found, call parse
## on the output tree. Otherwise continue.

class parser():
    
    tree = None; node_list = []; sequences = []; matches = []
    
    def parse(self, tree, grammar):
        parser.tree = tree; parser.sequences = []
        parser.matches = []; parser.node_list = []
        print "Input tree: " 
        print tree
        parser.generate_subsequences(parser.tagged_list_from_tree(parser.tree))
        print parser.sequences
        for rule in grammar:
            for sequence in parser.sequences:
                if parser.matches != []:
                    continue
                parser.test_sequence(sequence, rule)
                
            print 'New tree: '
            parser.parse(parser.update_tree(parser.tree, parser.matches[0], rule[0]), grammar)
            
    
    def test_sequence(self, sequence, rule):
        index = 0; sequence_rejected = False; index_array = []
        print "\n\nTesting sequence: " + parser.print_sequence(sequence) + " with rule: " + str(rule[1])
        for entity in rule[1]:
            if sequence_rejected:
                continue
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
        if index_array != []: parser.matches = parser.matches + [index_array]
    
    def update_tree(self, original_tree, nodes_to_chunk, chunk_name, array = []):
        updated_tree = original_tree.copy()
        nodes_to_chunk.reverse()
        for index in nodes_to_chunk:
            array.insert(0, original_tree[index])
            updated_tree.pop(index)
        updated_tree.insert(nodes_to_chunk.pop(), nltk.tree.Tree(chunk_name, array))
        print updated_tree; return updated_tree
        
    def tagged_list_from_tree(self, tree):
        #Can some of this complexity be removed using tree.treepositions(order='inorder') 
        for index, child in enumerate(tree):
            if isinstance(child, nltk.tree.Tree):
                #print "Child: " + str(child[0])
                parser.node_list.append(node("CHUNK", child, index))    
            elif not isinstance(child, str):
                parser.node_list.append(node(child[1], child[1], index)) 
            else:
                parser.tagged_list_from_tree(child)

    def generate_subsequences(self, list):
        for index in range(len(parser.node_list)):
            parser.sequences = parser.sequences + [parser.node_list[index:len(parser.node_list)]]
    
    def print_sequence(self, sequence):
        str = ""
        for item in sequence:
            str = str + " " + item.tag
        return str
    
class node():
    def __init__(self, tag, word, index): 
        self.tag = tag; self.word = word; self.index = index
        
    def print_node(self):
        print "TAG: %s || Body: %s || Index: %s" % (self.tag, self.word, self.index) 
                         
def chunker():
    parser = nltk.RegexpParser(original_grammar)
    test_tree = treebank.tagged_sents()[0]
    return parser.parse(test_tree)
    
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
           
]

result = chunker()
parser = parser()
parser.parse(result, grammar)
