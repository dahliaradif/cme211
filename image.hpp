#ifndef IMAGE_HPP
#define IMAGE_HPP
#include <string>
#include <boost/multi_array.hpp>
#include "hw6.hpp"

class Image
{
  private:
    std::string filename;
    boost::multi_array<unsigned char, 2> image;

  public:
    Image(std::string filename);
    void Save(std::string filename);
    
    void BoxBlur(float kernel);
    unsigned int Sharpness();
};
void Convolution(boost::multi_array<unsigned char, 2> &input,
                     boost::multi_array<unsigned char, 2> &output,
                     boost::multi_array<float, 2> &kernel);

#endif /* IMAGE_HPP */