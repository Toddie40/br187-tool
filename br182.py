import sys
import numpy as np

class Radiator:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def ViewFactor(self, separation, type='p',):
        X = self.width / separation
        Y = self.height / separation

        if type == 'o': # orthogonal
            return 1 / (2 * np.pi) * (  np.arctan(X) - (1/np.sqrt(1+Y**2))*np.arctan(X/np.sqrt(1+Y**2))  )
        if type == 'c': # corner
            return 1 / (2 * np.pi) * (X / np.sqrt(1 + X**2)) * np.arctan(Y / np.sqrt(1+X**2)  +  Y / np.sqrt(1+Y**2) * np.arctan(X/np.sqrt(1+Y**2)) )
        if type == 'p': # parallel
            X = self.width / ( 2 * separation)
            Y = self.height / ( 2 * separation)
            return ( 2 / np.pi ) * ( (X / np.sqrt(1 + X**2)) * np.arctan(Y / np.sqrt(1 + X**2))  +  ( Y / np.sqrt(1+Y**2) ) * np.arctan(X/np.sqrt(1+Y**2)) )
        else:
            print("Unrecognised type!")
            return False

#TODO think of clevcer way to iteratively approach solution of this fiddly graph. it's so sensitive so im struglling to approach it closely and quickly
def CalculateMinimumSafeDistance(radiator: Radiator, intensity, iterations, precision=0.1):
    safeIntensity = 12.6
    startingDistance = 0.1 #don't want divede by zero errors
    increment = precision

    finalIncedentRad = 0
    distance = startingDistance
    for i in range(0, iterations):
        viewFactor = radiator.ViewFactor(distance)
        incedentRad = intensity * viewFactor

        if incedentRad > safeIntensity:
            distance += increment
            continue
        else:
            return np.round(distance, 1)
    print("Unable to reach solution, consider increasing the number of iterations")
    return np.round(distance,1)

def main():

    #parsing arguments
    import argparse
    parser = argparse.ArgumentParser(   description="A program for calculating the required percent protected area of an external wall",
                                        epilog="If you need any help don't hesitate to ask\nAnd if you have any feature requests then feel free to send them my way!\n\tAlex.Todd@ofrconsultants.com"
                                        )
    parser.add_argument('width', help="the width of the radiating rectangle in meters", type=float)
    parser.add_argument('height', help="the height of the radiating rectangle in meters", type=float)
    parser.add_argument('separation', help="the separation distance between the radiator and the receiving surface in meters. (If you are using boundary distances then this will be twice the boundary distance).",type=float)
    parser.add_argument('--type', help="the type of analysis to perform. 'o' orthogonal, 'c' corner, 'p' parallel. By default this is set as 'p'", choices=['c','o','p'], type=str, default='p')
    parser.add_argument('--title', help="a title for the analysis", type=str, default="unnamed analysis")
    args = parser.parse_args()
    #done parsing args

    type = args.type
    title = args.title
    radiator = Radiator(args.width, args.height)
    viewFactor = radiator.ViewFactor(args.separation, type=type)

    print("BR 187 | Unprotected Area Calculator\nAuthor: A. Todd\nDate: 06/02/2020\nOFR Consultants\n")
    print("Performing assessment: "+title+"\nOf type: "+type)
    print("geometry:\n width: {}m\n height: {}m\n separation: {}m".format(args.width, args.height, args.separation))
    print("View factor for radiator at this separation distance: "+str(viewFactor))
    print("-------------------------------------------------------------------------------\n")

    I_source = [84.6, 168] #low and high values for low and standard fire load

    I_received = np.array(I_source) * viewFactor

    unprotectedArea = np.round(np.clip(12.6/I_received * 100,0,100),1)

    for index, source in enumerate(I_source):
        print("For a source of "+str(I_source[index])+"kW/sqm")
        print("Minimum safe distance for 100% unprotected area: {}m\n".format(CalculateMinimumSafeDistance(radiator, I_source[index], 1000)))
        print("Maximum unprotected area allowable for separation of {}m: ".format(args.separation)+str(unprotectedArea[index])+"%")
        print("If the building is sprinklered, this can be increased to "+str(np.clip(unprotectedArea[index] * 2,0,100))+"%")
        print("-------------------------------------------------------------------------------\n")

if __name__ == "__main__":
    main()
