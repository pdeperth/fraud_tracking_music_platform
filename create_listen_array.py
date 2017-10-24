def create_line(line):
    row = [0]*6
    number = ''
    count = 0
    for char in line:
        if char != ',':
            number = number + char
        elif char == ',':
                number = int(number)
                row[count]= number
                number = ''
                count +=1
        row[count] = number[:-1] # this one is for the ip_address. -1 for the \r at the end of the line.
    return row

def create_listen_array(file_input):
    line = file_input.readline()
    # create an array out of of the listening log file
    listen = np.empty((0,6))
    line_counter = 0
    while line:
        row = [0]*6
        number = ''
        count = 0
        for char in line:
            if char != ',':
                number = number + char
            elif char == ',':
                    number = int(number)
                    row[count]= number
                    number = ''
                    count +=1
            row[count] = number[:-2] # this one is for the ip_address. -2 for the /r and /n at the end of the line.
        listen = np.vstack([listen, row])
        line = file_input.readline()
        line_counter += 1
        if line_counter%1000 == 0:
            print('%s lines put in the array.',line_counter)
    return listen
