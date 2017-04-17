# Name: Matthew Seneque
# Student Number:  10401788

# This file is provided to you as a starting point for the "jokebot.py" program of Assignment 2
# of CSP1150/CSP5110 in Semester 1, 2016.  It aims to give you just enough code to help ensure
# that your program is well structured.  Please use this file as the basis for your assignment work.
# You are not required to reference it.


# Import the required modules.
import json
import random
import tkinter
import tkinter.messagebox


MAX_RATING = 5
DATA_FILE = 'data.txt'


class ProgramGUI:

    def __init__(self):
        # On keypress events
        def keydownReturn(e):
            if e.keysym == 'Return':
                self.rateJoke()

        def keydownNav(e):
            if e.keysym == 'Right':
                self.nextJoke()
            if e.keysym == 'Left':
                self.previousJoke()

        # This is the constructor of the class.
        # It is responsible for loading and reading the data file and creating the user interface.
        self.main = tkinter.Tk()
        self.main.title('Joke Bot')
        self.main.geometry('620x300')
        self.main.resizable(width=True, height=True)
        self.currentJoke = 0

        # Create StringVar to store the current jokes
        self.jokeSetup = tkinter.StringVar()
        self.jokePunchline = tkinter.StringVar()
        self.jokeRatingResults = tkinter.StringVar()

        # Set up the Frame
        self.frm1 = tkinter.Frame(self.main, padx=8, pady=4)

        # Use grid 21 rows, 7 columns to place all form widgets.
        self.jokeSetupLabel = tkinter.Label(self.frm1, textvariable=(self.jokeSetup), font=("Helvetica", 16, "bold"), padx=25, wraplength=500)
        self.jokeSetupLabel.grid(row=0, rowspan=10, column=2, columnspan=5, sticky="n")

        self.jokePunchlineLabel = tkinter.Label(self.frm1, textvariable=self.jokePunchline, font=("Helvetica", 14, "italic"), padx=20, pady=10, wraplength=510, relief="groove")
        self.jokePunchlineLabel.grid(row=11, rowspan=5, column=2, columnspan=5, sticky="n")

        self.goCoral = tkinter.Button(self.frm1, text='Coralify', command=self.coralifyPopup)
        self.goCoral.grid(row=16, column=4, sticky="w")

        self.jokeRatingResultsLabel = tkinter.Label(self.frm1, textvariable=self.jokeRatingResults)
        self.jokeRatingResultsLabel.grid(row=18, column=2, columnspan=5, sticky="s")

        self.yourRatingLabel = tkinter.Label(self.frm1, text='Your Rating:')
        self.yourRatingLabel.grid(row=19, column=3, sticky="e")

        self.yourRatingEntry = tkinter.Entry(self.frm1, width=3)
        self.yourRatingEntry.grid(row=19, column=4, sticky="w")
        self.yourRatingEntry.bind("<KeyPress>", keydownNav)
        self.yourRatingEntry.bind("<Return>", keydownReturn)

        self.yourRatingSubmit = tkinter.Button(self.frm1, text='Submit', command=self.rateJoke)
        self.yourRatingSubmit.grid(row=19, column=4, rowspan=2, sticky="n")

        self.jokePreviousButton = tkinter.Button(self.frm1, text='<<<<\n\n\n\n\n\n\nprev\n\n\n\n\n\n\n<<<<', command=self.previousJoke)
        self.jokePreviousButton.grid(row=0, rowspan=21, column=1, sticky="w")

        self.jokeNextButton = tkinter.Button(self.frm1, text='>>>>\n\n\n\n\n\n\nnext\n\n\n\n\n\n\n>>>>', command=self.nextJoke)
        self.jokeNextButton.grid(row=0, rowspan=21, column=7, sticky="e")

        self.horizontalRuleLabel = tkinter.Label(self.frm1, text="_" * 120)
        self.horizontalRuleLabel.grid(row=21, column=1, columnspan=7)

        # Load the joke data
        self.getData()

        # Show the current joke from the data file.
        self.showJoke()

        # Pack the grid
        self.frm1.grid()

        # Set initial focus on height Entry widget
        self.yourRatingEntry.focus_set()

        tkinter.mainloop()

    def showJoke(self):
        # This method is responsible for displaying a joke in the GUI.
        currentJoke = self.currentJoke
        if len(self.data[currentJoke]['setup']) > 150:
            tkinter.messagebox.showerror('Invalid Length', 'Joke ' + str(currentJoke + 1) + ' setup is too long.\nThe setup must be less than 150 characters in length')
        else:
            self.jokeSetup.set(self.data[currentJoke]['setup'])
            self.jokePunchline.set(self.data[currentJoke]['punchline'])
            numOfRatings = self.data[currentJoke]['numOfRatings']
            try:
                avg = float(self.data[currentJoke]['sumOfRatings']) / self.data[currentJoke]['numOfRatings']
            except:
                avg = 0
            textRated = 'Rated ' + str(numOfRatings) + ' time' + ('. ' if numOfRatings is 1 else 's. ')
            textAverage = 'Average rating is ' + ('0' if float(str('%.1f' % avg)) == 0 else str('%.1f' % avg).rstrip('.0')) + '/' + str(MAX_RATING) + '.'
            self.jokeRatingResults.set(textRated + textAverage)

    def rateJoke(self):
        # This method is responsible for validating and recording the rating that a user gives a joke.
        try:
            if int(self.yourRatingEntry.get()) < 0 or int(self.yourRatingEntry.get()) > 5:
                raise ValueError
            else:
                numOfRatings = self.data[self.currentJoke]['numOfRatings']
                sumOfRatings = self.data[self.currentJoke]['sumOfRatings']
                newSubmitRating = int(self.yourRatingEntry.get())
                numOfRatings += 1
                sumOfRatings += newSubmitRating
                self.data[self.currentJoke]['numOfRatings'] = numOfRatings
                self.data[self.currentJoke]['sumOfRatings'] = sumOfRatings
                self.saveData()
                self.nextJoke()
                if self.isLastJoke is True:
                    if tkinter.messagebox.askyesno("End of list", "You have reached the end of the list\n'Yes' to quit\n'No' to keep voting"):
                        self.main.destroy()
        except ValueError:
            # show error box
            tkinter.messagebox.showerror('Invalid input', 'Enter a number from 0 to ' + str(MAX_RATING))
        except:
            tkinter.messagebox.showerror('Error', 'Something went wrong whilst rating the joke.')

    def nextJoke(self):
        # Display the next joke.
        if self.currentJoke < (len(self.data) - 1):
            self.currentJoke += 1
            self.showJoke()
            self.yourRatingEntry.delete(0, 'end')
            self.isLastJoke = False
        else:
            self.isLastJoke = True

    def previousJoke(self):
        # Display the previous joke.
        if self.currentJoke > 0:
            self.currentJoke -= 1
            self.showJoke()

    def getData(self, dataFileName=DATA_FILE):
        # Attempts to open the joke data from the joke data file in json format. If no file is found the user is notified.
        try:
            f = open(dataFileName, 'r')
            self.data = json.loads(f.read())
            f.close()
        except:
            tkinter.messagebox.showerror('error', '... UNABLE TO LOAD JOKE FILE (' + DATA_FILE + ') ...')
            self.data = [{"punchline": "Or move an existing joke file to this directory.", "numOfRatings": 0, "setup": "Please use the jokebot admin.py program to create some jokes.", "sumOfRatings": 0}]
            self.yourRatingEntry.configure(state='disabled')

    def saveData(self, dataFileName=DATA_FILE):
        # Attempts to save the joke data to the joke data file in json format. If an error occurs the user is notified.
        try:
            f = open(dataFileName, 'w')
            json.dump(self.data, f)
            f.close()
        except:
            tkinter.messagebox.showerror('error', '... UNABLE TO WRITE JOKE TO FILE ...')

    def coralifyPopup(self):
        # create the coralify window
        self.coralify = tkinter.Toplevel()

        self.coralify.title('Coral!!')
        self.coralify.resizable(width=True, height=True)

        # Set the popup window dimensions and parameters.
        self.width = 426
        self.height = 868 / 4
        self.fontName = "Arial"
        self.fontSize = 13
        self.fontColor = ["black", "white"]
        self.fontOffset = [[0, 0], [2, -1]]

        self.w = tkinter.Canvas(self.coralify, width=self.width, height=self.height * 4)
        self.w.pack(fill='x')

        # Loads the image file from the same directory.
        self.image = tkinter.PhotoImage(file='coral-all-images.png')
        self.w.create_image(0, 0, image=self.image, anchor='nw')

        # Frame 1 - Setup
        self.setup = self.data[self.currentJoke]['setup']
        for textLayer in range(2):
            self.w.create_text(self.width - 5 + self.fontOffset[textLayer][0], (self.height / 3) + self.fontOffset[textLayer][1],
                               text=self.setup,
                               font=(self.fontName, self.fontSize, "bold"),
                               fill=self.fontColor[textLayer],
                               anchor="se",
                               justify="right",
                               width=self.width * (7 / 10))

        # Frame 2 - Dad please
        self.dadPlease = ['Dad please ...', 'Dad stop it!']
        for textLayer in range(2):
            self.w.create_text(self.width / 8 + self.fontOffset[textLayer][0], (self.height * 2) - (self.height / 6) + self.fontOffset[textLayer][1],
                               text=random.choice(self.dadPlease),
                               font=(self.fontName, int(self.fontSize * (7 / 10)), "bold"),
                               fill=self.fontColor[textLayer],
                               anchor="nw",
                               justify="left")

        # Frame 3 - Punchline
        self.punchline = self.data[self.currentJoke]['punchline']
        for textLayer in range(2):
            self.w.create_text(self.width - 5 + self.fontOffset[textLayer][0], (self.height * 2) + (self.height / 4) + self.fontOffset[textLayer][1],
                               text=self.punchline,
                               font=(self.fontName, self.fontSize, "bold"),
                               fill=self.fontColor[textLayer],
                               anchor="se",
                               justify="right",
                               width=self.width * (8 / 10))

        # Frame 4 - Coral
        punchList = self.data[self.currentJoke]['punchline'].split(' ')
        punchLen = len(punchList)
        if punchLen > 1:
            self.coral = (punchList[(punchLen - 2)].upper(), punchList[(punchLen - 1)].upper(), 'CORAL!')
        else:
            self.coral = (punchList[(punchLen - 1)].upper(), 'CORAL!')
        for textLayer in range(2):
            self.w.create_text(self.width + self.fontOffset[textLayer][0], self.height * 4 + self.fontOffset[textLayer][1],
                               text=self.coral,
                               font=(self.fontName, int(self.fontSize * (17 / 10)), "bold"),
                               fill=self.fontColor[textLayer],
                               anchor="se",
                               justify="right",
                               width=self.width * (8 / 10))

        tkinter.mainloop()


# Create an object of the ProgramGUI class to begin the program.
progGUI = ProgramGUI()
