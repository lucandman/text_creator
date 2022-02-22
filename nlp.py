# -*- coding: utf-8 -*-
'''
Inspiration: Wu Dao 2.0
'''

#make into class and read text from txt class
#start with a word that is capitalized -> choose next word based on probability -> end if next added is '.'

#make everything function format so it's easier to be called


import numpy as np

class Poem:
    def __init__(self, s = 'poem.txt'):
        if not isinstance(s, str):
            raise Exception('needs to be  txt filename')
        with open(s) as f:
            text = f.read()
        self.text = text
        self.dic = {}
        self.words = text.split()
    
    def aux_lists(self):
        words = self.words
        
        signs = []
        for word in words:
            if not word.isalpha():
                for i in word:
                    if not i.isalpha():
                        if i in signs:
                            continue
                        signs.append(i)
        self.signs = signs
        
        i = 0    
        while i < len(words): #can be made more effcient (not check all words every time new ones are added)
            for s in signs:
                if s in words[i] and words[i] != s:
                    words[i] = words[i][:-1]
                    if words[i-1] != s:
                        words.insert(i+1, s)
            i += 1
        
        count_list = []

        for word in words:
            count_list.append(word.lower())
            
        self.count_list = count_list
        self.words = words
    
    def probabilities(self):
        words, dic, count_list = self.words, self.dic, self.count_list
        for i in range(len(words)):
            word = words[i]
            if word in dic.keys():
                if i == len(words) - 1:
                    dic[word][1].append('')
                else:
                    dic[word][1].append(words[i+1])
            else:
                prob = count_list.count(count_list[i]) / len(words)
                a = []
                if i == len(words) - 1:
                    a.append('')
                else:
                    a.append(words[i+1])            
                dic[word] = [prob, a] #change it so that each word has values: all words that might follow it and the porbabiltiy -> choose

        for key in dic.keys():
            dic[key][1] = list(set(dic[key][1]))
        
        self.words, self.dic, self.count_list = words, dic, count_list
    
    def find_beg(self):
        dic = self.dic
        begs = []
        begs.append(list(dic.keys())[0])
        be = dic['.'][1].copy() #ändern damit auch ? ! usw included sind!!
        if '' in be:
            be.remove('')
        begs.extend(be)
        begs_prob = []
        for i in begs:
            begs_prob.append(dic[i][0])
        beg_prob = []
        for i in begs_prob:
            beg_prob.append(i / sum(begs_prob))

        anfang_ind = np.random.choice([i for i in range(len(begs))], p = np.array(beg_prob))
        anfang = begs[anfang_ind]
        
        return anfang

    def create(self, anfang):
        dic = self.dic
        signs = self.signs
        ret = anfang
        current = anfang
        while True:
            new = dic[current][1]
            new_pro = []
            for n in new:
                if n == '':
                    new_pro.append(0)
                else:
                    new_pro.append(dic[n][0])
            new_prob = []
            for i in new_pro:
                new_prob.append(i / sum(new_pro))
            new_ind = np.random.choice([i for i in range(len(new))], p = np.array(new_prob))
            current = new[new_ind]
            if current in signs:
                ret += current
                if current in ['.', '?', '!']:
                    break
            #if ' "
            else:
                ret += ' ' + current
        return ret
        
    def run(self):
        self.aux_lists()
        self.probabilities()
        a = self.find_beg()
        return self.create(a)
        
    def __repr__(self):
        return f"{self.run()}"
        

print(Poem())




        
        
        
        
        
        
        
        
        
        
        
        
        
        