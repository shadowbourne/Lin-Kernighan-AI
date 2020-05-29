import os
import sys
import time
import random
import copy
import heapq
if __name__ != "__main__":
    import concurrent.futures

def read_file_into_string(input_file, from_ord, to_ord):
    # take a file "input_file", read it character by character, strip away all unwanted
    # characters with ord < "from_ord" and ord > "to_ord" and return the concatenation
    # of the file as the string "output_string"
    the_file = open(input_file,'r')
    current_char = the_file.read(1)
    output_string = ""
    while current_char != "":
        if ord(current_char) >= from_ord and ord(current_char) <= to_ord:
            output_string = output_string + current_char
        current_char = the_file.read(1)
    the_file.close()
    return output_string

def stripped_string_to_int(a_string):
    # take a string "a_string" and strip away all non-numeric characters to obtain the string
    # "stripped_string" which is then converted to an integer with this integer returned
    a_string_length = len(a_string)
    stripped_string = "0"
    if a_string_length != 0:
        for i in range(0,a_string_length):
            if ord(a_string[i]) >= 48 and ord(a_string[i]) <= 57:
                stripped_string = stripped_string + a_string[i]
    resulting_int = int(stripped_string)
    return resulting_int

def get_string_between(from_string, to_string, a_string, from_index):
    # look for the first occurrence of "from_string" in "a_string" starting at the index
    # "from_index", and from the end of this occurrence of "from_string", look for the first
    # occurrence of the string "to_string"; set "middle_string" to be the sub-string of "a_string"
    # lying between these two occurrences and "to_index" to be the index immediately after the last
    # character of the occurrence of "to_string" and return both "middle_string" and "to_index"
    middle_string = ""              # "middle_string" and "to_index" play no role in the case of error
    to_index = -1                   # but need to initialized to something as they are returned
    start = a_string.find(from_string,from_index)
    if start == -1:
        flag = "*** error: " + from_string + " doesn't appear"
        #trace_file.write(flag + "\n")
    else:
        start = start + len(from_string)
        end = a_string.find(to_string,start)
        if end == -1:
            flag = "*** error: " + to_string + " doesn't appear"
            #trace_file.write(flag + "\n")
        else:
            middle_string = a_string[start:end]
            to_index = end + len(to_string)
            flag = "good"
    return middle_string,to_index,flag

def string_to_array(a_string, from_index, num_cities):
    # convert the numbers separated by commas in the file-as-a-string "a_string", starting from index "from_index",
    # which should point to the first comma before the first digit, into a two-dimensional array "distances[][]"
    # and return it; note that we have added a comma to "a_string" so as to find the final distance
    # distance_matrix = []
    if from_index >= len(a_string):
        flag = "*** error: the input file doesn't have any city distances"
        #trace_file.write(flag + "\n")
    else:
        row = 0
        column = 1
        row_of_distances = [0]
        flag = "good"
        while flag == "good":
            middle_string, from_index, flag = get_string_between(",", ",", a_string, from_index)
            from_index = from_index - 1         # need to look again for the comma just found
            if flag != "good":
                flag = "*** error: there aren't enough cities"
                # trace_file.write(flag + "\n")
            else:
                distance = stripped_string_to_int(middle_string)
                row_of_distances.append(distance)
                column = column + 1
                if column == num_cities:
                    distance_matrix.append(row_of_distances)
                    row = row + 1
                    if row == num_cities - 1:
                        flag = "finished"
                        row_of_distances = [0]
                        for i in range(0, num_cities - 1):
                            row_of_distances.append(0)
                        distance_matrix.append(row_of_distances)
                    else:
                        row_of_distances = [0]
                        for i in range(0,row):
                            row_of_distances.append(0)
                        column = row + 1
        if flag == "finished":
            flag = "good"
    return flag

def make_distance_matrix_symmetric(num_cities):
    # make the upper triangular matrix "distance_matrix" symmetric;
    # note that there is nothing returned
    for i in range(1,num_cities):
        for j in range(0,i):
            distance_matrix[i][j] = distance_matrix[j][i]

# read input file into string

#######################################################################################################
############ now we read an input file to obtain the number of cities, "num_cities", and a ############
############ symmetric two-dimensional list, "distance_matrix", of city-to-city distances. ############
############ the default input file is given here if none is supplied via a command line   ############
############ execution; it should reside in a folder called "city-files" whether it is     ############
############ supplied internally as the default file or via a command line execution.      ############
############ if your input file does not exist then the program will crash.                ############

input_file = "AISearchfile058.txt"

#######################################################################################################

# you need to worry about the code below until I tell you; that is, do not touch it!

if len(sys.argv) == 1:
    file_string = read_file_into_string("../city-files/" + input_file,44,122)
