
import numpy as np
from random import randint,random

class Matrix():

    def __init__(self,shape,ones):
        self.featNb = shape[0]
        self.valNb = shape[1]
        if ones:
            self.matrix = np.ones(shape)
        else:
            self.matrix = np.zeros((self.featNb,self.valNb))

    #@classmethod def with_language(self,language)
            
    def match_to_language(self,language):
        for obj_meaning in training_data:
            self.update(obj_meaning)

    def __str__(self):
        return str(self.matrix)
    
    def update(self,obj_meaning):
        for i in range(len(obj_meaning)):
            self.matrix[obj_meaning[i]-1][i] = True

    def isExpressible(self,obj_meaning):
        b = True
        for i in range(self.valNb):
            b = b and self.matrix[obj_meaning[i]-1][i] 
        return b

    def expressivity_score(self,obj_meaning):
        n = len(obj_meaning)
        expressed_nb = sum([self.isExpressible(obj) for obj in obj_meaning])
        #return "{0:.2f}".format(expressed_nb/n)
        return expressed_nb/n
        
class MatrixList(Matrix):
    def __init__(self,dim_list,ones=False):
        self.matrixList = [Matrix(dim,ones) for dim in dim_list]
        self.dim_list = dim_list
        self.nb = len(dim_list)

    def __getitem__(self,index):
        return self.matrixList[index]

    def __str__(self):
        s = ""
        for i in range(self.nb):
            s += str(self[i])
            s += "\n"
        return s

    @classmethod
    def match_to(self,dim_list,language_list):
        ml = MatrixList(dim_list)
        for i in range(ml.nb):
            ml[i].match_to_language(language_list[i])
        return ml
        
    def chose_meaning(self,obj):
        index_list = []
        for i in range(self.nb):
            if self.matrixList[i].isExpressible(obj[i]):
                index_list.append(i)
        if index_list != []:
            return index_list[randint(0,len(index_list)-1)]
        else:
            return None

    def invent(self,obj):
        rand = randint(0,self.nb-1)
        self[rand].update(obj[rand])
        
        
    def expressivity_score(self,obj_meanings):
        l = []
        for i in range(self.nb):
            #print("Meaning Space "+str(self.dim_list[i])+" : "+self[i].expressivity_score(obj_meanings[i]))
            l.append(self[i].expressivity_score(obj_meanings[i]))
        return l

            
    
def init_rand_meanings(dim_list,n):
    l = []
    for dim in dim_list:
        acc = []
        for i in range(n):
            acc.append([randint(0,dim[0]-1) for j in range(dim[1])])
        l.append(acc)
    return l


# DIMENSION : VxF
def simulation(dim_list,language_list=None,n=100,r=50,iterations=50,invention=0.1,verbose=False):
    
    #Create n objects and their value for each feature of each meaning space
    obj_meanings = init_rand_meanings(dim_list,n)
    #Initialise the speaker matrices randomly
    speaker_matrices = MatrixList(dim_list,ones=True)
    
    for t in range(iterations):
        #Initialise the matrices of the learner, filled with zeros
        learner_matrices = MatrixList(dim_list,ones=False)
        for production in range(r):
            #Pick a random object
            rand_index = randint(0,n-1)
            rand_obj = [obj_meanings[i][rand_index] for i in range(len(dim_list))]
            #Pick, if any, an expressible meaning space for that object
            chosen_meaning_index = speaker_matrices.chose_meaning(rand_obj)
            #Learner acquired the meanings, and update its matrix accordingly
            if chosen_meaning_index != None:
                learner_matrices[chosen_meaning_index].update(rand_obj[chosen_meaning_index])
            else:
                if (random()<invention):
                    learner_matrices.invent(rand_obj)
        if verbose:
            print("Expressivity of the "+str(t)+"-th iteration")
            speaker_matrices.expressivity_score(obj_meanings)

                    
        #The student becomes the master
        speaker_matrices = learner_matrices


    
    return speaker_matrices.expressivity_score(obj_meanings)


def average(dim_list,simu_nb):
    l = simulation(dim_list)
    for simu in range(simu_nb-1):
        ll = simulation(dim_list)

        for i in range(len(l)):
            l[i] += ll[i]

    print(l)
    avg = [l[i]/simu_nb for i in range(len(l))]

    return zip(dim_list,avg)
