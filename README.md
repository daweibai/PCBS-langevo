# Iteratred Learning Model for language evolution

Introduced by Pinker & Bloom (1990), iterated learning is a paradigm that is used to study language transmission. Then in 2001, Simon Kirby implanted the paradigm into computer modeling. His 2001 paper is the first journal paper to present the Iterated Learning Model (ILM) in language evolution. It shows that compositionality emerges out of iterated learning. 
<p></p>
In the present project, I try to reproduce a simplified version of Kirby's (2001) ILM.

The model works as follows:

It has four components: 
- a meaning space: a 5x5 table, the positions of which represents meaning. It has two meaning components, A and B, that create a space from (a0, b0) to (a4, b4).
- a signal space: an ordered linear string of characters drawn from lower-case letters. The length limit for each string is 10 characters. 
- one adult and one learner within each iteration. There's only one transmission chain, that is, one single adult agent speaks his grammar to one learner. Then the latter becomes an adult, and speaks to the next learner. 

The ILM works like any other iterated learning paradigm. The output of one agent is the input of the next. Then this process is repeated over multiple generations. To be more precise: 

1. Each adult (except for the first one) has an internal representation of the grammar, that is, how the meanings are mapped to the strings. He generates a set of 50 strings based on his grammar, and passes the (meaning, grammar) pairs to the learner.
2. Before the learner receives the strings, he has no grammar. The first adult dosen't have a grammar either. He generates random strings to pass on to the first learner.
3. Each learner as the capacity (equivalent to Universal Grammar) to parse the input strings and induce the grammar. He does so by extracting the common substrings of strings he hears. For instance, if he receives (a0, b0) mapped onto "fsdfr" and (a0, b1) onto "fsdptdgfmr", he will notice that the common substring "fsd" and infer the rule "fsd" means a0, when the other mea b0 and b1. Note that he can only do so if the two strings share a same sub-meaning-component. For instance, if there is a common substring between (a0, b0) and (a3, b4), then he won't infer any rule. But if the second meaning was (a0, b4), given that the two meanings share a0, a rule will be infered for a0. In my model, I simplify the meaning component A to "prefix", B to "suffix". In other words, when the agent notices a common string at the beginning or at the end of both words, he will add his rule into the corresponding A or B rule space. My model don't allow circumfixes: if there's a common string in the middle, it doesn't count, contrary to Simon Kirby's original model.
4. The rules that the learner infers will be mapped onto two rule space of 5x5, one for the meaning component A, one for B. This isn't in Simon Kirby's original model. He used a more complex Context-Free Grammar based algorithms that I'm not capable of implementing.
5. Then the learner becomes an adult. He produces 50 strings generated from his rule space. The production is simple: for a meaning, if the adult has rules for both meaning component, then he concatenates the rules to produce the string. If he only has one meaning component, then the other half will be a random string. If he doesn't have any rule for the meaning, then he generates a random string.

For example, the first (random) production is:
```
['oywuxdoag', 'okegbwtnku', 'juodih', 'b', 'v']
['lobsejjofd', 'cyeziht', 'slitntbuk', 'q', 'sypcc']
['dhsbxun', 'fzbbfkimvx', 'vxjxqmb', 'zyzch', 'fovg']
['hphq', 'sxzpusa', 'g', 'fseq', 'auxjj']
['khnlukfbjc', 'nqfrgzcim', 'iyuas', 'mr', 'os']
```



# Reference
Kirby, S. (2001). Spontaneous evolution of linguistic structure-an iterated learning model of the emergence of regularity and irregularity. IEEE Transactions on Evolutionary Computation, 5(2), 102-110.
<p></p>
Pinker, S., & Bloom, P. (1990). Natural language and natural selection. Behavioral and brain sciences, 13(4), 707-727.
