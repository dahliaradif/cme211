#include <iostream>
#include <string>
#include "hw6.hpp"
#include "image.hpp"
#include <boost/multi_array.hpp>

Image::Image(std::string inputFile)
{
    filename = inputFile;
    ReadGrayscaleJPEG(filename, this->image); //like self. in python
}

void Image::Save(std::string outputFile)
{
    if (outputFile == "")
    {
        outputFile = filename;
    }

    WriteGrayscaleJPEG(outputFile, this->image);
}

void Convolution(boost::multi_array<unsigned char, 2> &input,
                 boost::multi_array<unsigned char, 2> &output,
                 boost::multi_array<float, 2> &kernel)
{
    int kernelRows = (int)kernel.shape()[0];
    int kernelCols = (int)kernel.shape()[1];
    int inputRows = (int)input.shape()[0];
    int inputCols = (int)input.shape()[1];
    double outputPixel = 0;
    //check conditions before trying to perform the convolution
    if (input.shape()[0] != output.shape()[0] || input.shape()[1] != output.shape()[1])
    {
        std::cerr << "ERROR: Input and output cannot be difference sizes." << std::endl;
        exit(1);
    }
    if (kernelRows != kernelCols || kernelRows < 3 || kernelRows % 2 == 0)
    {
        std::cerr << "ERROR: Kernel must be square, bigger than 3, and odd." << std::endl;
        exit(1);
    }

    for (int i = 0; i < inputRows; i++)
    {
        for (int j = 0; j < inputCols; j++)
        {
            outputPixel = 0;
            for (int k = 0; k < kernelRows; k++)
            {
                for (int m = 0; m < kernelCols; m++)
                {
                    //indices for accessing relevant pixels in image
                    int rowIndex = i + k - ((kernelRows - 1) / 2);
                    int colIndex = j + m - ((kernelCols - 1) / 2);
                    //edge handling
                    if (colIndex < 0)
                    {
                        colIndex = 0;
                    }
                    if (rowIndex < 0)
                    {
                        rowIndex = 0;
                    }
                    if (colIndex >= inputCols)
                    {
                        colIndex = inputCols - 1;
                    }
                    if (rowIndex >= inputRows)
                    {
                        rowIndex = inputRows - 1;
                    }
                    outputPixel += kernel[k][m] * input[rowIndex][colIndex];
                }
            }
            //handling overflow/underflow with unsigned characters
            if (outputPixel > 255)
            {
                outputPixel = 255;
            }
            if (outputPixel < 0)
            {
                outputPixel = 0;
            }
            output[i][j] = (unsigned char)outputPixel;
        }
    }
}

void Image::BoxBlur(float kernelSize)
{
    boost::multi_array<unsigned char, 2> input(boost::extents[(int)image.shape()[0]][(int)image.shape()[1]]);
    input = this->image;
    boost::multi_array<float, 2> boxBlurKernel(boost::extents[(int)kernelSize][(int)kernelSize]);
    for (int i = 0; i < kernelSize; i++)
    {
        for (int j = 0; j < kernelSize; j++)
        {
            float k = 1 / (kernelSize * kernelSize);
            boxBlurKernel[i][j] = k;
        }
    }
    Convolution(input, image, boxBlurKernel);
}
unsigned int Image::Sharpness()
{
    boost::multi_array<unsigned char, 2> output(boost::extents[(int)image.shape()[0]][(int)image.shape()[1]]);
    boost::multi_array<float, 2> LaplacianKernel(boost::extents[3][3]);
    LaplacianKernel[1][1] = -4;
    LaplacianKernel[0][0] = 0;
    LaplacianKernel[0][2] = 0;
    LaplacianKernel[2][0] = 0;
    LaplacianKernel[2][2] = 0;
    LaplacianKernel[0][1] = 1;
    LaplacianKernel[1][0] = 1;
    LaplacianKernel[1][2] = 1;
    LaplacianKernel[2][1] = 1;
    Convolution(image, output, LaplacianKernel);

    //std::max_element returns a pointer, so need to access the element to which it is pointing
    unsigned int max = (unsigned int)*std::max_element(output.origin(), output.origin() + output.num_elements());
    return max;
}
