# This code was produced by Dr Sam Perry from University of Southampton Department of Chemistry
# I hope you find this code useful! 
# The Github folder contains how to guides on how to edit the code in order to create your own smart worksheet.
# Start with the master code segment, then add in the various types of question that you would like to include to build up the worksheet
# The master document contains a number of built in functions that are able to record student responses, calculate correct answers, record grades and provide feedback.
# There are also separate question codes, that contain sample codes for how to ask certain types of questions based on the desired response. These include:
    # - Submission of a single value without grading
    # - Submission of a single value with grading against a given answer
    # - Submission of a single value with grading against a value calculated by the worksheet
    # - Checkbox answers where student click the box next to the correct answer
    # - Submission of a range of answers within the same question, with grading against given answers
    # - Submission of a range of answers within the same question, with grading values calculated by the worksheet 
    # - Plotting of scatter plots with associated regression analysis
    # - Plotting a line plot with peak finding and integration capabilities
# As you are building your worksheet, copy the relevant question type into the questions section of the master document
# The only areas you need to edit are marked by the ### symbols (only three # in a row. Single # are coding comments designed to assist users interested in the Python code)
# You can therefore use the find function in your code editor to search for ###, and edit the associated sections.
# Edit the sections next to the ### symbol to alter question text, answers, and formualas used to calculate values. The code will do the rest!
# Good luck and enjoy!!  

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import numpy as np 
from matplotlib import pyplot as plt
import statsmodels.api as sm
import os
#from cryptography.fernet import Fernet #Can uncomment if going back to encrypting. No need to import if only hiding the file 
from csv import reader as csv_reader
from subprocess import run as subprocess_run
from subprocess import DEVNULL as subprocess_DEVNULL

