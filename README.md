# Iteratred Learning Model for language evolution

Introduced by Pinker & Bloom (1990), iterated learning is a paradigm that is used to study language transmission. Then in 2001, Simon Kirby implanted the paradigm into computer modeling. His 2001 paper is the first journal paper to present the Iterated Learning Model (ILM) in language evolution. It shows that compositionality emerges out of iterated learning. 
<p></p>
In the present project, I try to reproduce the ILM by Kirby (2001). Bottleneck effect

The model works as follows:

It has four components: 
- a meaning space: a 5x5 table from (a0, b0) to (a4, b4), the positions of which represents meaning.
- a signal space: an ordered linear string of characters drawn from lower-case letters. The length limit for each string is 10 characters. 
- one adult and one learner within each iteration. There's only one transmission chain, that is, one single adult agent speaks his grammar to one learner. Then the latter becomes an adult, and speaks to the next learner. 

The ILM works like any other iterated learning paradigm. The output of one agent is the input of the next. Then this process is repeated over multiple generations. To be more precise: 

Each adult (except for the first one) has an internal representation of the grammar, that is, how the meanings are mapped to the strings.
The learner receives
Each agent as the capacity to parse the input strings and induce the grammar. For instance, if (a0, 
produces 50 strings generated from 



# Reference
Kirby, S. (2001). Spontaneous evolution of linguistic structure-an iterated learning model of the emergence of regularity and irregularity. IEEE Transactions on Evolutionary Computation, 5(2), 102-110.
<p></p>
Pinker, S., & Bloom, P. (1990). Natural language and natural selection. Behavioral and brain sciences, 13(4), 707-727.
