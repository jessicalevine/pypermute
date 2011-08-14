from sys import exit

def menu():
    """Offers the user main menu choices"""
    while(True):
        print "Type 'perm' or press enter to create a permutation or type 'exit' to exit the program"

        choice = raw_input()

        if choice == "exit":
            exit(0)
        elif (choice == "") | (choice == "perm"):
            std()
        else:
            print "\nPlease enter a valid choice\n"



def std():
    """Provide the standard interactive interface for permutation creation.

    Guides the user through a step by step permutation creation, calls 
    permutation calculator and returns permutations. Also handles file output.
    """
    #Inputs all user choices and options
    draws = int (raw_input("\nSize of Set: "))
    rangeMax = int (raw_input("Value Range of Numbers (1-?): "))

    incAll = (raw_input("\nPrint all results and analysis? (no for individual selection) (y/n): "))
    if incAll == "n":
        incPerms = raw_input("Print Permuations? (y/n): ") == "y"
        incPermCount = raw_input("Print Number of Permutations? (y/n): ") == "y"
        incFreqGraph = raw_input("Print Sum Frequency Graph? (y/n): ") == "y"
    else:
        incPerms = True
        incPermCount = True
        incFreqGraph = True

    outputToFile = raw_input("\nOutput results to file? (s for previously selected data only) (y/s/n): ")
    if (outputToFile == "y") | (outputToFile == "s"):
        filename = raw_input("Enter the filename: ")

    outputR = raw_input("\nOutput sum distribution as R data? (R is a statistics application) (y/n): ") == "y"
    if outputR:
        rFilename = raw_input("Enter the R data filename: ")   

    #Calculate permutations
    perms = calculate_permutations(draws, rangeMax)

    #Prepare and print standard output
    disp = format_output(perms, draws, rangeMax, incPerms, incPermCount, incFreqGraph)
    print disp

    #Output permutations to file
    if (outputToFile == "y") | (outputToFile == "s"):
        output_to_file(perms, draws, rangeMax, outputToFile, filename, disp)
        print "Successfully output data to " + filename + "\n"

    #Output data in a format R can understand
    if outputR:
        output_r_data(perms, rFilename)
        print "Successfully output R data to " + rFilename
        print "Set R to 'Input column names as first row'"
        print "R will input the distribution as a single varible, Sums"
        print "A histogram of Sums will return a relevant graph\n"

    #Wait for user response
    cont = raw_input("Enter to continue...\n")
 


def calculate_permutations(draws, rangeMax):
    """Calculate all permutations of set size "draws" and number range 1-rangeMax.

    This function calculates all permutations of a number of numerical draws,
    given a range from 1 to n. The first parameter is the number of draws, 
    while the second is the max value of a single draw (n). It returns
    the permutations as a list.
    """
    perms = []
    #Form an initial array 1-rangeMax
    for i in xrange (1, rangeMax + 1):
        perms.append([i])
    
    for i in xrange (1, draws):
        perms = step_permute(perms, rangeMax)
    return perms


def step_permute(perms, rangeMax):
    """Perform one exponential step of a permutation.

    This function works by, on each method call, adding one digit of each 
    possible value to each existing permutation. When this is performed 
    draws number of times, all permutations are created.
    """
    newPerms = []
    for perm in perms:
        newPerms.extend(permute_combination(perm, rangeMax))
    return newPerms

def permute_combination(perm, rangeMax):
    """Add rangeMax new permutations from an existing permutation.  

    This function takes one existing permutation, and returns a list of
    new permutations each with another digit of each possible digit value.
    """
    perms = []
    for i in xrange (1, rangeMax + 1):
        perms.append(perm + [i])
    return perms


def calculate_sum_frequencies_dist(perms):
    """Create a FrequencyDistribution to count frequency of each sum across the permutations."""
    dist = FrequencyDistribution()
    for perm in perms:
        dist.add(sum(perm))
    return dist

def output_to_file(perms, draws, rangeMax, choice, filename, selective_output):
    """Output selected permutations to file in the selected format."""
    output = open(filename, "w")
    output.write("+---pypermute by Jordan Goldstein---+\n")
    output.write("Given: " + str(draws) + " numbers each having a value 1-" + str(rangeMax) + "\n")

    if choice == "y":
        output.write(format_output(perms, draws, rangeMax, True, True, True))
    elif choice == "s":
        output.write(selective_output)
    output.close()

def output_r_data(perms, filename):
    """Output a given set of permutations' sums in a format R can understand."""
    output = open(filename, "w")
    output.write("Sums\n")

    for perm in perms:
        output.write(str(sum(perm)) + "\n")

    output.close()
        

def format_output(perms, draws, rangeMax, incPerms, incPermCount, incFreqGraph):
    """Format output of a set of permutations based on three booleans."""
    output = ""
    if incPerms:
        for perm in perms:
            output += str(perm) +"\n"
        output += "\n"

    permNum = str(len(perms))
    expectedPermNum = str(pow(rangeMax, draws)) 
    numMsg = " permutations, where the expected number of permutations is "
    valid = permNum + numMsg + expectedPermNum

    if incPermCount:
        output += valid + "\n\n"

    if incFreqGraph:
        output += "Sum Frequency Distribution:\n\n"
        output += (calculate_sum_frequencies_dist(perms)).graph() + "\n"

    return output
        

class FrequencyDistribution:
    """Provide an easy way to calculate frequencies of a distribution of numbers.
    
    FrequencyDistribution leverages a simple dictionary/associative array
    to perform its function, but provides an easy interface for
    updating frequencies and outputting a graph.
    """
    
      
    def __init__(self):
        self.dist = { }

    def __str__(self):
       return str(self.dist)

    #Adds a new value to the distribution or updates its frequency
    def add(self, value): 
        if value in self.dist.keys():
            freq = self.dist[value]
            del self.dist[value]
            self.dist[value] = freq + 1
        else:
            self.dist[value] = 1  

    #Returns an ASCII graph of the frequencies
    def graph(self):
        temp = []

        #Create a list of values for finding the max length of a graph row
        for key in self.dist.keys():
            temp.append(self.dist[key])

        #Calculate the space adjusment (based on max key length) for the sum header
        spaceAdj = len(str(max(self.dist.keys()))) - 1

        #Form the graph header
        graph = "S" + (spaceAdj * " ") + "|Frequency\n"
        graph += "-" * max(temp) + "\n"

        #Add each graph row
        for key in self.dist.keys():
            #Calculate the space adjusment (based on max key length) for each sum key 
            spaceAdjNum = len(str(max(self.dist.keys()))) - len(str(key))
            #Format sum key column of each row
            graph += str(key) + (spaceAdjNum * " ") + "|"
            #Format frequency column of each row
            graph += ("*" * self.dist[key]) + "(" + str(self.dist[key]) + ")\n" 
        
        return graph        
            
if __name__ == "__main__":
    menu()           
    