else:
    input_file = sys.argv[1]
    file_string = read_file_into_string("../city-files/" + input_file,44,122)
file_string = file_string + ","         # we need to add a final comma to find the city distances
                                        # as we look for numbers between commas
if __name__ == '__main__':
    print("I'm working with the file " + input_file + ".")
                                        
# get the name of the file

name_of_file,to_index,flag = get_string_between("NAME=", ",", file_string, 0)

if flag == "good":
    if __name__ == '__main__':
        print("I have successfully read " + input_file + ".")
    # get the number of cities
    num_cities_string,to_index,flag = get_string_between("SIZE=", ",", file_string, to_index)
    num_cities = stripped_string_to_int(num_cities_string)
else:
    print("***** ERROR: something went wrong when reading " + input_file + ".")
if flag == "good":
    if __name__ == '__main__':
        print("There are " + str(num_cities) + " cities.")
    # convert the list of distances into a 2-D array
    distance_matrix = []
    to_index = to_index - 1             # ensure "to_index" points to the comma before the first digit
    flag = string_to_array(file_string, to_index, num_cities)
if flag == "good":
    # if the conversion went well then make the distance matrix symmetric
    make_distance_matrix_symmetric(num_cities)
    if __name__ == '__main__':
        print("I have successfully built a symmetric two-dimensional array of city distances.")
else:
    print("***** ERROR: something went wrong when building the two-dimensional array of city distances.")

#######################################################################################################
############ end of code to build the distance matrix from the input file: so now you have ############
############ the two-dimensional "num_cities" x "num_cities" symmetric distance matrix     ############
############ "distance_matrix[][]" where "num_cities" is the number of cities              ############
#######################################################################################################

# now you need to supply some parameters ...

#######################################################################################################
############ YOU NEED TO INCLUDE THE FOLLOWING PARAMETERS:                                 ############
############ "my_user_name" = your user-name, e.g., mine is dcs0ias                        ############

my_user_name = "xzts63"

############ "my_first_name" = your first name, e.g., mine is Iain                         ############

my_first_name = "Max"

############ "my_last_name" = your last name, e.g., mine is Stewart                        ############

my_last_name = "Woolterton"

############ "alg_code" = the two-digit code that tells me which algorithm you have        ############
############ implemented (see the assignment pdf), where the codes are:                    ############
############    BF = brute-force search                                                    ############
############    BG = basic greedy search                                                   ############
############    BS = best_first search without heuristic data                              ############
############    ID = iterative deepening search                                            ############
############    BH = best_first search with heuristic data                                 ############
############    AS = A* search                                                             ############
############    HC = hilling climbing search                                               ############
############    SA = simulated annealing search                                            ############
############    GA = genetic algorithm                                                     ############

alg_code = "LK"

############ you can also add a note that will be added to the end of the output file if   ############
############ you like, e.g., "in my basic greedy search, I broke ties by always visiting   ############
############ the first nearest city found" or leave it empty if you wish                   ############

added_note = ""

############ the line below sets up a dictionary of codes and search names (you need do    ############
############ nothing unless you implement an alternative algorithm and I give you a code   ############
############ for it when you can add the code and the algorithm to the dictionary)         ############

codes_and_names = {'BF' : 'brute-force search',
                   'BG' : 'basic greedy search',
                   'BS' : 'best_first search without heuristic data',
                   'ID' : 'iterative deepening search',
                   'BH' : 'best_first search with heuristic data',
                   'AS' : 'A* search',
                   'HC' : 'hilling climbing search',
                   'SA' : 'simulated annealing search',
                   'GA' : 'genetic algorithm',
                   'LK' : 'Lin-Kernighan'}

#######################################################################################################
############    now the code for your algorithm should begin                               ############
#######################################################################################################

#USER DEFINED VARIABLES
#time to which to run algorithm for
TIMEOUT = 105
#number of processes to launch, set to 0 to disable multiprocessing if your system does not support it
NO_OF_CORES = 4
#M closest cities to inspect for each yi
M = 5
#BEGINNING OF ALGORITHM FUNCTIONS
def length_of_edge(p):
    z = list(p)
    return distance_matrix[z[0]][z[1]]

