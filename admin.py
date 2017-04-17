# Name: Matthew Seneque
# Student Number: 10401788

# This is the Jokebot admin program. This program alows you to add / remove / view jokes from the json joke data file.


# Import the json module to allow us to read and write data in JSON format.
import json

# This is the the maximum rating that can be given to a joke.
MAX_RATING = 5

# This is the top ratings filter for displaying jokes with averages above TOP_RATINGS.
TOP_RATINGS = 4


# This function repeatedly prompts for input until an integer is entered.
# See Point 1 of the "Functions in admin.py" section of the assignment brief.
# CSP5110 Requirement: Also enforce a minimum value of 1.
# zeroIndex (True) is used to adjust the output to key values to match those
# of a zero indexed list.
#
# inputs: prompt as string
#        zeroIndex as boolean
# outputs: inputValue as integer
def inputInt(prompt, zeroIndex=False):
    while True:
        try:
            inputValue = int(input(prompt))
            if inputValue >= 1:
                return(inputValue - zeroIndex)
        except:
            pass
        print('** Please enter a positive integer **')


# This function repeatedly prompts the user for an input until something is entered
# that is less than 150 characters. Once validated, the input string is returned.
#
# input: prompt as string
# output: inputValue as string
def inputSomething(prompt):
    while True:
        inputValue = input(prompt)
        if len(inputValue.strip()) > 150:
            print("\nInput too long:\nPlease enter less then 150 Characters.\n")
            continue
        elif inputValue.strip() != '':
            return(inputValue.strip())


# This function opens "data.txt" in write mode and writes dataList to it
# in JSON format.
#
# inputs: dataList as list (JSON format)
# outputs: none
def saveChanges(dataList):
    try:
        f = open('data.txt', 'w')
        json.dump(dataList, f)
        f.close()

    except:
        print("... UNABLE TO WRITE JOKE TO FILE ...")


# This function prints the joke list in a numbered order. With a query
# string to filter the list results.
#
# inputs: query as string, default is ''
#         top as boolean, default is False
# output: Prints numbered list to screen, Returns Nothing.
def printList(query='', showTop=False):
    jokeFound = False
    avg = 0
    showAvgRatingsAbove = showTop * TOP_RATINGS
    print('\nList of jokes:')
    if len(data) == 0:
        print('\nPlease add some jokes!!\nThe data file is empty.')
    else:
        for key, item in enumerate(data, start=1):
            if showAvgRatingsAbove > 0:
                try:
                    avg = float(data[key - 1]['sumOfRatings']) / data[key - 1]['numOfRatings']
                except:
                    avg = 0
            # search for query in joke setup and punchline, (that is above the average rating if selected).
            if ((query.lower() in item['setup'].lower()) or (query.lower() in item['punchline'].lower())) & (avg >= showAvgRatingsAbove):
                # Limits the list display of the setup to 50 chars.
                print('\t', key, ') ', item['setup'][:50], sep='', end='')
                print('...') if len(item['setup']) > 50 else print('')
                jokeFound = True

        if jokeFound is False:
            print('\nNo results found')
    print('\n')


# Attempt to open data.txt and read the joke data. If there is no file then an
# empty list is created.
try:
    f = open('data.txt', 'r')
    data = json.loads(f.read())
    f.close()
except:
    data = []
    print("\n** UNABLE TO LOAD JOKE DATA FILE **\n")


print('\nWelcome to the Joke Bot Admin Program.\n')

# Initiates the endless loop until the user enters q for quit.
while True:
    print('Choose [a]dd, [t]op, [l]ist, [s]earch, [v]iew, [d]elete or [q]uit.')
    choice = input('> ').lower().split(' ', 1)

    # Add a new joke.
    if choice[0] == 'a':
        jSetup = inputSomething('Enter joke setup>> ')
        jPunchline = inputSomething('Enter joke punchline>> ')
        newJoke = {"setup": jSetup, "punchline": jPunchline, "numOfRatings": 0, "sumOfRatings": 0}
        data.append(newJoke)
        saveChanges(data)
        print('\n** Joke Saved **\n')

    elif choice[0] == 't':
        printList(showTop=True)

    elif choice[0] == 'l':
        printList()

    elif choice[0] == 's':
        try:
            searchQuery = choice[1]
        except:
            searchQuery = inputSomething('Search >> ')

        printList(query=searchQuery)

    # View a joke.
    elif choice[0] == 'v':
        try:
            n = int(choice[1]) - 1
        except:
            n = inputInt('Enter the index number of the joke to View >>', zeroIndex=True)

        try:
            print('\n\t', data[n]['setup'], '\n\t', data[n]['punchline'], '\n')
            numOfRatings = data[n]['numOfRatings']
            sumOfRatings = float(data[n]['sumOfRatings'])
            if numOfRatings > 0:
                try:
                    avg = sumOfRatings / numOfRatings
                except:
                    avg = 0
                # text example: "Rated 2 times."
                textRated = '\t Rated ' + str(numOfRatings) + ' time' + ('. ' if numOfRatings is 1 else 's. ')
                # text example: "Average rating is 1.2/5"
                textAverage = 'Average rating is ' + ('0' if float(str('%.1f' % avg)) == 0 else str('%.1f' % avg).rstrip('.0')) + '/' + str(MAX_RATING) + '.'
                print(textRated, textAverage, '\n')
            else:
                print('\t ** Joke has not been rated yet **\n')
        except:
            print('Index number does not exist.')

    # Delete a joke
    elif choice[0] == 'd':
        try:
            n = int(choice[1]) - 1
        except:
            n = inputInt('Enter the index number to Delete >> ', zeroIndex=True)

        try:
            del data[n]
            saveChanges(data)
            print('\n** Joke Deleted **\n')
        except:
            print('Index number does not exist.')

    # Quit the program.
    elif choice[0] == 'q':
        print('\nGoodbye!')
        break

    else:
        # Print "invalid choice" message.
        print('\n** invalid choice **\n')
