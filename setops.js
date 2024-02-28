//helper function to get list length
const l_length = (l) => !l.length ? 0 : 1 + l_length(l.slice(1));

//recursive merge sort function
const merge_sort = (l) => {
    //base case
    if (l_length(l) <= 1) {
        return l;
    }
    //merge two sorted lists
    return merge(merge_sort(l.slice(0, l_length(l) / 2)), merge_sort(l.slice(l_length(l) / 2)));
};

//helper merge function, using loops not recursion
const merge = (l1, l2) => {
    const result = [];
    let i = 0;
    let j = 0;
    while (i < l_length(l1) && j < l_length(l2)) {
        if (l1[i] <= l2[j]) {
            result.push(l1[i]);
            i++;
            continue;
        }
        result.push(l2[j]);
        j++;
    }

    while (i < l_length(l1)) {
        result.push(l1[i]);
        i++;
    }

    while (j < l_length(l2)) {
        result.push(l2[j]);
        j++;
    }

    return result;
};

//recursive binary search
//assumes a sorted list
const binary_search = (x, l, start, end) => {
    //base
    if (end >= start) {
        const mid = Math.floor((start + end) / 2);

        //return true if value is found
        if (l[mid] === x) {
            return true;
        }
        //if not, recursive search based on whether the desired value is larger or smaller
        else if (l[mid] > x) {
            return binary_search(x, l, start, end - 1);
        } else {
            return binary_search(x, l, mid + 1, end);
        }
    } else {
        //return false if not found in lists
        return false;
    }
};

//recursive function to make all characters in a string lowercase
//uses ascii codes
const recursive_lowercase = (str) => {
    if (str === "") {
        return str;
    } else if ('A' <= str[0] && str[0] <= 'Z') {
        return String.fromCharCode(str.charCodeAt(0) + 32) + recursive_lowercase(str.slice(1));
    } else {
        return str[0] + recursive_lowercase(str.slice(1));
    }
};

//list of delimiters and numbers used to parse input
const delim = ["", " ", ",", ".", "<", ">", "/", "?",
    ";", ":", "'", "\"", "{", "}", "[",
    "]", "\\", "|", "`", "~", "!", "@",
    "#", "$", "%", "^", "&", "*", "(",
    ")", "+", "=", "-", "_", "\n", "\t"];
const nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];

