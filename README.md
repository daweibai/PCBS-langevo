# Iteratred Learning Model for language evolution

Introduced by Pinker & Bloom (1990), iterated learning is a paradigm that is used to study language transmission. Then in 2001, Simon Kirby implanted the paradigm into computer modeling. His 2001 paper is the first journal paper to present the Iterated Learning Model (ILM) in language evolution. It shows that compositionality emerges out of iterated learning. 
<p></p>
The present project is an attempt to reproduce a simplified version of Kirby's (2001) ILM. No code was provided in Kirby's paper, so I'll try to build the model with my own code.


The model works as follows:

It has four components: 
- a meaning space: a 5x5 table, the positions of which represents meaning. It has two meaning components, A and B, that create a space from (a<sub>0</sub>, b<sub>0</sub>) to (a<sub>4</sub>, b<sub>4</sub>).
- a signal space: an ordered linear string of characters drawn from lower-case letters. The length limit for each string is 10 characters. 
- one adult and one learner within each iteration. There's only one transmission chain, that is, one single adult agent speaks his grammar to one learner. Then the latter becomes an adult, and speaks to the next learner. 

The ILM works like any other iterated learning paradigm: the output of one agent is the input of the next. Then, this process is repeated over multiple generations. To be more precise: 

1. Each adult (except for the first one) has an internal representation of the grammar, that is, a rule space about how the meaning spce is mapped to strings. He generates a set of 50 strings based on his grammar, and passes the (meaning, grammar) pairs to the learner.
2. Before the learner receives the strings, he has no grammar. The first adult dosen't have a grammar either. He generates random strings to pass on to the first learner.
3. Each learner as the capacity (equivalent to Universal Grammar) to parse the input strings and induce the grammar. He does so by extracting the common substrings of strings he hears. For instance, if he receives (a<sub>0</sub>, b<sub>0</sub>) mapped onto "fsdfr" and (a<sub>0</sub> b<sub>1</sub>) onto "fsdptdgfmr", he will notice that the common substring "fsd" and infer the rule "fsd" means a0, when the other meaning component is b<sub>0</sub> and b<sub>1</sub>. Note that he can only do so if the two strings share a same sub-meaning-component. For instance, if there is a common substring between (a<sub>0</sub>, b<sub>0</sub>) and (a<sub>3</sub>, b<sub>4</sub>), then he won't infer any rule. But if the second meaning was (a<sub>0</sub>, b<sub>4</sub>), given that the two meanings share a<sub>0</sub>, a rule will be infered for a0. Notice that my model don't allow circumfixes: if there's a common string in the middle, it doesn't count, contrary to Simon Kirby's original model. But it shouldn't change much the iteration evolution anyway.
4. The rules that the learner infers will be mapped onto two rule spaces of 5x5, one for the meaning component A, one for B. This isn't in Simon Kirby's original model. He used a more complex Context-Free Grammar based algorithms that I'm not capable of implementing. In his model, same rules of the same meaning components are merged into a more general rule. This isn't necessary if you have a rule space: the same rules can simply be kept in their respective slot.
5. Then the learner becomes an adult. He produces 50 strings generated from his rule space. The production is simple: for a meaning, if the adult has rules for both meaning component, then he concatenates the rules to produce the string. If he only has one meaning component, then the other half will be a random string. If he doesn't have any rule for the meaning, then he generates a random string. The 50 strings are mapped onto the 5x5 meaning space. Notice that the 50 produced strings don't necessarily cover all the 25 meaning slots (Bottleneck).
6. The learner, upon receiving the adults' production, parses the sting-meaning pairs to infer the rules.
7. Iterate.

For example, the first (random) production from the first adult is:
```python
['qxnreh', 'slkdtz', 'akfg', 'iyifvtp', 'henjzf']
['ywf', 'krb', 'jtgkil', 'qcm', 'th']
['bwymfjx', 'wjfjmbye', 'syncwkhgp', 'lio', 'jppqbvrbke']
['mnkzz', 'mcwtfxxpwk', 'dazd', 'ztpzocij', 'cjokz']
['qyu', 'id', 'splg', 'tzthqmk', 'qml']
```
The first learner will infer, for the meaning component A:

```python
['a0', 'a1', 'a2', 'a3', 'a4']
['Pq', '', 'Sg', '', '']
['', '', '', '', '']
['', '', '', '', '']
['', '', '', '', '']
['Pq', '', 'Sg', '', '']
```

