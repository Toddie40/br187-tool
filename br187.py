import sys
import numpy as np

class Radiator:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def ViewFactor(self, separation, type='p',):
        if not separation == 0:
            X = self.width / separation
            Y = self.height / separation

        if type == 'o': # orthogonal
            return 1 / (2 * np.pi) * (  np.arctan(X) - (1/np.sqrt(1+Y**2))*np.arctan(X/np.sqrt(1+Y**2))  ) if not separation == 0 else 0.25
        if type == 'c': # corner
            return 1 / (2 * np.pi) * (X / np.sqrt(1 + X**2)) * np.arctan(Y / np.sqrt(1+X**2)  +  Y / np.sqrt(1+Y**2) * np.arctan(X/np.sqrt(1+Y**2)) ) if not separation == 0 else 0.25
        if type == 'p': # parallel
            X = self.width / ( 2 * separation)
            Y = self.height / ( 2 * separation)
            return ( 2 / np.pi ) * ( (X / np.sqrt(1 + X**2)) * np.arctan(Y / np.sqrt(1 + X**2))  +  ( Y / np.sqrt(1+Y**2) ) * np.arctan(X/np.sqrt(1+Y**2)) ) if not separation == 0 else 1
        else:
            print("Unrecognised type!")
            return False


class Analysis:

    # A nice dictionary to store the proper names of types
    typeDict = {'o':'orthogonal',
                'p':'parallel',
                'c':'corner'}

    def __init__(self, title, type, separation, radiator, iterations=10000, precision=0.01):
        self.title = title
        self.type = type
        self.radiator = radiator
        self.iterations = iterations
        self.precision = precision
        self.separation = separation
        self.viewFactor = self.radiator.ViewFactor(self.separation, type=self.type)

    #TODO think of clevcer way to iteratively approach solution of this fiddly graph. it's so sensitive so im struglling to approach it closely and quickly
    def calculate_minimum_safe_distance(self, intensity, iterations, precision):
        safeIntensity = 12.6
        startingDistance = 0.1 #don't want divede by zero errors
        increment = precision

        finalIncedentRad = 0
        distance = startingDistance
        for i in range(0, iterations):
            viewFactor = self.radiator.ViewFactor(distance)
            incedentRad = intensity * viewFactor

            if incedentRad > safeIntensity:
                distance += increment
                continue
            else:
                return np.round(distance, 1)
        print("Unable to reach accurate solution, consider increasing the number of iterations")
        return np.round(distance,1)

    def calculate(self):
        results = {
                    'Title' : self.title,
                    'Type': self.typeDict[self.type],
                    'Separation': self.separation,
                    'View Factor': self.viewFactor,
                    'Radiator Dimensions' : {
                        'Width': self.radiator.width,
                        'Height': self.radiator.height
                    },
                    'Reduced Fire Load': {
                        'Safe Distance': 0,
                        'Unprotected Area': {
                            'unsprinklered' : 0,
                            'sprinklered' : 0
                        }
                    },
                    'Standard Fire Load': {
                        'Safe Distance': 0,
                        'Unprotected Area': {
                            'unsprinklered' : 0,
                            'sprinklered' : 0
                        }
                    }
        }
        #reduced fire Load
        I_received_reduced = 84 * self.viewFactor
        results['Reduced Fire Load']['Safe Distance'] = self.calculate_minimum_safe_distance(84, self.iterations, self.precision)
        results['Reduced Fire Load']['Unprotected Area']['unsprinklered'] = np.round(np.clip(12.6/I_received_reduced * 100,0,100),1)
        results['Reduced Fire Load']['Unprotected Area']['sprinklered'] = np.round(np.clip(12.6/I_received_reduced * 100 * 2,0,100),1)

        #standard fire load
        I_received_standard = 168 * self.viewFactor
        results['Standard Fire Load']['Safe Distance'] = self.calculate_minimum_safe_distance(168, self.iterations, self.precision)
        results['Standard Fire Load']['Unprotected Area']['unsprinklered']= np.round(np.clip(12.6/I_received_standard * 100,0,100),1)
        results['Standard Fire Load']['Unprotected Area']['sprinklered']= np.round(np.clip(12.6/I_received_standard * 100 * 2,0,100),1)

        self.results = results

        return results

    def save_results(self, path=None):
        import csv
        if path == None:
            path = str(self.title)+".csv"
        with open (path, 'w') as file:
            writer = csv.DictWriter(file, self.results.keys())
            writer.writeheader()
            writer.writerow(self.results)
        return True

    def pretty_print_dict(self,d,indent=0):
        for key, value in d.items():
            if isinstance(value, dict):
                print("\t" * indent + str(key))
                self.pretty_print_dict(value,indent + 1)
            else:
                print(indent * "\t" + "{}: {}".format(key, value))
        return True
    def print_results(self):
        self.pretty_print_dict(self.results)


def main():

    title_string = """
--------------------------------------------------------------------------------------------------------
BR 187 | External Fire Spread Calculator
A calculator based on the BR 187 standard for calculating external fire spread to neighbouring buildings

Author: Alex Todd
OFR Consultants
"""

    print(title_string)
    #parsing arguments
    import argparse
    parser = argparse.ArgumentParser(   description="A program for calculating the required percent protected area of an external wall",
                                        epilog="If you need any help don't hesitate to ask\nAnd if you have any feature requests then feel free to send them my way!\n\tAlex.Todd@ofrconsultants.com",
                                        usage="%(prog)s WIDTH HEIGHT SEPARATION [--type {'c','p','o'}] [--title TITLE]"
                                        )
    parser.add_argument('width', help="the width of the radiating rectangle in meters", type=float)
    parser.add_argument('height', help="the height of the radiating rectangle in meters", type=float)
    parser.add_argument('separation', help="the separation distance between the radiator and the receiving surface in meters. (If you are using boundary distances then this will be twice the boundary distance).",type=float)
    parser.add_argument('--type', help="the type of analysis to perform. 'o' orthogonal, 'c' corner, 'p' parallel. By default this is set as 'p'", choices=['c','o','p'], type=str, default='p')
    parser.add_argument('--title', help="a title for the analysis", type=str, default="unnamed analysis", nargs='*')
    # REMEMBER TO UPDATE USAGE IF ADDING ARGUMENTS
    args = parser.parse_args()
    #done parsing args

    type = args.type
    title = ' '.join(args.title) # convert the list into a string

    analysis = Analysis(title, type, args.separation, Radiator(args.width, args.height))

    results = analysis.calculate()
    analysis.save_results()
    analysis.print_results()

if __name__ == "__main__":
    main()
