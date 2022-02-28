def read_dynamic_p():

    with open("dynamic_params.txt", "r") as f:
        lines = f.readlines()

    # save params to a dictionary
    dynamic_params = {}
    for line in lines:
        temp = line.strip("\n").split(" ")
        dynamic_params[temp[0]] = eval(temp[2]) 

    return dynamic_params

if __name__ == "__main__":
    print(read_dynamic_p())