and for the meaning component B:
```python
['b0', '', '', '', '', '']
['b1', '', '', '', '', '']
['b2', '', 'Se', '', '', 'Se']
['b3', '', '', '', '', '']
['b4', 'Pq', '', '', '', 'Pq']
```
"P" and "S" are nonterminals that mean "shared prefix" and "shared suffix". The learner noticed that for instance, both (a<sub>0</sub>, b<sub>0</sub>) and (a<sub>0</sub>, b<sub>4</sub>) begin with "q", and both (a<sub>2</sub>, b<sub>2</sub>) and (a<sub>4</sub>, b<sub>2</sub>) end with "e".

The code is composed of :
- A rule space, that is a global variable that will be modfied by functions in each iteration:
```python
rules = {
#Initial rule space. A is for column rules. B for row rules.
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
```

- A string generator that generates a random string:

```python
def str_gen(size, chars=string.ascii_lowercase):
#generate a random string of length between 1 and 10
    return ''.join(random.choice(chars) for x in range(size))
```

- An empty meaning space that all learners are equipped of before exposure to language:

```python
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

- A common substring finder that takes two strings as input, and gives a common prefix and a common suffix as output. If there's no common prefix or common suffix, then it returns two empty strings:

```python
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

```
- The first adult's random signal space, outside the functions:
```python
first_agent = []
for b in range(5):
    row = [] 
    for a in range(5):
        row.append(str_gen(randint(1, 10)))
    first_agent.append(row)
```

- A parser for columns, that takes a space of utterance and modifies the column rules. Nonterminals "P" and "S" are placed in the beginning of the rule. They simply indicate if the rule is about a prefix or a suffix. Therefore, subsequent functions can identify the placement of the characters. Of course they will be omitted during production:
```python
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
```

- A similar parser for rows, that takes the same space of utterance and modifies the rows rules:

```python
def row_parser(utter):
#   Grammar induction for the rows. The function takes utterances and modifies the rules.

    global rules
    for b in range(5): #row
        for a in range(5): #column
            for a2 in np.arange(a,5): 
                #compare two elements in the same row
                if substr_finder(utter[b][a],utter[b][a2])[0] != '' \
                and substr_finder(utter[b][a],utter[b][a2])[1] == '':
                    #if find common prefix and not common suffix
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
```

- A production function, that takes the number of utterances (that will be defined as 50) and returns a 5x5 space of utterance. Notice that the generated strings can be longer than 10 characters, which is a bug that I haven't fixed. Also, when multiple strings are produced for the same meaning (there are 50 strings for 25 meanings, for there are necessarily meanings receiving more than one string), only the last one is kept. In Kirby's model, he kept the shortest. Moreover, A component and B component can both be prefix or suffix rules, I can't merely merge them together. Instead, So need to put them in order depending on their categories. I arbitrarily decided that if both A and B components are sufffix rules, then update the A component, and if both are prefix rules, then update the B component:
```python
def production(n_of_utter):
#   produce utterances. If there's a rule, produce as the rule says. If there isn't, generate random string
    global rules
    produc = empty_meaning_space()
    for n in range(n_of_utter):
        col = randint(0, 4)
        row = randint(0, 4)
#        randomly choose a meaning to produce a string for
        if rules["A"][row+1][col] != '' and rules["A"][row+1][col][0] == 'P' and\
        rules["B"][row][col+1] != '' and rules["B"][row][col+1][0] == 'S':
#            if A rule is for prefix, B for suffix
            produc[row][col] = rules["A"][row+1][col][1:] +rules["B"][row][col+1][1:]
#            merge two rules prefix + suffix to for a word
#            doesn't take the shortest one, but the last one for that meaning
        elif rules["A"][row+1][col] != '' and rules["A"][row+1][col][0] == 'S' \
        and rules["B"][row][col+1] != '' and rules["B"][row][col+1][0] == 'P':
#            if A rule is for suffix, B for prefix
            produc[row][col] = rules["B"][row][col+1][1:] + rules["A"][row+1][col][1:]
        elif rules["A"][row+1][col] == '' and rules["B"][row][col+1] != '' and \
        rules["B"][row][col+1] == 'P':
#            if A rule is empty, B rule is for prefix
#            could be more than 10 characters
            produc[row][col] = rules["B"][row][col+1][1:] + str_gen(randint(1, 9))
        elif rules["A"][row+1][col] == '' and rules["B"][row][col+1] != '' and \
        rules["B"][row][col+1] == 'S':
#            if A rule is empty, B rule is for suffix
            produc[row][col] = str_gen(randint(1, 9)) + rules["B"][row][col+1][1:]
        elif rules["A"][row+1][col] != '' and rules["A"][row+1][col] == 'P' and\
        rules["B"][row][col+1] == '':
