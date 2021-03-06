# make file for sofm - OSX
# Developed on Eva's brand new Airbook, compilers etc were already installed
# Neessary steps were:
# 1) check that Xcode developer suite installed
# 2) agree to the Xcode license, this meant scrolling
#    through a long EULA to the end at which point you
#    get a prompt asking you to agree
# 3) once Xcode had been activated as above, the link
#    stage needs to be run with sudo
INSTALLDIR = ../bin
TARGET	= 	solo
SOURCE	= 	MATRIX.cc \
		cntProLSClass.cc LLSSearchClass.cc \
		matrixObj.cc solo.cc readDataPC.cc sofmFreqClass.cc \
		corrcoef.c eigsrt.c gaussj.c jacobi.c nrutil.c

TMPOBJ	=	$(SOURCE:%.cc=%.o)
OBJ	=	$(TMPOBJ:%.c=%.o)
# we disable the IEEE floating point operation and enable use of the NPU (-ffast-math)
# using the IEE floating point was very slow using gcc V4.8 under Windows
CC 	= 	/usr/bin/gcc -ffast-math -Wall -I.
CXX = 	/usr/bin/g++ -ffast-math -Wall -I.
LIB	=	-lm -v 
RM	=	rm -f
CP  =   cp

# we link using -static to make a stand-alone executable and use
# -s to strip out debugging symbols to reduce the executable size
$(TARGET)	: $(OBJ)
		  sudo $(CXX) -o $(TARGET) $(OBJ) $(LIB)

install:
		$(CP) $(TARGET) $(INSTALLDIR)

clean:
		$(RM) $(TARGET) $(OBJ)

%.o		: %.cc 
		  $(CXX) -c $< -o $@
%.o		: %.c 
		  $(CC) -c $< -o $@
