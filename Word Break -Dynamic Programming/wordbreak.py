'''
Dynamic programming approach to the word break problem

Authors: Christopher Jens Johnson

Command-line program that opens a file of phrases, such as "thisphrasecanbesplit", or "thisphrasecannotbesplittt", and uses an iterative
dynamic programming approach to determine if strings can be split or not, from the bottom up. To do so, it maintains a truths table and
list of legal words to use for back-tracking.
'''

import fileinput

dictionary = set()

def open_dict():
    '''Open dictionary file (hard-coded) and add items to dictionary set'''
    dictionary_file = open("diction10k.txt", "r")
    for line in dictionary_file:
        dictionary.add(line.strip().split()[0])
    dictionary_file.close()

def word_lookup(word):
    '''Called by word split method to determine if a word'''
    if word in dictionary:
        return True
    return False


def iterative_split(string):

    length = len(string)

    
    truths = [False for i in range(length)]   # Our DP solution: truths[i] memorizes where or not the string can be split up to index i
    words = ['' for i in range(length)]    # A container that will hold the words that create the optimal solution


    # First, check all valid partitions from index 0->i (for example, in 'programmingisfun', 'program' and 'programmming' would both be valid
    # partitions), if a partition is valid, then we set the endex of its leftmost character to True (as we know we can split the string up to
    # this point). We also memorize the bucket for that index as the word that granted us said partition.
    for i in range(length):
        if word_lookup(string[:i+1]):
            truths[i] = True
            words[i] = string[:i+1]

        # If we know that a string is splittable up to index i, we next check all indices j (i+1 <= j <= length), to determine if we can
        # make a word between i and j. If we can, we set j's truth value to True, as we can make a partition using partitions up to i and
        # the partition between i and j. We also use the same DP memorization and save the string in words[j]
        if truths[i]:
            for j in range(i+1, length):
                if (truths[j] == False and word_lookup(string[i+1:j+1])):
                    truths[j] = True
                    words[j] = string[i+1:j+1]

    return_string = ''
    
    if truths[-1]:
        # Backtracking: Once we have determined that a string is splittable, we need to backtrack and list all of the words that granted us
        # this partition. If an index i is splittable (i.e. truths[i]), we know that we have also saved the word between that partition and
        # all other partitions, so we can trace back through our indices in a reverse manner and concatenate a string (or list in this case)
        # of all of the words of the most recent partition, reverse that string (or list), and then print it
        index = len(words)-1
        print_list = []
        while index > 0:
            print_list.insert(0, words[index])
            index -= len(words[index])
        return_string = " ".join(print_list)

    
    # We return truths of [-1], as we can determine if a string is splittable if its nth index is splittable (we have solved the whole problem)
    return truths[-1], return_string.strip()
  
    
    
def main():
    # Set up dictionary, diction10k.txt, and parse input file (standard input)
    open_dict()
    with fileinput.input() as file:
        
        # Opening file, read how many phrases there are (num_phrases), and read each phrase into string
        num_phrases = int(file.readline().strip().split()[0])
        for phrase in range(num_phrases):
            string = file.readline().strip()
            iterative_bool, iterative_string = iterative_split(string)
            print("phrase number:", phrase+1)
            print(string, "\n")
            print("iterative attempt:")
            if iterative_bool:
                print("YES, can be split")
                print(iterative_string)
            else:
                print("NO, cannot be split")
            print("\n\n")
            



if __name__ == "__main__":
    main()