//recursively parse the input
const parse = (str, cur, res) => {
    //base
    if (str === "") {
        //if there's currently a word, eof has been reached
        if (l_length(cur) > 0) {
            res.push(cur);
        }
        return res;
    }

    //check if there is at least one character in the current word
    if (l_length(cur) > 0) {

        //case 1: current character is a-z
        //no delimiter can be accepted into word
        if (!nums.includes(cur.slice(-1)) && !delim.includes(cur.slice(-1))) {

            //if the head of the input is another alphabetic char, word continues
            if (!nums.includes(str[0]) && !delim.includes(str[0])) {
                cur += str[0];
                return parse(str.slice(1), cur, res);
            }

            //if the head of the input is delimiter, the word has ended
            if (delim.includes(str[0])) {
                //add it to the list and start fresh
                res.push(cur);
                return parse(str.slice(1), "", res);
            }

            //if the head of the input is a number, the word has ended
            //but, a new word with the number has begun
            if (nums.includes(str[0])) {
                res.push(cur);
                return parse(str.slice(1), str[0], res);
            }

        }

        //case 2: current character is 0-9
        else if (nums.includes(cur.slice(-1))) {

            //if the head of the input is a number, word continues
            if (nums.includes(str[0])) {
                cur += str[0];
                return parse(str.slice(1), cur, res);
            }

            //if the head of the input is a ".", AND there is not
            //already a decimal in the current word, word becomes decimal
            if (str[0] === "." && !cur.includes(".")) {
                cur += str[0];
                return parse(str.slice(1), cur, res);
            }

            //if the head is ".", but there is already a decimal,
            //word has ended
            if (str[0] === "." && cur.includes(".")) {
                res.push(cur);
                return parse(str.slice(1), "", res);
            }

            //if the head is alphabetical, word is over but new one begins
            if (!delim.includes(str[0]) && !nums.includes(str[0])) {
                res.push(cur);
                return parse(str.slice(1), str[0], res);
            }

            //any other delimiter, word has ended
            if (delim.includes(str[0]) && str[0] !== ".") {
                res.push(cur);
                return parse(str.slice(1), "", res);
            }

        }

        //case 3: current character in word is a decimal point
        else if (cur.slice(-1) === "." && nums.includes(cur[cur.length - 2])) {

            //if head is number, continue decimal:
            if (nums.includes(str[0])) {
                cur += str[0];
                return parse(str.slice(1), cur, res);
            }

            //if head is alphabetical, the current word should have
            //its decimal removed, added to the result list, then a new
            //word should begin with the head
            if (!nums.includes(str[0]) && !delim.includes(str[0])) {
                res.push(cur.slice(0, -1));
                return parse(str.slice(1), str[0], res);
            }

            //if the head is another delimiter, current word should have its
            // decimal removed, added, then start new word
            if (delim.includes(str[0])) {
                res.push(cur.slice(0, -1));
                return parse(str.slice(1), "", res);
            }

        }

    }

    //otherwise, the current word is empty
    else {
        //Check if the char at the head of the input is valid
        if (!delim.includes(str[0])) {
            //add it if so, then make a recursive call with the new word
            cur += str[0];
            return parse(str.slice(1), cur, res);
        } else {
            //otherwise, just move on to the next char in the input string
            return parse(str.slice(1), cur, res);
        }
    }
};

const main = () => {

    //some simple functions to help
    const l_head = (l) => l[0];
    const l_last = (l) => l[l.length - 1];
    const l_join = (l) => l.reduce((x, y) => x + y, "");

    //lambda function to be used in set operations
    const l_removedup = (l) => [...new Set(l)];

    //lambda functions to be used in set operations
    const l_union = (l1, l2) => l_removedup([...l1, ...l2]);
    const l_intersection = (l1, l2) => l2.filter(x => l1.includes(x));
    const l_difference = (l1, l2) => l1.filter(x => !l2.includes(x));

    let a_set, b_set, operation, fs;

    //getting command line arguments
    try {
        if (process.argv.length < 3 || process.argv[2].length === 0) {
            throw new Error("A string containing the two files and operations should be passed. Ex. 'set1=a.txt;set2=b.txt;operation=union'");
        }

        //parse thru argument using built-in function
        const args = process.argv[2].split(";");
        const f1 = args[0].split("=")[1];
        const f2 = args[1].split("=")[1];
        operation = args[2].split("=")[1];

        if (!f1 || !f2 || !operation) {
            throw new Error("Invalid argument. Ex. 'set1=a.txt;set2=b.txt;operation=union'");
        }

        //read files, remove dups, parse and sort into lists
        fs = require('fs');
        const a_content = fs.readFileSync(f1, 'utf8');
        const b_content = fs.readFileSync(f2, 'utf8');

        a_set = merge_sort(l_removedup(parse(recursive_lowercase(a_content), "", [])));
        b_set = merge_sort(l_removedup(parse(recursive_lowercase(b_content), "", [])));

    } catch (e) {
        console.log(`${e}`);
        process.exit(1);
    }

    //perform operation
    let result;
    if (operation === "union") {
        result = merge_sort(l_union(a_set, b_set));
    } else if (operation === "intersection") {
        result = merge_sort(l_intersection(a_set, b_set));
    } else if (operation === "difference") {
        result = merge_sort(l_difference(a_set, b_set));
    } else {
        console.log("Invalid operation. Use 'union', 'intersection', or 'difference'");
        process.exit(1);
    }

    //write to output file
    const result_content = result.join("\n");
    fs.writeFileSync("result.txt", result_content);
  
};

if (require.main === module) {
    main();
}