class Feedback:
    
    def __init__(self, master):
        
        '''-------- Core variables --------'''
        
        ### These values wil control how the worksheet treats and stores answers
        self.decimals = 3 ### What is the standard number of decimal places that should be used for all answers
        self.sigfig = 3 ### What is the standard number of significant figures that should be used for all answers?
        
        '''-------- Titles and introduction --------'''
        
        ### Add in the text for your introduction, title and subheading into these sections         
        self.introduction_text = "This worksheet forms the assessment and feedback for the Introduction to Electrochemistry practical. Work through the questions below one at a time and hit submit when ready. If your answer is correct, the worksheet will award full marks. If not, a point penalty will be applied and you will receive some feedback on how best to tackle common errors."# \n\n The answers should be completed one at a time in order. Do not skip questions. Some questions will depends on previous answers, and so skipping questions may cause errors to be carried forwards and will lose you marks. \n\n You may take as many attempts as you wish to submit a correct answer. You may also select solve to have the answer given to you. In this case the answer will be revealed and a score of zero awarded for that question. \n\n Be aware that the worksheet is sensitive to the format of your answers, particularly to decimal places and significant figures. To access the highest marks, pay attention to the following: \n\n Unless otherwise stated, all answers should be given to 3 significant figures (3 s.f.). For example, 𝜋 would be reported as 3.14. \n\n For very small numbers, powers may be represented using e-n to mean x10⁻ⁿ, although decimals will be accepted as well. An acceptable decreasing sequence could be 0.1, 0.01, 0.001, 0.0001, 1e-05, 1e-06. Note that the format is 1e-05, not 1e-5 nor 1 e-05. \n\n Numbers that meet multiple of these conditions should follow all rules For example 1.2300004 x 10\u207B\u2075 should be reported to 3 s.f. as 1.23e-05 \n\nAs an extra note, there is a strange querk with the worksheet that sometimes the scrollbar does not let you scroll all the way to the botom. If this happens, maximise, unmaximise, and then maximise the window, and the scrollbar will return to normal."
        self.worksheet_heading = "Introduction to Electrochemistry"
        self.worksheet_subheading = "Smart worksheet and feedback form"
        
        
        
        ''' -------- Dictionary to store a record of penalty attempts -------- '''
        
        self.parameter_dictionary = {}
        self.entry_dictionary = {}
        self.button_dictionary = {}
        self.checkbutton_dictionary = {}
        self.checkbutton_label_dictionary = {}
        self.label_loc_dictionary = {}
        self.question_list = []
        self.plot_button_dictionary = {}

        '''-------- Scroll bar set up  --------'''
        
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(fill=BOTH, expand=1)
        
        self.main_canvas = Canvas(self.main_frame)
        self.main_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=VERTICAL, command=self.main_canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.main_canvas.bind('<Configure>', lambda e: self.main_canvas.configure(scrollregion = self.main_canvas.bbox("all")))
        
        self.useable_frame = ttk.Frame(self.main_canvas)
        
        self.main_canvas.create_window(0,0, window=self.useable_frame, anchor = 'nw')
        
        
        ''' -------- Header for the worksheet -------- '''
        
        # This is a basic frame added to the window. Widgets are put inside. Line 1 creates the frame, line 2 puts it on the window.
        self.frame_header = ttk.Frame(self.useable_frame)
        self.frame_header.pack(expand=True, fill='both')
        
        #This is for adding a logo. Line 1 loads the image and gives it a variable name. Line 2 makes it smaller by sampling every nxnth pixel. Line 3 adds it to position in a grid
        self.logo = PhotoImage(file = self.resource_path('soton_logo.png'))
        self.small_logo = self.logo#.subsample(10,10)
        ttk.Label(self.frame_header, image = self.small_logo).grid(row=0, column=0, rowspan=3, sticky='nsew', padx=(30,30))
        # This adds a title and subtitle to the header frame
        ttk.Label(self.frame_header, text = self.worksheet_heading, font =('Segoe UI', 18)).grid(row=0, column=1, sticky='nsew')
        ttk.Label(self.frame_header, text = self.worksheet_subheading, font =('Segoe UI', 14)).grid(row=1, column=1, sticky='nsew')
        #This is for adding a logo. Line 1 loads the image and gives it a variable name. Line 2 makes it smaller by sampling every nxnth pixel. Line 3 adds it to position in a grid
        self.osprey_logo = PhotoImage(file = self.resource_path('logo_small.png'))
        self.small_osprey_logo = self.osprey_logo#.subsample(15,15)
        ttk.Label(self.frame_header, image = self.small_osprey_logo).grid(row=0, column=3, rowspan=3, sticky='nsew')
        
        
        
        ''' -------- Glabel parameters -------- '''
        
        self.frames_list = []
        self.penalty_count = 0
        
        ''' -------- Username request -------- '''
        
        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_username = ttk.Frame(self.useable_frame)
        self.frame_username.config(padding = (10,10))
        self.frame_username.pack(expand=True, fill='both')
        
        # This creates a title for an entry field
        ttk.Label(self.frame_username, text = "\t\tEnter your username here:").grid(row=0,column=0,sticky='nsew')
        # This creates an entry window for the user to add data. Line 1 creates the entry box, line 2 adds it to position on the grid. 
        self.entry_username = ttk.Entry(self.frame_username, width = 24)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        self.button_username = ttk.Button(self.frame_username, text = "Submit", command=self.submit_username)
        self.button_username.grid(row=0, column=3, padx=10, pady=5, sticky = 'nsew')
        
        ''' -------- Add in the separator line between the sections -------- '''
        #This adds a separator line at the end of a frame
        ttk.Separator(self.frame_username).grid(columnspan=6, sticky="ew")
        
        ''' -------- Introduction -------- '''
        
        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_introduction = ttk.Frame(self.useable_frame)
        self.frame_introduction.config(padding = (10,10))
        self.frames_list.append(self.frame_introduction)
        
        # This creates a title for an entry field
        ttk.Label(self.frame_introduction, wraplength = 800, text = self.introduction_text).grid(row = 0, column = 0, stick = "nsew")
        
        ''' -------- Add in the separator line between the sections -------- '''
        #This adds a separator line at the end of a frame
        ttk.Separator(self.frame_introduction).grid(columnspan=6, sticky='ew')
        
        ''' ================================================================================================================================================================= '''
        ''' ==='''                                                     ''' ==='''
        ''' ===''' '''QUESTIONS ARE INSERTED INTO THIS SECTION HERE''' ''' ==='''
        ''' ==='''                     '''|  |'''                      ''' ==='''
        ''' ==='''                     '''|  |'''                      ''' ==='''
        ''' ==='''                     '''|  |'''                      ''' ==='''
        ''' ==='''                 '''----   ----'''                   ''' ==='''
        ''' ==='''                  '''\       /'''                    ''' ==='''
        ''' ==='''                   '''\     /'''                     ''' ==='''
        ''' ==='''                    '''\   /'''                      ''' ==='''
        ''' ==='''                     '''\ /'''                       ''' ==='''


        
        ''' ================================================================================================================================================================= '''
        
        ''' -------- Section q1 for the worksheet -------- '''
        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_q1 = ttk.Frame(self.useable_frame)
        self.frame_q1.config(padding = (10,10))
        self.frames_list.append(self.frame_q1)
        
        #The lists create a record of all of the buttons, entry fields etc as they are made so they can be disabled after an answer is given and graded
        self.button_list_q1 = []
        self.entry_list_q1 = []
        
        ''' -------- Question q1 -------- '''
        ### These are the things that you need to change to build your worksheet 
        question_q1 = "Question 1: What was the radius of your electrode (in m)?" ###Add in the text for the question you want to ask. The question has to be kept inside the quote marks for the code to work, e.g. "This is the text for my question"
        
        # This creates a title for an entry field
        ttk.Label(self.frame_q1, text = question_q1, wraplength = 800).grid(row=0, column=0, padx=10, sticky='w')
        # This creates an entry window for the user to add data. Line 1 creates the entry box, line 2 adds it to position on the grid. 
        self.entry_q1 = ttk.Entry(self.frame_q1, width = 24)
        self.entry_q1.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        self.entry_list_q1.append(self.entry_q1)
        
        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a submit button 
        self.button_submit_q1 = ttk.Button(self.frame_q1, text = "Submit", command = lambda: self.submit_value("q1", self.frame_q1, self.entry_q1.get(), self.button_list_q1, self.entry_list_q1))
        self.button_submit_q1.grid(row=0, column=2, padx=10, pady=5, sticky = 'w')
        self.button_list_q1.append(self.button_submit_q1)
        
        ''' -------- Add components into relevant dictionaries -------- '''
        # This section will be used to auto complete and block out entries that have already been completed if students close and then reopen the worksheet
        self.entry_dictionary["q1"] = self.entry_list_q1
        self.button_dictionary["q1"] = self.button_list_q1
        self.question_list.append("q1")
        
        ''' -------- Add in the separator line between the sections -------- '''
        #This adds a separator line at the end of a frame
        ttk.Separator(self.frame_q1).grid(columnspan=7, sticky="ew")
        
        ''' ================================================================================================================================================================= '''
        
        ''' -------- Section q2 for the worksheet -------- '''
        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_q2 = ttk.Frame(self.useable_frame)
        self.frame_q2.config(padding = (10,10))
        self.frames_list.append(self.frame_q2)
        
        #The lists create a record of all of the buttons, entry fields etc as they are made so they can be disabled after an answer is given and graded
        self.button_list_q2 = []
        self.entry_list_q2 = []
        
        ''' -------- Question  q2 -------- '''
        ### These are the things that you need to change to build your worksheet 
        question_q2 = "Question 2: What was the area of your electrode (in m²)?" ###Add in the text for the question you want to ask. The question has to be kept inside the quote marks for the code to work, e.g. "This is the text for my question"
        max_score_q2 = 1.0 ### Record the max score for this question
        penalty_q2 = 0.25 ### Record the penalty for each incorrect attempt
        feedback_q2 = ["It looks like you forgot to square the radius of your electrode. Remember that the formula for the area of a circle is 𝜋r²", "Remember that the formula for the area of a circle is 𝜋r², and check you have reported your answer to the correct number of decimal places. Also note that the correct format for very small numbers such as 10⁻⁶ is 1e-06, not 1e-6."] ### Add in the message you want to pop up here, inside the quote marks after message =.
        solved_feedback_q2 = ["Remember that the formula for the area of a circle is 𝜋r², and check you have reported your answer to the correct number of decimal places. Also note that the correct format for very small numbers such as 10⁻⁶ is 1e-06, not 1e-6."]
        sf_q2 = self.sigfig ### How many significant figures should the answer be rounded to? Enter None if you do not want any rounding, or self.sigfig to call the global sigfig number that was defined earlier
        wrong_answers_q2 = [] ### enter any common wrong answers that require specific feedback here, comma separated and inside quote marks. This can be left blank if not needed
        
        
        ''' -------- Calculate the correct answer based on a previous answer -------- ''' 
        ### You will need to add in your own calculations in order to use a previous entry to produce a new answer 
        def calculate_answer_q2():
            return lambda value: np.pi*(float(value)**2) ### Use a calculation in python format to calculate the correct answer. value is used to present the number that will be taken from a previous answer
        
        values_q2 = [self.entry_q1] ### Use this line to state which question the value you need for the calculation comes from. In this case, q1 means it is coming from question 1
        answer_q2 = calculate_answer_q2() #This is a preparatory function so the script is ready to do the calculation after a number has been added to the previous question

        
        
        ''' -------- Calculate the wrong answer based on a previous answer -------- ''' 
        wrong_values_q2 = []
        
        ### You will need to add in your own calculations in order to use a previous entry to produce a new answer 
        def calculate_wrong_q2_1():
            return lambda value: np.pi*(float(value)) ### Use a calculation in python format to calculate the correct answer. value is used to present the number that will be taken from a previous answer
        
        wrong_answers_q2.append(calculate_wrong_q2_1())
        wrong_values_q2.append(values_q2)


        ''' -------- Enter the question -------- '''
        
        # This creates a title for an entry field
        ttk.Label(self.frame_q2, text = question_q2, wraplength = 800).grid(row=0, column=0, padx=10, sticky='w')
        # This creates an entry window for the user to add data. Line 1 creates the entry box, line 2 adds it to position on the grid, line 3 adds the entry into the list for later use
        self.entry_q2 = ttk.Entry(self.frame_q2, width = 24)
        self.entry_q2.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        self.entry_list_q2.append(self.entry_q2)
        
        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a submit button 
        self.button_submit_q2 = ttk.Button(self.frame_q2, text = "Submit", command = lambda: self.submit_1answer("q2", self.frame_q2, self.entry_q2.get(), [answer_q2( *self.input_values(values_q2) )], max_score_q2, penalty_q2, feedback_q2, self.function_list_on_variable_list(wrong_answers_q2, wrong_values_q2), self.button_list_q2, self.entry_list_q2, sf=sf_q2))
        self.button_submit_q2.grid(row=0, column=3, padx=10, pady=5, sticky = 'w')
        self.button_list_q2.append(self.button_submit_q2)
        
        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a solve button 
        self.button_solve_q2 = ttk.Button(self.frame_q2, text = "Solve", command = lambda: self.solve_1answer("q2", self.frame_q2, [answer_q2( *self.input_values(values_q2) )],  max_score_q2, solved_feedback_q2, self.button_list_q2, self.entry_list_q2, sf=sf_q2))
        self.button_solve_q2.grid(row=0, column=4, padx=10, pady=5, sticky = 'w')
        self.button_list_q2.append(self.button_solve_q2)
        
        ''' -------- Add components into relevant dictionaries -------- '''
        # This section will be used to auto complete and block out entries that have already been completed if students close and then reopen the worksheet
        self.entry_dictionary["q2"] = self.entry_list_q2
        self.button_dictionary["q2"] = self.button_list_q2
        self.label_loc_dictionary["q2"] = [6, 0, self.frame_q2] #If a student has already entered an answer on a previous attempt, this is where the label containing their score will appear. Format is [column, row, frame number]
        self.question_list.append("q2")
        
        ''' -------- Add in the separator line between the sections -------- '''
        #This adds a separator line at the end of a frame
        ttk.Separator(self.frame_q2).grid(columnspan=5, sticky="ew")    

        ''' ================================================================================================================================================================= '''
        
        
        ''' -------- Section q3 for the worksheet -------- '''
        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_q3 = ttk.Frame(self.useable_frame)
        self.frame_q3.config(padding = (10,10))
        self.frames_list.append(self.frame_q3)
        
        #The lists create a record of all of the buttons, entry fields etc as they are made so they can be disabled after an answer is given and graded
        self.button_list_q3 = []
        self.entry_list_q3 = []
        
        ''' -------- Question q3 -------- '''
        ### These are the things that you need to change to build your worksheet 
        question_q3 = "Question 3: What was the concentration of CuSO\u2084 (in mol m\u207B\u00B3)?"###Add in the text for the question you want to ask. The question has to be kept inside the quote marks for the code to work, e.g. "This is the text for my question"
        max_score_q3 = 1.0 ### Record the max score for this question
        penalty_q3 = 0.25 ### Record the penalty for each incorrect attempt
        answer_q3 = [5.0] ### Record the answer for this question. The answer must be kept inside the square brackets to work. Multiple acceptable answers can be given by separating them with commas, e.g. [answer1 , answer2, answer3]
        wrong_answers_q3 = [] ### enter any common wrong answers that require specific feedback here, comma separated and inside quote marks. This can be left blank if not needed
        feedback_q3 = ["Make sure you have used the correct unit conversion to report the concentration in mol m\u207B\u00B3. Sometimes it helps to think conceptually about unit conversions. If there is 1 mole in a cubic decimeter, how mnay moles could you fit in a cubic meter?"] ### Add in the message you want to pop up here, inside the quote marks after message =. If you want a unit to appear after the correct answer, include this at the start. If using the wrong answers option, inlcude a list of feedbacks in the same order as in the wrong answers. The final item should then be for generic feedback if none of the wrong answers are chosen.
        solved_feedback_q3 = ["This practical used 5 mM of copper, or 0.005 mol dm\u207B\u00B3. There are 10 dm in a m, so there must be 10\u00B3 dm\u00B3 in 1 m\u00B3. If the volume is 1000x bigger, then there must be 1000x as many moles, i.e. 1000 x 0.005 = 5 mol m\u207B\u00B3."] #Sometimes it is helpful to provide more specific feedback if the solve button has been pressed. 
        sf_q3 = self.sigfig ### How many significant figures should the answer be rounded to? Enter None if you do not want any rounding, or self.sigfig to call the global sigfig number that was defined earlier
        
        # This creates a title for an entry field
        ttk.Label(self.frame_q3, text = question_q3, wraplength=800).grid(row=0, column=0, padx=10, sticky='w')
        # This creates an entry window for the user to add data. Line 1 creates the entry box, line 2 adds it to position on the grid.
        self.entry_q3 = ttk.Entry(self.frame_q3, width = 24)
        self.entry_q3.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        self.entry_list_q3.append(self.entry_q3)

        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a submit button 
        self.button_submit_q3 = ttk.Button(self.frame_q3, text = "Submit", command = lambda: self.submit_1answer("q3", self.frame_q3, self.entry_q3.get(), answer_q3, max_score_q3, penalty_q3, feedback_q3, wrong_answers_q3, self.button_list_q3, self.entry_list_q3, sf=sf_q3))
        self.button_submit_q3.grid(row=0, column=3, padx=10, pady=5, sticky = 'w')
        self.button_list_q3.append(self.button_submit_q3)

        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a solve button 
        self.button_solve_q3 = ttk.Button(self.frame_q3, text = "Solve", command = lambda: self.solve_1answer("q3", self.frame_q3, answer_q3, max_score_q3, solved_feedback_q3, self.button_list_q3, self.entry_list_q3, sf=sf_q3))
        self.button_solve_q3.grid(row=0, column=4, padx=10, pady=5, sticky = 'w')
        self.button_list_q3.append(self.button_solve_q3)

        ''' -------- Add components into relevant dictionaries -------- '''
        # This section will be used to auto complete and block out entries that have already been completed if students close and then reopen the worksheet
        self.entry_dictionary["q3"] = self.entry_list_q3
        self.button_dictionary["q3"] = self.button_list_q3
        self.label_loc_dictionary["q3"] = [6, 0, self.frame_q3] #If a student has already entered an answer on a previous attempt, this is where the label containing their score will appear. Format is [column, row, frame number]
        self.question_list.append("q3")
        
        ''' -------- Add in the separator line between the sections -------- '''
        #This adds a separator line at the end of a frame
        ttk.Separator(self.frame_q3).grid(columnspan=7, sticky="ew")        
        
        ''' ================================================================================================================================================================= '''
        
        ''' -------- Section q4 for the worksheet -------- '''
        
        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_q4 = ttk.Frame(self.useable_frame)
        self.frame_q4.config(padding = (10,10))
        self.frames_list.append(self.frame_q4)
        
        #The lists create a record of all of the buttons, entry fields etc as they are made so they can be disabled after an answer is given and graded
        self.button_list_q4 = []
        self.entry_list_q4 = []
        
        ''' -------- Question q4 -------- '''   
        ### These are the things that you need to change to build your worksheet 
        max_score_q4 = 1.0 ### Record the max score for this question
        penalty_q4 = 0.25 ### Record the penalty for each incorrect attempt
        feedback_q4 = ["\n\nRemember that linear equations take the form y = mx + c. \nValues for y and x should therefore be selected to match components from the Randles–Ševčík equation such that a linear relationship is achieved, with other parameters contained in the gradient and/or intercept. \n\nIn order to find a liner relationship, try lining up the generic expression y = mx + c with the Randles–Ševčík equation. y would be iₚ seeing as they're both on the left of the equation, and there is no term for the intercept, so we don't have to worry about c (a scan rate of zero means you aren't sweeping at all, so there would be no peaks and iₚ would be zero, therefore the intercept of the linear plot should be zero). \n\nSo we know what y is and we don't have a value for c, now we just look at the remaining terms in the Randles–Ševčík equation and assign them to either m or x. Which of the options given in the checkboxes would be assigned to x?"]  ### Add in the message you want to pop up here, inside the quote marks after message =. If you want a unit to appear after the correct answer, include this at the start.
        solved_feedback_q4 = ["Remember that linear equations take the form y = mx + c. \nValues for y and x should therefore be selected to match components from the Randles–Ševčík equation such that a linear relationship is achieved, with other parameters contained in the gradient and/or intercept. \n\nIn order to find a liner relationship, try lining up the generic expression y = mx + c with the Randles–Ševčík equation. y would be iₚ seeing as they're both on the left of the equation, and there is no term for the intercept, so we don't have to worry about c (a scan rate of zero means you aren't sweeping at all, so there would be no peaks and iₚ would be zero, therefore the intercept of the linear plot should be zero). \n\nSo we know what y is and we don't have a value for c, now we just look at the remaining terms in the Randles–Ševčík equation and assign them to either m or x. x variables are what we change, which in this experiment was the scan rate. The Randles–Ševčík equation gives scan rate (𝜈) in terms of the its root (𝜈¹\u141F²), so that's the form we use if we want a linear y = mx + c style plot."]
        answer_q4 = ["| 𝑖ₚ | vs 𝜈¹\u141F²"] ### Record the answer for this question. The answer must be kept inside the square brackets to work. Multiple acceptable answers can be given by separating them with commas, e.g. [answer1 , answer2, answer3]
        wrong_answers_q4 = ["| 𝑖ₚ | vs 𝜈",  "| 𝑖ₚ |¹\u141F² vs 𝜈¹\u141F²", "| 𝑖ₚ | vs 𝜈⁻¹\u141F²", "| 𝑖ₚ |⁻¹\u141F² vs 𝜈⁻¹\u141F²", "| 𝑖ₚ | vs ln(𝜈)"] ### enter any common wrong answers that require specific feedback here, comma separated and inside quote marks. This can be left blank if not needed
        
        feedback_q4 = ["The Randles–Ševčík equation does not directly relate 𝑖ₚ to 𝜈. Looking at the equation, in order to achieve 𝜈 on the right hand side, you would have to square both sides of the equation. This would give 𝑖ₚ² as a function of 𝜈. So, 𝑖ₚ vs. 𝜈 cannot be linear. \n\nRemember that linear equations take the form y = mx + c. \nValues for y and x should therefore be selected to match components from the Randles–Ševčík equation such that a linear relationship is achieved, with other parameters contained in the gradient and/or intercept. \n\nIn order to find a liner relationship, try lining up the generic expression y = mx + c with the Randles–Ševčík equation. y would be iₚ seeing as they're both on the left of the equation, and there is no term for the intercept, so we don't have to worry about c (a scan rate of zero means you aren't sweeping at all, so there would be no peaks and iₚ would be zero, therefore the intercept of the linear plot should be zero). \n\nSo we know what y is and we don't have a value for c, now we just look at the remaining terms in the Randles–Ševčík equation and assign them to either m or x. Which of the options given in the checkboxes would be assigned to x?", "The Randles–Ševčík equation does not directly relate 𝑖ₚ¹\u141F² to 𝜈. Looking at the equation, in order to achieve 𝑖ₚ¹\u141F² on the left hand side, you would have to root both sides of the equation. This would give 𝑖ₚ¹\u141F² as a function of 𝜈¹\u141F⁴. So, 𝑖ₚ¹\u141F² vs. 𝜈¹\u141F² cannot be linear.\n\nRemember that linear equations take the form y = mx + c. \nValues for y and x should therefore be selected to match components from the Randles–Ševčík equation such that a linear relationship is achieved, with other parameters contained in the gradient and/or intercept. \n\nIn order to find a liner relationship, try lining up the generic expression y = mx + c with the Randles–Ševčík equation. y would be iₚ seeing as they're both on the left of the equation, and there is no term for the intercept, so we don't have to worry about c (a scan rate of zero means you aren't sweeping at all, so there would be no peaks and iₚ would be zero, therefore the intercept of the linear plot should be zero). \n\nSo we know what y is and we don't have a value for c, now we just look at the remaining terms in the Randles–Ševčík equation and assign them to either m or x. Which of the options given in the checkboxes would be assigned to x?", "The Randles–Ševčík equation does not directly relate 𝑖ₚ to 𝜈⁻¹\u141F². Looking at the equation, in order to achieve 𝜈⁻¹\u141F² on the right hand side, you would have to do some very complicated and unnecessary mathematical rearrangments. So, 𝑖ₚ vs 𝜈⁻¹\u141F² cannot be linear.\n\nRemember that linear equations take the form y = mx + c. \nValues for y and x should therefore be selected to match components from the Randles–Ševčík equation such that a linear relationship is achieved, with other parameters contained in the gradient and/or intercept. \n\nIn order to find a liner relationship, try lining up the generic expression y = mx + c with the Randles–Ševčík equation. y would be iₚ seeing as they're both on the left of the equation, and there is no term for the intercept, so we don't have to worry about c (a scan rate of zero means you aren't sweeping at all, so there would be no peaks and iₚ would be zero, therefore the intercept of the linear plot should be zero). \n\nSo we know what y is and we don't have a value for c, now we just look at the remaining terms in the Randles–Ševčík equation and assign them to either m or x. Which of the options given in the checkboxes would be assigned to x?", "The Randles–Ševčík equation does not directly relate 𝑖ₚ⁻¹\u141F² to 𝜈⁻¹\u141F². Looking at the equation, in order to achieve 𝜈⁻¹\u141F² on the right hand side and 𝑖ₚ⁻¹\u141F² on the left, you would have to do some very complicated and unnecessary mathematical rearrangments. So, 𝑖ₚ⁻¹\u141F² vs 𝜈⁻¹\u141F² cannot be linear.\n\nRemember that linear equations take the form y = mx + c. \nValues for y and x should therefore be selected to match components from the Randles–Ševčík equation such that a linear relationship is achieved, with other parameters contained in the gradient and/or intercept. \n\nIn order to find a liner relationship, try lining up the generic expression y = mx + c with the Randles–Ševčík equation. y would be iₚ seeing as they're both on the left of the equation, and there is no term for the intercept, so we don't have to worry about c (a scan rate of zero means you aren't sweeping at all, so there would be no peaks and iₚ would be zero, therefore the intercept of the linear plot should be zero). \n\nSo we know what y is and we don't have a value for c, now we just look at the remaining terms in the Randles–Ševčík equation and assign them to either m or x. Which of the options given in the checkboxes would be assigned to x?", "The Randles–Ševčík equation does not directly relate 𝑖ₚ to ln(𝜈). Looking at the equation, in order to achieve ln(𝜈) on the right hand side, you would have to square and take the log of both sides. So, 𝑖ₚ vs ln(𝜈) cannot be linear.\n\nRemember that linear equations take the form y = mx + c. \nValues for y and x should therefore be selected to match components from the Randles–Ševčík equation such that a linear relationship is achieved, with other parameters contained in the gradient and/or intercept. \n\nIn order to find a liner relationship, try lining up the generic expression y = mx + c with the Randles–Ševčík equation. y would be iₚ seeing as they're both on the left of the equation, and there is no term for the intercept, so we don't have to worry about c (a scan rate of zero means you aren't sweeping at all, so there would be no peaks and iₚ would be zero, therefore the intercept of the linear plot should be zero). \n\nSo we know what y is and we don't have a value for c, now we just look at the remaining terms in the Randles–Ševčík equation and assign them to either m or x. Which of the options given in the checkboxes would be assigned to x?"]
        
        self.labels_q4 = ["| 𝑖ₚ | vs 𝜈", "| 𝑖ₚ | vs 𝜈¹\u141F²", "| 𝑖ₚ |¹\u141F² vs 𝜈¹\u141F²", "| 𝑖ₚ | vs 𝜈⁻¹\u141F²", "| 𝑖ₚ |⁻¹\u141F² vs 𝜈⁻¹\u141F²", "| 𝑖ₚ | vs ln(𝜈)"] ### Record all of the possible checkboxes you want to show, including the correct answer and all wrong answers. The list of possible labels should be inside the square brackets, with each label inside quote marks. E.g. ["label 1", "label 2", label 3"]
        self.checkbutton_cols_q4 = 2 ### How many columns do you want the checkboxes to be divided between?
        
        #The lists create a record of all of the buttons, entry fields etc as they are made so they can be disabled after an answer is given and graded
        self.button_list_q4 = []
        self.entry_list_q4 = []
        
        # This creates a title for an entry field
        ttk.Label(self.frame_q4, wraplength=450, text = "Question 4: The Randles–Ševčík equation defines the relationship between peak current (𝑖ₚ) and scan rate (𝜈) for a reversible system, where").grid(row=0, column=0, padx=10, sticky='w')
        
        # This adds in an image to be used for an equation along with the question
        self.eq_Randles = PhotoImage(file = self.resource_path('Randles.png'))
        #self.eq_Randles = self.eq_Randles.subsample(2,2) #This line is available to resize the image if needed
        ttk.Label(self.frame_q4, image = self.eq_Randles).grid(row=1, column=0)
        
        # This creates question text for an entry field
        ttk.Label(self.frame_q4, wraplength=450, text = "Based on this, which relationship would you expect to be linear?").grid(row=2, column=0, padx=10, sticky='w')
         
        #This function will create all of the text boxes 
        self.checkbuttons_q4, self.checkbutton_labels_q4 = self.create_checkbuttons("q4", self.frame_q4, 0, 1, self.labels_q4, answer_q4, self.checkbutton_cols_q4)
        
        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a submit button
        self.button_submit_q4 = ttk.Button(self.frame_q4, text = "Submit", command=lambda: self.submit_1checkbox("q4", self.frame_q4, answer_q4, self.labels_q4, self.checkbutton_labels_q4, max_score_q4, penalty_q4, feedback_q4, wrong_answers_q4, self.button_list_q4, self.checkbuttons_q4))
        self.button_submit_q4.grid(row=0, column=self.checkbutton_cols_q4+1, rowspan=round(len(self.labels_q4)/self.checkbutton_cols_q4), padx=10, pady=5, sticky = 'w')
        self.button_list_q4.append(self.button_submit_q4)
        
        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a solve button
        self.button_solve_q4 = ttk.Button(self.frame_q4, text = "Solve", command=lambda: self.solve_1checkbox("q4", self.frame_q4, answer_q4, self.checkbutton_labels_q4, max_score_q4, penalty_q4, solved_feedback_q4, self.button_list_q4, self.checkbuttons_q4))
        self.button_solve_q4.grid(row=0, column=self.checkbutton_cols_q4+2, rowspan=round(len(self.labels_q4)/self.checkbutton_cols_q4), padx=10, pady=5, sticky = 'w')
        self.button_list_q4.append(self.button_solve_q4)
        
        ''' -------- Add components into relevant dictionaries -------- '''
        # This section will be used to auto complete and block out entries that have already been completed if students close and then reopen the worksheet
        self.checkbutton_dictionary["q4"] = self.checkbuttons_q4
        self.checkbutton_label_dictionary["q4"] = self.checkbutton_labels_q4
        self.button_dictionary["q4"] = self.button_list_q4
        self.label_loc_dictionary["q4"] = [self.checkbutton_cols_q4+3, 0, self.frame_q4] #If a student has already entered an answer on a previous attempt, this is where the label containing their score will appear. Format is [column, row, frame number]
        self.question_list.append("q4")
        
        ''' -------- Add in the separator line between the sections -------- '''
        #This adds a separator line at the end of a frame
        ttk.Separator(self.frame_q4).grid(columnspan=5, sticky="ew")
        
        ''' ================================================================================================================================================================= '''
        
        ''' -------- Section q5 introduction for the worksheet -------- '''

        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_q5_intro = ttk.Frame(self.useable_frame)
        self.frame_q5_intro.config(padding = (10,10))
        self.frames_list.append(self.frame_q5_intro)

        ''' -------- Question q5 -------- '''        
        
        # This creates an introductory text field
        ttk.Label(self.frame_q5_intro, wraplength=800, text = "For the following question, it is VERY important that you enter values to the highest possible precision, otherwise the spreadsheet may mark your answer as wrong. \n\nThe smart worksheet uses the numbers you give to calculate the correct answer, so if the data you enter here has a different number of significant figures compared to the data you are working on in Excel, your answer may be marked as incorrect. Copy as many decimals as possible directly from Excel to access full marks. \n\nRemember, SI units are important in graphical analysis. Your potentiostat will often convert units for ease of reading (converting amps into microamps, for example), so you may need to convert to SI units before proceeding. \n\nHint: The Randles Ševčík equation uses the absolute peak current value, so if you're using a reduction current, remember to take this into account.\n\nYou may also find the following keyboard shortcuts helpful: \tCTRL+C = copy \t CTRL+V = paste \t CTRL+A = select all").grid(row=0, column=0, padx=10, sticky='w')
        
        
        ''' ================================================================================================================================================================= '''
        
        ''' This code creates a scatter plot from user submitted data. Data may be entered as comma separated numbers or by copying a column from Excel.
        Code starts with an introduction section that lets the creator introduce the plot, for example encouraging students to use precise values.
        If the option to plot a linear trendline is chosen, the plot will also calculate the gradient, intercept, and confidence intervals. 
        These can be accessed later in the code through the following options:
            
            gradient = ['q1', 'm']
            intercept = ['q1', 'c']
            upper 95% confidence interval = ['q1', 'CI_high']
            lower 95% condience interval = ['q1', 'CI_low']
            
        The format of the above is for reading values out of a dictionary of parameters that is automatically updated when a scatter plot with a trendline is made

        '''
        
        ''' -------- Section q5 for the worksheet -------- '''

        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_q5 = ttk.Frame(self.useable_frame)
        self.frame_q5.config(padding = (10,10))
        self.frames_list.append(self.frame_q5)
        
        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_plot1 = ttk.Frame(self.useable_frame)
        self.frame_plot1.config(padding = (10,10))
        self.frames_list.append(self.frame_plot1)
        
        #The lists create a record of all of the buttons, entry fields etc as they are made so they can be disabled after an answer is given and graded
        self.button_list_q5 = []
        self.entry_list_q5 = []

        ''' -------- Question q5 -------- ''' 
        ### These are the things that you need to change to build your worksheet 
        
        ### This creates a title for an entry field. Enter the text you want to apper next to the x data entry box between the quote marks below:
        ttk.Label(self.frame_q5, wraplength=450,  text = "Question 5a: Enter in the x data for your linear plot. You may enter your data as comma separated numbers, or by copying a column of data directly from Excel.").grid(row=0, column=0, padx=10, sticky='w')
        
        ### This creates a title for an entry field. Enter the text you want to apper next to the y data entry box between the quote marks below:
        ttk.Label(self.frame_q5, wraplength = 450, text = "Question 5b: Enter in the y data for your linear plot. You may enter your data as comma separated numbers, or by copying a column of data directly from Excel.").grid(row=1, column=0, padx=10, sticky='w')
        
        # This creates an entry window for the user to add data. Line 1 creates the entry box, line 2 adds it to position on the grid.
        self.entry_q5x = ttk.Entry(self.frame_q5, width = 30)
        self.entry_q5x.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        self.entry_list_q5.append(self.entry_q5x)

        # This creates an entry window for the user to add data. Line 1 creates the entry box, line 2 adds it to position on the grid.
        self.entry_q5y = ttk.Entry(self.frame_q5, width = 30)
        self.entry_q5y.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        self.entry_list_q5.append(self.entry_q5y)

        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a plot button
        self.button_plot_q5 = ttk.Button(self.frame_q5, text = "Plot", command=lambda: self.plot_scatter("q5", self.frame_plot1, self.entry_q5x.get(), self.entry_q5y.get(), self.button_list_q5, self.entry_list_q5, trendline=True))
        self.button_plot_q5.grid(row=0, column=3, rowspan = 2, padx=10, pady=5, sticky = 'w')
        self.button_list_q5.append(self.button_plot_q5)

        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a reset button
        self.button_reset_q5 = ttk.Button(self.frame_q5, text = "Reset", command=lambda:self.reset_scatter(self.button_list_q5, self.entry_list_q5, self.frame_plot1))
        self.button_reset_q5.grid(row=0, column=4, rowspan = 2, padx=10, pady=5, sticky = 'w')

        ''' -------- Add components into relevant dictionaries -------- '''
        # This section will be used to auto complete and block out entries that have already been completed if students close and then reopen the worksheet
        self.entry_dictionary["q5"] = self.entry_list_q5
        self.button_dictionary["q5"] = self.button_list_q5
        self.question_list.append("q5")
        self.plot_button_dictionary["q5"] = self.button_plot_q5

        ''' -------- Add in the separator line between the sections -------- '''
        #This adds a separator line at the end of a frame
        ttk.Separator(self.frame_q5).grid(columnspan=5, sticky="ew")
        
        ''' ================================================================================================================================================================= '''
        
        ''' -------- Section q6 Introduction for the worksheet -------- '''
        
        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_q6_intro = ttk.Frame(self.useable_frame)
        self.frame_q6_intro.config(padding = (10,10))
        self.frames_list.append(self.frame_q6_intro)   

        ''' -------- Introductory text -------- '''
        ### These are the things that you need to change to build your worksheet 
        ### This creates the text that will form your introduction
        ttk.Label(self.frame_q6_intro, text = "The following questions will give you the opportunity to enter formatting information onto your graph, including trendline equation and axis labels. \n\t • Answers should be entered in Python format using math mode text. \n\t\t E.g. for 𝑖ₚ enter $i_p$ and for 𝑡⁻¹\u141F² enter $t^{-1/2}$. \n\tYou don't need to use modulus symbols (||) in your answer, i.e enter 𝑖ₚ not | 𝑖ₚ | . \n\t • Use negative powers where indicated in units. \n\t\t E.g. for mol dm⁻³ enter mol dm$^{-3}$, rather than mol/dm$^3$ \n\t • Multiply out brackets when used for powers. \n\t\t E.g. enter V¹\u141F² s⁻¹\u141F² rather than (V s⁻¹\u141F²)¹\u141F² \n\t • Use symbols for parameter names (for example, scan rate is 𝜈) \n\t • Remember that parameters should be italic but units should not. So, for length (𝑙) = 4 metres (m), 𝑙 (the distance parameter) is italic, and m (the unit metres) is not. \n\t\t The expression is therefore 𝑙 = 4 m, which would be coded as $l$ = 4 m. \n\t • It's recommended to keep your code as simple as possible, particuarly in the use of mathmode. \n\t\t E.g. 𝑘₁ / s⁻¹ could be written in many ways, but the simplest is to only use $$ around the parts that need them, i.e. $k_1$ / s$^{-1}$ \n\t • All values should be reported following the numbering conventions detailed at the top of this worksheet. \n\n Most importantly - Take advantage of the Preview button, which lets you view your text input on the graph without impacting your score \n").grid(row=0, column=0, padx=10, sticky='nsew')

        ''' -------- Add in the separator line between the sections -------- '''
        #This adds a separator line at the end of a frame
        ttk.Separator(self.frame_q6_intro).grid(columnspan=5, sticky="ew")
        
        ''' ================================================================================================================================================================= '''
        
        ''' -------- Section q6 for the worksheet -------- '''
        
        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_q6 = ttk.Frame(self.useable_frame)
        self.frame_q6.config(padding = (10,10))
        self.frames_list.append(self.frame_q6)

        ''' -------- Question q6 -------- '''

        ### These are the things that you need to change to build your worksheet  
        max_score_q6 = 1.0 ### Record the max score for this question
        penalty_q6 = 0.25 ### Record the penalty for each incorrect attempt
        question_q6 = "Question 6: Enter in your x axis label. Take care to follow all instructions given in the text above. (Hint: the worksheet will accept lower case v in place of nu for simplicity." ###Add in the text for the question you want to ask. The question has to be kept inside the quote marks for the code to work, e.g. "This is the text for my question"
        sf_q6 = None ### How many significant figures should the answer be rounded to? Enter None if you do not want any rounding, or self.sigfig to call the global sigfig number that was defined earlier
        
        ### Calling graphing data from previous question answers
        self.x_data_location_q6 = self.entry_q5x ### This tells the worksheet which previous question to use in order to find the x data. This format ... = self.entry_q5x.get() indicates the code with get x data from question 5 (q5). To get data from a different question, replace q5 with the appropriate q number
        self.y_data_location_q6 = self.entry_q5y ### This tells the worksheet which previous question to use in order to find the y data. This format ... = self.entry_q5y.get() indicates the code with get y data from question 5 (q5). To get data from a different question, replace q5 with the appropriate q number
        
        ### Comma separated list of possible answers. Any of these answers would be marked as correct. If statement combines the fact that nu and 0.5 can be represented in different ways
        nu = ['v', 'ν', '𝜈', r'\nu'] #All possible ways of saying nu r'\nu' is needed to ensure \nu is read as "nu" and not as "newline u"
        power = ["0.5", "1/2"] #All possible ways of saying 0.5
        answer_q6 = ["$" + n + "^{" + p + "}$/V$^{" + p + "}$s$^{-" + p + "}$" for n in nu for p in power] + ["$" + n + "^{" + p + "}/\mathrm{V}^{" + p + "}\mathrm{s}^{-" + p + "}$" for n in nu for p in power]       
        
        ### Many of the wrong answers should have the same feedback (arrangements of symbols etc) so this will build the list
        wrong_answers_q6 = [[n + "$^{" + p + "}$/V$^{" + p + "}$s$^{-" + p + "}$" for n in nu for p in power] + [n + "$^{" + p + "}/\mathrm{V}^{" + p + "}\mathrm{s}^{-" + p + "}$" for n in nu for p in power],["$" + n + "^{" + p + "}$/(Vs$^{-1}$)$^{" + p + "}$" for n in nu for p in power] + ["$" + n + "^{" + p + "}/(\mathrm{V}\mathrm{s}^{-1})^{-" + p + "}$" for n in nu for p in power] , ["$" + n + "^{" + p + "}/V^{" + p + "}s^{-" + p + "}$" for n in nu for p in power] , ["$" + n + "$/Vs$^{-1}$" for n in nu]]
        feedback_q6 = ["It looks like this answer would give an x axis variable that is not in italics. Pay close attention to the formatting instructions for a good axis label. Variables should be in italics, and units should not. \n\nFor example, time in seconds should be given as $t$ / s, so that the variable t is italic and the unit s is not.", "It looks like you've forgotten to multiply out all of the brackets. Check the formatting guide for the units given in the smart worksheet. For units of (mol dm⁻³)², multiply out the brackets to give mol² dm⁻⁶.", "It looks like this code would create an x axis that is all italics. Note the guidance in the smart worksheet. Only variables should be italic. Units should not. A time axis in seconds should therefore be coded as $t$ / s. You can move $ signs to only surround characters that you wish to be italic, or numbers that should be super/subscript. By keeping only the key characters inside the $ signs, you can avoid accdientally making everything italic." , "It looks like you have used the wrong units for the root of scan rate here. V s⁻¹ is correct for the scan rate, but what are the units of v⁻¹\u141F²?", "Ensure that you have included the correct units for your axis label. Remember that any power or factor applied to the unit should also be applied to the variable. Also, check your Python text formatting to achieve subscripts and/or superscripts where needed. You can take advantage of the Preview button to see how your code will look on the plot without penalty."] 
        solved_feedback_q6 = ["The variable for the x axis is the square root of the scan rate (v⁻¹\u141F²). Since scan rate has the units V s⁻¹, the root of scan rate must require us to take the root of the units, i.e. (V s⁻¹)¹\u141F² = V¹\u141F² s⁻¹\u141F². \n\n The coding for this uses math mode to provide italics and superscripts. Anything inside the $ signs is italic, and ^ can be used for superscript. To superscript multiple characters, as in v⁻¹\u141F², we wrap the superscripted characters in curly brackets {}.\n\n There are multiple ways to do this, as can be seen in the list of acceptable answers, though the simplest would be just to use dollar signs around the superscript and italic characters, \n\n e.g. $v^{0.5}$ / V$^{0.5}$ s$^{-0.5}$"]
    
        #The lists create a record of all of the buttons, entry fields etc as they are made so they can be disabled after an answer is given and graded
        self.button_list_q6 = []
        self.entry_list_q6 = []
        
        # This creates a title for an entry field
        ttk.Label(self.frame_q6,wraplength=450, text = question_q6).grid(row=0, column=0, padx=10, sticky='w')
        # This creates an entry window for the user to add data. Line 1 creates the entry box, line 2 adds it to position on the grid. 
        self.entry_q6 = ttk.Entry(self.frame_q6, width = 30)
        self.entry_q6.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        self.entry_list_q6.append(self.entry_q6)

        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a preview button
        self.button_preview_q6 = ttk.Button(self.frame_q6, text = "Preview", command=lambda: self.plot_scatter("q6", self.frame_plot1, self.x_data_location_q6.get(), self.y_data_location_q6.get(), self.button_list_q6, self.entry_list_q6, xlabel=self.entry_q6.get(), trendline=True, preview=True))
        self.button_preview_q6.grid(row=0, column=2, padx=10, pady=5, sticky = 'w')
        #Preview buttons are not added to the list of buttons, as the button list is used to disable buttons after submission. There is no need to disable a preview button and it can be useful for the student to use preview to visualise a correcct answer if they have used "Solve"
        
        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a submit button
        self.button_submit_q6 = ttk.Button(self.frame_q6, text = "Submit", command=lambda: [self.submit_1answer("q6", self.frame_q6, self.entry_q6.get(), answer_q6, max_score_q6, penalty_q6, feedback_q6, wrong_answers_q6, self.button_list_q6, self.entry_list_q6, sf=sf_q6), self.button_preview_q6.invoke()])
        self.button_submit_q6.grid(row=0, column=3, padx=10, pady=5, sticky = 'w')
        self.button_list_q6.append(self.button_submit_q6)
        
        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a solve button
        self.button_solve_q6 = ttk.Button(self.frame_q6, text = "Solve", command=lambda: [self.solve_1answer("q6", self.frame_q6, answer_q6, max_score_q6, solved_feedback_q6, self.button_list_q6, self.entry_list_q6, sf=sf_q6) , self.button_preview_q6.invoke()])
        self.button_solve_q6.grid(row=0, column=4, padx=10, pady=5, sticky = 'w')
        self.button_list_q6.append(self.button_solve_q6)
        
        ''' -------- Add components into relevant dictionaries -------- '''
        # This section will be used to auto complete and block out entries that have already been completed if students close and then reopen the worksheet
        self.entry_dictionary["q6"] = self.entry_list_q6
        self.button_dictionary["q6"] = self.button_list_q6
        self.label_loc_dictionary["q6"] = [6, 0, self.frame_q6] #If a student has already entered an answer on a previous attempt, this is where the label containing their score will appear. Format is [column, row, frame number]
        self.question_list.append("q6")
        
        ''' -------- Add in the separator line between the sections -------- '''
        #This adds a separator line at the end of a frame
        ttk.Separator(self.frame_q6).grid(columnspan=5, sticky="ew")

        ''' ================================================================================================================================================================= '''
        
        ''' -------- Section q7 for the worksheet -------- '''
        
        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_q7 = ttk.Frame(self.useable_frame)
        self.frame_q7.config(padding = (10,10))
        self.frames_list.append(self.frame_q7)

        ''' -------- Question q7 -------- '''

        ### These are the things that you need to change to build your worksheet 
        max_score_q7 = 1.0 ### Record the max score for this question
        penalty_q7 = 0.25 ### Record the penalty for each incorrect attempt
        question_q7 = "Question 7: Enter in your y axis label. Take care to follow all instructions given in the text above" ###Add in the text for the question you want to ask. The question has to be kept inside the quote marks for the code to work, e.g. "This is the text for my question"
        sf_q7 = None ### How many significant figures should the answer be rounded to? Enter None if you do not want any rounding, or self.sigfig to call the global sigfig number that was defined earlier
        
        ### Calling graphing data from previous question answers
        self.x_data_location_q7 = self.entry_q5x ### This tells the worksheet which previous question to use in order to find the x data. This format ... = self.entry_q5x.get() indicates the code with get x data from question 5 (q5). To get data from a different question, replace q5 with the appropriate q number
        self.y_data_location_q7 = self.entry_q5y ### This tells the worksheet which previous question to use in order to find the y data. This format ... = self.entry_q5y.get() indicates the code with get y data from question 5 (q5). To get data from a different question, replace q5 with the appropriate q number
        self.xlabel_location_q7 = self.entry_q6 ### As above, this gets information for the xaxis label from q6. To get the label from a different question, replace q6 with the appropriate question label.
        
        ### Comma separated list of possible answers. Any of these answers would be marked as correct. If statement combines the fact that nu and 0.5 can be represented in different ways
        p_val = ['p', '{p}', '\mathrm{p}'] #All possible ways of expressing p in ip
        answer_q7 = ["$i_" + p +"$ / A" for p in p_val] + ["$i_" + p + "\mathrm{A}$" for p in p_val] 
        
        wrong_answers_q7 = [["i$_" + p +"$/A" for p in p_val], ["$i_" + p +"/A$" for p in p_val], ["$i_" + p +"$/mA" for p in p_val] + ["$i_" + p +"$/$\mu$A" for p in p_val] + ["$i_" + p +"/\mu$A" for p in p_val] + ["$i_" + p +"$/μA" for p in p_val]]
        feedback_q7 = ["It looks like this code would create a y axis label where the variable is not in italics. Pay close attention to the formatting instructions for a good axis label. Variables should be in italics, and units should not. \n\nFor example, time in seconds should be given as $t$ / s, so that the variable t is italic and the unit s is not.", "It looks like this code would create a y axis that is all italics. Note the guidance in the smart worksheet. Only variables should be italic. Units should not. A time axis in seconds should therefore be coded as $t$ / s. You can move $ signs to only surround characters that you wish to be italic, or numbers that should be super/subscript. By keeping only the key characters inside the $ signs, you can avoid accdientally making everything italic.", "It looks like you have tried to enter values using the wrong units. You were asked to include all of your data using SI units. The SI unit for current is amps (A), not mA or μA. You may want to go back and check the data that you entered into your graph. Your y data in amps should be very small (around 10⁻⁶ A)" ,  "Ensure that you have included the correct units for your axis label. Also, check your Python text formatting to achieve subscripts and/or superscripts where needed. You can take advantage of the Preview button to see how your code will look on the plot without penalty."] ### Add in the message you want to pop up here, inside the quote marks after message =.
        solved_feedback_q7 = ["The correct units for peak current is amps, or A. In terms of python coding, peak current (𝑖ₚ) can be coded using math mode and subscripts, where an underscore (_) gives you the subscript. Only the 𝑖ₚ terms should be inside the $ signs, as we don't want the amps unit (A) to be italic. This gives the correct python coding as $i_p$ / A.\n\nIf you were trying to enter an answer in milliamps or microamps, this was marked wrong as you were asked to use SI units. You should go back and check the values that you submitted to your graph and ensure the numbers entered are in amps. They should be very small, around 10⁻⁶ A."]
        #The lists create a record of all of the buttons, entry fields etc as they are made so they can be disabled after an answer is given and graded
        self.button_list_q7 = []
        self.entry_list_q7 = []
        
        # This creates a title for an entry field
        ttk.Label(self.frame_q7, wraplength=450, text = question_q7).grid(row=0, column=0, padx=10, sticky='w')
        # This creates an entry window for the user to add data. Line 1 creates the entry box, line 2 adds it to position on the grid. 
        self.entry_q7 = ttk.Entry(self.frame_q7, width = 30)
        self.entry_q7.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        self.entry_list_q7.append(self.entry_q7)

        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a preview button
        self.button_preview_q7 = ttk.Button(self.frame_q7, text = "Preview", command=lambda: self.plot_scatter("q7", self.frame_plot1, self.x_data_location_q7.get(), self.y_data_location_q7.get(), self.button_list_q7, self.entry_list_q7, xlabel=self.xlabel_location_q7.get(), ylabel=self.entry_q7.get(), trendline=True, preview=True))
        self.button_preview_q7.grid(row=0, column=2, padx=10, pady=5, sticky = 'w')
        #Preview buttons are not added to the list of buttons, as the button list is used to disable buttons after submission. There is no need to disable a preview button and it can be useful for the student to use preview to visualise a correcct answer if they have used "Solve"
        
        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a submit button
        self.button_submit_q7 = ttk.Button(self.frame_q7, text = "Submit", command=lambda: [self.submit_1answer("q7", self.frame_q7, self.entry_q7.get(), answer_q7, max_score_q7, penalty_q7, feedback_q7, wrong_answers_q7, self.button_list_q7, self.entry_list_q7), self.button_preview_q7.invoke()] )
        self.button_submit_q7.grid(row=0, column=3, padx=10, pady=5, sticky = 'w')
        self.button_list_q7.append(self.button_submit_q7)
        
        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a solve button
        self.button_solve_q7 = ttk.Button(self.frame_q7, text = "Solve", command=lambda: [self.solve_1answer("q7", self.frame_q7, answer_q7, max_score_q7, solved_feedback_q7, self.button_list_q7, self.entry_list_q7) , self.button_preview_q7.invoke()] )
        self.button_solve_q7.grid(row=0, column=4, padx=10, pady=5, sticky = 'w')
        self.button_list_q7.append(self.button_solve_q7)
        
        ''' -------- Add components into relevant dictionaries -------- '''
        # This section will be used to auto complete and block out entries that have already been completed if students close and then reopen the worksheet
        self.entry_dictionary["q7"] = self.entry_list_q7
        self.button_dictionary["q7"] = self.button_list_q7
        self.label_loc_dictionary["q7"] = [6, 0, self.frame_q7] #If a student has already entered an answer on a previous attempt, this is where the label containing their score will appear. Format is [column, row, frame number]
        self.question_list.append("q7")
        
        ''' -------- Add in the separator line between the sections -------- '''
        #This adds a separator line at the end of a frame
        ttk.Separator(self.frame_q7).grid(columnspan=5, sticky="ew")
    
        ''' ================================================================================================================================================================= '''
        
        
        ''' -------- Section q8 for the worksheet -------- '''
        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_q8 = ttk.Frame(self.useable_frame)
        self.frame_q8.config(padding = (10,10))
        self.frames_list.append(self.frame_q8)

        #The lists create a record of all of the buttons, entry fields etc as they are made so they can be disabled after an answer is given and graded
        self.button_list_q8 = []
        self.entry_list_q8 = []

        ''' -------- Question  q8 -------- '''
        ### These are the things that you need to change to build your worksheet 
        question_q8 = "Question 8: What is the gradient of your trendline? Use a linear regression to ensure you have sufficient precision." ###Add in the text for the question you want to ask. The question has to be kept inside the quote marks for the code to work, e.g. "This is the text for my question"
        max_score_q8 = 2.0 ### Record the max score for this question
        penalty_q8 = 0.5 ### Record the penalty for each incorrect attempt
        sf_q8 = self.sigfig ### How many significant figures should the answer be rounded to? Enter None if you do not want any rounding, or self.sigfig to call the global sigfig number that was defined earlier 
        feedback_q8 = ["It looks like you have carried out the correct calculation but used the wrong data. The value you have entered is negative, but the question asked you to use absolute values of current, i.e. only positive values. You can see the reason for this by checking with the Randles–Ševčík equation, which takes the modulus peak current. \n\nReset the graph above, and enter in the absolute values of peak current as required.  You may want tot take the opportunity to check the other specified data requirements to make sure that you have followed those as well." , "Ensure you are using the correct value from the regression table. Remember that Excel calls the gradient XVariable. This value should just be copied straight out of a regression table without needing any conversions at all, just make sure you are using the correct number of significant figures."]  ### Add in the message you want to pop up here, inside the quote marks after message =.
        solved_feedback_q8 = ["Ensure you are using the correct value from the regression table. Remember that Excel calls the gradient XVariable. This value should just be copied straight out of a regression table without needing any conversions at all, just make sure you are using the correct number of significant figures."]

        ''' -------- Calculate the correct answer based on a previous answer -------- ''' 
        m = ["q5", "m"] ### Use this line to call a value that was calculated separately, such as a gradient or regression value, add in the label for the question where the data was submitted, followed by the label assigned to the parameter. Both should be in quote marks, and inside square brackets, separated by a comma. For example, for a gradient from question 5, enter ["q5", "m"].

        def calculate_answer_q8():
            # The correct answer is called from a combination of the data from a previous question and user defined parameters
            return lambda m : np.abs(float(m)) if np.abs(float(m))<0.01 else ( np.abs(float(m)) / 1e3 if np.abs(float(m))<10  else np.abs(float(m)) / 1e6) ### Use a calculation in python format to calculate the correct answer. The format uses the colon as a separator for all parameters that you would call from a different question. They are first named on the left of the colon, then used in the equation on the right

        answer_q8 = calculate_answer_q8() #This is a preparatory function so the script is ready to do the calculation after a number has been added to the previous question

        ### Use the values option to add in details for all of the values you are taking from other areas of the worksheet. If multiple values are used, separate them with commas inside the square brackets. For example, [m, c, A]. 
        ### The important thing is that these are given in the same order as in your function that calculates the answer.
        values_q8 = [m]
        
        ''' -------- Calculate the wrong answer based on a previous answer -------- ''' 
                ### You will need to add in your own calculations in order to use a previous entry to produce a new answer 
        wrong_answers_q8 = []       
        wrong_values_q8=[]

        def calculate_wrong_q8_1():
            return lambda  m : -1*np.abs(float(m)) ### Use a calculation in python format to calculate the correct answer. value is used to present the number that will be taken from a previous answer

        wrong_q8_1 = calculate_wrong_q8_1() #This is a preparatory function so the script is ready to do the calculation after a number has been added to the previous question
        wrong_answers_q8.append(wrong_q8_1)
        wrong_values_q8.append(values_q8)
        


        ''' -------- Enter the question -------- '''

        # This creates a title for an entry field
        ttk.Label(self.frame_q8, wraplength=450, text = question_q8).grid(row=0, column=0, padx=10, sticky='w')
        # This creates an entry window for the user to add data. Line 1 creates the entry box, line 2 adds it to position on the grid, line 3 adds the entry into the list for later use
        self.entry_q8 = ttk.Entry(self.frame_q8, width = 24)
        self.entry_q8.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        self.entry_list_q8.append(self.entry_q8)

        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a submit button 
        self.button_submit_q8 = ttk.Button(self.frame_q8, text = "Submit", command = lambda: self.submit_1answer("q8", self.frame_q8, self.entry_q8.get(), [answer_q8( *self.input_values(values_q8) )], max_score_q8, penalty_q8, feedback_q8, self.function_list_on_variable_list(wrong_answers_q8, wrong_values_q8), self.button_list_q8, self.entry_list_q8, sf=sf_q8)) #The * by the input values separate the answers from the tuple, so they can be used as inputs for the function
        self.button_submit_q8.grid(row=0, column=3, padx=10, pady=5, sticky = 'w')
        self.button_list_q8.append(self.button_submit_q8)

        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a solve button 
        self.button_solve_q8 = ttk.Button(self.frame_q8, text = "Solve", command = lambda: self.solve_1answer("q8", self.frame_q8, [answer_q8( *self.input_values(values_q8) )],  max_score_q8, feedback_q8, self.button_list_q8, self.entry_list_q8, sf=sf_q8))
        self.button_solve_q8.grid(row=0, column=4, padx=10, pady=5, sticky = 'w')
        self.button_list_q8.append(self.button_solve_q8)

        ''' -------- Add components into relevant dictionaries -------- '''
        # This section will be used to auto complete and block out entries that have already been completed if students close and then reopen the worksheet
        self.entry_dictionary["q8"] = self.entry_list_q8
        self.button_dictionary["q8"] = self.button_list_q8
        self.label_loc_dictionary["q8"] = [6, 0, self.frame_q8] #If a student has already entered an answer on a previous attempt, this is where the label containing their score will appear. Format is [column, row, frame number]
        self.question_list.append("q8")

        ''' -------- Add in the separator line between the sections -------- '''
        #This adds a separator line at the end of a frame
        ttk.Separator(self.frame_q8).grid(columnspan=5, sticky="ew")         
        
        ''' ================================================================================================================================================================= '''
        
        ''' -------- Section q9 introduction for the worksheet -------- '''

        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_q9_intro = ttk.Frame(self.useable_frame)
        self.frame_q9_intro.config(padding = (10,10))
        self.frames_list.append(self.frame_q9_intro)

        ''' -------- Question q9 intro -------- '''        
        
        # This creates an introductory text field
        ttk.Label(self.frame_q9_intro, wraplength=800, text = "For the following questions, it is VERY important that you enter values to the highest possible precision, otherwise the spreadsheet may mark your answer as wrong. For example, if your cell calulates the area as 5.14576574525345134534... do not use 5.1416 in your calculation, refer to the cell so that the calculation uses the full precision value. Using a low precision version may result in a correct answer being marked as incorrect.").grid(row=0, column=0, padx=10, sticky='w')
    
        ''' ================================================================================================================================================================= '''
        
        ''' -------- Section q9 for the worksheet -------- '''
        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_q9 = ttk.Frame(self.useable_frame)
        self.frame_q9.config(padding = (10,10))
        self.frames_list.append(self.frame_q9)
        
        #The lists create a record of all of the buttons, entry fields etc as they are made so they can be disabled after an answer is given and graded
        self.button_list_q9 = []
        self.entry_list_q9 = []
        
        ''' -------- Question  q9 -------- '''
        ### These are the things that you need to change to build your worksheet 
        question_q9 = "Question 9: Use the Randles–Ševčík equation and the gradient from your trendline to determine the diffusion coefficient (D) of copper in m\u00B2 s\u207B\u00B9" ###Add in the text for the question you want to ask. The question has to be kept inside the quote marks for the code to work, e.g. "This is the text for my question"
        max_score_q9 = 4.0 ### Record the max score for this question
        penalty_q9 = 1.0 ### Record the penalty for each incorrect attempt
        sf_q9 = self.sigfig ### How many significant figures should the answer be rounded to? Enter None if you do not want any rounding, or self.sigfig to call the global sigfig number that was defined earlier 
        feedback_q9 = ["It looks like you may have forgotten to square the final term. Don't forget that D in the Randles Ševčík equation is in the form of D¹\u141F², so the final step will be to square your answer", "It looks like you may have used the wrong value of n in your calculation. Using the Randles Ševčík equation equation to calculate the diffusion coefficient works by looking at the peak caused by one electrochemical reaction. What reaction specifically is causing the peak you are looking at? How many electrons are transferred during that reaction?",  "Double check your calculations, and pay particular attention to your unit conversions. As a rough guide, the answer should be on the order of 10\u207B\u00B9\u2070 m, i.e. 1e-10"]  ### Add in the message you want to pop up here, inside the quote marks after message =.
        solved_feedback_q9 = ["The diffusion coefficient (D) can be determined from the gradient of the Randles–Ševčík plot. Looking at the Randles–Ševčík equation, plotting 𝑖ₚ versus v⁻¹\u141F² will leave the gradient as equal to all other terms, 2.69x10⁵ x n³\u141F² x A x c x D¹\u141F² \n\n n is 1, A is your area and c is your concentration, both of which you have already found above.\n\n A quick rearrangement will give the D¹\u141F² = m / (2.69x10⁵ x n³\u141F² x A x c), so D = (m / (2.69x10⁵ x n³\u141F² x A x c))²" ]
        
        ''' -------- Calculate the correct answer based on a previous answer -------- ''' 
        ### You will need to add in your own calculations in order to use a previous entry to produce a new answer         
        c = self.entry_q3 ### Use this line to state which question(s) the value(s) you need for the calculation comes from. In this case, q3 means it is coming from question 3
        a = self.entry_q1 ### Use this line to state which question(s) the value(s) you need for the calculation comes from. In this case, q2 means it is coming from question 2
        m = ["q5", "m"] ### Use this line to call a value that was calculated separately, such as a gradient or regression value, add in the label for the question where the data was submitted, followed by the label assigned to the parameter. Both should be in quote marks, and inside square brackets, separated by a comma. For example, for a gradient from question 5, enter ["q5", "m"].
        
        def calculate_answer_q9():
            # The correct answer is called from a combination of the data from a previous question and user defined parameters
            return lambda m, c, a: (np.abs(float(m)) / ((np.pi*float(a)**2)*float(c)*2.69e5))**2 ### Use a calculation in python format to calculate the correct answer. The format uses the colon as a separator for all parameters that you would call from a different question. They are first named on the left of the colon, then used in the equation on the right
        
        answer_q9 = calculate_answer_q9() #This is a preparatory function so the script is ready to do the calculation after a number has been added to the previous question
        
        ### Use the values option to add in details for all of the values you are taking from other areas of the worksheet. If multiple values are used, separate them with commas inside the square brackets. For example, [m, c, A]. 
        ### The important thing is that these are given in the same order as in your function that calculates the answer.
        values_q9 = [m , c , a]
        
                
        ''' -------- Calculate the wrong answer based on a previous answer -------- ''' 
                ### You will need to add in your own calculations in order to use a previous entry to produce a new answer 
        wrong_answers_q9 = []       
        wrong_values_q9=[]
        
        def calculate_wrong_q9_1():
            return lambda m, c, a: (np.abs(float(m)) / ((np.pi*float(a)**2)*float(c)*2.69e5)) ### Use a calculation in python format to calculate the correct answer. value is used to present the number that will be taken from a previous answer
        
        wrong_q9_1 = calculate_wrong_q9_1() #This is a preparatory function so the script is ready to do the calculation after a number has been added to the previous question
        wrong_answers_q9.append(wrong_q9_1)
        wrong_values_q9.append(values_q9)
        
        def calculate_wrong_q9_2():
            return lambda m, c, a: (np.abs(float(m)) / ((np.pi*float(a)**2)*(2**1.5)*float(c)*2.69e5))**2 ### Use a calculation in python format to calculate the correct answer. value is used to present the number that will be taken from a previous answer
        
        wrong_q9_2 = calculate_wrong_q9_2() #This is a preparatory function so the script is ready to do the calculation after a number has been added to the previous question
        wrong_answers_q9.append(wrong_q9_2)
        wrong_values_q9.append(values_q9)
        
        ''' -------- Enter the question -------- '''
        
        # This creates a title for an entry field
        ttk.Label(self.frame_q9, wraplength=450, text = question_q9).grid(row=0, column=0, padx=10, sticky='w')
        # This creates an entry window for the user to add data. Line 1 creates the entry box, line 2 adds it to position on the grid, line 3 adds the entry into the list for later use
        self.entry_q9 = ttk.Entry(self.frame_q9, width = 24)
        self.entry_q9.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        self.entry_list_q9.append(self.entry_q9)
        
        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a submit button 
        self.button_submit_q9 = ttk.Button(self.frame_q9, text = "Submit", command = lambda: self.submit_1answer("q9", self.frame_q9, self.entry_q9.get(), [answer_q9( *self.input_values(values_q9) )], max_score_q9, penalty_q9, feedback_q9, self.function_list_on_variable_list(wrong_answers_q9, wrong_values_q9), self.button_list_q9, self.entry_list_q9, sf=sf_q9)) #The * by the input values separate the answers from the tuple, so they can be used as inputs for the function
        self.button_submit_q9.grid(row=0, column=3, padx=10, pady=5, sticky = 'w')
        self.button_list_q9.append(self.button_submit_q9)
        
        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a solve button 
        self.button_solve_q9 = ttk.Button(self.frame_q9, text = "Solve", command = lambda: self.solve_1answer("q9", self.frame_q9, [answer_q9( *self.input_values(values_q9) )],  max_score_q9, solved_feedback_q9, self.button_list_q9, self.entry_list_q9, sf=sf_q9))
        self.button_solve_q9.grid(row=0, column=4, padx=10, pady=5, sticky = 'w')
        self.button_list_q9.append(self.button_solve_q9)
        
        ''' -------- Add components into relevant dictionaries -------- '''
        # This section will be used to auto complete and block out entries that have already been completed if students close and then reopen the worksheet
        self.entry_dictionary["q9"] = self.entry_list_q9
        self.button_dictionary["q9"] = self.button_list_q9
        self.label_loc_dictionary["q9"] = [6, 0, self.frame_q9] #If a student has already entered an answer on a previous attempt, this is where the label containing their score will appear. Format is [column, row, frame number]
        self.question_list.append("q9")
        
        ''' -------- Add in the separator line between the sections -------- '''
        #This adds a separator line at the end of a frame
        ttk.Separator(self.frame_q9).grid(columnspan=5, sticky="ew")    
        
        ''' ================================================================================================================================================================= '''

        ''' -------- Section q10 for the worksheet -------- '''
        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_q10 = ttk.Frame(self.useable_frame)
        self.frame_q10.config(padding = (10,10))
        self.frames_list.append(self.frame_q10)

        #The lists create a record of all of the buttons, entry fields etc as they are made so they can be disabled after an answer is given and graded
        self.button_list_q10 = []
        self.entry_list_q10 = []
        self.flag_list_q10 = []

        ''' -------- Question  q10 -------- '''
        ### These are the things that you need to change to build your worksheet 
        question_q10 = "Question 10: Perform a linear regression in Excel to determine the 95% confidence intervals for your linear fit." ###Add in the text for the question you want to ask. The question has to be kept inside the quote marks for the code to work, e.g. "This is the text for my question"
        max_score_q10 = 2.0 ### Record the max score for this question
        penalty_q10 = 0.5 ### Record the penalty for each incorrect attempt
        feedback_q10 = ["It looks like you may have entered your confidence values the wrong way around. The headings 'lower' and 'upper' 95% confidence values should be labelled clearly in Excel. The upper and lower refers to the magnitude of the value, so this canbe confusing when working with negative gradients. Double check the regression table headings to make sure you are using the correct one", "It looks like you may have used the confidence values from the intercept rather than for the gradient. Remember that Excel calls the gradient 'XVariable' in the regression table. You should select the upper and lower confidence values from this row.", "Ensure you are using the correct value from the regression table. Remember that Excel calls the gradient XVariable. This value should just be copied straight out of a regression table without needing any conversions at all, just make sure you are using the correct number of significant figures."]  ### Add in the message you want to pop up here, inside the quote marks after message =.
        wrong_answers_q10 = []
        sf_q10 = self.sigfig ### How many significant figures should the answer be rounded to? Enter None if you do not want any rounding, or self.sigfig to call the global sigfig number that was defined earlier 
        self.labels_q10 = ["Lower 95% :", "Upper 95% :"] ### Add in the labels that will go over the top of each entry box
        answer_cols_q10 = 2 ### How many columns do you want the answer boxes to be divided between?

        ''' -------- Calculate the correct answer based on a previous answer -------- '''      
        answer_list_q10 = []
        self.values_list_q10 = []
        
        ### You will need to add in your own calculations in order to use a previous entry to produce a new answer         
        CI_low = [["q5", "CI_low"]] ### Use this line to call a value from an entry box or one that was calculated separately such as a gradient or regression value, add in the label for the question where the data was submitted, followed by the label assigned to the parameter. Both should be in quote marks, and inside square brackets, separated by a comma. For example, for a gradient from question 5, enter ["q5", "m"].
        CI_high = [["q5", "CI_high"]] ### You should include once set of values per question
        c_CI_low = [["q5", "c_CI_low"]]
        c_CI_high = [["q5", "c_CI_high"]]

        self.values_list_q10 = [CI_low, CI_high] ### Add the values here in the same order as they are required based on the labels written in self.labels_q1
        
        def calculate_answer_q10(): #This is the function where you will calculate the answer. In the case where you want multiple functions, use _1, _2, _3 etc after the question number so they can be distinguished
            # The correct answer is called from a combination of the data from a previous question and user defined parameters
            return lambda CI : float(CI) ### Use a calculation in python format to calculate the correct answer. The format uses the colon as a separator for all parameters that you would call from a different question. They are first named on the left of the colon, then used in the equation on the right. Any parameters you use should be in a float function - i.e. to use a parameter called m in the equation 2*m, enter 2*float(m)

        for i in range(len(self.values_list_q10)):
            answer_list_q10.append(calculate_answer_q10()) # a list of functions is made containing the same function duplicated to match the number of paramters that are being added. This is done for wider code cross compatibility 


        ''' -------- Calculate the wrong answer based on a previous answer -------- ''' 
        self.values_list_q10_wrong = []
        
                ### You will need to add in your own calculations in order to use a previous entry to produce a new answer 
        def calculate_wrong_q10_1():
            return lambda CI : float(CI) ### Use a calculation in python format to calculate the correct answer. value is used to present the number that will be taken from a previous answer
        
        self.values_list_q10_wrong += [CI_high, CI_low]
        
        for i in range(len(self.values_list_q10)):
            wrong_answers_q10.append(calculate_wrong_q10_1()) # a list of functions is made containing the same function duplicated to match the number of paramters that are being added. This is done for wider code cross compatibility 

        def calculate_wrong_q10_2():
            return lambda CI : float(CI) ### Use a calculation in python format to calculate the correct answer. value is used to present the number that will be taken from a previous answer
        
        self.values_list_q10_wrong += [c_CI_low, c_CI_high]
        
        for i in range(len(self.values_list_q10)):
            wrong_answers_q10.append(calculate_wrong_q10_2()) # a list of functions is made containing the same function duplicated to match the number of paramters that are being added. This is done for wider code cross compatibility 

        

        ''' -------- Enter the question -------- '''
        row = 1
        column = 0
            
        # This creates headings to go on top of entry fields in a table format
        for i in range(len(self.labels_q10)):
            
            if column == answer_cols_q10 *2 :#Dividing all of the entry labels up between 2 columns 
                column = 0
                row = row+3
            ttk.Label(self.frame_q10, text = self.labels_q10[i]).grid(column = column, row = row+1) #Add in the label to go above the entry box
            flag = ttk.Label(self.frame_q10, text = "")
            flag.grid(column = column+1, row = row, sticky="w") #Add in a blank label ready to receive either a correct or incorrect flag
            entry_box = ttk.Entry(self.frame_q10, width = 20)
            entry_box.grid(column = column+1, row = row+1, padx=5, pady=5, sticky='w') #Add in the entry box ready to take the answers
            self.entry_list_q10.append(entry_box)
            self.flag_list_q10.append(flag)
            column = column + 2

        # This creates a title for an entry field
        ttk.Label(self.frame_q10, wraplength=600, text = question_q10).grid(row=0, column=0, columnspan = column, padx=10, sticky='w')

        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a submit button 
        self.button_submit_q10 = ttk.Button(self.frame_q10, text = "Submit", command = lambda: self.submit_answer_array("q10", self.frame_q10, self.input_values(self.entry_list_q10) , self.function_list_on_variable_list(answer_list_q10, self.values_list_q10), max_score_q10, penalty_q10, feedback_q10, self.function_list_on_variable_list(wrong_answers_q10, self.values_list_q10_wrong), self.button_list_q10, self.entry_list_q10, self.flag_list_q10, answer_cols_q10, sf=sf_q10)) 
        self.button_submit_q10.grid(row=0, column=column+1, rowspan=row+3, padx=10, pady=5, sticky = 'w')
        self.button_list_q10.append(self.button_submit_q10)

        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a solve button 
        self.button_solve_q10 = ttk.Button(self.frame_q10, text = "Solve", command = lambda: self.solve_answer_array("q10", self.frame_q10, self.function_list_on_variable_list(answer_list_q10, self.values_list_q10),  max_score_q10, feedback_q10, self.button_list_q10, self.entry_list_q10, self.flag_list_q10, answer_cols_q10, sf=sf_q10))
        self.button_solve_q10.grid(row=0, column=column+2, padx=10, rowspan=row+3, pady=5, sticky = 'w')
        self.button_list_q10.append(self.button_solve_q10)

        # The submit and solve button functions are a bit convoluted in design. This has been done in order to make the code more user friendly for novice Python users to ammend
        # The function to calculate the answer is written by the user, taking in values either from other entry boxes or that have been calculated by other functions. Python by default would run this immediately when the worksheet is opened, which would throw in an error since no values have been entered yet! 
        # To get around this, the function includes a lambda function and is passed to a list containing all of the functions that will be used in this question. This allows the user to change the name of their function without having to edit any other code further downstream
        # The submit_answer_array function combined user entered values (question number, frame number etc), with the functions and variables in order to both calculate the answer and carry out the grading and feedback submission. 
        # self.input_values(self.entry_list_q10) takes all of the values from the entry boxes that have been created, and assembles them in the same order they were created. This allows them to be checked one, by one against the list of answers
        # self.function_list_on_variable_list(answer_list_q10, self.values_list_q10) is a fairly convoluted way to get hold of all of the answers from the function(s) created by the user. The self.function_list_on_variable_list() part does the answer comparing and solving. Inside the brackets, the (answer_list_q10, self.values_list_q10) combines the list of functions and the list of values, so that each function takes the corresponding value to calculate the correct answer
        # This could certainly be done in a more Pythonic way, but the aim is to allow manipulation of the code by a novice user with minimal steps, which this hopefully achieves. 
        
        ''' -------- Add components into relevant dictionaries -------- '''
        # This section will be used to auto complete and block out entries that have already been completed if students close and then reopen the worksheet
        self.entry_dictionary["q10"] = self.entry_list_q10
        self.button_dictionary["q10"] = self.button_list_q10
        self.label_loc_dictionary["q10"] = [answer_cols_q10*2 +3 , 2, self.frame_q10] #If a student has already entered an answer on a previous attempt, this is where the label containing their score will appear. Format is [column, row, frame number]
        self.question_list.append("q10")
        
        ''' -------- Add in the separator line between the sections -------- '''
        #This adds a separator line at the end of a frame
        ttk.Separator(self.frame_q10).grid(columnspan=10, sticky="ew")    

        ''' ================================================================================================================================================================= '''
        
        
        ''' -------- Section q11 for the worksheet -------- '''
        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_q11 = ttk.Frame(self.useable_frame)
        self.frame_q11.config(padding = (10,10))
        self.frames_list.append(self.frame_q11)

        #The lists create a record of all of the buttons, entry fields etc as they are made so they can be disabled after an answer is given and graded
        self.button_list_q11 = []
        self.entry_list_q11 = []
        self.flag_list_q11 = []

        ''' -------- Question  q11 -------- '''
        ### These are the things that you need to change to build your worksheet 
        question_q11 = "Question 11: Based on this, determine the min and max possible values of D for copper in m² s⁻¹" ###Add in the text for the question you want to ask. The question has to be kept inside the quote marks for the code to work, e.g. "This is the text for my question"
        max_score_q11 = 2.0 ### Record the max score for this question
        penalty_q11 = 0.5 ### Record the penalty for each incorrect attempt
        feedback_q11 = ["It looks like you may have forgotten to square the final term. The calculation here is the same as for how you calculated your diffusion coefficient from the gradient. Don't forget that D in the Randles Ševčík equation is in the form of D¹\u141F², so the final step will be to square your answer", "The calculation here is the same as for how you calculated your diffusion coefficient from the gradient. Double check your calculations, and pay particular attention to your unit conversions. Most of the complicated unit conversion is handled by the 2.69x10⁵ constant, so if you want units of m² s⁻¹ you just need to make sure that current and scan rate are in SI units (A and V/s respectively), and that all dimensional terms are in metres.\n\n Ensure you are using the correct value from the regression table, Excel calls gradient XVariable. As a check, your confidence values should be very close to the gradeint. Remember that the confidence levels are expressed with the same units as the gradient, so the conversion of a 95% confidence value to a diffusion coefficient would be the same calculation as the conversion of a gradient to a diffusion coefficient."]  ### Add in the message you want to pop up here, inside the quote marks after message =.
        self.labels_q11 = ["Lower D value", "Upper D value"] ### Add in the labels that will go over the top of each entry box
        answer_cols_q11 = 2 ### How many columns do you want the answer boxes to be divided between?
        sf_q11 = self.sigfig ### How many significant figures should the answer be rounded to? Enter None if you do not want any rounding, or self.sigfig to call the global sigfig number that was defined earlier 
        wrong_answers_q11 = []

        ''' -------- Calculate the correct answer based on a previous answer -------- ''' 

        answer_list_q11 = []
        self.values_list_q11 = []

        ### You will need to add in your own calculations in order to use a previous entry to produce a new answer         
        c = self.entry_q3 ### Use this line to state which question(s) the value(s) you need for the calculation comes from. In this case, q3 means it is coming from question 3
        a = self.entry_q1 ### Use this line to state which question(s) the value(s) you need for the calculation comes from. In this case, q2 means it is coming from question 2

        CI_low = ["q5", "CI_low"] ### Use this line to call a value that was calculated separately, such as a gradient or regression value, add in the label for the question where the data was submitted, followed by the label assigned to the parameter. Both should be in quote marks, and inside square brackets, separated by a comma. For example, for a gradient from question 5, enter ["q5", "m"].
        CI_high = ["q5", "CI_high"] ### Use this line to call a value that was calculated separately, such as a gradient or regression value, add in the label for the question where the data was submitted, followed by the label assigned to the parameter. Both should be in quote marks, and inside square brackets, separated by a comma. For example, for a gradient from question 5, enter ["q5", "m"].

        varied_values_list_q11 = [CI_low, CI_high] ### Add the values that will be different for every question here in the same order as they are required based on the labels written in self.labels_q11
        common_values_list_q11 = [c, a] ### Add the values that will be the same for every question here in the same order as they are required based on the labels written in self.labels_q11
        
        for i in range(len(varied_values_list_q11)):
            temp = []
            temp.append(varied_values_list_q11[i])
            for j in range(len(common_values_list_q11)):
                temp.append(common_values_list_q11[j])
            self.values_list_q11.append(temp)

        def calculate_answer_q11():
            # The correct answer is called from a combination of the data from a previous question and user defined parameters
            ### For the values in the function below, add in functions that are always the same first, and items that change for every entry last. For example, for a function of a * b + c where c is always the same but a and b will change for each answer, the function should be defined by return lambda c, a, b = a * b + c
            return lambda CI, c, a: (float(CI) / ((np.pi*float(a)**2)*float(c)*2.69e5))**2 ### Use a calculation in python format to calculate the correct answer. The format uses the colon as a separator for all parameters that you would call from a different question. They are first named on the left of the colon, then used in the equation on the right
        
        for i in range(len(self.values_list_q11)):
            answer_list_q11.append(calculate_answer_q11()) # a list of functions is made containing the same function duplicated to match the number of paramters that are being added. This is done for wider code cross compatibility 

        
        ''' -------- Calculate the wrong answer based on a previous answer -------- ''' 
                ### You will need to add in your own calculations in order to use a previous entry to produce a new answer 
        def calculate_wrong_q11_1():
            return lambda CI, c, a: (float(CI) / ((np.pi*float(a)**2)*float(c)*2.69e5)) ### Use a calculation in python format to calculate the correct answer. value is used to present the number that will be taken from a previous answer

        self.values_list_q11_wrong_1 = []
        
        varied_values_list_q11 = [CI_high, CI_low] ### Add the values that will be different for every question here in the same order as they are required based on the labels written in self.labels_q11
        common_values_list_q11 = [c, a] ### Add the values that will be the same for every question here in the same order as they are required based on the labels written in self.labels_q11

        for i in range(len(varied_values_list_q11)):
            temp = []
            temp.append(varied_values_list_q11[i])
            for j in range(len(common_values_list_q11)):
                temp.append(common_values_list_q11[j])
            self.values_list_q11_wrong_1.append(temp)

        for i in range(len(self.values_list_q11_wrong_1)):
            wrong_answers_q11.append(calculate_wrong_q11_1()) # a list of functions is made containing the same function duplicated to match the number of paramters that are being added. This is done for wider code cross compatibility 

        


        ''' -------- Enter the question -------- '''
            
        row = 1
        column = 0
            
        # This creates headings to go on top of entry fields in a table format
        for i in range(len(self.labels_q11)):
            
            if column == answer_cols_q11 *2 :#Dividing all of the entry labels up between 2 columns 
                column = 0
                row = row+3
            ttk.Label(self.frame_q11, text = self.labels_q11[i]).grid(column = column, row = row+1) #Add in the label to go above the entry box
            flag = ttk.Label(self.frame_q11, text = "")
            flag.grid(column = column+1, row = row, sticky="w") #Add in a blank label ready to receive either a correct or incorrect flag
            entry_box = ttk.Entry(self.frame_q11, width = 20)
            entry_box.grid(column = column+1, row = row+1, padx=5, pady=5, sticky='w') #Add in the entry box ready to take the answers
            self.entry_list_q11.append(entry_box)
            self.flag_list_q11.append(flag)
            column = column + 2

        # This creates a title for an entry field
        ttk.Label(self.frame_q11, wraplength=600, text = question_q11).grid(row=0, column=0, columnspan = column, padx=10, sticky='w')
        
        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a submit button 
        self.button_submit_q11 = ttk.Button(self.frame_q11, text = "Submit", command = lambda: self.submit_answer_array("q11", self.frame_q11, self.input_values(self.entry_list_q11) , self.function_list_on_variable_list(answer_list_q11, self.values_list_q11), max_score_q11, penalty_q11, feedback_q11, self.function_list_on_variable_list(wrong_answers_q11, self.values_list_q11_wrong_1), self.button_list_q11, self.entry_list_q11, self.flag_list_q11, answer_cols_q11, sf=sf_q11)) 
        self.button_submit_q11.grid(row=0, column=column+1, rowspan=row+3, padx=10, pady=5, sticky = 'w')
        self.button_list_q11.append(self.button_submit_q11)

        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a solve button 
        self.button_solve_q11 = ttk.Button(self.frame_q11, text = "Solve", command = lambda: self.solve_answer_array("q11", self.frame_q11, self.function_list_on_variable_list(answer_list_q11, self.values_list_q11),  max_score_q11, feedback_q11, self.button_list_q11, self.entry_list_q11, self.flag_list_q11, answer_cols_q11, sf=sf_q11))
        self.button_solve_q11.grid(row=0, column=column+2, padx=10, rowspan=row+3, pady=5, sticky = 'w')
        self.button_list_q11.append(self.button_solve_q11)

        # The submit and solve button functions are a bit convoluted in design. This has been done in order to make the code more user friendly for novice Python users to ammend
        # The function to calculate the answer is written by the user, taking in values either from other entry boxes or that have been calculated by other functions. Python by default would run this immediately when the worksheet is opened, which would throw in an error since no values have been entered yet! 
        # To get around this, the function includes a lambda function and is passed to a list containing all of the functions that will be used in this question. This allows the user to change the name of their function without having to edit any other code further downstream
        # The submit_answer_array function combined user entered values (question number, frame number etc), with the functions and variables in order to both calculate the answer and carry out the grading and feedback submission. 
        # self.input_values(self.entry_list_q11) takes all of the values from the entry boxes that have been created, and assembles them in the same order they were created. This allows them to be checked one, by one against the list of answers
        # self.function_list_on_variable_list(answer_list_q11, self.values_list_q11) is a fairly convoluted way to get hold of all of the answers from the function(s) created by the user. The self.function_list_on_variable_list() part does the answer comparing and solving. Inside the brackets, the (answer_list_q11, self.values_list_q11) combines the list of functions and the list of values, so that each function takes the corresponding value to calculate the correct answer
        # This could certainly be done in a more Pythonic way, but the aim is to allow manipulation of the code by a novice user with minimal steps, which this hopefully achieves. 
        
        ''' -------- Add components into relevant dictionaries -------- '''
        # This section will be used to auto complete and block out entries that have already been completed if students close and then reopen the worksheet
        self.entry_dictionary["q11"] = self.entry_list_q11
        self.button_dictionary["q11"] = self.button_list_q11
        self.label_loc_dictionary["q11"] = [answer_cols_q11*2 +3 , 2, self.frame_q11] #If a student has already entered an answer on a previous attempt, this is where the label containing their score will appear. Format is [column, row, frame number]
        self.question_list.append("q11")
        
        ''' -------- Add in the separator line between the sections -------- '''
        #This adds a separator line at the end of a frame
        ttk.Separator(self.frame_q11).grid(columnspan=10, sticky="ew")    

        ''' ================================================================================================================================================================= '''

        ''' -------- Section q12 for the worksheet -------- '''
        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_q12 = ttk.Frame(self.useable_frame)
        self.frame_q12.config(padding = (10,10))
        self.frames_list.append(self.frame_q12)
        
        #The lists create a record of all of the buttons, entry fields etc as they are made so they can be disabled after an answer is given and graded
        self.button_list_q12 = []
        self.entry_list_q12 = []
        
        ''' -------- Question  q12 -------- '''
        ### These are the things that you need to change to build your worksheet 
        question_q12 = "Question 12: Finally what is the error on your calculated value of D in m² s⁻¹?" ###Add in the text for the question you want to ask. The question has to be kept inside the quote marks for the code to work, e.g. "This is the text for my question"
        max_score_q12 = 2.0 ### Record the max score for this question
        penalty_q12 = 0.5 ### Record the penalty for each incorrect attempt
        feedback_q12 = ["Remember that the error is defined as the maximum difference between the upper and lower D values, as were calculated from the 95% confidence values, and the actual value of D. It looks like you have entered the smallest of these two values, rather than the largest. Replace your answer with the larger of the two options. You can use a MAX function to determine this, or read the values directly out of Excel." , "Remember that the error is defined as the maximum difference between the upper and lower D values, as were calculated from the 95% confidence values, and the actual value of D. It looks like you have entered the difference between the lower and upper values (Dmax - Dmin), rather than the largest difference between the values and D (max(Dmax - D, D - Dmin)." , "Remember that the error is defined as the maximum difference between the upper and lower D values, as were calculated from the 95% confidence values, and the actual value of D. You have already calculated these values in the previous step, or if you hit solve they are not displayed in the boxes. \n\nThe error should be the difference between either the upper D value and D, or the lower D value and D, whichever is larger. You do not need to add in ± or any signs or symbols along with your answer here."] ### Add in the message you want to pop up here, inside the quote marks after message =.
        sf_q12 = self.sigfig ### How many significant figures should the answer be rounded to? Enter None if you do not want any rounding, or self.sigfig to call the global sigfig number that was defined earlier 
        wrong_answers_q12 = []
        
        ### You will need to add in your own calculations in order to use a previous entry to produce a new answer         
        c = self.entry_q3 ### Use this line to state which question(s) the value(s) you need for the calculation comes from. In this case, q3 means it is coming from question 3
        a = self.entry_q1 ### Use this line to state which question(s) the value(s) you need for the calculation comes from. In this case, q2 means it is coming from question 2
        m = ["q5", "m"] ### Use this line to call a value that was calculated separately, such as a gradient or regression value, add in the label for the question where the data was submitted, followed by the label assigned to the parameter. Both should be in quote marks, and inside square brackets, separated by a comma. For example, for a gradient from question 5, enter ["q5", "m"].
        CI_low = ["q5", "CI_low"] ### Use this line to call a value from an entry box or one that was calculated separately such as a gradient or regression value, add in the label for the question where the data was submitted, followed by the label assigned to the parameter. Both should be in quote marks, and inside square brackets, separated by a comma. For example, for a gradient from question 5, enter ["q5", "m"].
        CI_high = ["q5", "CI_high"] ### Use this line to call a value from an entry box or one that was calculated separately such as a gradient or regression value, add in the label for the question where the data was submitted, followed by the label assigned to the parameter. Both should be in quote marks, and inside square brackets, separated by a comma. For example, for a gradient from question 5, enter ["q5", "m"].
       
        ''' -------- Calculate the correct answer based on a previous answer -------- ''' 
        ### You will need to add in your own calculations in order to use a previous entry to produce a new answer 
        def calculate_answer_q12():
            return lambda CI_high, CI_low, m, c, a: np.max ( [ np.abs( ((float(m) / ((np.pi*float(a)**2)*float(c)*2.69e5))**2) - ((float(CI_low) / ((np.pi*float(a)**2)*float(c)*2.69e5))**2) ) , np.abs( ((float(CI_high) / ((np.pi*float(a)**2)*float(c)*2.69e5))**2) - ((float(m) / ((np.pi*float(a)**2)*float(c)*2.69e5))**2) ) ] )


        ### Use the values option to add in details for all of the values you are taking from other areas of the worksheet. If multiple values are used, separate them with commas inside the square brackets. For example, [m, c, A]. 
        ### The important thing is that these are given in the same order as in your function that calculates the answer.
        values_q12 = [CI_high, CI_low, m, c, a]
        answer_q12 = calculate_answer_q12() #This is a preparatory function so the script is ready to do the calculation after a number has been added to the previous question
        
        
        ''' -------- Calculate the wrong answer based on a previous answer -------- ''' 
        
        wrong_values_q12 = []
        
        ### You will need to add in your own calculations in order to use a previous entry to produce a new answer 
        def calculate_wrong_q12_1():
            return lambda CI_high, CI_low, m, c, a: np.min ( [ np.abs( ((float(m) / ((np.pi*float(a)**2)*float(c)*2.69e5))**2) - ((float(CI_low) / ((np.pi*float(a)**2)*float(c)*2.69e5))**2) ) , np.abs( ((float(CI_high) / ((np.pi*float(a)**2)*float(c)*2.69e5))**2) - ((float(m) / ((np.pi*float(a)**2)*float(c)*2.69e5))**2) ) ] )

        wrong_answers_q12.append(calculate_wrong_q12_1())
        wrong_values_q12.append(values_q12)
        
        def calculate_wrong_q12_2():
            return lambda CI_high, CI_low, m, c, a: np.abs( ((float(CI_high) / ((np.pi*float(a)**2)*float(c)*2.69e5))**2) - ((float(CI_low) / ((np.pi*float(a)**2)*float(c)*2.69e5))**2) )

        wrong_answers_q12.append(calculate_wrong_q12_2())
        wrong_values_q12.append(values_q12)


        ''' -------- Enter the question -------- '''
        
        # This creates a title for an entry field
        ttk.Label(self.frame_q12, wraplength=450, text = question_q12).grid(row=0, column=0, padx=10, sticky='w')
        # This creates an entry window for the user to add data. Line 1 creates the entry box, line 2 adds it to position on the grid, line 3 adds the entry into the list for later use
        self.entry_q12 = ttk.Entry(self.frame_q12, width = 24)
        self.entry_q12.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        self.entry_list_q12.append(self.entry_q12)
        
        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a submit button 
        self.button_submit_q12 = ttk.Button(self.frame_q12, text = "Submit", command = lambda: self.submit_1answer("q12", self.frame_q12, self.entry_q12.get(), [answer_q12( *self.input_values(values_q12) )], max_score_q12, penalty_q12, feedback_q12, self.function_list_on_variable_list(wrong_answers_q12, wrong_values_q12),  self.button_list_q12, self.entry_list_q12, sf=sf_q12)) #The * by the input values separate the answers from the tuple, so they can be used as inputs for the function
        self.button_submit_q12.grid(row=0, column=3, padx=10, pady=5, sticky = 'w')
        self.button_list_q12.append(self.button_submit_q12)
        
        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a solve button 
        self.button_solve_q12 = ttk.Button(self.frame_q12, text = "Solve", command = lambda: self.solve_1answer("q12", self.frame_q12, [answer_q12( *self.input_values(values_q12) )],  max_score_q12, feedback_q12, self.button_list_q12, self.entry_list_q12, sf=sf_q12))
        self.button_solve_q12.grid(row=0, column=4, padx=10, pady=5, sticky = 'w')
        self.button_list_q12.append(self.button_solve_q12)
        
        ''' -------- Add components into relevant dictionaries -------- '''
        # This section will be used to auto complete and block out entries that have already been completed if students close and then reopen the worksheet
        self.entry_dictionary["q12"] = self.entry_list_q12
        self.button_dictionary["q12"] = self.button_list_q12
        self.label_loc_dictionary["q12"] = [6, 0, self.frame_q12] #If a student has already entered an answer on a previous attempt, this is where the label containing their score will appear. Format is [column, row, frame number]
        self.question_list.append("q12")
        
        ''' -------- Add in the separator line between the sections -------- '''
        #This adds a separator line at the end of a frame
        ttk.Separator(self.frame_q12).grid(columnspan=5, sticky="ew")    
        
        ''' ================================================================================================================================================================= '''
        
        ''' This code creates a smooth line plot from user submitted data. Data may be entered as comma separated numbers or by copying a column from Excel.
        Code starts with an introduction section that lets the creator introduce the plot, for example encouraging students to use precise values.
        There is an option to add labels to certain regions of the plot. This works with a max/min searching function over certain regions of the data
        Peak labelling function can be deleted with no negative impact on the the plot

        '''
        
        ''' -------- Section q13 introduction for the worksheet -------- '''

        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_q13_intro = ttk.Frame(self.useable_frame)
        self.frame_q13_intro.config(padding = (10,10))
        self.frames_list.append(self.frame_q13_intro)

        ''' -------- Question q13 intro -------- '''        
        
        # This creates an introductory text field
        ttk.Label(self.frame_q13_intro, wraplength=800, text = "This section includes entry boxes for you to plot your full copper CV data (i.e. the CV over the full potential range that shows all possible copper redox peaks. Data should be copied directly over from Excel by copying the column of data. Make sure to only select the numbers, not any text headings. The worksheet will then read down the column that you have pasted in to generate the plot.\n\nYou may also find the following keyboard shortcuts helpful: \tCTRL+C = copy \t CTRL+V = paste \t CTRL+A = select all").grid(row=0, column=0, padx=10, sticky='w')
        
        ''' ================================================================================================================================================================= '''
        
        ''' -------- Section q13 for the worksheet -------- '''

        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_q13 = ttk.Frame(self.useable_frame)
        self.frame_q13.config(padding = (10,10))
        self.frames_list.append(self.frame_q13)
        
        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_plot2 = ttk.Frame(self.useable_frame)
        self.frame_plot2.config(padding = (10,10))
        self.frames_list.append(self.frame_plot2)
        
        #The lists create a record of all of the buttons, entry fields etc as they are made so they can be disabled after an answer is given and graded
        self.button_list_q13 = []
        self.entry_list_q13 = []

        ''' -------- Question q13 -------- ''' 
        ### These are the things that you need to change to build your worksheet 
        ###Enter parameters to be used in the graph - axis titles etc 
        question_q13x = "Question 13a: Enter in the x data for your full copper CV. You may enter your data as comma separated numbers, or by copying a column of data directly from Excel."
        question_q13y = "Question 13b: Enter in the y data for your full copper CV. You may enter your data as comma separated numbers, or by copying a column of data directly from Excel."
        self.xlabel_q13 = "$E$ vs Pt / V" ### enter the x axis title
        self.ylabel_q13 = "$i$ / A" ### enter the y axis title
        
        ### This section is for the labels to be added into the plot. Delete this section if you do not want to add in any peak labels
        self.label_list_q13 = ["1", "2", "3", "4"] ### Enter the labels you would like to add to the plot for peak assignments
        self.label_location_list_q13 = [[0,1] , [0,1] , [0.85,1] , [0,0.25]] ### Enter the region where each of the labels appears in the same order as above. The format is [0,1] where there first number is start point, and the second number is the end point. The value is a multiplier for the length of the data, so [0:1] will look over all data, [0:0.5] will start at the beginning and stop half way, [0.75,1] will start at the 3/4 mark and continue to the end etc.
        self.label_min_max = ["min", "max", "max", "min"] ### Enter whether the peak should be detected as a minimum or maximum peak 
        
        #This creates a title for an entry field
        ttk.Label(self.frame_q13, wraplength=450, text = question_q13x).grid(row=0, column=0, padx=10, sticky='w')
        ttk.Label(self.frame_q13, wraplength=450, text = question_q13y).grid(row=1, column=0, padx=10, sticky='w')
        
        # This creates an entry window for the user to add data. Line 1 creates the entry box, line 2 adds it to position on the grid.
        self.entry_q13x = ttk.Entry(self.frame_q13, width = 30)
        self.entry_q13x.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        self.entry_list_q13.append(self.entry_q13x)

        # This creates an entry window for the user to add data. Line 1 creates the entry box, line 2 adds it to position on the grid.
        self.entry_q13y = ttk.Entry(self.frame_q13, width = 30)
        self.entry_q13y.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        self.entry_list_q13.append(self.entry_q13y)

        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a plot button
        self.button_plot_q13 = ttk.Button(self.frame_q13, text = "Plot", command=lambda: self.plot_line("q13", self.frame_plot2, self.entry_q13x.get(), self.entry_q13y.get(), self.button_list_q13, self.entry_list_q13, xlabel=self.xlabel_q13, ylabel=self.ylabel_q13, label_list = self.label_list_q13, label_loc = self.label_location_list_q13, label_min_max = self.label_min_max))
        self.button_plot_q13.grid(row=0, column=3, rowspan = 2, padx=10, pady=5, sticky = 'w')
        self.button_list_q13.append(self.button_plot_q13)

        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a reset button
        self.button_reset_q13 = ttk.Button(self.frame_q13, text = "Reset", command=lambda:self.reset_line(self.button_list_q13, self.entry_list_q13, self.frame_plot2))
        self.button_reset_q13.grid(row=0, column=4, rowspan = 2, padx=10, pady=5, sticky = 'w')
        
        ''' -------- Add components into relevant dictionaries -------- '''
        # This section will be used to auto complete and block out entries that have already been completed if students close and then reopen the worksheet
        self.entry_dictionary["q13"] = self.entry_list_q13
        self.button_dictionary["q13"] = self.button_list_q13
        self.question_list.append("q13")
        self.plot_button_dictionary["q13"] = self.button_plot_q13
        
        ''' -------- Add in the separator line between the sections -------- '''
        #This adds a separator line at the end of a frame
        ttk.Separator(self.frame_q13).grid(columnspan=5, sticky="ew")
        
        ''' ================================================================================================================================================================= '''
        
        ''' This code allows the student to submit multiple answers into multiple textboxes within the same question. 
        This can be useful for questions with multiple parts or solutions
        The number of answers if defined by giving a number of accepted answers in the list below.
        The example here uses the multiple value set up to assign reactions to multiple peaks in the same graph'''
        
        ''' -------- Section q14 for the worksheet -------- '''
        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_q14 = ttk.Frame(self.useable_frame)
        self.frame_q14.config(padding = (10,10))
        self.frames_list.append(self.frame_q14)

        #The lists create a record of all of the buttons, entry fields etc as they are made so they can be disabled after an answer is given and graded
        self.button_list_q14 = []
        self.entry_list_q14 = []
        self.flag_list_q14 = []

        ''' -------- Question  q14 -------- '''
        ### These are the things that you need to change to build your worksheet 
        question_q14 = "Question 14: Match up the reaction to the peak. Type only the number into the correct box. Not all reactions are present in the CV so some boxes should remain blank. All boxes must be correctly filled and/or correctly empty for full marks to be awarded" ###Add in the text for the question you want to ask. The question has to be kept inside the quote marks for the code to work, e.g. "This is the text for my question"
        max_score_q14 = 4.0 ### Record the max score for this question
        penalty_q14 = 1.0 ### Record the penalty for each incorrect attempt
        feedback_q14 = ["When reading a CV you should trace around the plot in the same direction in which it was scanned experimentally. Follow the scan direction of the CV and consider what species is present before and after the peak. \n\nYou are starting on the right hand side of the CV, with CuSO₄ (you know this because the current is zero, so no net rate of reaction, or you can check your experimental parameters in your notebook / lab script). So, at this point all of the copper is in the form of Cu²⁺. You then sweep to the left and get a negative peak, which will be a reduction. What would Cu²⁺ be reduced to? Sweeping more negatively gives another peak. What species would be reduced here? You can apply the same logic to oxidations (positive peaks) in the forward sweep.\n\n You can also get clues from where you are looking at the CV. If you are looking in a region of positive potential, that will be an oxidising environment, so you could expect to see peaks for reactions involving the most oxidised form of copper, and vice versa.\n\nAnother hint you get from CVs is in the shape of the peaks. Consider a reaction of A + e⁻ → B. If both species are in solution, you would expect the characteristic 'duck shape'. This is because the duck shape is created by diffusion controlled electrochemical reactions - the electrode was to 'wait' for more A to arrive before it can be reduced to B. \n\nHowever, if one species is in solution and the other is a solid, you would expect a very different peak shape. For example, in A(s) + e⁻ → B(aq) you don't have to wait for a A to arrive at the electrode, it's already stuck on the surface. The reduction of A is therefore not diffusion controlled and should give a symmetrical Gaussian peak."]  ### Add in the message you want to pop up here, inside the quote marks after message =.
        solved_feedback_q14 = ["When reading a CV you should trace around the plot in the same direction in which you it was scanned experimentally. Follow the scan direction of the CV and consider what species is present before and after the peak. \n\nYou are starting on the right hand side of the CV, with CuSO₄ (you know this because the current is zero, so no net rate of reaction, or you can check your experimental parameters in your notebook / lab script). So, at this point all of the copper is in the form of Cu²⁺. You then sweep to the left and see a negative peak which tells us we have a reduction. That gives two options, Cu²⁺ → Cu⁺ or Cu²⁺ → Cu⁰\n\nIf we look further to the left of the sweep, there's another reduction peak. This indicates that a further reduction must be possible. Cu⁰ cannot be further reduced, so this peak must be Cu²⁺ → Cu⁺, and so the following peak must be Cu⁺ → Cu⁰. \n\nWe can also use the peak shape to help identify the peak. The peak has that classic 'duck shape', indicating both species are in solution. This is because the duck shape is created by diffusion controlled electrochemical reactions - the electrode was to 'wait' for more A to arrive before it can be reduced to B. Cu⁰ is a solid, which would not give a duck shape peak, so the peak must be due to Cu²⁺ → Cu⁺, which are both solution species."]
        self.labels_q14= ["Cu⁰ → Cu⁺ + e⁻", "Cu⁰ → Cu²⁺ + 2e⁻", "Cu⁺ → Cu²⁺ + e⁻", "Cu⁺ + e⁻ → Cu⁰", "Cu²⁺ + 2e⁻ → Cu⁰", "Cu²⁺ + e⁻ → Cu⁺"] ### Add in the labels for the user to assign 
        self.answers_q14 = [["2"],[""],["3"],["1"],[""],["4"]] ###Add in the correct answer in the same order as above. If the box should remain blank, enter "". To accept a range of answers, enter the range in format (lowest number, highest number). If multiple answers are acceptible, enter each one inside square brackets in the format [["answer 1", "answer 2"], ["answer 1", "answer 2"]]
        answer_cols_q14 = 3 ### How many columns do you want the answer boxes to be divided between?     
        sf_q14 = None ### How many significant figures should the answer be rounded to? Enter None if you do not want any rounding, or self.sigfig to call the global sigfig number that was defined earlier 
        wrong_answers_q14 = []
        
        
        ''' -------- Enter the question -------- '''

        row = 1
        column = 0
        max_col_check = []

        # This creates headings to go on top of entry fields in a table format
        for i in range(len(self.labels_q14)):
            max_col_check.append(column) #keep track of the largest value column where something is added. Submit buttons will then be placed to the right of this. 
            
            if column == answer_cols_q14 *2 :#Dividing all of the entry labels up between 2 columns 
                column = 0
                row = row+3
            ttk.Label(self.frame_q14, text = self.labels_q14[i]).grid(column = column, row = row+1) #Add in the label to go above the entry box
            flag = ttk.Label(self.frame_q14, text = "")
            flag.grid(column = column+1, row = row, sticky="w") #Add in a blank label ready to receive either a correct or incorrect flag
            entry_box = ttk.Entry(self.frame_q14, width = 10)
            entry_box.grid(column = column+1, row = row+1, padx=5, pady=5, sticky='w') #Add in the entry box ready to take the answers
            self.entry_list_q14.append(entry_box)
            self.flag_list_q14.append(flag)
            column = column + 2
            
        column = np.max(max_col_check) #sets the column from this point as being the largest previous column value where something was added. This is important to make sure that the button is still to the right of all entry boxes when there is an uneven distribution of entry boxes across the columns 
        
        ttk.Label(self.frame_q14, wraplength=600, text = question_q14).grid(row=0, column=0, columnspan = column, padx=10, sticky='w')
        
        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a submit button 
        self.button_submit_q14 = ttk.Button(self.frame_q14, text = "Submit", command = lambda: self.submit_answer_array("q14", self.frame_q14, self.input_values(self.entry_list_q14) , self.answers_q14, max_score_q14, penalty_q14, feedback_q14, wrong_answers_q14, self.button_list_q14, self.entry_list_q14, self.flag_list_q14, answer_cols_q14, sf=sf_q14))
        self.button_submit_q14.grid(row=0, column=column+1, rowspan=row+3, padx=5, pady=5, sticky = 'w')
        self.button_list_q14.append(self.button_submit_q14)

        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a solve button 
        self.button_solve_q14 = ttk.Button(self.frame_q14, text = "Solve", command = lambda: self.solve_answer_array("q14", self.frame_q14, self.answers_q14,  max_score_q14, solved_feedback_q14, self.button_list_q14, self.entry_list_q14, self.flag_list_q14, answer_cols_q14, sf=sf_q14))
        self.button_solve_q14.grid(row=0, column=column+2, padx=10, rowspan=row+3, pady=5, sticky = 'w')
        self.button_list_q14.append(self.button_solve_q14)

        # The submit and solve button functions are a bit convoluted in design. This has been done in order to make the code more user friendly for novice Python users to ammend
        # The function to calculate the answer is written by the user, taking in values either from other entry boxes or that have been calculated by other functions. Python by default would run this immediately when the worksheet is opened, which would throw in an error since no values have been entered yet! 
        # To get around this, the function includes a lambda function and is passed to a list containing all of the functions that will be used in this question. This allows the user to change the name of their function without having to edit any other code further downstream
        # The submit_answer_array function combined user entered values (question number, frame number etc), with the functions and variables in order to both calculate the answer and carry out the grading and feedback submission. 
        # self.input_values(self.entry_list_q14) takes all of the values from the entry boxes that have been created, and assembles them in the same order they were created. This allows them to be checked one, by one against the list of answers
        # self.function_list_on_variable_list(answer_list_q14, self.values_list_q14) is a fairly convoluted way to get hold of all of the answers from the function(s) created by the user. The self.function_list_on_variable_list() part does the answer comparing and solving. Inside the brackets, the (answer_list_q14, self.values_list_q14) combines the list of functions and the list of values, so that each function takes the corresponding value to calculate the correct answer
        # This could certainly be done in a more Pythonic way, but the aim is to allow manipulation of the code by a novice user with minimal steps, which this hopefully achieves. 
        
        ''' -------- Add components into relevant dictionaries -------- '''
        # This section will be used to auto complete and block out entries that have already been completed if students close and then reopen the worksheet
        self.entry_dictionary["q14"] = self.entry_list_q14
        self.button_dictionary["q14"] = self.button_list_q14
        self.label_loc_dictionary["q14"] = [answer_cols_q14*2 +3 , 2, self.frame_q14] #If a student has already entered an answer on a previous attempt, this is where the label containing their score will appear. Format is [column, row, frame number]
        self.question_list.append("q14")
        
        ''' -------- Add in the separator line between the sections -------- '''
        #This adds a separator line at the end of a frame
        ttk.Separator(self.frame_q14).grid(columnspan=10, sticky="ew")            
        
        ''' ================================================================================================================================================================= '''
        
        ''' -------- Section q15 for the worksheet -------- '''
        
        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_q15 = ttk.Frame(self.useable_frame)
        self.frame_q15.config(padding = (10,10))
        self.frames_list.append(self.frame_q15)
        
        #The lists create a record of all of the buttons, entry fields etc as they are made so they can be disabled after an answer is given and graded
        self.button_list_q15 = []
        self.entry_list_q15 = []
        
        ''' -------- Question q15 -------- '''   
        ### These are the things that you need to change to build your worksheet 
        max_score_q15 = 1.0 ### Record the max score for this question
        penalty_q15 = 0.25 ### Record the penalty for each incorrect attempt
        #feedback_q15 = ["To find the answer, first check the units - since the calculation is to find time, the units should be in seconds. Scan rate has units of V/s, and potential has units of V, what calculation would give you an answer in s? \n\nSecond, consider scale. If the scan rate is 1 V s⁻¹, a sweep from 0 V to 1 V would take the same amount of time as from 99 V to 100 V. Does your answer take this into account?\n\nDon't get confused by the summation symbol ( ∑ ). This is important in calculating the time data, as the calculation involving scan rate and potential will only return the time that passed in a single potential step. To calculate the time that passes over multiple potential steps, you would therefore add the time that passes in each step together."] ### Add in the message you want to pop up here, inside the quote marks after message =. If you want a unit to appear after the correct answer, include this at the start.
        answer_q15 = ["𝑡ᵢ = ∑ { (𝐸ᵢ - 𝐸ᵢ₋₁) / 𝜈 }"] ### Record the answer for this question. The answer must be kept inside the square brackets to work. Multiple acceptable answers can be given by separating them with commas, e.g. [answer1 , answer2, answer3]
        wrong_answers_q15 = ["𝑡ᵢ = { ∑ 𝐸ᵢ / 𝜈 }", "𝑡ᵢ = ∑ { 𝐸ᵢ x 𝜈 }", "𝑡ᵢ = ∑ { (𝐸ᵢ - 𝐸ᵢ₋₁) x 𝜈 }"]
        self.labels_q15 = ["𝑡ᵢ = ∑ { 𝐸ᵢ / 𝜈 }", "𝑡ᵢ = ∑ { (𝐸ᵢ - 𝐸ᵢ₋₁) / 𝜈 }", "𝑡ᵢ = ∑ { 𝐸ᵢ x 𝜈 }", "𝑡ᵢ = ∑ { (𝐸ᵢ - 𝐸ᵢ₋₁) x 𝜈 }"] ### Record all of the possible checkboxes you want to show, including the correct answer and all wrong answers. The list of possible labels should be inside the square brackets, with each label inside quote marks. E.g. ["label 1", "label 2", label 3"]
        self.checkbutton_cols_q15 = 2 ### How many columns do you want the checkboxes to be divided between?
        
        feedback_q15 = ["We can demonstrate that 𝑡ᵢ = ∑ 𝐸ᵢ / 𝜈 is not the correct option by putting some theoretical numbers in there and trying to do the calculation. Imagine scanning the potential from 0.1 V to 0.2 V. How would you know which potential to put in? The scan rate is fixed, but putting either 0.1 or 0.2 V would give you different answers. Also, adding in the next potential, 0.3 V, would give a different answer again, despite the scan rate being constant. \n\nTo find the answer, first check the units - since the calculation is to find time, the units should be in seconds. Scan rate has units of V/s, and potential has units of V, what calculation would give you an answer in s? \n\nSecond, consider scale. If the scan rate is 1 V s⁻¹, a sweep from 0 V to 1 V would take the same amount of time as from 99 V to 100 V. Does your answer take this into account?\n\nDon't get confused by the summation symbol ( ∑ ). This is important in calculating the time data, as the calculation involving scan rate and potential will only return the time that passed in a single potential step. To calculate the time that passes over multiple potential steps, you would therefore add the time that passes in each step together.","We can demonstrate that 𝑡ᵢ = ∑ 𝐸ᵢ x 𝜈 is not the correct option by putting some theoretical numbers in there and checking the units. We want to have t in seconds. 𝐸 has units of V and 𝜈 has units of V/s. So, 𝐸ᵢ x 𝜈 would have units of V²/s, not s.\n\nTo find the answer, first check the units - since the calculation is to find time, the units should be in seconds. Scan rate has units of V/s, and potential has units of V, what calculation would give you an answer in s? \n\nSecond, consider scale. If the scan rate is 1 V s⁻¹, a sweep from 0 V to 1 V would take the same amount of time as from 99 V to 100 V. Does your answer take this into account?\n\nDon't get confused by the summation symbol ( ∑ ). This is important in calculating the time data, as the calculation involving scan rate and potential will only return the time that passed in a single potential step. To calculate the time that passes over multiple potential steps, you would therefore add the time that passes in each step together.", "We can demonstrate that 𝑡ᵢ = ∑ (𝐸ᵢ - 𝐸ᵢ₋₁) x 𝜈 is not the correct option by putting some theoretical numbers in there and checking the units. We want to have t in seconds. 𝐸 has units of V and 𝜈 has units of V/s. So, (𝐸ᵢ - 𝐸ᵢ₋₁) x 𝜈 would have units of V²/s, not s.\n\nTo find the answer, first check the units - since the calculation is to find time, the units should be in seconds. Scan rate has units of V/s, and potential has units of V, what calculation would give you an answer in s? \n\nSecond, consider scale. If the scan rate is 1 V s⁻¹, a sweep from 0 V to 1 V would take the same amount of time as from 99 V to 100 V. Does your answer take this into account?\n\nDon't get confused by the summation symbol ( ∑ ). This is important in calculating the time data, as the calculation involving scan rate and potential will only return the time that passed in a single potential step. To calculate the time that passes over multiple potential steps, you would therefore add the time that passes in each step together."] 
        
                        #The lists create a record of all of the buttons, entry fields etc as they are made so they can be disabled after an answer is given and graded
        self.button_list_q15 = []
        self.entry_list_q15 = []
        
        # This creates a title for an entry field
        ttk.Label(self.frame_q15, wraplength=450, text = "Question 15: In electrochemistry, the the area under a peak is related to the charge passed for an electrochemical reaction, as is defined by:").grid(row=0, column=0, padx=10, sticky='w')
        
        # This adds in an image to be used for an equation along with the question
        self.eq_Qit = PhotoImage(file = self.resource_path('Qit.png'))
        #self.eq_Randles = self.eq_Randles.subsample(2,2) #This line is available to resize the image if needed
        ttk.Label(self.frame_q15, image = self.eq_Qit).grid(row=1, column=0)
        
        # This creates question text for an entry field
        ttk.Label(self.frame_q15, wraplength=450, text = "where 𝑄 is the charge passed, 𝑖 is the current and 𝑡 is the time. In a CV, data is presented as current versus potential, rather than current versus time. How can a potential axis for a CV be converted into a time axis so that this integration is valid? Note, the notation 𝑡ᵢ indicates the ith value of 𝑡, so if a sequence of 𝑡 was [0,0.1,0.2,0.3,0.4], 𝑡₁ = 0, 𝑡₂ = 0.1, 𝑡₃ = 0.2... etc").grid(row=2, column=0, padx=10, sticky='w')
         
        #This function will create all of the text boxes 
        self.checkbuttons_q15, self.checkbutton_labels_q15 = self.create_checkbuttons("q15", self.frame_q15, 0, 1, self.labels_q15, answer_q15, self.checkbutton_cols_q15)
        
        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a submit button
        self.button_submit_q15 = ttk.Button(self.frame_q15, text = "Submit", command=lambda: self.submit_1checkbox("q15", self.frame_q15, answer_q15, self.labels_q15, self.checkbutton_labels_q15, max_score_q15, penalty_q15, feedback_q15, wrong_answers_q15, self.button_list_q15, self.checkbuttons_q15))
        self.button_submit_q15.grid(row=0, column=self.checkbutton_cols_q15+1, rowspan=round(len(self.labels_q15)/self.checkbutton_cols_q15), padx=10, pady=5, sticky = 'w')
        self.button_list_q15.append(self.button_submit_q15)
        
        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a solve button
        self.button_solve_q15 = ttk.Button(self.frame_q15, text = "Solve", command=lambda: self.solve_1checkbox("q15", self.frame_q15, answer_q15, self.checkbutton_labels_q15, max_score_q15, penalty_q15, feedback_q15, self.button_list_q15, self.checkbuttons_q15))
        self.button_solve_q15.grid(row=0, column=self.checkbutton_cols_q15+2, rowspan=round(len(self.labels_q15)/self.checkbutton_cols_q15), padx=10, pady=5, sticky = 'w')
        self.button_list_q15.append(self.button_solve_q15)
        
        ''' -------- Add components into relevant dictionaries -------- '''
        # This section will be used to auto complete and block out entries that have already been completed if students close and then reopen the worksheet
        self.checkbutton_dictionary["q15"] = self.checkbuttons_q15
        self.checkbutton_label_dictionary["q15"] = self.checkbutton_labels_q15
        self.button_dictionary["q15"] = self.button_list_q15
        self.label_loc_dictionary["q15"] = [self.checkbutton_cols_q15+3, 0, self.frame_q15] #If a student has already entered an answer on a previous attempt, this is where the label containing their score will appear. Format is [column, row, frame number]
        self.question_list.append("q15")
        
        ''' -------- Add in the separator line between the sections -------- '''
        #This adds a separator line at the end of a frame
        ttk.Separator(self.frame_q15).grid(columnspan=5, sticky="ew")
        
        
        ''' ================================================================================================================================================================= '''
        
        ''' This code creates a smooth line plot from user submitted data. Data may be entered as comma separated numbers or by copying a column from Excel.
        Code starts with an introduction section that lets the creator introduce the plot, for example encouraging students to use precise values.
        This is a larger code section where the first question allows the student to plot the data
        The second section allows the student to select the region of the data that should be used as a peak to be integrated and a baseline for the background subtraction
        Baseline fitting, subtraction and integration are all done automatically in the background, and the area under the peak is shown on the graph

        '''
        
        ''' -------- Section q16 introduction for the worksheet -------- '''

        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_q16_intro = ttk.Frame(self.useable_frame)
        self.frame_q16_intro.config(padding = (10,10))
        self.frames_list.append(self.frame_q16_intro)

        ''' -------- Question q16 intro -------- '''        

        # This creates an introductory text field
        ttk.Label(self.frame_q16_intro, wraplength=800, text = "For this section, you will need to use your answer to the previous question to calculate a new x dataset featuring a time axis. You chosen formula involves a summation and a calculation. You may find it easiest to do this in two separate columns in Excel, where one column first deals with the calculation inside the curly brackets, and the second column deals with the sum.\n\nRemember, when copying functions in Excel, Excel will update the cell reference (the letter and the number). For example, copying a formula involving cell A1 down by one row will change all references from A1 to A2. You can fix cell references by using the dollar sign, e.g. $A$1 would stay as $A$1 even after being copied.\n\n\tA1\t copied down rows → \t A1 \t|\t $A$1 \t copied down rows → \t $A$1 \n\t\t\t\t\t A2 \t|\t\t\t\t\t $A$1 \n\t\t\t\t\t A3 \t|\t\t\t\t\t $A$1 \n\t\t\t\t\t A4 \t|\t\t\t\t\t $A$1 \n\nCheck the Excel tutorial documents if you need help with this. \n\nYou may also find the following keyboard shortcuts helpful: \tCTRL+C = copy \t CTRL+V = paste \t CTRL+A = select all").grid(row=0, column=0, padx=10, sticky='w')


        ''' -------- Section q16 for the worksheet -------- '''

        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_q16 = ttk.Frame(self.useable_frame)
        self.frame_q16.config(padding = (10,10))
        self.frames_list.append(self.frame_q16)

        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_plot3 = ttk.Frame(self.useable_frame)
        self.frame_plot3.config(padding = (10,10))
        self.frames_list.append(self.frame_plot3)

        #The lists create a record of all of the buttons, entry fields etc as they are made so they can be disabled after an answer is given and graded
        self.button_list_q16 = []
        self.entry_list_q16 = []

        ''' -------- Question q16 -------- ''' 
        ### These are the things that you need to change to build your worksheet 
        ###Enter parameters to be used in the graph - axis titles etc 
        question_q16x = "Question 16a: Enter in the x data for your plot of 𝑖 vs 𝑡 and enter it here. You may enter your data as comma separated numbers, or by copying a column of data directly from Excel. Hint: A common mistake here is to forget the summation part of the calculation."
        question_q16y = "Question 16b: Enter in the y data for your plot of 𝑖 vs 𝑡. You may enter your data as comma separated numbers, or by copying a column of data directly from Excel."
        self.xlabel_q16 = "$t$ / s" ### enter the x axis title
        self.ylabel_q16 = "$i$ / A" ### enter the y axis title

        #This creates a title for an entry field
        ttk.Label(self.frame_q16, wraplength=450, text = question_q16x).grid(row=0, column=0, padx=10, sticky='w')
        ttk.Label(self.frame_q16, wraplength=450, text = question_q16y).grid(row=1, column=0, padx=10, sticky='w')

        # This creates an entry window for the user to add data. Line 1 creates the entry box, line 2 adds it to position on the grid.
        self.entry_q16x = ttk.Entry(self.frame_q16, width = 30)
        self.entry_q16x.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        self.entry_list_q16.append(self.entry_q16x)

        # This creates an entry window for the user to add data. Line 1 creates the entry box, line 2 adds it to position on the grid.
        self.entry_q16y = ttk.Entry(self.frame_q16, width = 30)
        self.entry_q16y.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        self.entry_list_q16.append(self.entry_q16y)

        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a plot button
        self.button_plot_q16 = ttk.Button(self.frame_q16, text = "Plot", command=lambda: self.plot_line("q16", self.frame_plot3, self.entry_q16x.get(), self.entry_q16y.get(), self.button_list_q16, self.entry_list_q16, xlabel=self.xlabel_q16, ylabel=self.ylabel_q16))
        self.button_plot_q16.grid(row=0, column=3, rowspan = 2, padx=10, pady=5, sticky = 'w')
        self.button_list_q16.append(self.button_plot_q16)

        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a reset button
        self.button_reset_q16 = ttk.Button(self.frame_q16, text = "Reset", command=lambda:self.reset_line(self.button_list_q16, self.entry_list_q16, self.frame_plot3))
        self.button_reset_q16.grid(row=0, column=4, rowspan = 2, padx=10, pady=5, sticky = 'w')

        ''' -------- Add components into relevant dictionaries -------- '''
        # This section will be used to auto complete and block out entries that have already been completed if students close and then reopen the worksheet
        self.entry_dictionary["q16"] = self.entry_list_q16
        self.button_dictionary["q16"] = self.button_list_q16
        self.question_list.append("q16")
        self.plot_button_dictionary["q16"] = self.button_plot_q16

        ''' -------- Add in the separator line between the sections -------- '''
        #This adds a separator line at the end of a frame
        ttk.Separator(self.frame_q16).grid(columnspan=5, sticky="ew")
        
        ''' ================================================================================================================================================================= '''

        ''' -------- Section q17 for the worksheet -------- '''
        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_q17 = ttk.Frame(self.useable_frame)
        self.frame_q17.config(padding = (10,10))
        self.frames_list.append(self.frame_q17)

        #The lists create a record of all of the buttons, entry fields etc as they are made so they can be disabled after an answer is given and graded
        self.button_list_q17 = []
        self.entry_list_q17 = []
        self.flag_list_q17 = []

        ''' -------- Question  q17 -------- '''
        ### These are the things that you need to change to build your worksheet 
        question_q17 = "Question 17: Based on your answer to the previous question, a graph has been plotted. In order to accurately integrate the Cu⁰ oxidation peak, it is first necessary to perform a background subtraction. The background subtraction is done by carrying out a linear fit to a region of the data that corresponds to the background signal. Use the two text boxes to enter in a lower and upper 𝑡 value that will be used to the linear fit. \n\n Hit Preview to see the linear fit and adjust as needed, then click submit when you are ready. \n\nHint: This worksheet has preset coded limits for where the baseline should be based on your lab script. To make sure you don't push these limits, it is better to choose a middle range for your baseline, rather than pushing the data range to its limit. If the worksheet says the range is incorrect, you may have miscalculated the time axis. The time range should be between 0 and ~ 350 s. Check with a demonstrator if unsure." ###Add in the text for the question you want to ask. The question has to be kept inside the quote marks for the code to work, e.g. "This is the text for my question"
        max_score_q17 = 2.0 ### Record the max score for this question
        penalty_q17 = 0.5 ### Record the penalty for each incorrect attempt
        feedback_q17 = ["When fitting the background for a peak, the linear fit is desigined to present a projection of how the background signal would look if it were to continue in a linear fashion underneath the peak. This should therefore be a fit of a linear region before the onset of the peak (i.e. to the left of the peak). \n\nNote that the question is asking what data range should be used to perform a linear fit that can be extrapolated to make a baseline. The data used to fit the baseline should therefore not contain any of the same data that makes up that peak. \n\nThe extrapolated baseline will not necessarily connect up the left and right hand side of the peak to be integrated, it is fine if it runs linearly underneath. \n\nMake sure that the linear region is relatively flat and confined to a resonable region of the plot. If you believe the region you have selected is ok, the selected region may just be too wide, so select a narrower window.\n\nFor the selection of the peak itself, use the change in colour to make sure that you are selecting the whole of the peak from the bottom to the top. The integration would only take part in the region that you select, so have you captured the entirity of the area under the peak?"]  ### Add in the message you want to pop up here, inside the quote marks after message =.
        wrong_answers_q17 = []
        self.labels_q17= ["baseline lower 𝑡", "baseline upper 𝑡", "peak lower 𝑡", "peak upper 𝑡"] ### Add in the labels for the user to assign 
        self.answers_q17 = [[(150, 250)] , [(150, 250)],[ (200,300)], [(200,300)]] ###Add in the correct answer in the same order as above. If the box should remain blank, enter "". To accept a range of answers, enter the range in format (lowest number, highest number). 
        answer_cols_q17 = 2 ### How many columns do you want the answer boxes to be divided between?
        self.integration_unit_q17 = "C" ### If the function is doing an integration, this will display the unit next to the value on the graph
        sf_q17 = None ### How many significant figures should the answer be rounded to? Enter None if you do not want any rounding, or self.sigfig to call the global sigfig number that was defined earlier 
        
        ### To plot data from a previous question, enter the corresponding question number below. This set up allows you to overwrite an old plot with new or additional data
        q_number = "q16" #Enter the question number in for format "q1" for question 1     
        
        ''' -------- Enter the question -------- '''

        row = 1
        column = 0

        # This creates headings to go on top of entry fields in a table format
        for i in range(len(self.labels_q17)):
            
            if column == answer_cols_q17 *2 :#Dividing all of the entry labels up between 2 columns 
                column = 0
                row = row+3
            ttk.Label(self.frame_q17, text = self.labels_q17[i]).grid(column = column, row = row+1) #Add in the label to go above the entry box
            flag = ttk.Label(self.frame_q17, text = "")
            flag.grid(column = column+1, row = row, sticky="w") #Add in a blank label ready to receive either a correct or incorrect flag
            entry_box = ttk.Entry(self.frame_q17, width = 10)
            entry_box.grid(column = column+1, row = row+1, padx=5, pady=5, sticky='w') #Add in the entry box ready to take the answers
            self.entry_list_q17.append(entry_box)
            self.flag_list_q17.append(flag)
            column = column + 2

        ttk.Label(self.frame_q17, wraplength=600, text = question_q17).grid(row=0, column=0, columnspan = column, padx=10, sticky='w')

        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a preview button
        self.button_preview_q17 = ttk.Button(self.frame_q17, text = "Preview", command=lambda: self.plot_line("q17", self.frame_plot3, self.input_values([[q_number, "x"]]), self.input_values([[q_number, "y"]]), self.button_list_q17, self.entry_list_q17, xlabel=self.input_values([[q_number, "xlabel"]]), ylabel=self.input_values([[q_number, "ylabel"]]), integrate_vals=self.input_values(self.entry_list_q17), sf=self.sigfig, integration_unit=self.integration_unit_q17, preview=True ))
        self.button_preview_q17.grid(row=0, column=column+1, rowspan=row+3, padx=10, pady=5, sticky = 'w')

        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a submit button 
        self.button_submit_q17 = ttk.Button(self.frame_q17, text = "Submit", command = lambda: self.submit_answer_array("q17", self.frame_q17, self.input_values(self.entry_list_q17) , self.answers_q17, max_score_q17, penalty_q17, feedback_q17, wrong_answers_q17, self.button_list_q17, self.entry_list_q17, self.flag_list_q17, answer_cols_q17, sf=sf_q17))
        self.button_submit_q17.grid(row=0, column=column+2, rowspan=row+3, padx=5, pady=5, sticky = 'w')
        self.button_list_q17.append(self.button_submit_q17)

        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a solve button 
        self.button_solve_q17 = ttk.Button(self.frame_q17, text = "Solve", command = lambda: [self.solve_answer_array("q17", self.frame_q17, self.answers_q17,  max_score_q17, feedback_q17, self.button_list_q17, self.entry_list_q17, self.flag_list_q17, answer_cols_q17, sf=sf_q17) , self.button_preview_q17.invoke() ] )
        self.button_solve_q17.grid(row=0, column=column+3, padx=10, rowspan=row+3, pady=5, sticky = 'w')
        self.button_list_q17.append(self.button_solve_q17)

        # The submit and solve button functions are a bit convoluted in design. This has been done in order to make the code more user friendly for novice Python users to ammend
        # The function to calculate the answer is written by the user, taking in values either from other entry boxes or that have been calculated by other functions. Python by default would run this immediately when the worksheet is opened, which would throw in an error since no values have been entered yet! 
        # To get around this, the function includes a lambda function and is passed to a list containing all of the functions that will be used in this question. This allows the user to change the name of their function without having to edit any other code further downstream
        # The submit_answer_array function combined user entered values (question number, frame number etc), with the functions and variables in order to both calculate the answer and carry out the grading and feedback submission. 
        # self.input_values(self.entry_list_q17) takes all of the values from the entry boxes that have been created, and assembles them in the same order they were created. This allows them to be checked one, by one against the list of answers
        # self.function_list_on_variable_list(answer_list_q17, self.values_list_q17) is a fairly convoluted way to get hold of all of the answers from the function(s) created by the user. The self.function_list_on_variable_list() part does the answer comparing and solving. Inside the brackets, the (answer_list_q17, self.values_list_q17) combines the list of functions and the list of values, so that each function takes the corresponding value to calculate the correct answer
        # This could certainly be done in a more Pythonic way, but the aim is to allow manipulation of the code by a novice user with minimal steps, which this hopefully achieves. 
        
        ''' -------- Add components into relevant dictionaries -------- '''
        # This section will be used to auto complete and block out entries that have already been completed if students close and then reopen the worksheet
        self.entry_dictionary["q17"] = self.entry_list_q17
        self.button_dictionary["q17"] = self.button_list_q17
        self.label_loc_dictionary["q17"] = [answer_cols_q17*2 +3 , 2, self.frame_q17] #If a student has already entered an answer on a previous attempt, this is where the label containing their score will appear. Format is [column, row, frame number]
        self.question_list.append("q17")
        self.plot_button_dictionary["q17"] = self.button_preview_q17
        
        ''' -------- Add in the separator line between the sections -------- '''
        #This adds a separator line at the end of a frame
        ttk.Separator(self.frame_q17).grid(columnspan=10, sticky="ew")            
        
        ''' ================================================================================================================================================================= '''

        ''' -------- Section q18 for the worksheet -------- '''
        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_q18 = ttk.Frame(self.useable_frame)
        self.frame_q18.config(padding = (10,10))
        self.frames_list.append(self.frame_q18)
        
        #The lists create a record of all of the buttons, entry fields etc as they are made so they can be disabled after an answer is given and graded
        self.button_list_q18 = []
        self.entry_list_q18 = []

        ''' -------- Question  q18 -------- '''
        ### These are the things that you need to change to build your worksheet 
        max_score_q18 = 2.0 ### Record the max score for this question
        penalty_q18 = 0.5 ### Record the penalty for each incorrect attempt
        feedback_q18 = ["It looks like you have used the wrong value of n (number of electrons) in your calculations. Have a look at exactly what reaction is occuring to produce this oxidation peak (it may help to look back at Question 14). How many electrons are being transferred during this oxidation from Cu to Cu⁺?", "It looks like you have only completed half of the calculation. This is the correct value for the number of moles, but the question asked for the mass of copper,reported in grams. Use the atomic mass of copper provided (63.5 g mol⁻¹) to convert your determined number of moles into mass.", "Double check the parameters in Faraday's law, and rearrange the equation so that you are able to solve for the mass of copper. It might help to do this as a two step calculations, where you first calculate the number of moles of copper (m) and then use the atomic mass of copper to convert this values from moles to grams. You shouldn't need to do any unit conversions as charge is given to you in C, Faraday's constant is in C mol⁻¹ and copper's atomic mass is in g mol⁻¹. \n\nMake sure you consider how many electrons are being transferred during the reation at the peak you are looking at. You may want to refer back your answers to question 14 to double check how many electrons are being transferred here."] ### Add in the message you want to pop up here, inside the quote marks after message =.
        sf_q18 = self.sigfig ### How many significant figures should the answer be rounded to? Enter None if you do not want any rounding, or self.sigfig to call the global sigfig number that was defined earlier 
        question_q18 = "Question 18: Faraday's law relates charge passed for an electrochemical reaction to the number of moles of a product consumed:" ###Add in the text for the question you want to ask. The question has to be kept inside the quote marks for the code to work, e.g. "This is the text for my question"
        wrong_answers_q18 = [] 
        
        ''' -------- Calculate the correct answer based on a previous answer -------- ''' 
        ### You will need to add in your own calculations in order to use a previous entry to produce a new answer 
        def calculate_answer_q18():
            return lambda area: (area / 96485) * 63.5 ### Use a calculation in python format to calculate the correct answer. value is used to present the number that will be taken from a previous answer

        ### You will need to add in your own calculations in order to use a previous entry to produce a new answer         
        area = ["q17", "area"] ### Use this line to data from a previously generated plot. Add in the label for the question where the data was submitted, followed by if it is x or y data. Both should be in quote marks, and inside square brackets, separated by a comma. For example, for x data from question 5, enter ["q5", "x"].

        ### Use the values option to add in details for all of the values you are taking from other areas of the worksheet. If multiple values are used, separate them with commas inside the square brackets. For example, [m, c, A]. 
        ### The important thing is that these are given in the same order as in your function that calculates the answer.
        values_q18 = [area]
        answer_q18 = calculate_answer_q18() #This is a preparatory function so the script is ready to do the calculation after a number has been added to the previous question
        
        ''' -------- Calculate the wrong answer based on a previous answer -------- ''' 
        
        wrong_values_q18 = []
        
        ### You will need to add in your own calculations in order to use a previous entry to produce a new answer 
        def calculate_wrong_q18_1():
            return lambda area: (area / (2*96485)) * 63.5

        wrong_answers_q18.append(calculate_wrong_q18_1())
        wrong_values_q18.append(values_q18)
        
        ### You will need to add in your own calculations in order to use a previous entry to produce a new answer 
        def calculate_wrong_q18_2():
            return lambda area: (area / 96485)

        wrong_answers_q18.append(calculate_wrong_q18_2())
        wrong_values_q18.append(values_q18)
        

        ''' -------- Enter the question -------- '''

        # This creates a title for an entry field
        ttk.Label(self.frame_q18, wraplength=450, text = question_q18).grid(row=0, column=0, padx=10, sticky='w')

        # This adds in an image to be used for an equation along with the question
        self.eq_Faraday = PhotoImage(file = self.resource_path('Faraday.png'))
        #self.eq_Randles = self.eq_Randles.subsample(2,2) #This line is available to resize the image if needed
        ttk.Label(self.frame_q18, image = self.eq_Faraday).grid(row=1, column=0)

        # This creates question text for an entry field
        ttk.Label(self.frame_q18, wraplength=450, text = "where 𝑄 is the charge passed, 𝑚 is the number of moles reacted,𝑛 is the number of electrons transferred and 𝐹 is Faraday's constant. Assuming that the molecular mass of copper is 63.5 g mol⁻¹ and Faraday's constant is 96485 C mol⁻¹, what mass of copper was deposited onto the electrode during your CV? Give your answer in g").grid(row=2, column=0, padx=10, sticky='w')
         
        # This creates an entry window for the user to add data. Line 1 creates the entry box, line 2 adds it to position on the grid, line 3 adds the entry into the list for later use
        self.entry_q18 = ttk.Entry(self.frame_q18, width = 24)
        self.entry_q18.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        self.entry_list_q18.append(self.entry_q18)
        
        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a submit button 
        self.button_submit_q18 = ttk.Button(self.frame_q18, text = "Submit", command = lambda: self.submit_1answer("q18", self.frame_q18, self.entry_q18.get(), [answer_q18( *self.input_values(values_q18) )], max_score_q18, penalty_q18, feedback_q18, self.function_list_on_variable_list(wrong_answers_q18, wrong_values_q18), self.button_list_q18, self.entry_list_q18, sf=sf_q18)) #The * by the input values separate the answers from the tuple, so they can be used as inputs for the function
        self.button_submit_q18.grid(row=0, column=3, padx=10, pady=5, sticky = 'w')
        self.button_list_q18.append(self.button_submit_q18)

        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a solve button 
        self.button_solve_q18 = ttk.Button(self.frame_q18, text = "Solve", command = lambda: self.solve_1answer("q18", self.frame_q18, [answer_q18( *self.input_values(values_q18) )],  max_score_q18, feedback_q18, self.button_list_q18, self.entry_list_q18, sf=sf_q18))
        self.button_solve_q18.grid(row=0, column=4, padx=10, pady=5, sticky = 'w')
        self.button_list_q18.append(self.button_solve_q18)
        
        ''' -------- Add components into relevant dictionaries -------- '''
        # This section will be used to auto complete and block out entries that have already been completed if students close and then reopen the worksheet
        self.entry_dictionary["q18"] = self.entry_list_q18
        self.button_dictionary["q18"] = self.button_list_q18
        self.label_loc_dictionary["q18"] = [6, 0, self.frame_q18] #If a student has already entered an answer on a previous attempt, this is where the label containing their score will appear. Format is [column, row, frame number]
        self.question_list.append("q18")

        ''' -------- Add in the separator line between the sections -------- '''
        #This adds a separator line at the end of a frame
        ttk.Separator(self.frame_q18).grid(columnspan=5, sticky="ew")    

        ''' ================================================================================================================================================================= '''
        
        ''' -------- Section final for the worksheet -------- '''
        # This creates a frame for section of questions. Widgets are put inside. Line 1 creates the frame, line 2 adds padding around it, line 3 puts it onto the window. 
        self.frame_final = ttk.Frame(self.useable_frame)
        self.frame_final.config(padding = (10,10))
        self.frames_list.append(self.frame_final)

        #The lists create a record of all of the buttons, entry fields etc as they are made so they can be disabled after an answer is given and graded
        self.button_list_final = []
 
        ''' -------- Enter the closing message -------- '''

        # This creates a title for an entry field
        ttk.Label(self.frame_final, wraplength=450, text = "Hit submit to submit your grade. Important - if you do not hit submit below, you will score zero for this worksheet").grid(row=0, column=0, padx=10, sticky='w')

        
        # This creates a button to cause an action. Line 1 creates the button, and assigns a function to be called when it is pressed with 'command'. Line to adds it to position on the grid.
        # This is a submit button 
        self.button_submit_final = ttk.Button(self.frame_final, text = "Submit", command = lambda: self.send_file(fname))
        self.button_submit_final.grid(row=0, column=3, padx=10, pady=5, sticky = 'w')
        self.button_list_final.append(self.button_submit_final)

        ''' -------- Add in the separator line between the sections -------- '''
        #This adds a separator line at the end of a frame
        ttk.Separator(self.frame_final).grid(columnspan=5, sticky="ew")    

        ''' ================================================================================================================================================================= '''

        
    ''' -------- Functions are all below here -------- '''
    
    ''' -------- Function to read the value from an entry box -------- '''
    
    def read_entry(self, entry):
        return entry.get()
    
    ''' -------- Function to check if something has been answered on a previous attempt -------- '''
    
    def check_previous(self, filename, qnumber):
        
        # This section creates empty lists ready to receive the qnumbers 
        q_number_list = []
        
        # Get the contents of the Github file that has been storing all of the data
        file = filename
        with open(file, 'r') as data:
        
            #Split the data into columns to access the data 
            for val in data.splitlines():
                line = val.split("\t")
                #This section till check if there is already an entry for each question number before it is imported. For example, if the table read q1... q2... q2... q3... the code would skip the second q2 score. This prevents students taking multiple goes at questions to cheat the scoring system
                if line[0] not in q_number_list:
                    q_number_list.append(line[0])
            
            if qnumber in q_number_list:
                return True
    
    ''' -------- Function to call the value of a parameter that had been calculated from a line of best fit or similar operation -------- '''
    
    def call_parameter(self, q_number, parameter):
        return self.parameter_dictionary[q_number][parameter]    
    
    ''' -------- Function to take values from a previous operation and convert them into a tuple so they can be used as inputs for calculation functions  -------- '''
    
    def input_values(self, values):
        output = []
        for value in values:
            if isinstance(value, ttk.Entry):#If the value is an entry field, the function applies .get() to get the value
                output.append(value.get() )
            elif isinstance(value, str):
                output.append(value) #if the value is a string, append the string
            elif isinstance(value, float):
                output.append(value) #if the value is a float, append the flaot
            else:
                output.append( self.parameter_dictionary[value[0]][value[1]] ) #If not, it must be in a dictionary, so the appropirate dictionary value is called
        if len(output) == 1:    # If there's only one value, this can be returned as a float to enter into formula
            try:
                output = float(output[0]) #if the single item is a number, make it a float so it can be used in calculations
                output = output, #output is then turned into a tuple. this allows the same function to be used to deal with functions containing one or multiple input values
            except: #if the single item is a list of values, the whole list is passed on 
                output = output[0] 

        else:
            output= tuple(output) # if there is more than one value, it will need to be turned into a tuple before it can be passed on to a function   
        return output

    
    ''' -------- Function run a list of functions on a list of inputs to return a list of outputs  -------- '''
    
    def function_list_on_variable_list(self, function, inputs):
        output = []
        for i in range(len(inputs)):                 
            values = self.input_values(inputs[i])   
            if isinstance(values, float): #if the value is just a float, add the value alone  
                output.append([function[i](values)])
            else: #if the value is a tuple it needs the star so that the parameters within the tuple are accessible to the function
                output.append([function[i](*values)])
        return output
    
    
    
    ''' -------- Function to convert numbers to a desired number of signficant figures -------- '''
    
    #NB: This function was taken from a Stack Overflow answer by Scott Gigante (https://stackoverflow.com/users/3996580/scott-gigante) answer can be found at https://stackoverflow.com/questions/18915378/rounding-to-significant-figures-in-numpy 
    
    def signif(self, x, p):
        x = np.asarray(x)
        x_positive = np.where(np.isfinite(x) & (x != 0), np.abs(x), 10**(p-1))
        mags = 10 ** (p - 1 - np.floor(np.log10(x_positive)))
        return np.round(x * mags) / mags
    
    
    ''' -------- Function to clear a frame of all its contents -------- '''
        
    def clear_frame(self, frame):
        for frame in frame.winfo_children():
            frame.destroy()
            
    ''' -------- Function to create a y = m x + c format trendline equation as a string using regression data -------- '''
    
    def trendline_equation(self, x, y, x_param, y_param):
        
        if "\n" in x:
            x_string = x.splitlines()
            xdata = [float(e) for e in x_string if e not in ["", "\n", "\t"]] #values are only taken if they are not whitespace values, i.e. ignore all spaces, newlines, tabs etc
        #If there are no line breaks in the entry box,check to see if it is comma separated. The spreadsheet will be best if these are the only two options
        elif "," in x:
            xdata = [float(e) for e in x.split(",") if e not in ["", "\n", "\t"]]
        #Final option is that the data is being passed as already processed x or y data, in which case leave it be
        else:
            xdata = x
            
        if "\n" in y:
            y_string = y.splitlines()
            ydata = [float(e) for e in y_string if e not in ["", "\n", "\t"]] #values are only taken if they are not whitespace values, i.e. ignore all spaces, newlines, tabs etc
        #If there are no line breaks in the entry box, assume that the data is comma separated. The spreadsheet will be best if these are the only two options
        elif "," in y:
            ydata = [float(e) for e in y.split(",") if e not in ["", "\n", "\t"]]
        else:
            ydata = y

        m, c = np.polyfit(xdata, ydata, 1)
        
        # The correct answer is called from a combination of the data from a previous question and user defined parameters to give list of acceptable y = mx + c format answers 
        m = self.signif(m,self.sigfig) #round m to the predefined number of decimals
        c = self.signif(c,self.sigfig) #round c to the predefined number of decimals
        
        correct_label = []
        
        if c > 0:#case where c is positive, so the format is y = mx + c
            for i in range(len(x_param)):
                for j in range(len(y_param)):
                    correct_label.append(str(y_param[j] + " = " + str(m) + str(x_param[i]) + " + " + str(c)))
                    
        elif c == 0:#case where c is zero, so the format is y = mx
            for i in range(len(x_param)):
                for j in range(len(y_param)):
                    correct_label.append(str(y_param[j]) + " = " + str(m) + str(x_param[i]))
                    
        else:#case where c is negative, so the format is y = mx - c
            for i in range(len(x_param)):
                for j in range(len(y_param)):
                    correct_label.append(str(y_param[j]) + " = " + str(m) + str(x_param[i]) + " - " + str(np.abs(c))) #This line gets complicated - have to take an absolute value of a negative intercept so that the equation reads as y = mx - c rather than y = mx + -c
             
        start_len = len(correct_label)
        
        for i in range(start_len):
            label = correct_label[i].replace("$","")
            label = "$"+label+"$"
            correct_label.append(label)
        
        return correct_label
    
    
    '''-------- Function to encrypt / decrypt savefiles -------- '''
    
    #NB: This code was taken from a geeksforgeeks post by user kapilchhipa (https://www.geeksforgeeks.org/user/kapilchhipa/contributions/?itm_source=geeksforgeeks&itm_medium=article_author&itm_campaign=auth_user) answer can be found at (https://www.geeksforgeeks.org/encrypt-and-decrypt-files-using-python/
    
    def encrypt(self, filename):

        # try to hide the file after encryption 
        subprocess_run(f'attrib +h "{filename}"', shell=True, stdout=subprocess_DEVNULL, stderr=subprocess_DEVNULL)

    def decrypt(self, filename):
        
        # try to unhide the file so that it can be read by python
        subprocess_run(f'attrib -h "{filename}"', shell=True, stdout=subprocess_DEVNULL, stderr=subprocess_DEVNULL)

            
    ''' -------- Function to write a file to / ammend a file -------- ''' 
    
    def send_to_file(self, filename, newline):
        #if the file is there, decrypt it, otherwise continue to make the file 
        try:
            self.decrypt(filename)
        except:
            pass
        with open(filename, 'a') as f:
            f.write(newline)
        self.encrypt(filename)
        
    
    ''' -------- Function to create a savefile for scores based on the username given -------- ''' 
    
    # The function is first defined and given a name
    def submit_username(self):
        # The text is from the entry box is called to be used by the function using the .get() function
        username = self.entry_username.get()

        # This will create a filename based on the user ID to save their progress. The first line makes the filename (fname) accessible outside the function. The second line creates the filename
        global fname
        fname = str(username)+".csv"    
        global fname_penalty
        fname_penalty = "_"+str(username)+"_penalty.csv"
        
        #Checks if the file is already there from a previous attempt, if it is, it will decrypyt it before use, if not it will create it 
        try:
            self.decrypt(fname)
        except:
            pass
        #Create the file that will store the scores and add in a header
        newline = "Question No \t Score \t Max Score \t Entries \n" #This is the line that will be written to the file
        # Opens the file and writes a heading onto it for the question number and score. First line opens the file, second line writes the heading, third line encrypts the file
        with open (fname,'a') as f:
            f.write(newline)
        self.encrypt(fname)
                
        
        #Entry text box and submit button are disabled after the user submits their ID to prevent changes
        self.button_username.state(['disabled']) 
        self.entry_username.state(['disabled'])
        for item in self.frames_list:
            item.pack(expand=True, fill='both')
            
            
        #Check if the entry is already recorded in the github file
        for q in self.question_list:
            if self.read_file(fname, q):
                #if it is, pull in the previously recorded score, max score and entry
                score, max_score, entry_text = self.read_file(fname, q)
                
                #This section will either fill in entry boxes or check off checkbuttons
                if entry_text == "checkbutton": #If the score datafile contains the phrase "checkbutton", proceed to check the correct answer 
                    for label in self.checkbutton_label_dictionary[q]:
                        label.set("correct")                  
                    for checkbutton in self.checkbutton_dictionary[q]:
                        checkbutton.state(['disabled'])
                        
                else: #otherwise, there will be entry fields that should have the correct answer typed into them
                    #Fill the entries with the previously given answers and then disable them   
                    entry_text = entry_text.strip("|") #remove the trailing | character to avoid creating an additional empty list item
                    all_entry_texts = [text for text in entry_text.split("|")] #turn the | separated entries into a list of entries
                    for i in range(len(all_entry_texts)): #for each entered text item
                        this_entry = self.entry_dictionary[q][i] #choose the correct entry box
                        this_entry.insert(0,str(all_entry_texts[i])) #insert the correct answer
                        this_entry.state(['disabled']) #disable the entry box
                
                #if the question involved a plot, hit the plot button again so that values such as gradient and confidence limits can be recalculated
                if q in self.plot_button_dictionary:
                    self.plot_button_dictionary[q].invoke()   
                    
                #disable all the buttons
                for button in self.button_dictionary[q]:
                    button.state(['disabled']) 
                
                #Try to add the score labels back onto the worksheet for work already completed
                #This is put in as a try statement because plots do not have score labels, but do have entry fields, so plots should skip this section without error
                try:
                    row = int(self.label_loc_dictionary[q][1]) #call the row and column location and frame number for the score label
                    column = int(self.label_loc_dictionary[q][0])
                    frame_number = self.label_loc_dictionary[q][2]
                    if score == "0": 
                        ttk.Label(frame_number, text = "Solved! "+str(score)+" / "+str(max_score), foreground="Red").grid(row=row, column=column, padx=0, sticky='w')
                    else:
                        ttk.Label(frame_number, text = "Correct! "+str(score)+" / "+str(max_score), foreground="Green").grid(row=row, column=column, padx=0, sticky='w')
                except:
                    pass
     
        
    ''' -------- Function to create a series of checkbuttons based on a list of labels -------- '''
        
    def create_checkbuttons(self, q_number, frame_number, start_row, start_col, labels, correct_answer, num_cols):
        
        checkbuttons = []
        checkbutton_labels = []
        row = start_row
        column = start_col
        
        for i in range(len(labels)):#for each item that's listed in the list of labels 
            if column == num_cols + start_col:#Dividing all of the entry labels up between 2 columns 
                column = start_col
                row = row+1
            checkbutton = ttk.Checkbutton(frame_number, text = labels[i])
            checkbutton.grid(column = column, row = row, padx=10, pady=5, sticky='w')
            var = StringVar() #defines a variable for the checkbox so that it can be assigned as either right or wrong 
            
            if labels[i] in correct_answer:
                checkbutton.config(variable = var, onvalue = "correct", offvalue = "wrong")
                var.set("wrong") #the correct answer has to be set to wrong at the start to make sure it isn't ticked at the beginning 
            else:
                checkbutton.config(variable = var, onvalue = "wrong", offvalue = "correct")
                var.set("correct")

            column = column+1
                        
            checkbuttons.append(checkbutton) #Add each entry box to a list so that they can be called upon to find the answer later. Since they are done in the same order, the ith label will correspond to the ith entry box
            checkbutton_labels.append(var)
            
        return checkbuttons, checkbutton_labels
    
    ''' -------- Function to submit a value without grading -------- '''
    
    def submit_value(self, q_number, frame_number, given_answer, buttons, entries, sf=None):
            
        # Write the value to the users file name. first line creates the line of text that will be added, second line sends it to Github 
        newline = str(q_number) + '\t'+'0'+'\t'+'0'+'\t'+str(given_answer)+'\n'
        self.send_to_file(fname, newline) 
        
        # Disables the related entry fields after the score has been awarded
        for button in buttons:
            button.state(['disabled'])
        for entry in entries:
            entry.state(['disabled'])

    ''' -------- Function to solve a single answer and give feedback -------- '''
    
    def submit_1answer(self, q_number, frame_number, given_answer, correct_answer, max_score, penalty_score, feedback_list, wrong_answers, buttons, entries, sf=None):
        
        #Remove whitespace from the given answer and replace all – with -  as these would result in the strings not matching
        given_answer = given_answer.replace(" ", "").replace("–", "-").replace("\n", "")
        
        #Check to see if a range of answers is acceptable
        if isinstance(correct_answer[0], tuple): #if the answer is given as a tuple then this means the answer has to be between two values. Code below goes through the greater than / less than options
            if float(given_answer) >= float(correct_answer[0][0]) and float(given_answer) <= float(correct_answer[0][1]):#if they are the same, add 1 to the total of correct answers
                correct = [str(given_answer)]
        
        #Rounds the answer if significant figures have been requested, otherwise just adds it to the list of correct answers
        elif sf is not None:
            correct = [str(self.signif(float(e), sf)) for e in correct_answer]
            #This given answer is also rounded to the same number of sfs at this point. This helps to negate issues such as trailing zeros or conflict between entering small values as decimals or using e-n 
            given_answer = self.signif(float(given_answer), sf) #This line can be included to stop penalising adding too many significant figures 
        else:
            correct = [str(e).replace("–", "-").replace(" ","") for e in correct_answer] #.replace("–", "-") will swap out all – for - to get around the string comparison seeing these as different
        
        
        # If the given answer is the same as the correct answer...
        if str(given_answer) in correct:
            # Look up the penalty value from the Github file
            penalty_count = self.read_penalty(fname_penalty)
            
            # Calculate score based on max score - the total penalty 
            score = max_score - (penalty_count*penalty_score)
            # If penalties resulted in a negative number, just give a zero score 
            if score < 0:
                score = 0
            
            # Write the score to the users file name. first line creates the line of text that will be added, second line sends it to Github 
            newline = str(q_number) + '\t'+str(score)+'\t'+str(max_score)+'\t'+str(given_answer)+'\n'
            self.send_to_file(fname, newline) 
            
            # Add a Correct! message to the window next to the text box so the user knows that they are done. Also show the score on the screen as their score / max score 
            ttk.Label(frame_number, text = "Correct! "+str(score)+" / "+str(max_score), foreground="Green").grid(row=0, column=6, padx=0, sticky='w')
            
            # Disables the related entry fields after the score has been awarded
            for button in buttons:
                button.state(['disabled'])
            for entry in entries:
                entry.state(['disabled'])
                
            # Reset the penalty count to zero
            self.send_to_file(fname_penalty, "0\n") 
            
        else:
            # A wrong answer adds one to the penalty count. This will be used to calculate the penalty score once a correct answer is reached
            # Look up the penalty value. The try line looks to see if there is a recorded penalty. If there is, it is taken, if not, the penality is recorded as zero
            penalty_count = self.read_penalty(fname_penalty)
            penalty_count = penalty_count + 1
            self.send_to_file(fname_penalty, str(penalty_count)+'\n')
            
            #Start with generic feedback, and overwrite if any of the below conditions are met 
            feedback = feedback_list[-1]
            # If the given answer was included in the list of common wrong answers, choose the related specific feedback. Otherwise, choose the generic feedback. 
            if sf is not None:
                for i in range(len(wrong_answers)):
                    wrong_floats = [str(self.signif(float(e), sf)) for e in wrong_answers[i]]
                    if str(given_answer) in wrong_floats:
                        feedback = feedback_list[i] 
            else:            
                for i in range(len(wrong_answers)):
                    if str(given_answer) in wrong_answers[i]:
                        feedback = feedback_list[i]
                        
            
            
            # If sigfig control is requested, this code checks to see if the answer is correct but to the wrong number of sig figs. This will then produce specific feedback to focus on sig figs 
            if sf is not None:
                listofsfs = [1,2,3,4,5,6,7,8,9,10]
                listofsfs.remove(sf)
                wrongsf = [str(self.signif(float(e), s)) for e in correct_answer for s in listofsfs]
            
                # If the given answer is the correct answer, but given to the wrong number of significant figures, give a focused piece of feedback. 
                if str(given_answer) in wrongsf:
                    feedback = "It looks like you might have the right idea, but have inputted the answer to an incorrect number of significant figures. This worksheet requires all answer to be entered to " + str(sf) + " significant figures. Instructions for significant figures and other formatting guidelines are given at the top of this worksheet."
                
                # Check if the answer is the wrong order of mangitude. This might indicate a unit error, which should have a focused piece of feedback
                listofmagnitudes = [1e-12,1e-11,1e-10,1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1,1,1e1,1e2,1e3,1e4,1e5,1e6,1e7,1e8,1e9,1e10,1e11,1e12]
                wrongmagnitude = [str(self.signif(float(e)*m,sf)) for m in listofmagnitudes for e in correct_answer]
                if str(given_answer) in wrongmagnitude:
                    feedback = "It looks like you have the right idea, but have inputted a number to the wrong order of magnitude. This usually happens when there is an error in the units.\n\nFor example, a question asks what is the area of a square with a 10 cm side length where the answer should be in m². You might correctly calculate that the area is 100 cm², but then forget to convert the answer in to m² to get the correct answer for submission (0.01 m²).\n\nLook over your calculations for possible unit errors. Common ones include measurement errors (converting mL into L or cm in m) or instrument errors (a potentiostat might report current in μA, when you need the answer in A)."
                    
                # Check if the given answer is within 5% of the correct answer. If so, it might be a problem with carried precision  
                correct_range = [(float(e)*1.05 , float(e*0.95)) for e in correct_answer]
                for i in range(len(correct_range)): 
                    if float(given_answer) <= correct_range[i][0] and float(given_answer) >= correct_range[i][1]:
                        feedback = "Your answer is very close (within ~5%) of the correct answer. This usually indicates that you have made a precision error in your calculations. Make sure that you carry the highest possible precision value through all of your calculations. You are submitting numbers rounded to significant figures here, but you should still use high precision numbers in all calculations."
                
            # A popup window will show if a wrong score is submitted. This will show a message with some feedback for the user to help with their next attempt. 
            messagebox.showinfo(title = "Feedback", message = "The answer is not "+str(given_answer)+ ". " + feedback)
    
    
       
    ''' -------- Function to solve a single question answer and give the user the answer, with the user getting a score of zero as a result --------'''
    
    def solve_1answer(self, q_number, frame_number, correct_answer, max_score, feedback_list, buttons, entries, sf=None, reset=None):
        
        # Feedback to quote will be last generic item out of the list. 
        feedback = feedback_list[-1]
        
        #Check to see if a range of answers were acceptable
        if isinstance(correct_answer[0], tuple): #if the answer is given as a tuple then this means the answer has to be between two values. Code below goes through the greater than / less than options
            low_range = float(correct_answer[0][0]) #find the lowest limit of accetable answers
            high_range = float(correct_answer[0][1]) #find the highest limit of acceptable answers
            diff = high_range - low_range #find the difference between the two
            correct = [str(low_range+diff)]
            message_text = "The correct answer should have been beween " + str(low_range) + " and " + str(high_range) + ". "
        
        #Check to see if rounding to a number of significant figures was requested 
        elif len(correct_answer) == 1:
            if sf is not None:
                correct = [str(self.signif(float(correct_answer[0]), sf))]
            else:
                correct = [str(correct_answer[0])]

            message_text = "The correct answer was " + str(correct[0]) + ". " + feedback
        
        else:
            if sf is not None:
                correct = [self.signif(float(e), sf) for e in correct_answer]
            else:
                correct = [str(e) for e in correct_answer]
        
            message_text = "The correct answer could have been accepted as any of: \n"
            for i in range(len(correct)):
                message_text=message_text + "  •  " + correct[i] + "\n"

            message_text = message_text + feedback
            
        # A pop up message tells the user what the correct answer should have been, and gives some feedback to the user as advice for next time 
        messagebox.showinfo(title = "Feedback", message = message_text)
        
        #Set the score as zero
        score = 0
        
        # Write the score to the users file name. first line creates the line of text that will be added, second line sends it to Github 
        newline = str(q_number) + '\t'+str(score)+'\t'+str(max_score)+'\t'+str(correct[0])+' \n'
        self.send_to_file(fname, newline)
        
        # Reset the penalty count to zero
        self.send_to_file(fname_penalty, '0\n')
        
        # Add a Sovled! message to the window next to the text box so the user knows that they are done. Also show the score on the screen as 0 / max score 
        ttk.Label(frame_number, text = "Solved 0 / "+str(max_score), foreground="Red").grid(row=0, column=6, padx=0, sticky='w')
        
        # Disables the related entry fields after the score has been awarded
        for button in buttons:
            button.state(['disabled'])
        for entry in entries:
            entry.delete(0,END)
            entry.insert(0,str(correct[0]))
            entry.state(['disabled'])
        # Disable the reset button, so that a solved answer does not allow for any more user input. Try statement is used because not all questions have a reset button, so it can be skipped 
        try:
            reset.state(['disabled'])
        except:
            pass
        
    ''' -------- Function to reset a question for another attempt, but retains the count of previous errors --------'''
    
    # The function is first defined and given a name
    def reset_1answer(self, buttons, entries):
        # Enables the related entry fields after the reset button is pressed. previous error count is maintained
        for button in buttons:
            button.state(['!disabled']) 
        for entry in entries:
            entry.state(['!disabled'])
    
    
            
    ''' -------- Function to compare a checkbox selection to the correct answer and give feedback -------- '''  
    
    # The function is first defined and given a name
    def submit_1checkbox(self, q_number, frame_number, correct_answer, labels, checkbuttonlabels, max_score, penalty_score, feedback_list, wrong_answers, buttons, checkbuttons):
        # The checkboxes from the question are checked to see if correctly selected or deselected using the .get() function
        correct_sum = 0
        list_wrong = []
        for i in range(len(checkbuttonlabels)):
            if checkbuttonlabels[i].get() == "correct":
                correct_sum = correct_sum + 1 
            elif labels[i] not in correct_answer:
                list_wrong.append(labels[i])
        
        if correct_sum == len(labels):
            # Look up the penalty value. 
            penalty_count = self.read_penalty(fname_penalty)
            # Calculate score based on max score - the total penalty 
            score = max_score - (penalty_count*penalty_score)
            # If penalties resulted in a negative number, just give a zero score
            if score < 0:
                score = 0
            
            # Write the score to the users file name. first line creates the line of text that will be added, second line sends it to Github 
            newline = str(q_number) + '\t'+str(score)+'\t'+str(max_score)+'\t'+"checkbutton" + '\n'
            self.send_to_file(fname, newline)
            
            # Reset the penalty count to zero
            self.send_to_file(fname_penalty, "0\n") 
            
            # Add a Correct! message to the window next to the text box so the user knows that they are done. Also show the score on the screen as their score / max score 
            ttk.Label(frame_number, text = "Correct! "+str(score)+" / "+str(max_score), foreground="Green").grid(row=1, column=6, padx=0, sticky='w')
            # Disable the related entry fields after the score has been awarded
            for button in buttons:
                button.state(['disabled'])
            for checkbutton in checkbuttons:
                checkbutton.state(['disabled'])
    
        else:
            # A wrong answer adds one to the penalty count. This will be used to calculate the penalty score once a correct answer is reached
            # Look up the penalty value. The try line looks to see if there is a recorded penalty. If there is, it is taken, if not, the penality is recorded as zero
            penalty_count = self.read_penalty(fname_penalty)
            penalty_count = penalty_count + 1
            self.send_to_file(fname_penalty, str(penalty_count)+'\n')
            
            if list_wrong[0] in wrong_answers:
                feedback = feedback_list[wrong_answers.index(list_wrong[0])]
            else:
                feedback = feedback_list[-1]
            
            if len(list_wrong) == 1:
                string_wrong = str(list_wrong[0])
            else:
                string_wrong= str(list_wrong[0])
                for i in range(1, len(list_wrong)):
                    string_wrong = string_wrong + " or " + str(list_wrong[i])
            messagebox.showinfo(title = "Feedback", message = "The correct answer was not " + string_wrong +". " + str(feedback))
            
    ''' -------- Function to solve a checkbox selection and give the user the answer, with the user getting a score of zero as a result -------- '''
    
    # The function is first defined and given a name       
    def solve_1checkbox(self, q_number, frame_number, correct_answer, labels, max_score, penalty_score, feedback_list, buttons, checkbuttons):
        # Feedback for a solve will be the last item in the feedback list
        feedback = feedback_list[-1]
        
        # A pop up message tells the user what the correct answer should have been, and gives some feedback to the user as advice for next time
        messagebox.showinfo(title = "Feedback", message = "The correct answer was " + str(correct_answer[0]) + str(feedback))
        
        #Set the score as zero
        score = 0
        
        # Write the score to the users file name. first line creates the line of text that will be added, second line sends it to Github 
        newline = str(q_number) + '\t'+str(score)+'\t'+str(max_score)+'\t'+"checkbutton"+'\n'
        self.send_to_file(fname, newline)
        
        # Add a label with the score onto the worksheet 
        ttk.Label(frame_number, text = "Solved: 0 / "+str(max_score), foreground="Red").grid(row=1, column=6, padx=0, sticky='w')
        
        #Reset the penalty count 
        self.send_to_file(fname_penalty, '0\n')
        
        # Insert the correct answer into the entry box so that the user can see it for future reference. First line empties the entry box, second line adds the correct answer 
        for label in labels:
            label.set("correct")
        
        # Disable the related entry fields after the score has been awarded
        for button in buttons:
            button.state(['disabled'])
        for checkbutton in checkbuttons:
            checkbutton.state(['disabled'])
            
            
            
    ''' -------- Function to enter data from two comma separated text boxes and plot them as a scatter plot --------'''

    # The function is first defined and given a name
    def plot_scatter(self, q_number, frame_number, x, y, buttons, entries, xlabel = None, ylabel = None, trendline = None, equation = None, preview = None):
        
        #remove any new line characters and then comma separate the data
        if "\n" in x:
            x_string = x.splitlines()
            xdata = [float(e) for e in x_string if e not in ["", "\n", "\t"]] #values are only taken if they are not whitespace values, i.e. ignore all spaces, newlines, tabs etc
        #If there are no line breaks in the entry box,check to see if it is comma separated. The spreadsheet will be best if these are the only two options
        elif "," in x:
            xdata = [float(e) for e in x.split(",") if e not in ["", "\n", "\t"]]
        #Final option is that the data is being passed as already processed x or y data, in which case leave it be
        else:
            xdata = x
            
        if "\n" in y:
            y_string = y.splitlines()
            ydata = [float(e) for e in y_string if e not in ["", "\n", "\t"]] #values are only taken if they are not whitespace values, i.e. ignore all spaces, newlines, tabs etc
        #If there are no line breaks in the entry box, assume that the data is comma separated. The spreadsheet will be best if these are the only two options
        elif "," in y:
            ydata = [float(e) for e in y.split(",") if e not in ["", "\n", "\t"]]
        else:
            ydata = y
            
        #check to make sure that the x and y data are the same length, and trim the data if they are different
        if len(xdata) != len(ydata):
            minlength = min(len(xdata), len(ydata))
            xdata = xdata[0:minlength]
            ydata = ydata[0:minlength]            
        
        #trendline calculations for if they have been requested 
        if trendline is not None:
            
            # This section does a linear fit on the data to extract the gradient and intercept using numpy polyfit
            m, c = np.polyfit(xdata, ydata, 1)
            
            #This section calculates the upper and lower 95% confidence values 
            xdata_95 = sm.add_constant(xdata)
            model = sm.OLS(ydata,xdata_95)
            results = model.fit().conf_int(alpha=0.05)
            
            #Answers are stored in an array so this pulls out the individual values 
            CI_low = results[1][0]
            CI_high = results[1][1]
            
            #Also export the 95% confidence on the intercept - useful for the wrong answer calculations 
            c_CI_low = results[0][0]
            c_CI_high = results[0][1]
            
            yfit = []
            
            # This section creates the y data for a linear trendline
            for i in range(len(xdata)):
                yfit.append(m*xdata[i] + c)

            #Plot the line of best fit as a dashed line through the data points
            plt.plot(xdata, yfit, '--')
            
            # This line adds useful parameters into a dictionary of parameters
            
            dictionary_entry = {"m" : m} # A new dictionary entry is created for the gradient linking the value m to the label "m"
            self.parameter_dictionary[q_number] = dictionary_entry #The dictionary is nestered inside the parameters dictionary as part of a the question dictionary
            self.parameter_dictionary[q_number]["CI_low"] = CI_low #Additional parameters are added into the same question dictionary 
            self.parameter_dictionary[q_number]["CI_high"] = CI_high
            self.parameter_dictionary[q_number]["c_CI_low"] = c_CI_low
            self.parameter_dictionary[q_number]["c_CI_high"] = c_CI_high
            
            #Add in the trendline equation to the plot if it has been requested 
            if equation is not None:
                plt.text(xdata[0], 0.9*ydata[-1],str(equation))

        # Plot the x y data as a scatter 
        plt.plot(xdata, ydata, 'x')
        
        #Give the plot axis labels based on answers to q6 and q8. Try statement will skip this in cases where nothing has been entered
        if xlabel is not None: 
            plt.xlabel(str(xlabel))
        if ylabel is not None:
            plt.ylabel(str(ylabel))
    
        #Save and export the fiugre as a png image file 
        figname = str(q_number) + ".png"
        plt.savefig(figname, dpi=100)
        
        plt.clf()
        
        #Call the function to clear the contents of the frame to start with a clean slate
        self.clear_frame(frame_number)

        # This adds in an image to be used to show the plotted data. The fist line defines the location of the image, the second line imports it to a label to show, the third line gives it an image attribute (stops it getting garbage collected), the fourth line displays it
        figure = PhotoImage(file = figname)
        figurelabel = ttk.Label(frame_number, image = figure)
        figurelabel.image = figure
        figurelabel.grid(row=0, column=0)
        
        if preview != True: 
            # Disable the related buttons if a plot is pressed for submission rather than for a preview
            for button in buttons:
                button.state(['disabled'])
            for entry in entries:
                entry.state(['disabled'])
                
            #Prepare inputted data to export to Github so it can be reloaded if students close and then repoen the worksheet. This is skipped if the plot is for a preview
            newline = str(q_number) + '\t'+'0'+'\t'+'0'+'\t'+ str(xdata).strip('[]') + '|' + str(ydata).strip('[]') + '\n'
            self.send_to_file(fname, newline)

    ''' -------- Function to reset a comma separated scatter plot for another attempt --------'''

    # The function is first defined and given a name
    def reset_scatter(self, buttons, entries, frame_number):
        # Reenable the related entry fields after the reset button is pressed
        for button in buttons:
            button.state(['!disabled'])
        for entry in entries:
            entry.state(['!disabled'])
        
        #Call the function to clear the contents of the frame to start with a clean slate
        self.clear_frame(frame_number)
        
        
    ''' -------- Function to submit an array of questions and compare them to an array of answers with feedback --------'''
        
    def submit_answer_array(self, q_number, frame_number, given_answers, correct_answers, max_score, penalty_score, feedback_list, wrong_answers, buttons, entries, flags, no_cols, sf=None):
        
        #Start with generic feedback, and overwrite if any of the below conditions are met 
        feedback = feedback_list[-1]
        feedback_box = "" #added in to keep track of which boxes meet a specific criteria. This will determine if the full feedback is added, or just an addendum.
        
        checkall = 0 #Check all will be a running total of how many answers are right
        
        all_answers = "" #Make a long text string containing all answers to be exported to Github. This will be used to reload the answers if students close and reopen the worksheet
        
        for i in range(len(given_answers)): 
            given_answer = given_answers[i] #Get the given answer from the entry box
            
            #Remove whitespace from the given answer and replace all – with -  as these would result in the strings not matching
            given_answer = given_answer.replace(" ", "").replace("–", "-").replace("\n", "")
            
            all_answers = all_answers + str(given_answer) + "|" #add each of the given answers to a long text string that will be exported to Github
            correct_answer = correct_answers[i] #get the correct answer from the list 
            
            if str(given_answer) == "":
                flags[i].config(text="") #if the entry box is later made empty, remove the incorrect / correct flag
            
            if isinstance(correct_answer[0], tuple): #if the answer is given as a tuple then this means the answer has to be between two values. Code below goes through the greater than / less than options

                if float(given_answer) >= float(correct_answer[0][0]) and float(given_answer) <= float(correct_answer[0][1]):#if they are the same, add 1 to the total of correct answers
                    if str(given_answer).strip() != "": #only show the correct / incorrect flag if the box is not empty
                        flags[i].config(text="Correct!", foreground="Green")
                    checkall = checkall + 1 
                    
                else:
                    if str(given_answer).strip() != "": #only show the correct / incorrect flag if the box is not empty
                        flags[i].config(text="Incorrect!", foreground="Red")
                
            else:
            
                #If signficant figure adjustment is requested, this code will do it
                if sf is not None:
                    correct = [str(self.signif(float(e), sf)) for e in correct_answer]
                    given_answer = self.signif(float(given_answer), sf)
                else:
                    correct = [str(e).replace(" ", "").replace("–", "-") for e in correct_answer] #Remove whitespace from the given answer and replace all – with -  as these would result in the strings not matching
                
                if str(given_answer) in correct:#if they are the same, add 1 to the total of correct answers
                    if str(given_answer).strip() != "": #only show the correct / incorrect flag if the box is not empty
                        flags[i].config(text="Correct!", foreground="Green")
                    checkall = checkall + 1 
                    
                else:
                    if str(given_answer).strip() != "": #only show the correct / incorrect flag if the box is not empty
                        flags[i].config(text="Incorrect!", foreground="Red")    
                    
                    # If sigfig control is requested, this code checks to see if the answer is correct but to the wrong number of sig figs. This will then produce specific feedback to focus on sig figs 
                    if sf is not None:
                        listofsfs = [1,2,3,4,5,6,7,8,9,10]
                        listofsfs.remove(sf)
                        wrongsf = [str(self.signif(float(e), s)) for e in correct_answer for s in listofsfs]
                    
                        # If the given answer is the correct answer, but given to the wrong number of significant figures, give a focused piece of feedback. 
                        if str(given_answer) in wrongsf:
                            feedback = "It looks like you might have the right idea, but have inputted the answer to an incorrect number of significant figures. This worksheet requires all answer to be entered to " + str(sf) + " significant figures. Instructions for significant figures and other formatting guidelines are given at the top of this worksheet."
                        
                        # Check if the answer is the wrong order of mangitude. This might indicate a unit error, which should have a focused piece of feedback
                        listofmagnitudes = [1e-12,1e-11,1e-10,1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1,1,1e1,1e2,1e3,1e4,1e5,1e6,1e7,1e8,1e9,1e10,1e11,1e12]
                        wrongmagnitude = [str(self.signif(float(e)*m,sf)) for m in listofmagnitudes for e in correct_answer]
                        if str(given_answer) in wrongmagnitude:
                            if feedback_box == "": #if no feedback of this type has been created, start from scratch
                                feedback_box = feedback_box + str(i+1)
                            else: #if feedback of this type has already been added, add on to it
                                feedback_box = feedback_box + " and box " + str(i+1)       
                            feedback = "It looks like you have the right idea, but have inputted a number to the wrong order of magnitude in box "+feedback_box+". This usually happens when there is an error in the units.\n\nFor example, a question asks what is the area of a square with a 10 cm side length where the answer should be in m². You might correctly calculate that the area is 100 cm², but then forget to convert the answer in to m² to get the correct answer for submission (0.01 m²).\n\nLook over your calculations for possible unit errors. Common ones include measurement errors (converting mL into L or cm in m) or instrument errors (a potentiostat might report current in μA, when you need the answer in A)."
                            
                        
                        # Check if the given answer is within 5% of the correct answer. If so, it might be a problem with carried precision  
                        correct_range = [(float(e)*1.05 , float(e*0.95)) for e in correct_answer]                        
                        for r in range(len(correct_range)): 
                            if float(given_answer) <= correct_range[r][0] and float(given_answer) >= correct_range[r][1]:
                                if feedback_box == "": #if no feedback of this type has been created, start from scratch
                                    feedback_box = feedback_box + str(i+1)
                                else: #if feedback of this type has already been added, add on to it
                                    feedback_box = feedback_box + " and box " + str(i+1)
                                feedback = "Your answer in box " + feedback_box + " is very close (within ~5%) of the correct answer. This usually indicates that you have made a precision error in your calculations. Make sure that you carry the highest possible precision value through all of your calculations. You are submitting numbers rounded to significant figures here, but you should still use high precision numbers in all calculations."
                        
                    # If the given answer was included in the list of common wrong answers, choose the related specific feedback. Otherwise, choose the generic feedback. 
                    for w in range(len(wrong_answers)):
                        if sf is not None:
                            wrong_calc = [str(self.signif(float(e), sf)) for e in wrong_answers[w]]
                            
                        else:
                            wrong_calc = wrong_answers[w]
                        if str(given_answer) in wrong_calc:
                            feedback = feedback_list[int(w/len(given_answers))] #This code converts the fact that there is one feedback option per group of wrong answers. 

        # If all answers are correct:
        if int(checkall) == len(given_answers):
            
            # Look up the penalty value. The try line looks to see if there is a recorded penalty. If there is, it is taken, if not, the penality is recorded as zero
            penalty_count = self.read_penalty(fname_penalty)
            
            # Calculate score based on max score - the total penalty 
            score = max_score - (penalty_count*penalty_score)
            # If penalties resulted in a negative number, just give a zero score
            if score < 0:
                score = 0
            
            # Write the score to the users file name. first line creates the line of text that will be added, second line sends it to Github 
            newline = str(q_number) + '\t'+str(score)+'\t'+str(max_score)+'\t'+all_answers+'\n'
            self.send_to_file(fname, newline)
            
            # Reset the penalty count to zero
            self.send_to_file(fname_penalty, "0\n") 

            # Add a Correct! message to the window next to the text box so the user knows that they are done. Also show the score on the screen as their score / max score 
            ttk.Label(frame_number, text = "Correct! "+str(np.round(score,1))+" / "+str(max_score), foreground="Green").grid(row=2, column=no_cols*3+2, padx=0, sticky='w')
            # Disables the related entry fields after the score has been awarded
            for button in buttons:
                button.state(['disabled'])
            for entry in entries:
                entry.state(['disabled'])
            #Clear all the flag comments
            for flag in flags:
                flag.config(text="")
                
        else:
            # A wrong answer adds one to the penalty count. This will be used to calculate the penalty score once a correct answer is reached
            penalty_count = self.read_penalty(fname_penalty)
            penalty_count = penalty_count + 1
            self.send_to_file(fname_penalty, str(penalty_count)+'\n')
            
            # A popup window will show if a wrong score is submitted. This will show a message with some feedback for the user to help with their next attempt. 
            messagebox.showinfo(title = "Feedback", message = "You entered one or more incorrect options. " + feedback)
            
                
    ''' -------- Function to submit an array of questions and compare them to an array of answers with the user getting zero as a result --------'''
        
    def solve_answer_array(self, q_number, frame_number, correct_answers, max_score, feedback_list, buttons, entries, flags, no_cols, sf=None):
        
        feedback = feedback_list[-1]
        all_answers = "" #Make a long text string containing all answers to be exported to Github. This will be used to reload the answers if students close and reopen the worksheet 
        all_correct = [] #make a list of all correct answers to insert into text boxes at the end
        for i in range(len(correct_answers)):

            correct_answer = correct_answers[i] #get the correct answer from the list
            if isinstance(correct_answer[0], tuple): #if the answer is given as a tuple then this means the answer has to be between two values. Code below goes through the greater than / less than options
                low_range = float(correct_answer[0][0]) #find the lowest limit of accetable answers
                high_range = float(correct_answer[0][1]) #find the highest limit of acceptable answers
                diff = high_range - low_range #find the difference between the two
                
                if float(i+2) % 2 == 0: #if the index is even, then this is a min value, so choose from the lower end of the limit. Add 2 to avoid problems with zero
                    all_correct.append([low_range + diff*0.2]) #adds a value from the lower end of the range
                else:
                    all_correct.append([low_range + diff*0.8]) #adds a value from the higher end of the range
    
            else:
                if sf is not None:
                    correct = [str(self.signif(float(correct_answer[0]), sf))]
                else:
                    correct = [str(correct_answer[0])]
                all_correct.append(correct)
        
        # A pop up message tells the user what the correct answer should have been, and gives some feedback to the user as advice for next time
        messagebox.showinfo(title = "Feedback", message = "The correct answers are now shown in the boxes. "+feedback)
        
        #reset the penalty cont to zero
        self.send_to_file(fname_penalty, '0\n')
        
        #Set the score as zero
        score = 0

        # Add in a label with the final score
        ttk.Label(frame_number, text = "Solved: 0 / "+str(max_score), foreground="Red").grid(row=2, column=no_cols*3+2, padx=0, sticky='w')

        # Disables the related entry fields after the score has been awarded
        for button in buttons:
            button.state(['disabled'])   
        
        for i in range(len(entries)):
            entries[i].delete(0,END)
            entries[i].insert(0,str(all_correct[i][0]))
            entries[i].state(['disabled'])
            all_answers = all_answers + str(all_correct[i][0]) + "|" #add each of the correct answers to a long text string that will be exported to Github
        
        # Write the score to the users file name. first line creates the line of text that will be added, second line sends it to Github 
        newline = str(q_number) + '\t'+str(score)+'\t'+str(max_score)+'\t'+all_answers+'\n'
        self.send_to_file(fname, newline)
            
        #Clear all the flag comments
        for flag in flags:
            flag.config(text="")
            
    ''' -------- Function to enter data from two line break separated text boxes and plot them as a scatter plot --------'''

    # The function is first defined and given a name
    def plot_line(self, q_number, frame_number, x, y, buttons, entries, xlabel = None, ylabel = None, label_list = None, label_loc = None, label_min_max = None, integrate_vals = None, integration_unit = None, preview=None, sf=None):  
        
        # colorblind colour palette = ["#0072B2", "#009E73", "#E69F00", "#CC79A7"]
        
        #This section takes the numbers in the box and separates them at line breaks for use as x and y data. Line 1 pulls in the text as a string, line two separates each item at the point of the new line then line three turns it into a float 
        if "\n" in x:
            x_string = x.splitlines()
            x = [float(e) for e in x_string if e not in ["", "\n", "\t"]] #values are only taken if they are not whitespace values, i.e. ignore all spaces, newlines, tabs etc
        #If there are no line breaks in the entry box,check to see if it is comma separated. The spreadsheet will be best if these are the only two options
        elif "," in x:
            x = [float(e) for e in x.split(",") if e not in ["", "\n", "\t"]]
        #Final option is that the data is being passed as already processed x or y data, in which case leave it be
        else:
            x = x
        
        if "\n" in y:
            y_string = y.splitlines()
            y = [float(e) for e in y_string if e not in ["", "\n", "\t"]]
        #If there are no line breaks in the entry box,check to see if it is comma separated. The spreadsheet will be best if these are the only two options
        elif "," in y:
            y = [float(e) for e in y.split(",") if e not in ["", "\n", "\t"]]
        #Final option is that the data is being passed as already processed x or y data, in which case leave it be
        else: 
            y = y

        #check to make sure that the x and y data are the same length, and trim the data if they are different
        if len(x) != len(y):
            minlength = min(len(x), len(y))
            x= x[0:minlength]
            y = y[0:minlength] 
        
        # Plot the x y data  
        plt.plot(x, y, color = "#0072B2")
        
        #Give the plot axis labels based on answers to q6 and q8. Try statement will skip this in cases where nothing has been entered
        if xlabel is not None: 
            plt.xlabel(xlabel)
        if ylabel is not None:
            plt.ylabel(ylabel)
        
        #If labels have been requested, these are added here
        if label_list is not None:
            for i in range(len(label_list)):
                y_slice = y[int(len(y)*label_loc[i][0]):int(len(y)*label_loc[i][1])]
                if label_min_max[i] == "min":
                    ymin = np.min(y_slice)
                    xloc = x[y.index(ymin)]
                    plt.text(xloc, ymin, label_list[i][0], fontsize = 30)
                else:
                    ymax = np.max(y_slice)
                    xloc = x[y.index(ymax)]
                    plt.text(xloc, ymax, label_list[i][0], fontsize = 30)
                    
        #If a baseline subtracted integration is wanted for a peak this is added here
        if integrate_vals is not None:
            
            baseline_x = [float(integrate_vals[i]) for i in range(2)] #float the x values given for the min and max points on the baseline
            peak_x = [float(integrate_vals[i]) for i in range(2,4)] #float the x values given for the min and max points on the peak
            
            #This looks into the y data and find the corresponding data point for the x value given. The first line converts the data to an array so the code works. The second line finds the index value where the difference between the given value and the actual value is reported. The final line calls the correct y data point
            x_arr = np.asarray(x)
            baseline_indexes = [np.abs(x_arr-baseline_x[i]).argmin() for i in range(len(baseline_x))] #find the index values that correspond to the upper and lower t limits
            baseline_y = [y[index] for index in baseline_indexes]
            
            # This section does a linear fit on the data to extract the gradient and intercept using numpy polyfit
            baseline_m, baseline_c = np.polyfit(baseline_x, baseline_y, 1)

            # This section creates the y data for a linear trendline            
            baseline_x = x_arr[baseline_indexes[0]:]
            baseline_y = baseline_m * baseline_x + baseline_c
            
            #Plot the baseline
            plt.plot(baseline_x, baseline_y, color="#009E73", linestyle = "--")
            
            #subtract baseline for integration 
            y_arr = np.asarray(y)
            
            #select the integration range
            peak_indexes = [np.abs(x_arr-peak_x[i]).argmin() for i in range(len(peak_x))] #find the index values that correspond to the upper and lower t limits
            peak_x = x_arr[peak_indexes[0]:peak_indexes[1]]
            peak_y = y_arr[peak_indexes[0]:peak_indexes[1]]
            
            #plot the range that will make up the peak
            plt.plot(peak_x, peak_y, color="#E69F00")
            
            #calculate the integrated value
            integrate_y = peak_y - (peak_x*baseline_m + baseline_c) #subtract the baseline
            area = np.trapz(integrate_y, peak_x) #do the integration            
            print_area = str(self.signif(float(area), sf)) #turn it into a printable string with the correct number of sfs            
            area = print_area # stores the area as the 3sf version - students will only be given 3 sf for their calculations so it's important the code only uses the same level of precision as well
            try:
                print_area = print_area + " " + integration_unit
            except:
                pass
            
            plt.text(x[0], np.max(peak_y), "The calculated area is: "+print_area)

        plt.tight_layout()
        
        #Save and export the fiugre as a png image file 
        figname = str(q_number) + ".png"
        plt.savefig(figname, dpi=100)
        
        plt.clf()
        
        #Call the function to clear the contents of the frame to start with a clean slate
        self.clear_frame(frame_number)

        # This adds in an image to be used to show the plotted data. The fist line defines the location of the image, the second line imports it to a label to show, the third line gives it an image attribute (stops it getting garbage collected), the fourth line displays it
        figure = PhotoImage(file = figname)
        figurelabel = ttk.Label(frame_number, image = figure)
        figurelabel.image = figure
        figurelabel.grid(row=0, column=0)
            
        # This line adds the x and y data into a dictionary in case it needs to be used later 
        dictionary_entry = {"x" : x} # A new dictionary entry is created for the gradient linking the x data to the label "x"
        self.parameter_dictionary[q_number] = dictionary_entry #The dictionary is nestered inside the parameters dictionary as part of a the question dictionary
        self.parameter_dictionary[q_number]["y"] = y #Additional parameters are added into the same question dictionary 
        try:
            self.parameter_dictionary[q_number]["ylabel"] = ylabel #Only try these parameters, as they don't have to be given so may not be included
            self.parameter_dictionary[q_number]["xlabel"] = xlabel
            self.parameter_dictionary[q_number]["baseline_m"] = baseline_m
            self.parameter_dictionary[q_number]["baseline_c"] = baseline_c
            self.parameter_dictionary[q_number]["baseline_x"] = baseline_x
            self.parameter_dictionary[q_number]["baseline_y"] = baseline_y
            self.parameter_dictionary[q_number]["area"] = area
            
        except:
            pass 
        
        if preview != True: 
            # Disable the related buttons if a plot is pressed for submission rather than for a preview
            for button in buttons:
                button.state(['disabled'])
            for entry in entries:
                entry.state(['disabled'])
            
            #Prepare inputted data to export to Github so it can be reloaded if students close and then repoen the worksheet
            newline = str(q_number) + '\t'+'0'+'\t'+'0'+'\t'+ str(x).strip('[]') + '|' + str(y).strip('[]') + '\n'
            self.send_to_file(fname, newline)


    ''' -------- Function to reset a line plot for another attempt --------'''

    # The function is first defined and given a name
    def reset_line(self, buttons, entries, frame_number):
        # Disable the related entry fields after the score has been awarded
        for button in buttons:
            button.state(['!disabled'])
        for entry in entries:
            entry.state(['!disabled'])
        
        #Call the function to clear the contents of the frame to start with a clean slate
        self.clear_frame(frame_number)
    
    ''' -------- Function to read a file stored on Github to look for a specific q number --------'''
    
    def read_penalty(self, filename):
        
        # Get the contents of the file that has been storing all of the data
        try:
            file = self.decrypt(filename)
        except:
            pass
       
        try:
            with open(filename, 'r') as f:
            
                #Create a list of the penalty counts in the order they were recorded
                penalty_list = csv_reader(f, delimiter="\t")
                for line in penalty_list:
                    penalty = line
           
                # Return the last reported penalty value as the one to use in score calculatons
            return float(penalty[0])
        except: #if the code above errors, there is no error recorded in the text file, so the penalty count is zero
            return 0.0
        self.encrypt(filename)
        
    ''' -------- Function to read a file stored on Github to look for a specific q number --------'''
    
    def read_file(self, filename, q_number):
    
        # This section creates empty lists ready to receive the running scores from the workshop 
        q_number_list = []
        score_list = []
        max_list = []
        entry_list = []
        
        # Get the contents of the file that has been storing all of the data
        try: 
            self.decrypt(filename)
        except:
            pass
        with open(filename, 'r') as f:
            data = csv_reader(f, delimiter = "\t")
            #Split the data into columns to access the data 
            for line in data:
                #This section till check if there is already an entry for each question number before it is imported. 
                if line[0] not in q_number_list:
                    q_number_list.append(line[0])
                    score_list.append(line[1])
                    max_list.append(line[2])
                    entry_list.append(line[3])
                # The only case where multiple entries could be added is if the data plotting section is reset. It is important to use the last submitted version if the worksheet is reloaded, so this line makes sure that the most recent submission is loaded
                else:
                    # Find the index of the question that had a previous entry
                    index = q_number_list.index(line[0])
                    
                    # Delete the old entry
                    q_number_list.pop(index)
                    score_list.pop(index)
                    max_list.pop(index)
                    entry_list.pop(index)
                    
                    # Add in the new entry                    
                    q_number_list.append(line[0])
                    score_list.append(line[1])
                    max_list.append(line[2])
                    entry_list.append(line[3])
           
        self.encrypt(filename)

        # If the looked for q number is in the list of completed questions, return the score, max score and entry list as a tuple
        if q_number in q_number_list: 
            return score_list[q_number_list.index(q_number)], max_list[q_number_list.index(q_number)], entry_list[q_number_list.index(q_number)]
        else:
            return False
        
        
    ''' -------- Function to send the final complete score to file --------'''
    
    def send_file(self, filename):
        
        # This section creates empty lists ready to receive the running scores from the workshop 
        q_number_list = []
        score_list = []
        max_list = []
        
        # Get the contents of the file that has been storing all of the data
        try: 
            self.decrypt(filename)
        except:
            pass
        
        # read through the scores file, sum up the scores and report the final score as a total
        with open(filename, 'r') as f:
            data = csv_reader(f, delimiter = "\t")
            #Split the data into columns to access the data 
            for line in data:
                #This section till check if there is already an entry for each question number before it is imported. For example, if the table read q1... q2... q2... q3... the code would skip the second q2 score. This prevents students taking multiple goes at questions to cheat the scoring system
                if line[0] not in q_number_list and line[0] != "Final score:": #if the question number hasn't been included already, continue. Not equal to "final score" makes sure the script doesnt include a previous total row in a new total score generation
                    q_number_list.append(line[0])
                    score_list.append(line[1])
                    max_list.append(line[2])
            
            
            #Calculate the final score for the user, and also sum up the total score for the worksheet
            score = np.sum([float(score) for score in score_list[1:]])
            max_score = np.sum([float(score) for score in max_list[1:]])
            message_text = "Your final score is " + str(score) + " / " + str(max_score)
            
            #Post a label with the final score for the user to see
            ttk.Label(self.frame_final, text = message_text, foreground="Green").grid(row=0, column=5, padx=0, sticky='w')
        
        # write the score as a new line to the file 
        with open(filename, 'a') as f:
            # Write the final score to the users file name. first line creates the line of text that will be added, second line sends it to Github 
            newline = ("Final score:" + '\t '+str(score)+'\t'+str(max_score)+ "\t" +"complete" +'\n')
            f.write(newline)
        self.encrypt(filename)
        
        
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


''' -------- Final code block to run program --------''' 
            
def main():
    
    root = Tk()
    
    '''-------- Header and logo --------'''

    root.title("OSPREY") 
    #root.wm_iconphoto(True, PhotoImage(file="logo_small.png"))
    root.iconbitmap(default= "icon.ico")
    
    feedback = Feedback(root)
    root.mainloop()

if __name__ == "__main__": main()