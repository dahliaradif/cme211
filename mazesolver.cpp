#include <iostream>
#include <fstream>
#include <string>

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        std::cout << "Usage:" << std::endl;
        std::cout << " " << argv[0] << " <maze file> <solution file>" << std::endl;
        return 0;
    }
    std::string mazefile = argv[1];
    std::string solutionfile = argv[2];*/
    int arr[210][210] = {0};
    int nrow, ncol, row, col;
    std::ifstream input(mazefile); //opens file too
    if (input.is_open())
        input >> nrow >> ncol;
    else
        std::cerr << "File not correctly opened." << std::endl;

    while (input >> row >> col)
    {
        //Checking there is enough storage space in the array
        if (row > 210 or col > 210)
        {
            std::cout << "Not enough storage available" << std::endl;
            return 1;
        }
        else
        {
            arr[row][col] = 1;
        }
    }
    input.close();
    //Get the entry point of the maze
    int startCol;
    for (int k = 0; k < col; k++)
    {
        if (arr[0][k] == 0)
        {
            startCol = k;
        }
    }

    enum orientation
    {
        north = 1,
        east,
        west,
        south
    };
    int j = startCol;
    int i = 0; //starting row
    std::cout << i << "  " << j << std::endl;
    int forward = arr[i + 1][j];
    int right = arr[i][j - 1];
    int left = arr[i][j + 1];
    int back = arr[i - 1][j];
    int direction = 1;
    //1 if facing forward
    //2 if facing right
    //3 if facing left
    //4 if facing back (orientation looking straight from entrance)
    while (i < nrow - 1)
    {
        switch (direction)
        {
        case north:
            if (right == 0)
            {
                j = j - 1;
                forward = arr[i][j - 1];
                right = arr[i - 1][j];
                left = arr[i + 1][j];
                back = arr[i][j + 1];
                direction = east;
            }
            else if (forward == 0)
            {
                i = i + 1;
                forward = arr[i + 1][j];
                right = arr[i][j - 1];
                left = arr[i][j + 1];
                back = arr[i - 1][j];
                direction = north;
            }
            else if (left == 0)
            {
                j = j + 1;
                forward = arr[i][j + 1];
                right = arr[i + 1][j];
                left = arr[i - 1][j];
                back = arr[i][j - 1];
                direction = west;
            }
            else if (back == 0)
            {
                i = i - 1;
                forward = arr[i - 1][j];
                right = arr[i][j + 1];
                left = arr[i][j - 1];
                back = arr[i + 1][j];
                direction = south;
            }
            std::cout << i << "  " << j << std::endl;
            break;
        case east:
            if (right == 0)
            {
                i = i - 1;
                forward = arr[i - 1][j];
                right = arr[i][j + 1];
                left = arr[i][j - 1];
                back = arr[i + 1][j];
                direction = south;
            }
            else if (forward == 0)
            {
                j = j - 1;
                forward = arr[i][j - 1];
                right = arr[i - 1][j];
                left = arr[i + 1][j];
                back = arr[i][j + 1];
                direction = east;
            }
            else if (left == 0)
            {
                i = i + 1;
                forward = arr[i + 1][j];
                right = arr[i][j - 1];
                left = arr[i][j + 1];
                back = arr[i - 1][j];
                direction = north;
            }
            else if (back == 0)
            {
                j = j + 1;
                forward = arr[i][j + 1];
                right = arr[i + 1][j];
                left = arr[i - 1][j];
                back = arr[i][j - 1];
                direction = west;
            }
            std::cout << i << "  " << j << std::endl;
            break;
        case west:
            if (right == 0)
            {
                i = i + 1;
                forward = arr[i + 1][j];
                right = arr[i][j - 1];
                left = arr[i][j + 1];
                back = arr[i - 1][j];
                direction = north;
            }
            else if (forward == 0)
            {
                j = j + 1;
                forward = arr[i][j + 1];
                right = arr[i + 1][j];
                left = arr[i - 1][j];
                back = arr[i][j - 1];
                direction = west;
            }
            else if (left == 0)
            {
                i = i - 1;
                forward = arr[i - 1][j];
                right = arr[i][j + 1];
                left = arr[i][j - 1];
                back = arr[i + 1][j];
                direction = south;
            }
            else if (back == 0)
            {
                j = j - 1;
                forward = arr[i][j - 1];
                right = arr[i - 1][j];
                left = arr[i + 1][j];
                back = arr[i][j + 1];
                direction = east;
            }
            std::cout << i << "  " << j << std::endl;
            break;
        case south:
            if (right == 0)
            {
                j = j + 1;
                forward = arr[i][j + 1];
                right = arr[i + 1][j];
                left = arr[i - 1][j];
                back = arr[i][j - 1];
                direction = west;
            }
            else if (forward == 0)
            {
                i = i - 1;
                forward = arr[i - 1][j];
                right = arr[i][j + 1];
                left = arr[i][j - 1];
                back = arr[i + 1][j];
                direction = south;
            }
            else if (left == 0)
            {
                j = j - 1;
                forward = arr[i][j - 1];
                right = arr[i - 1][j];
                left = arr[i + 1][j];
                back = arr[i][j + 1];
                direction = east;
            }
            else if (back == 0)
            {
                i = i + 1;
                forward = arr[i + 1][j];
                right = arr[i][j - 1];
                left = arr[i][j + 1];
                back = arr[i - 1][j];
                direction = north;
            }
            std::cout << i << "  " << j << std::endl;
            break;
        default:
            break;
        }
       
    }
}
/* std::ofstream output;
    output.open(solutionfile);
    output << result;
    output.close();*/
