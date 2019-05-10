import re


def d_paths(dictionary, keys=None, key=None):
    '''
    Input:
        dictionary: Input Dictionary/ JSON file
        keys: List Optional
        key: List Optional
    Output:
        List of all the paths separated by "/" within the dictionary
    Description:
        Recursive function to drill down dictionary to get the underlying file paths
    '''

    if keys is None:
        keys = []
    if key is None:
        key = []
    if isinstance(dictionary, dict):
        for i in dictionary.keys():
            key.append([i, dictionary])
            if isinstance(dictionary[i], dict):
                d_paths(dictionary[i], keys, key)
            elif isinstance(dictionary[i], list):
                for number, item in enumerate(dictionary[i]):
                    key.append([str(number), dictionary[i][number]])
                    d_paths(dictionary[i][number], keys, key)
                    key.pop()
            else:
                keys.append("/".join([i for i, j in key]))
            key.pop()
    else:
        keys.append("/".join([i for i, j in key]))
    return keys


def d_findall(dictionary, regex_key):
    '''
    Input:
        dictionary: Dictionary
        regex_key: String.  Regex pattern to look within paths generated using "/" within the dictionary
    Output:
        dictionary of all the paths that satisfies the regex statement and associated output of the path
    Description:
        Output a dictionary which shows all the unique paths and their associated values
    '''
    paths = d_paths(dictionary)
    output = {}
    reg = re.compile(regex_key)
    for path in paths:
        regex = re.search(reg, path)
        if regex:
            temp = dictionary
            reference = "".join(path)
            for i in reference.split("/"):
                try:
                    temp = temp[int(i)]
                except ValueError:
                    temp = temp[i]
            output[reference] = temp
    return output


def d_find(dictionary, path):
    '''
    Input:
        dictionary: Dictionary
        path: String exact path separated by "/" and list within dictionary are differentiated by numerics
    Output:
        Exact value that the path leads to within the dictionary
    Description:
        Allows one to easily access data within a dict of dict if they know the path to it
    '''
    output = dictionary
    print_string = []
    all_paths = d_paths(dictionary)
    for key in path.split("/"):
        try:
            output = output[int(key)]
        except ValueError:
            try:
                output = output[key]
            except KeyError:
                print("{} within {} is not found in dictionary".format(key, path))
                print("Returning {}".format("/".join(print_string)))
                return output
        print_string.append(key)
    return output