#            if A rule is for prefix, B rule is empty            
            produc[row][col] = rules["A"][row+1][col][1:] + str_gen(randint(1, 9))  
        elif rules["A"][row+1][col] != '' and rules["A"][row+1][col] == 'S' and\
        rules["B"][row][col+1] == '':
#            if A rule is for suffix, B rule is empty            
            produc[row][col] = str_gen(randint(1, 9)) + rules["A"][row+1][col][1:] 
        elif rules["A"][row+1][col] == 'S' and rules["A"][row+1][col] == 'S' and\
        rules["B"][row][col+1] == '':
#            if A and Brule are for suffix            
            produc[row][col] = rules["A"][row+1][col][1:]         
        elif rules["A"][row+1][col] == 'P' and rules["A"][row+1][col] == 'P' and\
        rules["B"][row][col+1] == '':
#            if A and Brule are for prefix            
            produc[row][col] = rules["B"][row][col+1][1:]    
        else :
#            if both rules are empty, generate a random string
#            should I do this for the latter two cases?
            produc[row][col] = str_gen(randint(1, 10))    
    return produc
```

- And an iteration function, that takes the number of iterations and execute all the functions above over multiple iterations, and returns the utterance of the last iteration:
```python
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
Results are not as expected. After 100 iterations, the production is:
```python
['sj', 'cs', 'porzqohz', 'nyhnzor', 'co']
['hwnsbaaup', 'lwvz', 'uibdfnhb', 'xo', 'kt']
['rhgcxcp', 'ej', 'cj', 'xhdv', 'eo']
['cs', 'eo', 'cs', 'ss', 'vm']
['ce', '', 'eboiywtgpx', '', 'ke']
```
the rules are, for A component:

```python
['a0', 'a1', 'a2', 'a3', 'a4']
['Sj', 'Ss', 'Pc', 'Ps', 'So']
['Sp', 'Sk', 'Ss', 'Px', 'Pk']
['Sp', 'Pe', 'Pc', 'Px', 'So']
['Pc', 'Pe', 'Pc', 'Ps', 'St']
['Pc', 'Pe', 'Ss', 'Pe', 'Pk']
```
for B component:
```python
['b0', 'Ps', 'Pc', 'Pc', 'Ps', 'Pc']
['b1', 'Sk', 'Sk', 'St', 'Px', 'St']
['b2', 'Sj', 'Pe', 'Sj', 'Pb', 'Pe']
['b3', 'Ss', 'So', 'Ss', 'Ss', 'Ss']
['b4', 'Se', 'Pe', 'Se', 'Se', 'Se']
```

First of all, no convergence occurred, that is, no compositionality emerged after 100 generations (same after 500 generations).
Second of all, all the rules contain only one character. Both of them are not found in Kirby's paper. 

- Reflection on my work
This has been a challenging project. I modified some elements of the program compared to that explained in Kirby's paper. I didn't fully implement the Context-Free Grammar for rule induction and string production, although I kept some features of it (those I'm capable of implementing). I still don't understand why convergence doesn't happen. 


# AE
* What was your level in programming before starting the class (roughly)

I had no training in coding before coming to the Cogmaster. I followed the AT2 course last year, which is an introductory course to computational neuroscience. For all my codes, I mostly only used functions like the conditional and the "for" loop. I had never defined a function before this course. My goal was to plot figures and "as long as it works".

* What you learned while working for this class (throught the lectures and/or the project)

I learned to define functions, the dictionary and functions manipulating strings. I also learned to plan the structure of the codes before starting. The homeworks I did in AT2 didn't demande this sort of global planning.
I've never done a project as challenging as this one (I should have chosen something easier). For weeks I didn't have an idea about where to begin (and therefore neither did I know what to ask). I spent a lot of time trying to understand the ILM and the Context-Free Grammar. There's no code of ILM or CFG to be found on the Internet that I could understand. And given that I still don't understand how to implement CFG in Python, I didn't follow the algorithm sketches in Kirby's paper. Instead, I built the model from my understanding of the ILM, which is a great exercise.

* If you have any suggestions to improve the class for the future



# Reference
Kirby, S. (2001). Spontaneous evolution of linguistic structure-an iterated learning model of the emergence of regularity and irregularity. IEEE Transactions on Evolutionary Computation, 5(2), 102-110.
<p></p>
Pinker, S., & Bloom, P. (1990). Natural language and natural selection. Behavioral and brain sciences, 13(4), 707-727.
