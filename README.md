# Iteratred Learning Model for language evolution

Introduced by Pinker & Bloom (1990), iterated learning is a paradigm that is used to study language transmission. Then in 2001, Simon Kirby implanted the paradigm into computer modeling. His 2001 paper is the first journal paper to present the Iterated Learning Model (ILM) in language evolution. It shows that compositionality emerges out of iterated learning. 
<p></p>
In the present project, I try to reproduce a simplified version of Kirby's (2001) ILM.

The model works as follows:

It has four components: 
- a meaning space: a 5x5 table, the positions of which represents meaning. It has two meaning components, A and B, that create a space from (a0, b0) to (a4, b4).
- a signal space: an ordered linear string of characters drawn from lower-case letters. The length limit for each string is 10 characters. 
- one adult and one learner within each iteration. There's only one transmission chain, that is, one single adult agent speaks his grammar to one learner. Then the latter becomes an adult, and speaks to the next learner. 

The ILM works like any other iterated learning paradigm: the output of one agent is the input of the next. Then, this process is repeated over multiple generations. To be more precise: 

1. Each adult (except for the first one) has an internal representation of the grammar, that is, how the meanings are mapped to the strings. He generates a set of 50 strings based on his grammar, and passes the (meaning, grammar) pairs to the learner.
2. Before the learner receives the strings, he has no grammar. The first adult dosen't have a grammar either. He generates random strings to pass on to the first learner.
3. Each learner as the capacity (equivalent to Universal Grammar) to parse the input strings and induce the grammar. He does so by extracting the common substrings of strings he hears. For instance, if he receives (a0, b0) mapped onto "fsdfr" and (a0, b1) onto "fsdptdgfmr", he will notice that the common substring "fsd" and infer the rule "fsd" means a0, when the other mea b0 and b1. Note that he can only do so if the two strings share a same sub-meaning-component. For instance, if there is a common substring between (a0, b0) and (a3, b4), then he won't infer any rule. But if the second meaning was (a0, b4), given that the two meanings share a0, a rule will be infered for a0. In my model, I simplify the meaning component A to "suffix", B to "prefix". In other words, when the agent notices a common string at the beginning or at the end of both words, he will add his rule into the corresponding A or B rule space. My model don't allow circumfixes: if there's a common string in the middle, it doesn't count, contrary to Simon Kirby's original model.
4. The rules that the learner infers will be mapped onto two rule space of 5x5, one for the meaning component A, one for B. This isn't in Simon Kirby's original model. He used a more complex Context-Free Grammar based algorithms that I'm not capable of implementing. In his model, same rules of the same meaning components are merged into a more general rule. This isn't necessary if you have a rule space: the same rules can simply be kept in their respective slot.
5. Then the learner becomes an adult. He produces 50 strings generated from his rule space. The production is simple: for a meaning, if the adult has rules for both meaning component, then he concatenates the rules to produce the string. If he only has one meaning component, then the other half will be a random string. If he doesn't have any rule for the meaning, then he generates a random string. Notice that the 50 produced strings don't necessarily cover all the 25 meaning spaces.

For example, the first (random) production from the first adult is:
```
['oywuxdoag', 'okegbwtnku', 'juodih', 'b', 'v']
['lobsejjofd', 'cyeziht', 'slitntbuk', 'q', 'sypcc']
['dhsbxun', 'fzbbfkimvx', 'vxjxqmb', 'zyzch', 'fovg']
['hphq', 'sxzpusa', 'g', 'fseq', 'auxjj']
['khnlukfbjc', 'nqfrgzcim', 'iyuas', 'mr', 'os']
```
The first learner will infer, for the meaning component A:

```
['suf0', '', '', '', '', '']
['suf1', '', '', '', 'q', '']
['suf2', '', '', '', '', '']
['suf3', '', '', '', 'q', '']
['suf4', '', '', '', '', '']
```

and for the meaning component B:
```
['pre0', '', '', '', '', '']
['pre1', '', '', 's', '', 's']
['pre2', '', '', '', '', '']
['pre3', '', '', '', '', '']
['pre4', '', '', '', '', '']
```
This is because he noticed that both (a2, b1) and (a4, b1) begin with "s", and both (a3, b1) and (a3, b3) end with "q".

It's worth noting that what's called "prefix" and "suffix" here can be equaled to "semantic labels". We can imagine that the B component is the subject: pre0 = "je", pre1 = "tu", pre2 = "il", etc. And the A component could be one place predicates, e.g., suf0 = "manger", suf1 = "dormir", suf2 = "boire", etc. Therefore, the meaning pairs could be "je mange", "tu manges", etc.

The code is composed of a rule space, that is a global variable that will be modfied by functions in each iteration:
```
rules = {
#Initial rule space. A is for lefthand rules (prefix). B for righthand rules (suffix).
    "A":[ 
        ["pre0","","","","",""],
        ["pre1","","","","",""],
        ["pre2","","","","",""],
        ["pre3","","","","",""],
        ["pre4","","","","",""]
    ],
    "B":[ 
        ["suf0","","","","",""],
        ["suf1","","","","",""],
        ["suf2","","","","",""],
        ["suf3","","","","",""],
        ["suf4","","","","",""]
    ]
}
```

a string generator that generates a random string:

