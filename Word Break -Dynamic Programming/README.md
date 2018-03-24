# Word Break Problem- Dynamic Programming

#### Author(s): Christopher Jens Johnson

This project is a simple approach to the "word break" problem in dynamic programming. We're given a series of phrases, such as:

> thisisawordiamtryingtosplit

And we want to determine if we can split each phrase into a series of valid words, such as:

> this is a word i am trying to split


The program has a hard-coded dictionary ("`dict10k.txt`") from which it searches for valid words.


We use an iterative approach that examines valid substrings from 0->i, for all i <=n, and save their validity in a truths table. For each valid substring, we check to see if we can make a substring between that substring and another valid substring.


We use a command line input with a text file containing the phrases we want to split, formatted as:

`>> python3 wordbreak.py file.txt`

Where our final looks like:


`number of phrases`
`phrase 1`
`phrase 2`
`...`
`phrase n`

And output whether or not we can word break each string, printing the break if we can.
