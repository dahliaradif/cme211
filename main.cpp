#include <iostream>
#include <string>
#include <boost/multi_array.hpp>
#include <jpeglib.h>
#include "hw6.hpp"
#include "image.hpp"
using std::cout;
using std::endl;

int main()
{
    std::string inputFile = "stanford.jpg";
    Image image(inputFile);
    unsigned int sharpness = image.Sharpness();
    cout << "Original image:"
         << " " << sharpness << endl;

    Image image3(inputFile);
    image3.BoxBlur(3);
    image3.Save("BoxBlur03.jpg");
    unsigned int sharpness3 = image3.Sharpness();
    cout << "BoxBlur( 3):"
         << "    " << sharpness3 << endl;

    Image image7(inputFile);
    image7.BoxBlur(7);
    image7.Save("BoxBlur07.jpg");
    unsigned int sharpness7 = image7.Sharpness();
    cout << "BoxBlur( 7):"
         << "     " << sharpness7 << endl;

    Image image11(inputFile);
    image11.BoxBlur(11);
    image11.Save("BoxBlur11.jpg");
    unsigned int sharpness11 = image11.Sharpness();
    cout << "BoxBlur(11):"
         << "     " << sharpness11 << endl;

    Image image15(inputFile);
    image15.BoxBlur(15);
    image15.Save("BoxBlur15.jpg");
    unsigned int sharpness15 = image15.Sharpness();
    cout << "BoxBlur(15):"
         << "     " << sharpness15 << endl;

    Image image19(inputFile);
    image19.BoxBlur(19);
    image19.Save("BoxBlur19.jpg");
    unsigned int sharpness19 = image19.Sharpness();
    cout << "BoxBlur(19):"
         << "     " << sharpness19 << endl;

    Image image23(inputFile);
    image23.BoxBlur(23);
    image23.Save("BoxBlur23.jpg");
    unsigned int sharpness23 = image23.Sharpness();
    cout << "BoxBlur(23):"
         << "     " << sharpness23 << endl;

    Image image27(inputFile);
    image27.BoxBlur(27);
    image27.Save("BoxBlur27.jpg");
    unsigned int sharpness27 = image27.Sharpness();
    cout << "BoxBlur(27):"
         << "      " << sharpness27 << endl;
}
