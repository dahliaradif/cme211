import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.sparse import csr_matrix
import warnings

class Truss:
    def __init__(self, joints_file, beams_file, output_file):
        self.joints_file = joints_file
        self.beams_file = beams_file
        self.output_file = output_file
        self.start()
    
    def read_joints_file(self, joints_file):
        """Reading in the joints file, and creating a dictionary of""" 
        """relevant data, as well as lists of the forces and coordinates"""
        self.joints = {}
        self.x_coordinates = []
        self.y_coordinates = []
        self.Fx = []
        self.Fy = []
        file = np.loadtxt(self.joints_file)
        for i in range(len(file)):
            self.data = []
            index = int(file[i][0])
            x = file[i][1]
            y = file[i][2]
            self.data.append(x)
            self.data.append(y)
            self.data.append(int(file[i][5]))
            self.joints[index] = self.data
            self.x_coordinates.append(x) 
            self.y_coordinates.append(y)
            self.Fx.append(file[i][3])
            self.Fy.append(file[i][4])
       

    def read_beams_file(self, beams_file):
        """Function that reads in beam file using np.loadtxt, and""" 
        """stores the result in a dictionary"""
        self.beams = {}
        file = np.loadtxt(self.beams_file)
        for i in range(len(file)):
            self.data = []
            index = int(file[i][0])
            self.data.append(int(file[i][1]))
            self.data.append(int(file[i][2]))
            self.beams[index] = self.data
  

    def PlotGeometry(self, outputfile):
        """Optional function that creates a plot of the truss"""
        """if an output file is specified"""
        #min/max is used to ensure the axes are the correct size
        xmin = min(self.x_coordinates)
        ymin = min(self.y_coordinates)
        xmax = max(self.x_coordinates)
        ymax = max(self.y_coordinates)
        for key in self.beams:
            joint1 = self.beams[key][0]
            joint2 = self.beams[key][1]
            x1 = self.joints[joint1][0]
            x2 = self.joints[joint2][0]
            y1 = self.joints[joint1][1]
            y2 = self.joints[joint2][1]
            plt.plot([x1,x2],[y1,y2], color='blue', linewidth=1.0)
        ax=plt.gca()
        plt.ylim(ymin-0.7, ymax+0.7) #formatting
        ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(0.5))
        plt.xlim(xmin,xmax)
        plt.savefig(outputfile)
       
    def ComputeProjections(self, key):
        """Function that computes the projections of the beam"""
        """in the x and y direction for each beam"""
        joint1 = self.beams[key][0]
        joint2 = self.beams[key][1]
        x1 = self.joints[joint1][0]
        x2 = self.joints[joint2][0]
        y1 = self.joints[joint1][1]
        y2 = self.joints[joint2][1]
        a = np.array([x1,y1])
        b = np.array([x2,y2])
        dist = np.linalg.norm(a-b) #calculating distance 
        Bx = (x2-x1)/dist
        By = (y2-y1)/dist
        return(Bx, By, joint1, joint2)

    def ConstructMatrix(self):
        """This function creates the row, column, and value arrays"""
        """to create the matrix in COO format"""
        #Obtaining the fixed forces
        m = len(self.beams)
        n = len(self.joints)
        R = []
        self.i = []
        self.j = []
        self.values = []
        #creating a list of joints for which there is zero displacement
        for key in self.joints:
            if self.joints[key][2]==1:
                R.append(key)
        for key in self.beams:
            Bx_By_joints = self.ComputeProjections(key)
            Bx = Bx_By_joints[0]
            By = Bx_By_joints[1]
            joint1 = Bx_By_joints[2]
            joint2 = Bx_By_joints[3]
            #j-coordinate referencing the beam
            a = [key-1, key-1, key-1, key-1]
            self.j.extend(a) 
            #i-coordinate referencing Bx and By for both joints connected by the beam
            b = [joint1-1, joint2-1, joint1+n-1, joint2+n-1]
            self.i.extend(b)
            #Bx and By values
            c = [Bx, -Bx, By, -By]
            self.values.extend(c)
            #first two are the x values (+,-), second two are the y values (+,-)
        r = len(R)
        if r!=0:
            for k in range(r):
                joint = R[k]
                a = [m, m+1]
                self.j.extend(a)
                b = [joint-1, joint+n-1]
                self.i.extend(b)
                c = [1, 1]
                self.values.extend(c)
                m +=2

    def CreateSparseMatrix(self):
        """Function that takes the row, column and value arrays and"""
        """creates a sparse matrix in COO format"""
        row = np.array(self.i)
        col = np.array(self.j)
        values = np.array(self.values)
        self.matrix = sp.sparse.coo_matrix((values, (row, col)))
        self.matrix2 = self.matrix.todense()
        dimensions = np.shape(self.matrix2)
        m = dimensions[0]
        n = dimensions[1]
        if m != n:
            raise RuntimeError("Truss geometry not suitable for static equilibrium analysis")
    
    def ComputeBeamForce(self):
        """Function that solves the linear system Ax=b, where b"""
        """is given in the joints file. If matrix is singular, an"""
        """a RunTime error is raised"""
        self.BeamForces = []
        F = self.Fx + self.Fy
        b = np.array(F)
        warnings.filterwarnings("error", message = "Matrix is exactly singular")
        try:
            x = spsolve((csr_matrix(self.matrix)), b)
        except:
            raise RuntimeError("Cannot solve the linear system, unstable truss?")
        for i in range(len(self.beams)):
            self.BeamForces.append(self.roundResults(x[i], 3))

    def roundResults(self, number, precision):
        """Function that ensure that numbers are correctly signed and rounded"""
        rounded = round(number, precision)
        if rounded == -0.0:
            return 0
        return rounded

    def format(self, number, precision):
        """Function that formats negative numbers so that they align with"""
        """ positive ones"""
        result = ""
        if number >= 0:
            result = " "
        return result + precision.format(number) 
        #syntax for formatting numbers to ensure
        #that everything has 3 decimal places, as required

    def __repr__(self):
        """String representation of the Truss class"""
        string =  " Beam\t    Force\t" +'\n'
        string += "-----------------" + '\n'
        for i in range(len(self.BeamForces)):
            string += str(i+1)+'      ' 
            string += self.format(self.BeamForces[i],'{:.3f}')+'\n'
        return string

    def start(self):
        self.read_joints_file(self.joints_file)
        self.read_beams_file(self.beams_file)
        if self.output_file != None:
            self.PlotGeometry(self.output_file)
        self.ConstructMatrix()
        self.CreateSparseMatrix()
        self.ComputeBeamForce()

