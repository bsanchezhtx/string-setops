from functools import *
import sys
sys.setrecursionlimit(10000)

# small function to get the length of a list
l_length = lambda l: 0 if not l else 1 + l_length(l[1:])

# recursive merge sort function
def merge_sort(l):
	# base case
    if l_length(l) <= 1:
        return l
    # merging two sorted lists
    return merge(merge_sort(l[0:l_length(l) // 2]), merge_sort(l[l_length(l) // 2:]))

# helper function to merge lists
# uses loops and indices, we're unable to make it recursive
def merge(l1, l2):
    result = []
    i = 0
    j = 0
    while i < l_length(l1) and j < l_length(l2):
        if l1[i] <= l2[j]:
            result += [l1[i]]
            i += 1
            continue
        result += [l2[j]]
        j += 1

    while i < l_length(l1):
        result += [l1[i]]
        i +=  1
        
    while j < l_length(l2):
        result += [l2[j]]
        j += 1
        
    return result

# recursive binary search, returns true if the value is found, false if it's not
def binary_search(x, l, start, end):
    # base case
    if end >= start:
        mid = (start + end) // 2

        # return true if the value is found
        if l[mid] == x:
            return True
        # otherwise, perform a recursive search based on whether the
        # desire value is larger or smaller
        elif l[mid] > x:
            return binary_search(x, l, start, end - 1)
        else:
            return binary_search(x, l, mid + 1, end)
        
    else:
        # if the value wasn't found in the list, return false
        return False

# recursive function to make all characters in a string lowercase
# uses ascii codes
def recursive_lowercase(str):
    if str == "":
        return str
    elif 'A' <= str[0] <= 'Z':
        return chr(ord(str[0]) + 32) + recursive_lowercase(str[1:])
    else:
        return str[0] + recursive_lowercase(str[1:])
    

# list of delimiters and numbers, will be used to parse input
delim = ["", " ", ",", ".", "<", ">", "/", "?",
                ";", ":", "\'", "\"", "{", "}", "[", 
                "]", "\\", "|", "`", "~", "!", "@", 
                "#", "$", "%", "^", "&", "*", "(", 
                ")", "+", "=", "-", "_"]
nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]   

def parse(str, cur, res):
    # base case
    if not str:
        return res
    
    # check if there is at least one character in the current word
    if l_length(cur) > 0:

        # case 1, current character is a-z
        # no delimiter can be accepted into word
        if cur[-1] not in nums and cur[-1] not in delim:

            # if the head of input is another alphabetic char, word continues
            if str[0] not in nums and str[0] not in delim:
                cur += str[0]
                parse(str[1:], cur, res)

            # if the head of input is delimiter, the word has ended
            if str[0] in delim:
                # add it to list and start fresh
                res += [cur]
                parse(str[1:], "", res)

            # if the head of input is a number, the word has ended
            # but, a new word with the number has begun
            if str[0] in nums:
                res += [cur]
                parse(str[1:], f"{str[0]}", res)

        # case 2, current character is 0-9
        elif cur[-1] in nums:
            
            # if the head of the input is a number, word continues
            if str[0] in nums:
                cur += str[0]
                parse(str[1:], cur, res)

            # if the head of the input is a ".", AND there is not
            # already a decimal in the current word, word becomes decimal
            if str[0] == "." and "." not in cur:
                cur += str[0]
                parse(str[1:], cur, res)
            
            # if the head is ".", but there is already a decimal,
            # word has ended
            if str[0] == "." and "." in cur:
                res += [cur]
                parse(str[1:], "", res)

            # if the head is alphabetical, word is over but new one begins
            if str[0] not in delim and str[0] not in nums:
                res += [cur]
                parse(str[1:], f"{str[0]}", res)

            # any other delimiter, word has ended
            if str[0] in delim and not str[0] == ".":
                res += [cur]
                parse(str[1:], "", res)

        # case 3, current character in word is a decimal point
        elif cur[-1] == "." and cur[-2] in nums:

            # if head is number, continue decimal:
            if str[0] in nums:
                cur += str[0]
                parse(str[1:], cur, res)

            # if head is alphabetical, the current word should have
            # its decimal removed, added to the result list, then a new
            # word should begin with the head
            if str[0] not in nums and str[0] not in delim:
                res += [cur[0:-1]]
                parse(str[1:], f"{str[0]}", res)

            # if the head is another delimiter, current word should have its
            # decimal removed, added, then start new word
            if str[0] in delim:
                res += [cur[0:-1]]
                parse(str[1:], "", res)

    # otherwise, the current word is empty
    else:
        # check if the char at the head of the input is valid
        if str[0] not in delim:
            # add it if so, then make a recursive call with the new word
            cur += str[0]
            parse(str[1:], cur, res)
        else:
            # otherwise, just move on to the next char in the input string
            parse(str[1:], cur, res)

# main function to perform set operations
def main():

    # some simple lambda functions to help
    l_head = lambda l: l[0]
    l_last = lambda l: l[-1]
    l_join = lambda l: reduce(lambda x, y: x + y, l)
    l_removedup = lambda l: list(reduce(lambda x, y: x + [y] if y not in x else x, l, []))

    # lambda functions to be used in set operations
    l_union = lambda l1, l2: l_removedup(l1 + l2)
    l_intersection = lambda l1, l2: list(filter(lambda x: binary_search(x, l1, 0, l_length(l1)), l2))
    l_difference = lambda l1, l2: list(filter(lambda x: x not in l2, l1))

    # getting command line arguments
    try:
        # TODO: use sys.argv[1] when finished
        f1 = "testcases/a1.txt"
        f2 = "testcases/b1.txt"
        operation = "intersection"

        # getting input from files, sorting them, then assigning them to the lists
        # from here, the lists will not be mutated
        with open(f1, "r") as a:
            a_set = None

        with open(f2, "r") as b:
            b_set = None

    except Exception as e:
        print(f"{e}")
        sys.exit(0)

    
    # performing the selected operation
    if operation == "union":
        result = merge_sort(l_union(a_set, b_set))
    elif operation == "intersection":
        result = merge_sort(l_intersection(a_set, b_set))
    elif operation == "difference":
        result = merge_sort(l_difference(a_set, b_set))
    else:
        print("invalid operation")
        sys.exit(0)

    print(result)
    # writing to output file
    with open("result.txt", "w") as r:
        for word in result:
            r.write(f"{word}\n")

if __name__ == "__main__":
    main()