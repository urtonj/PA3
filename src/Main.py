import nltk; from nltk.corpus import treebank

class parser():
    
    node_list = []; sequences = []; matches = []; 
    position = 0; output_tree = None; tree = None;         
        
    def parse(self, tree, grammar):
        parser.tree = tree; parser.output_tree = tree 
        parser.sequences = []
        for rule in grammar: parser.test_all_sequences(rule) 
        return parser.output_tree 
    
    def test_all_sequences(self, rule):
        parser.node_list = []; parser.position = 0; new_sequence = False
        parser.generate_subsequences(parser.list_from_tree(parser.tree, rule))
        for sequence in parser.sequences:
            if new_sequence == True: continue
            parser.matches = []
            parser.test_sequence(sequence, rule)
            if parser.matches != []:
                new_sequence = True
                parser.tree = parser.update_tree(parser.tree, parser.matches, 
                                                 rule[0], parser.position)
                parser.sequences = []; parser.node_list = []
                parser.generate_subsequences(parser.list_from_tree(parser.tree, 
                                                                   rule))
                parser.test_all_sequences(rule)                
            else: parser.position += 1
                
    def test_sequence(self, sequence, rule):
        index = 0; sequence_rejected = False; index_array = []
        for entity in rule[1]:
            entity_rejected = False; tag = entity[0]; type = entity[1]
            while not entity_rejected and not sequence_rejected:
                if index >= len(sequence): continue 
                elif index > 0 and (sequence[index].tag == ","):
                    index_array.append(index); index += 1
                elif type == "+":
                    if sequence[index].tag == tag:
                        index_array.append(index); index += 1
                        type = "*"    
                    else:
                        sequence_rejected = True; entity_rejected = True
                        index_array = []
                elif isinstance(type, int):
                    if sequence[index].tag == tag:
                        index_array.append(index); index += 1
                        entity_rejected = True
                    else:
                        sequence_rejected = True; entity_rejected = True
                        index_array = []
                elif type == "?":
                    if sequence[index].tag == tag:
                        index_array.append(index); index += 1
                    entity_rejected = True
                elif type == "*":
                    if sequence[index].tag == tag:
                        index_array.append(index); index += 1
                    else: entity_rejected = True
                else: print "Unsupported operator found!"
        if index_array != []: parser.matches = index_array
    
    def update_tree(self, original_tree, nodes_to_chunk, chunk_name, offset):
        array = []; updated_tree = original_tree
        nodes_to_chunk.reverse()
        for n in range(len(nodes_to_chunk)): 
            nodes_to_chunk[n] = nodes_to_chunk[n] + offset
        for index in nodes_to_chunk:
            array.insert(0, original_tree[index])
            updated_tree.pop(index)
        updated_tree.insert(offset, nltk.tree.Tree(chunk_name, array))
        parser.output_tree = updated_tree; return updated_tree
        
    def list_from_tree(self, tree, rule):
        for n in range(len(tree)):
            if isinstance(tree[n], tuple):
                parser.node_list.append(node(tree[n][1], tree[n], n))
            else:
                if tree[n].node == "CHUNK":
                    parser.node_list.append(node('CHUNK', tree[n], n))
                else: parser.node_list.append(node(rule[0], tree[n], n))

    def generate_subsequences(self, list):
        for index in range(len(parser.node_list)):
            parser.sequences = parser.sequences + [parser.node_list[index:]]
    
class node():
    def __init__(self, tag, word, index): 
        self.tag = tag; self.word = word; self.index = index  

def get_chunked_trees(files, trees = []):
    original_parser = nltk.RegexpParser(original_grammar) 
    corpus = treebank.tagged_sents(files)
    for tree in corpus: trees += [original_parser.parse(tree)]
    return trees

def output_results(results):
    file = open('/Users/jasonurton/Desktop/results.txt', 'w')
    for result in results: file.write("%s\n\n" % str(result))
    file.close()
         
def start(parser):
    results = []
    trees = get_chunked_trees(eval_set)
    for tree in trees: results += [parser.parse(tree, grammar)]
    output_results(results)
      
original_grammar = r"""
CHUNK: {<DT>?<NN.*>+<VBG><NN.*>+}
       {<DT><CD>?<VBN><NN.*>*}
       {<DT><CD><VBG>?<NN.*>+}
       {<PDT>?<DT|WDT|PR.*>?<\$>?<CD>*<JJ.*>*<NN.*>*<POS>?<NN.*>*<\$>?<CD>*}
       {<WP.*>}
       {<EX>}  
"""

grammar = [    
( "SC|CHARACTERISTIC", [[("CHUNK"), ("+")], [("VBZ"), (1)], [("CHUNK"), ("+")], 
               [("IN"), ("*")], [("CC"), ("?")], [("RB"), ("?")], 
               [("CHUNK"), ("*")], [("VBG"), ("?")], [("CHUNK"), ("*")]] ),
( "SC|PASTACTION", [[("CHUNK"), (1)], [("CC"), ("?")], [("CHUNK"), ("*")], 
                    [("VBD"), (1)], [("VBN"), ("?")]]), 
( "SC|PRESENTACTION", [[("CHUNK"), (1)], [("CC"), ("?")], [("CHUNK"), ("*")], 
                    [("VBP"), (1)]] ), 
( "SC|ENTITY", [[("CHUNK"), ("+")], [("CC"), (1)], [("CHUNK"), ("+")], 
                [("IN"), ("?")], [("CHUNK"), ("?")]] ),
( "SC|ENTITY", [[("CHUNK"), ("+")], [("IN"), (1)], [("CHUNK"), ("+")]] ),
( "SC|ENTITY", [[("CHUNK"), (1)], [("CHUNK"), (1)], [("CHUNK"), ("+")]] )
]

test_set = ['wsj_0001.mrg', 'wsj_0002.mrg', 'wsj_0006.mrg', 'wsj_0007.mrg', 
            'wsj_0009.mrg', 'wsj_0013.mrg', 'wsj_0014.mrg', 'wsj_0027.mrg', 
            'wsj_0055.mrg', 'wsj_0067.mrg', 'wsj_0070.mrg', 'wsj_0074.mrg', 
            'wsj_0076.mrg', 'wsj_0080.mrg', 'wsj_0081.mrg', 'wsj_0084.mrg', 
            'wsj_0096.mrg', 'wsj_0115.mrg', 'wsj_0131.mrg', 'wsj_0147.mrg', 
            'wsj_0153.mrg', 'wsj_0154.mrg']

eval_set = ['wsj_0023.mrg', 'wsj_0054.mrg', 'wsj_0057.mrg', 'wsj_0063.mrg',
            'wsj_0066.mrg', 'wsj_0068.mrg', 'wsj_0069.mrg', 'wsj_0084.mrg', 
            'wsj_0124.mrg', 'wsj_0197.mrg']

parser = parser()
start(parser)