def make_valid_tour(tour, tour_edges, X, Y):
    if len(Y) - len(X) != 0:
        return [], False
    tour_edges_new = copy.deepcopy(tour_edges)
    for i in range(len(X)):
        Xii = list(X[i])
        tour_edges_new[Xii[0]].remove(Xii[1])
        tour_edges_new[Xii[1]].remove(Xii[0])
        Yii = list(Y[i])
        tour_edges_new[Yii[0]].add(Yii[1])
        tour_edges_new[Yii[1]].add(Yii[0])
    for i in tour_edges_new:
        if len(tour_edges_new[i]) != 2:
            return [], False
    new_tour = ['banana', 0]
    i = list(tour_edges_new[0])[0]
    new_tour += [i]
    for foo in range(num_cities-1):
        node_connections = list(tour_edges_new[i])
        for j in [0,1]:
            if node_connections[j] != new_tour[-2]:
                new_tour += [node_connections[j]]
                if node_connections[j] == new_tour[1]:
                    new_tour.pop(0)
                    if len(new_tour) == num_cities+1:
                        return [new_tour, tour_edges_new], True
                    else:
                        return [], False
                i = node_connections[j]
                break
    print('Error')
    sys.exit()

    
def find_edge_to_remove(tour, tour_edges, delta, broken_edges, created_edges, initial_node, latest_node, closest_cities):
    j = tour.index(latest_node)
    neighboursj = list(neighbours(j, tour))
    if distance_matrix[neighboursj[0]][latest_node] > distance_matrix[neighboursj[1]][latest_node]:
        potential_x = [neighboursj[0], neighboursj[1]]
    else:
        potential_x = [neighboursj[1], neighboursj[0]]
    for t in potential_x:
        xi = {latest_node, t}
        if xi not in created_edges and xi not in broken_edges and t != initial_node:
            Xi = broken_edges[:]
            Xi += [xi]
            reconnecting_edge = {t, initial_node}
            tempY = created_edges[:]
            tempY += [reconnecting_edge]
            new_tour_object, result = make_valid_tour(tour, tour_edges, Xi, tempY)
            if result == True:
                temp_delta = delta - length_of_edge(xi)
                if temp_delta + length_of_edge(reconnecting_edge) < 0:
                    # print(temp_delta + length_of_edge(reconnecting_edge))
                    return True, new_tour_object[0], new_tour_object[1]
                else:
                    return find_edge_to_add(tour, tour_edges, temp_delta, Xi, created_edges, initial_node, t, closest_cities)
    return False, [], {}

def find_edge_to_add(tour, tour_edges, delta, broken_edges, created_edges, initial_node, latest_node, closest_cities):
    for t in closest_cities[latest_node]:
        if t not in neighbours(latest_node, tour):
            yi = {latest_node, t}
            # print(yi)
            temp_delta = delta + length_of_edge(yi)
            if yi not in broken_edges and temp_delta < 0:
                tempY = created_edges[:]
                tempY += [yi]
                return find_edge_to_remove(tour, tour_edges, temp_delta, broken_edges, tempY, initial_node, t, closest_cities)
    return False, [], {}

def neighbours(i, tour):
    if i > 0 and i < num_cities:
        return {tour[i-1], tour[i+1]}
    else:
        return {tour[1], tour[-2]}

def apply_LK(tour, tour_edges, tour_set, closest_cities):
    for i in range(num_cities):
        t1 = tour[i]
        for t2 in neighbours(i,tour):
            x1 = {t1, t2}
            X = [x1]
            for j in tour_set.difference(set(x1)):
                t3 = j
                y1 = {t2, t3}
                delta1 = length_of_edge(y1) - length_of_edge(x1)
                Y = [y1]

                if delta1 < 0:
                    result = find_edge_to_remove(tour, tour_edges, delta1, X, Y, t1, t3, closest_cities)
                    if result[0]:
                        return result
    return False, tour, {}

def LIN_KERNIGHAN(X):
    start = X[0]
    TIMEOUT = X[1]
    M = X[2]
    heap = []
    template_closest_cities = [None] * num_cities
    closest_cities = []
    for i in range(num_cities):
        closest_cities.append([])
        i_dist = distance_matrix[i]
        for j in list(range(0,i))+list(range(i+1,num_cities)):
            heapq.heappush(heap, [i_dist[j], j])
        template_closest_cities[i] = heapq.nsmallest(M,heap)
        heap = []
    for i in range(num_cities):
        for j in range(M):
            closest_cities[i].append(template_closest_cities[i][j][1])
    # make random greedy tour
    min_tour = [random.randint(0,num_cities-1)]
    cities = list(range(min_tour[0])) + list(range(min_tour[0] + 1, num_cities))
    while len(min_tour)<num_cities:
        greedy_distance = distance_matrix[min_tour[-1]]
        min_length = greedy_distance[cities[0]]
        min_city = cities[0]
        min_city_i = 0
        for i in range(1,len(cities)):
            if greedy_distance[cities[i]] < min_length:
                min_length = greedy_distance[cities[i]]
                min_city_i = i
        min_tour.append(cities[min_city_i])
        cities.pop(min_city_i)
    min_tour += [min_tour[0]]
    tour = min_tour[:]
    tour_set = set(tour)
    min_tour_length = 0
    for i in range(len(min_tour)-1):
        min_tour_length += distance_matrix[min_tour[i]][min_tour[i+1]]
    while time.time() - start < TIMEOUT:
        tour_edges = {}
        for i in range(1, num_cities):
            tour_edges[tour[i]] = {tour[i+1], tour[i-1]}
        tour_edges[tour[0]] = {tour[1], tour[-2]}
        success = True
        while success and time.time() - start < TIMEOUT:
            success, tour, tour_edges = apply_LK(tour, tour_edges, tour_set, closest_cities)
        temp_tour_length = 0
        for i in range(num_cities):
            temp_tour_length += distance_matrix[tour[i]][tour[i+1]]
        if temp_tour_length < min_tour_length:
            min_tour_length = temp_tour_length
            min_tour = tour[:]
        tour.pop(-1)
        random.shuffle(tour)
        tour += [tour[0]]
    min_tour.pop(-1)
    return [min_tour_length, min_tour]