```
def str_gen(size, chars=string.ascii_lowercase):
#generate a random string of length between 1 and 10
    return ''.join(random.choice(chars) for x in range(size))
```

an empty meaning space that all learners are equipped of before exposure to language:

```
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
```

a common substring finder that takes two strings as input, and gives a common prefix and a common suffix as output. If there's no common prefix or common suffix, then it returns two empty strings:

```
def substr_finder(s1,s2):
#takes two strings and extract the common substrings in the beginning or at the end
    m = len(s1)
    n = len(s2)
    counter = [[0]*(n+1) for x in range(m+1)]
    longest = 0
    common = ''
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
        A = common
    else:
        A = ''
    if common == s1[-len(common):] and common == s2[-len(common):]:
#        for suffix rules
        B = common
    else:
        B = ''
    return A,B

```
the first adult's random signal space, outside the functions:
```
first_agent = []
for b in range(5):
    row = [] 
    for a in range(5):
        row.append(str_gen(randint(1, 10)))
    first_agent.append(row)
```

a parser for columns, that takes a space of utterance and modifies the column rules:
```
def column_parser(utter):
    global rules
#Grammar induction for the columns. The function takes utterances and modifies the rules.
    for b in range(5): #row
        for a in range(5): #column
            for a2 in np.arange(a,5): 
                #compare two elements
                if substr_finder(utter[b][a],utter[b][a2])[0] != '' \
                and substr_finder(utter[b][a],utter[b][a2])[1] == '':
                    rules["A"][b][a+1] = substr_finder(utter[b][a],utter[b][a2])[0]
                    rules["A"][b][a2+1] = substr_finder(utter[b][a],utter[b][a2])[0]
```

a parser for rows, that takes the same space of utterance and modifies the rows rules:

```
def row_parser(utter):
#Grammar induction for the rows
    global rules
    for a in range(5): #row
        for b in range(5): #column
            for b2 in np.arange(b,5): 
                #compare two elements
                if substr_finder(utter[b][a],utter[b2][a])[0] == '' \
                and substr_finder(utter[b][a],utter[b2][a])[1] != '':
                    rules["B"][b][a+1] = substr_finder(utter[b][a],utter[b2][a])[1]
                    rules["B"][b2][a+1] = substr_finder(utter[b][a],utter[b2][a])[1]
```

a production function, that takes the number of utterances (that will be defined as 50) and returns a 5x5 space of utterance:
```
def production(n_of_utter):
#produce utterances. If there's a rule, produce as the rule says. If there isn't, generate random string
    global rules
    produc = empty_meaning_space()
    for n in range(n_of_utter):
        col = randint(0, 4)
        row = randint(0, 4)
        if rules["A"][row][col+1] != '' and rules["B"][row][col+1] != '':
            produc[row][col] = rules["A"][row][col+1]+rules["B"][row][col+1]
#            doesn't take the shortest one
        if rules["A"][row][col+1] == '' and rules["B"][row][col+1] != '':
            produc[row][col] = str_gen(randint(1, 10))+rules["B"][row][col+1]
#            could be more than 10 characters
        if rules["A"][row][col+1] != '' and rules["B"][row][col+1] == '':
            produc[row][col] = rules["A"][row][col+1] + str_gen(randint(1, 10))    
        if rules["A"][row][col+1] == '' and rules["B"][row][col+1] == '':
            produc[row][col] = str_gen(randint(1, 10))    
    return produc
```

an iteration function, that takes the number of iterations and execute all the functions above over multiple iterations, and returns the utterance of the last iteration:
```
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
            
        if i in np.arange(10,100,5):

            print(rules["A"][0])    

    return prod
```


Later on I realized that this model doesn't work. This is because the A and B rules only respectively account for suffixes and prefixes, therefore, if there's a common prefix in one column, or a common suffix in a row, no rules will be generated. I modified the code so that both A and B component can register common substrings in columns and rows, but unfortunately I can't make it work.

# AE
* What was your level in programming before starting the class (roughly)

I had no training in coding before coming to the Cogmaster. I followed the AT2 class last year, where we modeled neural networks. For all my codes, I mostly only used functions like the conditional and the "for" loop. I had never defined a function before this course. My goal was to plot figures and "as long as it works".

* What you learned while working for this class (throught the lectures and/or the project)

I learned to define functions, the dictionary and functions manipulating strings. I also learned to plan the structure of the codes before starting. The homeworks I did in AT2 didn't demande this sort of global planning.
I've never done a project as challenging as this one (I should have chosen something easier). For weeks I didn't have an idea about where to begin (and therefore neither did I know what to ask). I spent a lot of time trying to understand the ILM and the Context-Free Grammar. There's no code of ILM or CFG to be found on the Internet that I could understand. And given that I still don't understand how to implement CFG in Python, I didn't follow the algorithm sketches in Kirby's paper. Instead, I built the model from my understanding of the ILM, which is a great exercise.

* If you have any suggestions to improve the class for the future



# Reference
Kirby, S. (2001). Spontaneous evolution of linguistic structure-an iterated learning model of the emergence of regularity and irregularity. IEEE Transactions on Evolutionary Computation, 5(2), 102-110.
<p></p>
Pinker, S., & Bloom, P. (1990). Natural language and natural selection. Behavioral and brain sciences, 13(4), 707-727.
