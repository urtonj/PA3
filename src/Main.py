import nltk
from nltk.corpus import treebank

class parser():
    
    rule_index = 0; list_index = 0
    entity_tag = ""; entity_type = ""; entity_rejected = False
    list_tag = ""; rule_rejected = False
    output = ""
    tree = None; node_list = []; sequences = []
    
    def parse(self, tree, grammar):
        parser.tree = tree
        parser.generate_subsequences(parser.tagged_list_from_tree(parser.tree))
        for rule in grammar:
            for sequence in parser.sequences:
                parser.test_sequence(sequence, rule)
    
    def test_sequence(self, sequence, rule):
        print "\n\nTesting sequence: " + parser.print_sequence(sequence) + " with rule: " + str(rule[1])
        index = 0; sequence_rejected = False; result = ""
        for entity in rule[1]:
            print "Testing rule entity: " + str(entity)
            if sequence_rejected:
                print "Sequence rejected..."
                continue
            entity_rejected = False; tag = entity[0]; type = entity[1]
            while not entity_rejected:
                if index >= len(sequence):
                    print "Successful match!"; entity_rejected = True
                    continue 
                elif sequence[index].tag == "," or sequence[index].tag == ".":
                    result = result + " " + sequence[index].tag
                    print "Match: " + result
                    index += 1
                elif type == "+":
                    if sequence[index].tag == tag:
                        result = result + " " + sequence[index].tag
                        print "Match: " + result
                        index += 1
                        type = "*"    
                    else:
                        sequence_rejected = True
                        entity_rejected = True
                elif isinstance(type, int):
                    if sequence[index].tag == tag:
                        result = result + " " + sequence[index].tag
                        print "Match: " + result
                        index += 1
                        entity_rejected = True
                    else:
                        sequence_rejected = True
                        entity_rejected = True
                elif type == "?":
                    if sequence[index].tag == tag:
                        result = result + " " + sequence[index].tag
                        print "Match: " + result
                        index += 1
                    entity_rejected = True
                elif type == "*":
                    if sequence[index].tag == tag:
                        result = result + " " + sequence[index].tag
                        print "Match: " + result
                        index += 1
                    else: 
                        entity_rejected = True
                else:
                    print "Unsupported operator found!"
        
    def tagged_list_from_tree(self, tree): 
        for index, child in enumerate(tree):
            if isinstance(child, nltk.tree.Tree):
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
           
( "SUPERCHUNK1", [[("CHUNK"), ("+")], [("IN"), ("*")]] ),
           
]

result = chunker()    
parser = parser()
parser.parse(result, grammar)
