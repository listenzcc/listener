def encode_treeofwords(mytree, mystr):
    mystep = mytree
    b=False
    for c in mystr:
        mystep_old=mystep
        b=False
        bb=False
        if c in mystep:
            if mystep.index(c)==mystep.__len__()-1:
                mystep.append([])
            else:
                if list!=type(mystep[mystep.index(c)+1]):
                    mystep.insert(mystep.index(c)+1,[])
        else:
            mystep.append(c)
            mystep.append([])
        mystep=mystep[mystep.index(c)+1]
    mystep.append(0)

def decode_treeofwords(mytree,pre,words_list):
    for c in mytree:
        if str==type(c):
            decode_treeofwords(mytree[mytree.index(c)+1],pre+c,words_list)
        if list==type(c):
            None
        if int==type(c):
            #print(pre)
            words_list.append(pre)
"""
def return_subtree(mytree,mytrace):
    mytrace.reverse()
    while []!=mytrace:
        c=mytrace.pop()
        if c in mytree:
            mytree=mytree[mytree.index(c)+1]
        else:
            return -1
    return mytree
"""
def return_subtree(mytree,mytrace):
    for c in mytrace:
        if c in mytree:
            mytree=mytree[mytree.index(c)+1]
        else:
            return -1
    return mytree

