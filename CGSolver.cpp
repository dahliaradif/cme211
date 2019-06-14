#include <iostream>
#include <sstream>
#include <iomanip>
#include <fstream>
#include <vector>
#include "CGSolver.hpp"
#include "matvecops.hpp"
#include "sparse.hpp"

int CGSolver(SparseMatrix A,
             std::vector<double> &b,
             std::vector<double> &x,
             double const tol,
             std::vector<double> const &Th_vector,
             std::vector<double> const &Tc_vector,
             std::string soln_prefix)
{
    int niter_max = A.GetSize();
    std::vector<double> r_n;
    std::vector<double> r_n1;
    std::vector<double> p_n;
    std::vector<double> Ax = A.MulVec(x);
    std::vector<double> r_0 = vectorSubtraction(b, Ax);
    double beta;
    double norm_r0 = twoNorm(r_0);
    double norm_r = norm_r0;
    r_n = r_0;
    p_n = r_0;
    int n = 0;
    std::string outputfile = GetFileName(n, soln_prefix);
    WriteToFile(outputfile, Tc_vector, Th_vector, x);
    while (n < niter_max)
    {
        n += 1;
        double rT_r = dotProduct(r_n, r_n);
        double pT_A_p = A.A_norm(p_n, p_n);
        double alpha = rT_r / pT_A_p;
        std::vector<double> alpha_p = constVecMultiply(alpha, p_n);
        x = vectorAddition(x, alpha_p);
        std::vector<double> Ap = A.MulVec(p_n);
        std::vector<double> alpha_Ap = constVecMultiply(alpha, Ap);
        r_n1 = vectorSubtraction(r_n, alpha_Ap);
        norm_r = twoNorm(r_n1);
        if ((norm_r / norm_r0) < tol)
        {
            std::string outputfile = GetFileName(n, soln_prefix);
            WriteToFile(outputfile, Tc_vector, Th_vector, x);
            return n;
        }
        beta = dotProduct(r_n1, r_n1) / dotProduct(r_n, r_n);
        std::vector<double> beta_p = constVecMultiply(beta, p_n);
        p_n = vectorAddition(r_n1, beta_p);
        r_n = r_n1;
        if (n % 10 == 0)
        {
            std::string outputfile = GetFileName(n, soln_prefix);
            WriteToFile(outputfile, Tc_vector, Th_vector, x);
        }
    }
    return -1;
}

void WriteToFile(std::string filename,
                 std::vector<double> const &Tc,
                 std::vector<double> const &Th,
                 std::vector<double> const &z)
{
    std::ofstream output(filename);
    for (unsigned int i = 0; i < Tc.size(); i++)
    {
        output << Tc[i] << "\n";
    }
    for (unsigned int i = 0; i < z.size(); i++)
    {
        output << z[i] << "\n";
    }
    for (unsigned int i = 0; i < Th.size(); i++)
    {
        output << Th[i] << "\n";
    }
    output.close();
}

std::string GetFileName(int digit, std::string soln_prefix)
{
    std::string number = FormatNumber(digit);
    std::string output = soln_prefix + number + ".txt";
    return output;
}
std::string FormatNumber(int digit)
{
    std::ostringstream number;
    number << std::internal << std::setfill('0') << std::setw(3) << digit;
    return number.str();
}