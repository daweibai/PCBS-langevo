# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 03:39:42 2019

@author: Dawei
"""

#Reproduce Kirby's (2001) Iterated Learning Model simulating language evolution

import random
from random import randint
import string
import numpy as np

n_of_iterations = 100
#Number of iterations wanted

rules = {
#Initial rule spaces. A is for lefthand rules (prefix). B for righthand rules (suffix).
    "A":[ 
        ["a0","a1","a2","a3","a4"],
        ["","","","",""],
        ["","","","",""],
        ["","","","",""],
        ["","","","",""],
        ["","","","",""]
    ],
    "B":[ 
        ["b0","","","","",""],
        ["b1","","","","",""],
        ["b2","","","","",""],
        ["b3","","","","",""],
        ["b4","","","","",""]
    ]
}


def str_gen(size, chars=string.ascii_lowercase):
#Generate a random string of length between 1 and 10 defined later
    return ''.join(random.choice(chars) for x in range(size))


def empty_meaning_space():
#Generate an empty meaning space that will be the initial meaning space of every learner
    matrix = []
    row = []
    for b in range(5):
        row = [] 
        for a in range(5):
            row.append('')
        matrix.append(row)
    return matrix


def substr_finder(s1,s2):
#   takes two strings and extract the common substrings in the beginning or at the end
    m = len(s1)
    n = len(s2)
    counter = [[0]*(n+1) for x in range(m+1)]
    longest = 0
    common = ''
    prefix = ''
    suffix = ''
    for i in range(m):
        for j in range(n):
            if s1[i] == s2[j]:
                c = counter[i][j] + 1
                counter[i+1][j+1] = c
                if c > longest:
                    common = ''
                    longest = c
                    common = s1[i-c+1:i+1]
                elif c == longest:
                    common = s1[i-c+1:i+1]
    if common == s1[:len(common)] and common == s2[:len(common)]: 
#        for prefix rules
        prefix = common
    if common == s1[-len(common):] and common == s2[-len(common):]:
#        for suffix rules
        suffix = common
    return prefix,suffix
#Notice that my rules don't allow circumfixes. if there's a common string in th
#e middle, and a shorter common string in the beginning or in the end, it doesn
#'t count


#first agent
first_agent = []
for b in range(5):
    row = [] 
    for a in range(5):
        row.append(str_gen(randint(1, 10)))
    first_agent.append(row)


def row_parser(utter):
#   Grammar induction for the rows. The function takes utterances and modifies the rules.

    global rules
    for b in range(5): #row
        for a in range(5): #column
            for a2 in np.arange(a,5): 
#               compare two elements in the same row
                if substr_finder(utter[b][a],utter[b][a2])[0] != '' \
                and substr_finder(utter[b][a],utter[b][a2])[1] == '':
#                   if find common prefix and not common suffix
                    rules["B"][b][a+1] = 'P' + substr_finder(utter[b][a],utter[b][a2])[0]
                    rules["B"][b][a2+1] = 'P' + substr_finder(utter[b][a],utter[b][a2])[0]
#                   then add the common prefix to the grammar
#                   'P' is a functional character indicating it's a prefix
                elif substr_finder(utter[b][a],utter[b][a2])[0] == '' \
                and substr_finder(utter[b][a],utter[b][a2])[1] != '':
#                   if find common suffix and not common prefix
                    rules["B"][b][a+1] = 'S' + substr_finder(utter[b][a],utter[b][a2])[1]
                    rules["B"][b][a2+1] = 'S' + substr_finder(utter[b][a],utter[b][a2])[1]
#                   then add the common suffix to the grammar
#                   'S' is a functional character indicating it's a suffix                    


def column_parser(utter):
#   Grammar induction for the columns
    global rules
    for a in range(5): #column 
        for b in range(5): #row
            for b2 in np.arange(b,5): 
#               compare two elements
                if substr_finder(utter[b][a],utter[b2][a])[0] != '' \
                and substr_finder(utter[b][a],utter[b2][a])[1] == '':
#                   if find common prefix
                    rules["A"][b+1][a] = 'P' + substr_finder(utter[b][a],utter[b2][a])[0]
                    rules["A"][b2+1][a] = 'P' + substr_finder(utter[b][a],utter[b2][a])[0]
                if substr_finder(utter[b][a],utter[b2][a])[0] == '' \
                and substr_finder(utter[b][a],utter[b2][a])[1] != '':
#                   if find common suffix
                    rules["A"][b+1][a] = 'S' + substr_finder(utter[b][a],utter[b2][a])[1]
                    rules["A"][b2+1][a] = 'S' + substr_finder(utter[b][a],utter[b2][a])[1]


def production(n_of_utter):
#   produce utterances. If there's a rule, produce as the rule says. If there isn't, generate random string
    global rules
    produc = empty_meaning_space()
    for n in range(n_of_utter):
        col = randint(0, 4)
        row = randint(0, 4)
#       randomly choose a meaning to produce a string for
        if rules["A"][row+1][col] != '' and rules["A"][row+1][col][0] == 'P' and\
        rules["B"][row][col+1] != '' and rules["B"][row][col+1][0] == 'S':
#           if A rule is for prefix, B for suffix
            produc[row][col] = rules["A"][row+1][col][1:] +rules["B"][row][col+1][1:]
#           merge two rules prefix + suffix to for a word
#           doesn't take the shortest one, but the last one for that meaning
        elif rules["A"][row+1][col] != '' and rules["A"][row+1][col][0] == 'S' \
        and rules["B"][row][col+1] != '' and rules["B"][row][col+1][0] == 'P':
#           if A rule is for suffix, B for prefix
            produc[row][col] = rules["B"][row][col+1][1:] + rules["A"][row+1][col][1:]
        elif rules["A"][row+1][col] == '' and rules["B"][row][col+1] != '' and \
        rules["B"][row][col+1] == 'P':
#           if A rule is empty, B rule is for prefix
#           could be more than 10 characters
            produc[row][col] = rules["B"][row][col+1][1:] + str_gen(randint(1, 9))
        elif rules["A"][row+1][col] == '' and rules["B"][row][col+1] != '' and \
        rules["B"][row][col+1] == 'S':
#           if A rule is empty, B rule is for suffix
            produc[row][col] = str_gen(randint(1, 9)) + rules["B"][row][col+1][1:]
        elif rules["A"][row+1][col] != '' and rules["A"][row+1][col] == 'P' and\
        rules["B"][row][col+1] == '':
#           if A rule is for prefix, B rule is empty            
            produc[row][col] = rules["A"][row+1][col][1:] + str_gen(randint(1, 9))  
        elif rules["A"][row+1][col] != '' and rules["A"][row+1][col] == 'S' and\
        rules["B"][row][col+1] == '':
#           if A rule is for suffix, B rule is empty            
            produc[row][col] = str_gen(randint(1, 9)) + rules["A"][row+1][col][1:] 
        elif rules["A"][row+1][col] == 'S' and rules["A"][row+1][col] == 'S' and\
        rules["B"][row][col+1] == '':
#           if A and Brule are for suffix            
            produc[row][col] = rules["A"][row+1][col][1:]         
        elif rules["A"][row+1][col] == 'P' and rules["A"][row+1][col] == 'P' and\
        rules["B"][row][col+1] == '':
#           if A and Brule are for prefix            
            produc[row][col] = rules["B"][row][col+1][1:]    
        else :
#           if both rules are empty, generate a random string
#           should I do this for the latter two cases?
            produc[row][col] = str_gen(randint(1, 10))    
    return produc
            
        
def iteration(n_of_iteration):
    for i in range(n_of_iteration):
        if i == 0:
            prod = first_agent
            column_parser(prod) 
            row_parser(prod) 
        else:
            prod = production(50)
            column_parser(prod) 
            row_parser(prod) 
    for i in np.arange(10,10,100):
        for j in range (5):    
            print(prod[j])        
             

    return prod


i = iteration(n_of_iterations)

print('Production after', n_of_iterations, "iterations:")
for j in range (5):  
    print(i[j])

print('')

print('A rules:')
for j in range (6):
    print(rules["A"][j])

print('')

print('B rules:')
for j in range (5):    
    print(rules["B"][j])
