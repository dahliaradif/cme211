CXX := g++
CXXFLAGS := -O3 -std=c++11 -Wall -Wconversion -Wextra -pedantic

LDFLAGS := -ljpeg
TARGET := main
OBJS := main.o image.o hw6.o 
INCS := image.hpp hw6.hpp 

$(TARGET): $(OBJS)
	$(CXX) -o $(TARGET) $(OBJS) $(LDFLAGS)

%.o: %.cpp $(INCS)
	$(CXX) -c -o $@ $< $(CXXFLAGS)
.PHONY: clean
clean:
	$(RM) $(OBJS) $(TARGET)