def main(TIMEOUT, NO_OF_CORES, M):
    start= time.time()
    final_tour = list(range(num_cities))
    final_tour += [final_tour[0]]
    final_tour_length = 0
    for i in range(len(final_tour)-1):
                final_tour_length += distance_matrix[final_tour[i]][final_tour[i+1]]
    tour_object = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=NO_OF_CORES) as executor:
        multicore_tour_objects = executor.map(LIN_KERNIGHAN, [[time.time(), TIMEOUT, M]]*NO_OF_CORES)
        for tour_object in multicore_tour_objects:
            if tour_object[0] < final_tour_length:
                final_tour_length = tour_object[0]
                final_tour = tour_object[1][:]
    return final_tour, final_tour_length

if NO_OF_CORES == 0:
    tour_length, tour = LIN_KERNIGHAN([time.time(), TIMEOUT, M])
if __name__ == '__main__':
    if NO_OF_CORES != 0:
        import concurrent.futures
        tour, tour_length = main(TIMEOUT, NO_OF_CORES, M)
        

    #######################################################################################################
    ############ the code for your algorithm should now be complete and you should have        ############
    ############ computed a tour held in the list "tour" of length "tour_length"               ############
    #######################################################################################################

    # you do not need to worry about the code below; that is, do not touch it

    #######################################################################################################
    ############ start of code to verify that the constructed tour and its length are valid    ############
    #######################################################################################################

    check_tour_length = 0
    for i in range(0,num_cities-1):
        check_tour_length = check_tour_length + distance_matrix[tour[i]][tour[i+1]]
    check_tour_length = check_tour_length + distance_matrix[tour[num_cities-1]][tour[0]]
    flag = "good"
    if tour_length != check_tour_length:
        flag = "bad"
    if flag == "good":
        print("Great! Your tour-length of " + str(tour_length) + " from your " + codes_and_names[alg_code] + " is valid!")
    else:
        print("***** ERROR: Your claimed tour-length of " + str(tour_length) + "is different from the true tour length of " + str(check_tour_length) + ".")

    #######################################################################################################
    ############ start of code to write a valid tour to a text (.txt) file of the correct      ############
    ############ format; if your tour is not valid then you get an error message on the        ############
    ############ standard output and the tour is not written to a file                         ############
    ############                                                                               ############
    ############ the name of file is "my_user_name" + mon-dat-hr-min-sec (11 characters);      ############
    ############ for example, dcs0iasSep22105857.txt; if dcs0iasSep22105857.txt already exists ############
    ############ then it is overwritten                                                        ############
    #######################################################################################################

    if flag == "good":
        local_time = time.asctime(time.localtime(time.time()))   # return 24-character string in form "Tue Jan 13 10:17:09 2009"
        output_file_time = local_time[4:7] + local_time[8:10] + local_time[11:13] + local_time[14:16] + local_time[17:19]
                                                                # output_file_time = mon + day + hour + min + sec (11 characters)
        output_file_name = my_user_name + output_file_time + ".txt"
        f = open(output_file_name,'w')
        f.write("USER = " + my_user_name + " (" + my_first_name + " " + my_last_name + ")\n")
        f.write("ALGORITHM = " + alg_code + ", FILENAME = " + name_of_file + "\n")
        f.write("NUMBER OF CITIES = " + str(num_cities) + ", TOUR LENGTH = " + str(tour_length) + "\n")
        f.write(str(tour[0]))
        for i in range(1,num_cities):
            f.write("," + str(tour[i]))
        if added_note != "":
            f.write("\nNOTE = " + added_note)
        f.close()
        print("I have successfully written the tour to the output file " + output_file_name + ".")
        
        











    


