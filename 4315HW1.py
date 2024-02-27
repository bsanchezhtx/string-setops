import re

def read_file(file_path) :
    try:
        with open(file_path, 'r') as file:
            content = file.read().lower()
            words = re.findall(r'\w+', content)
            return words
    except FileNotFoundError:
        print(f"File {file_path} not found")
        return []


def union(A, B) :
    if not A:
        return B
    if not B:
        return A
    if A[0] == B[0]:
        return [A[0]] + union(A[1:], B[1:])
    elif A[0] < B[0]:
        return [A[0]] + union(A[1:], B)
    else:
        return [B[0]] + union(A, B[1:])

def intersection(A, B) :
    if not A or not B:
        return []
    if A[0] == B[0]:
        return [A[0]] + intersection (A[1:], B[1:])
    elif A[0] < B[0]:
        return intersection(A[1:], B)
    else:
        return intersection(A, B[1:])

def difference(A, B) :
    if not A:
        return []
    if not B:
        return A
    if A[0] in B:
      return difference(A[1:], B)
    else:
      return [A[0]] + difference(A[1:], B)

def sort(lst) :
  if not lst or len(lst) == 1:
    return lst
  index = lst.index(min(lst))
  return [lst.pop(index)] + sort(lst)

def write_result(result, output_file) :
    words =  list(set(result))
    sort_words = sort(words)
    with open(output_file, 'w') as file:
        if not sort_words:
            file.write("empty set")
        else:
            for word in sort_words:
                file.write(f"{word}\n")


def main() :
    f1 = input("first file: ")
    f2 = input("second file: ")
    operation = input("operation: ")

    A = read_file(f1)
    B = read_file(f2)
    

    if operation == 'union':
        result = union(A, B)
    elif operation == 'intersection':
        result = intersection(A, B)
    elif operation == 'difference':
        result = difference(A, B)
    else:
        print("Invalid operation")
        return

    write_result(result, "result.txt")


if __name__ == "__main__":
    main()