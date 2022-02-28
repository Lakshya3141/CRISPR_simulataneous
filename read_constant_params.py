def read_const_p():

    with open("constant_params.txt", "r") as f:
        lines = f.readlines()

    # save params to a dictionary
    const_params = {}
    for line in lines:
        temp = line.strip("\n").split(" ")
        const_params[temp[0]] = eval(temp[2]) 

    return const_params

if __name__ == "__main__":
    print(read_const_p())

