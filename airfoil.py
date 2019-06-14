import glob as glob
import math as math
import os as os
import sys

class Airfoil:
    """The Airfoil class inputs a directory and outputs the lift coefficient,"""
    """maximum pressure coefficient value for each angle, and the""" 
    """stagnation points for each angle."""

    def __init__(self, inputdir):
        """Initialising the input directory and the respective files inside"""
        self.directory = inputdir
        self.x_y_data = inputdir + "/xy.dat"
        self.ListOfAngleFiles = glob.glob(inputdir + "/*[0-9].*")
        self.start()

    def __repr__(self):
        """Formatting function that outputs the data in tabular form, with"""
        """ the correct  number of decimal places."""
        string = "Test Case: " + self.format_directory_name() +'\n'+'\n'
        string += "alpha\t  cl\t      stagnation pt"+'\n'
        string += "-----\t-------\t--------------------------"
        string += '\n'
        for result in self.results:
            string += self.format(result["angle"],'{:.2f}')+'\t'
            string += self.format(result["cl"],'{:.4f}')+'\t'
            string += "(" + self.format(result["xy"][0],'{:.4f}') + ", "
            string += self.format(result["xy"][1],'{:.4f}') + ") " 
            string += self.format(result["maxCp"],'{:.4f}')+'\n'
        return string

    def read_xy_data(self):
        """This function reads in the data from the xy.dat file in the"""
        """ directory."""
        X=[]
        Y=[]
        with open (self.x_y_data, "r") as f:
            coordinates = f.readlines()
      #don't read in the first line because it contains the name of the file 
            for coordinate in coordinates[1:]:
                coordinateSplit = coordinate.split()
                x = float(coordinateSplit[0])
                y = float(coordinateSplit[1])
                X.append(x)
                Y.append(y)
      #Run time error- if the number of x coordinates differs from the number of 
      #y coordinates, then return an error message.
                if len(X) != len(Y):
                    raise RuntimeError ("The coordinates file is incomplete.")
        f.close()
        return (X,Y)

    def get_angle(self, file_name):
        """This function extracts the angle from the name of the folders"""
        """ containing an angle number."""
        file_name = file_name.replace('.dat', '')
        indexPlus = file_name.rfind('+')
        indexMinus = file_name.rfind('-')
        if indexPlus > -1:
            return (float)(file_name[indexPlus:])
        if indexMinus > -1:
            return (float)(file_name[indexMinus:])
        return 0.0

    def read_angle_data(self, angle_data):
        """This function reads the angle data, adding the pressure coefficients"""
        """ to a list.""" 
        Cp = []
        with open (angle_data, "r") as f:
            lines = f.readlines()
            for line in lines[1:]:
                c_p = float('' .join(line.split()))
         #Run time error- if there is a missing pressure coefficient file, then 
          #we generate an error
                if c_p == '':
                    raise RuntimeError ("The angles file is incomplete.")
                Cp.append(c_p)
        f.close()    
        return(Cp)
     
    def get_chord(self, coordinates):
        """This function calculates the chord length."""
        X = coordinates[0]
        Y = coordinates[1]
        trailing_x = X[0]
        trailing_y = Y[0]
        leading_x = min(X)
        index_min = min(range(len(X)), key=X.__getitem__)
        leading_y = Y[index_min]
        chord = math.sqrt(((trailing_x-leading_x)**2) + ((trailing_y-leading_y)**2))
        return chord

    def perpendicular_panel_force(self, i, j, X, Y, Cp_list, chord):
        """Decomposing the function that calculates the lift coefficent."""
        """This function calculates the panel force coefficient for a single panel"""
        x1 = X[i]
        y1 = Y[i]
        x2 = X[j]
        y2 = Y[j]
        x_difference = x2-x1
        y_difference = y2-y1
        delta_x = (-1*((Cp_list[i] * y_difference)/chord))
        delta_y =  (Cp_list[i] * x_difference)/chord
        return(delta_x,delta_y)

    def total_force_coefficient(self, coordinates, Cp_list, chord):
        """This function calls the perpendicular_panel_force function on a"""
        """ forloop, iterating over the number of x coordinates"""
        X = coordinates[0]
        Y = coordinates[1]
    #counter for cx and cy; each time we calculate delta x or delta y, 
    #we increment the counter by the deltax and delta y
        cx = 0
        cy = 0
        for i in range(0, len(X)-1):
           # print(i)
            j=i+1
            #print(j)
            delta_c = (self.perpendicular_panel_force(i,j, X, Y, Cp_list, chord))
            delta_x = delta_c[0]
            delta_y=delta_c[1]
            cx += delta_x
            cy += delta_y
        return (cx, cy)
    
    def get_lift_coefficient(self, coordinates, Cp_list, chord, angle):
        """Function that calulcates the lift coefficient, decomposed into two"""
        """ other functions."""
        cx_and_cy = self.total_force_coefficient(coordinates, Cp_list, chord)
        cx = cx_and_cy[0]
        cy = cx_and_cy[1]
        angle = math.radians(angle) #cos and sine functions take radian inputs
        cl = (cy * (math.cos(angle))) - (cx * (math.sin(angle)))
        return cl

    def get_stagnation_point(self, coordinates, Cp_list):
        """Function that find the maximum pressure coefficent,""" 
        """and the respective (x,y) coordinates."""
        X = coordinates[0]
        Y = coordinates[1]
        max_Cp = max(Cp_list)
        index =  max(range(len(Cp_list)), key=Cp_list.__getitem__)
        x = (X[index] + X[index+1])/2
        y = (Y[index] + Y[index+1])/2
        return(max_Cp,x,y)

    def is_valid_directory(self):
        """Boolean function"""
        return os.path.isdir(self.directory)

    def do_xy_files_exist(self):
        """Boolean function"""
        return os.path.isfile(self.x_y_data)

    def do_angle_files_exist(self):
        return len(self.ListOfAngleFiles) > 0 

    def is_valid(self):
        """Run time error function that checks for a directory being valid,"""
        """ and for the existence of angle/xy files within the directory"""
        if self.is_valid_directory()== False:
            raise RuntimeError("{0} is not a valid directory." .format(self.directory)) 
        elif self.do_xy_files_exist() == False:
            raise RuntimeError("Coordinates file does not exist.")
        elif self.do_angle_files_exist() == False:
            raise RuntimeError("Angle files do not exist.")
        return True

    def format(self, number, precision):
        """Function that formats negative numbers so that they align with"""
        """ positive ones"""
        result = ""
        if number >= 0:
            result = " "
        return result + precision.format(number)
        #syntax for formatting numbers to ensure
        #that everything has 2 or 4 decimal places, as required

    def format_directory_name(self):
        """Function that formats the directory name in the format required"""
        directory = self.directory.replace('/', '')
        return (directory[0:4] + " " + directory[4:]).upper()

    def sort_results(self):
        """Sorting the array of dictionaries by increasing angle size"""
        newlist = sorted(self.results, key=lambda x: x["angle"])
        return newlist

    def round_results (self, number, precision):
        """Very small floating points round to -0.0. When this happens"""
        """we change it to 0."""
        rounded = round (number, precision)
        if rounded == -0.0:
            return 0
        return rounded

    def start(self):
        """This is the main function that calls all the other functions"""
        """ in a forloop iterating over the angle files, and returning"""
        """ the required output."""
        if self.is_valid():
            self.results = []
            for file in self.ListOfAngleFiles:
                angle = self.get_angle(file)
                Cp_list = self.read_angle_data(file)
                coordinates = self.read_xy_data()
                chord = self.get_chord(coordinates)
                cl = self.round_results(self.get_lift_coefficient(coordinates, Cp_list, chord, angle),4)
                max_Cp_x_y = self.get_stagnation_point(coordinates, Cp_list)
                max_Cp = self.round_results(max_Cp_x_y[0],4)
                x_y = max_Cp_x_y[1:]
                self.results.append({"angle": angle, "cl": cl, "xy": (x_y), "maxCp": max_Cp})
            self.results = self.sort_results()
