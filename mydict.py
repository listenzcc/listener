#! /usr/bin/python3
# Filename:mydict.py
print('hello world')

import io, os, re, sys, time
from myimport_getch import *
from myimport_treeofwords import *
from myimport_str_list import *

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

## def field
def encode_seek_dict(seek_,dict_):
    return seek_*100+dict_
def decode_seek_dict(myseek_):
    return [myseek_//100,myseek_%100]

def update_hash_word_myseek(str_,seek_,dict_,hash_word_myseek,list_allword,hash_of_firstchar,mywordtree):
    tmp0=str.split(str_, '\t')
    tmp1=str.split(tmp0[0], ', ')
    for mykey_ in tmp1:
        tmp=str.split(mykey_,' (')
        mykey=tmp[0]
        while hash_word_myseek.__contains__(mykey):
        	mykey += '_'
        hash_word_myseek[mykey]=encode_seek_dict(seek_,dict_)
        if not(mykey[0] in hash_of_firstchar.keys()):
            hash_of_firstchar[mykey[0]]=list_allword.__len__()
        list_allword.append(mykey)
        encode_treeofwords(mywordtree,str2list(mykey))

def input_refresh(mystr,stat,hash_word_myseek,dict_list,divider_reg,message,myhistlist):
    if 1==stat:
        myseek=hash_word_myseek.get(list2str(mystr))
        if None != myseek:
            [seek_,dict_]=decode_seek_dict(myseek)
            fid=open(dict_list[dict_], 'r', encoding='utf8')
            fid.seek(seek_)
            str_=fid.readline()
            #print('\033[92m')
            i=0
            i_lim=15
            while None==divider_reg.match(str_):
                if i<i_lim:
                    print(str_,end='',flush=True)
                    #print('\033[0m',end='')
                    i+=1
                else:
                    i=0
                    c=getch()
                    if '\x1b'==c: #ESC
                        mystr.clear()
                        print('>>',end='',flush=True)
                        return 0
                    if '\r'==c: # ENTER
                        i_lim=15
                    else:
                        i_lim=1

                str_=fid.readline()
                if ''==str_:
                    fid.close()
                    dict_+=1
                    try:
                        fid=open(dict_list[dict_],'r', encoding='utf8')
                    except IndexError as e:
                        break
            fid.close()
            # record in hist_
            myhistlist.append(list2str(mystr))
            fname='F:/TDDOWNLOAD/mydict_py/'
            #fname=os.getcwd();
            fname+='/hist_'
            fname+=time.strftime('%b-%d-%Y',time.localtime())
            with open(fname,'a', encoding='utf8') as f:
                print(list2str(mystr), file=f)
            mystr.clear()
            print('>>',end='',flush=True)
        else:
            print('\n\033[91mError 2: cannot find '+list2str(mystr)+'\033[0m')
            print(('>>'+list2str(mystr)),end='',flush=True)
    if 2==stat:
        if []==message:
            print(' ')
        else:
            print(message.pop().replace('\n','\n\033[91mwarning: ')+'\033[0m')
        print('>>'+list2str(mystr),end='',flush=True)
    if 3==stat:
        try:
            message_=message.pop()
        except IndexError as e:
            return 0
        if str!=type(message_):
            return 0
        while 0<mystr.__len__():
            mystr.pop()
            print('\b \b',end='',flush=True)
        for c in message_:
            print(c,end='')
            mystr.append(c)
        print('',end='',flush=True)
    return 0

def substat_recom(recomlist,mystr):
    #print('\033[93m')
    recomlist.reverse()
    tmplist=[]
    total_=recomlist.__len__()
    num_=0
    while (tmplist.__len__()<10) & ([]!=recomlist):
        tmplist.append(recomlist.pop())
        num_+=1
    i=0
    print('\n'+list2str(mystr)+'__ ['+str(num_)+'/'+str(total_)+']')
    for s in tmplist:
        print('['+str(i)+'] '+s)
        i+=1
    #print('\033[0m'+list2str(mystr),end='',flush=True)
    print(list2str(mystr),end='',flush=True)
    while True:
        c = getch()
        if '\t'==c:
            #print('\033[93m',end='')
            if 1==i:
                mystr.clear()
                for e in tmplist[0]:
                    mystr.append(e)
                #print('\033[0m',end='')
                break
            tmplist=[]
            while (tmplist.__len__()<10) & ([]!=recomlist):
                tmplist.append(recomlist.pop())
                num_+=1
            i=0
            if []==tmplist:
                #print('\033[0m',end='')
                break
            print('__ ['+str(num_)+'/'+str(total_)+']')
            for s in tmplist:
                print('['+str(i)+'] '+s)
                i+=1
            #print('\033[0m'+list2str(mystr),end='',flush=True)
            print(list2str(mystr),end='',flush=True)
            continue
        if c in '0123456789':
            try:
                return tmplist[int(c)]
            except IndexError as e:
                None
            continue
        if '\x7f'==c:
            mystr.pop()
            break
        break
    if c in ' -abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
        mystr.append(c)
    return -1

## prepare list of dicts: dict_list
dict_dir='F:\\TDDOWNLOAD\\mydict_py\\txt'
#dict_dir=os.path.join(os.getcwd(), 'txt')
fns = os.listdir(dict_dir)
fns.sort()
dict_list=[]
myreg = re.compile('oxford-gb_[0-9]{2}')
for f in fns:
    if myreg.match(f):
        dict_list.append(os.path.join(dict_dir,f))
#print(dict_list)

## prepare word map, a hash table: hash_word_myseek
divider_reg = re.compile('-{29}')
dict_=9
hash_word_myseek = {}
hash_of_firstchar = {}
list_allword = []
mywordtree=[]
for dict_ in range(0,dict_list.__len__()):
    print(dict_,flush=True)
    fid=open(dict_list[dict_], 'r' , encoding='utf8')
    switch_recordit = False
    while True:
        str_=fid.readline()
        if ''==str_:
            break
        if divider_reg.match(str_):
            myorder=''#input()
            if 's'==myorder:
                print(hash_word_myseek)
            switch_recordit = True
            seek_=fid.tell()
        else:
            #print(str_)
            if switch_recordit:
                update_hash_word_myseek(str_,seek_,dict_,hash_word_myseek,list_allword,hash_of_firstchar,mywordtree)
                switch_recordit = False
    fid.close()
#print(hash_word_myseek)
#print(list_allword)
#print(hash_of_firstchar)

## main body, check a word
message=['dict prepared!']
myhistlist = []
mystr=[]
mystat=2 # 0 nothing, 1 upload, 2 newline under current stat, 3 replace mystr
myseek=0
while True:
    mystat=input_refresh(mystr,mystat,hash_word_myseek,dict_list,divider_reg,message,myhistlist)
    c=getch()
    if '.'==c: #.
        print('\n.hist.')
        print(myhistlist)
        mystat=2
        continue
    if '\xe0H'==c: # UP
        if []==myhistlist:
            mystat=0
            continue
        message.append(myhistlist[myhistlist.__len__()-1])
        myhistlist.insert(0,myhistlist.pop())
        mystat=3
        continue
    if '\xe0P'==c: # DOWN
        if []==myhistlist:
            mystat=0
            continue
        message.append(myhistlist[myhistlist.__len__()-1])
        myhistlist.append(myhistlist[0])
        myhistlist.remove(myhistlist[0])
        mystat=3
        continue
    if '\x1b'==c: #ESC
        break
    if '\x08'==c: #Backspace
        try:
            mystr.pop()
            print('\b \b',end='',flush=True)
        except IndexError as e:
            mystat=0
        continue
    if '\r'==c: #Enter
        mystat=2
        if mystr.__len__()>0:
        	print('',flush=True)
        	mystat=1
        continue
    if '\t'==c: # Tab
        if []==mystr:
            mystat=0
            continue
        mysubtree=return_subtree(mywordtree,mystr)
        if -1==mysubtree:
            message=['\nno match!']
            mystat=2
            continue
        recomlist=[]
        decode_treeofwords(mysubtree,list2str(mystr),recomlist)
        t=substat_recom(recomlist,mystr)
        if -1==t:
            mystat=2
        else:
            print('', flush=True)
            mystr=str2list(t)
            mystat=1
        continue
    if c in ' -abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
        print(c,end='',flush=True)
        mystr.append(c)
        continue
    if '_'==c:
        t=input('_\ninput a num: ')
        try:
            num_=int(t)
        except ValueError as e:
            message=['not a num']
            mystat=2
            continue
        try:
            s=list_allword[num_]
            print(s)
        except IndexError as e:
            message=['wrong num']
            mystat=2
            continue
        mystr.clear()
        for c in s:
            mystr.append(c)
        print(mystr)
        mystat=1
        continue

print('\nbyebye')










