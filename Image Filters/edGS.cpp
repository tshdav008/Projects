#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <cmath>

using namespace std;

//a class that represents the three colour values (R,G,B) in each pixel. 

class Pixel {   private:

  unsigned int P1, P2, P3;


  public:

  Pixel () {};   
 void setPixels (unsigned int Pixel1, unsigned int Pixel2, unsigned int Pixel3);        
unsigned int getPixel1 ();   unsigned int getPixel2 ();   unsigned int getPixel3 (); };


  void Pixel::setPixels (unsigned int Pixel1, unsigned int Pixel2, unsigned int Pixel3)   {
      P1 = Pixel1;
      P2 = Pixel2;
      P3 = Pixel3;   }

  unsigned int Pixel::getPixel1 ()   {
      return P1;   }

  unsigned int Pixel::getPixel2 ()   {
      return P2;   } 

unsigned int Pixel::getPixel3 ()   {
      return P3;   }


//*****************int main () stars here! *****************

int main () {
    //information contained in the header file is represented by the following variables

    unsigned char Magic [2];
    unsigned int TotRows = 512;
    unsigned int TotCol = 512;
    unsigned int MaxVal = 255;



    int size = (3 * TotRows * TotCol);

    char *charImage = new char [size];

    //opening original image
    ifstream OldImage;
    OldImage.open ("image.ppm", ios::in | ios::binary);

    if (!OldImage)
    {
       cout << "\nError: Cannot open image file! " << endl;
    }

     //reading the header of the original image file
     OldImage >> Magic [0] >> Magic [1] >>  TotRows >>  TotCol >> MaxVal;


       OldImage.read(charImage, size);

         unsigned int val1, val2, val3;

         //an array of pixels, which is used to represent the image
         Pixel **PixelVal;

         PixelVal = new Pixel* [TotRows];
         int T=0;

//Reading the image data and setting the pixels values as unsigned integers
    for(int i=0; i < TotRows; i++)
    {
        PixelVal[i] = new Pixel [TotCol];

        for(int j=0; j < TotCol; j++)
        {
            val1 = (unsigned int)charImage[T];
            val2 = (unsigned int)charImage[T+1];
            val3 = (unsigned int)charImage[T+2];
            PixelVal[i][j].setPixels (val1, val2, val3);
            T=T+3;
        }
    }


   if (OldImage.fail())
    {
        cout << "Can't read image " << endl;
    }

OldImage.close();

//Calculating the grayscale in each pixel. 
//The values of the 3 colours (R, B and G) are all the same  
for(int i=0; i < TotRows; i++)
    {
        for(int j=0; j < TotCol; j++)
        {
val1=(PixelVal[i][j].getPixel1()+PixelVal[i][j].getPixel1()+PixelVal[i][j].getPixel1())/3;
            val2=val1;
            val3=val1;
            PixelVal[i][j].setPixels(val1, val2, val3);
        }
    }


unsigned int valX, valY = 0; unsigned int GX [3][3]; unsigned int GY [3][3];

//Sobel Horizontal Mask     
GX[0][0] = 1; GX[0][1] = 0; GX[0][2] = -1; 
GX[1][0] = 2; GX[1][1] = 0; GX[1][2] = -2;  
GX[2][0] = 1; GX[2][1] = 0; GX[2][2] = -1;

//Sobel Vertical Mask   
GY[0][0] =  1; GY[0][1] = 2; GY[0][2] =   1;    
GY[1][0] =  0; GY[1][1] = 0; GY[1][2] =   0;    
GY[2][0] = -1; GY[2][1] =-2; GY[2][2] =  -1;


//SOBEL edge detector implementation. 
//Note: in each Pixel, the values of the 3 colours is the same.Therefore 
//the calculation is performed on the first one only. The other 2 colours are
// then set to be = to the first one.

for(int i=0; i < TotRows; i++)
    {
        for(int j=0; j < TotCol; j++)
        {

            //setting the pixels around the border to 0, 
           //because the Sobel kernel cannot be allied to them
            if ((i==0)||(i==TotRows-1)||(j==0)||(j==TotCol-1))
            {
               valX=0;
               valY=0;
            }

            else
            {
                //calculating the X and Y convolutions
                for (int x = -1; x <= 1; x++)
                {
                    for (int y = -1; y <= 1; y++)
                    {
                        valX = valX + PixelVal[i+x][j+y].getPixel1() * GX[1+x][1+y];
                        valY = valY + PixelVal[i+x][j+y].getPixel1() * GY[1+x][1+y];
                    }
                }
            }

            //Gradient magnitude
             val1 = sqrt(valX*valX + valY*valY);

            //setting the new pixel value
            PixelVal[i][j].setPixels(val1, val1, val1);
        }
    } 


//creating a new file to host the copied image
    ofstream NewImage;
    NewImage.open ("image1.ppm", ios::out | ios::binary);

    if (!NewImage)
    {
        cout << "\nError: Cannot open image file! " <<endl;
    }

//writing the header in the new image file
    NewImage << "P6" << endl << TotRows << " " << TotCol << " " << MaxVal << endl;


T=0;
     for(int i=0; i < TotRows; i++)
    {
        for(int j=0; j < TotCol; j++)
        {
        val1 = PixelVal[i][j].getPixel1();
        val2 = PixelVal[i][j].getPixel2();
        val3 = PixelVal[i][j].getPixel3();
        charImage[T]=(unsigned char)val1;
        charImage[T+1]=(unsigned char)val2;
        charImage[T+2]=(unsigned char)val3;
        T=T+3;
        }
    }


cout << T;

    NewImage.write(charImage, size);

    if (NewImage.fail())
    {
        cout << "Can't write image " << endl;
    }

NewImage.close(); delete [] charImage;

for (int i = 0; i < TotRows; i++)
     {
         delete [] PixelVal[i];
     }

     delete [] PixelVal;


    return 0; }
