from math import tan, radians

class Board():
    def __init__(self, project_name, part_name, length, angle1, angle2):
        self.project_name = project_name
        self.part_name = part_name
        self.length = length
        self.angle1 = angle1
        self.angle2 = angle2

        if not self.angle1:
            self.angle1 = Angle(90, Length(0,0))
        if not self.angle2:
            self.angle2 = Angle(90, Length(0,0))

    def __repr__(self):
        out_str = ""
        if self.project_name:
            out_str += self.project_name + ":"
        if self.part_name:
            out_str += self.part_name + ":"
        if self.angle1.degrees > 0 or self.angle2.degrees > 0:
            out_str += str((self.angle1, self.angle2)) + " "
        
        return out_str + str(self.length)

    def __eq__(self, other):
        return self.length == other.length and ((self.angle1 == other.angle1 and self.angle2 == other.angle2) or (self.angle1 == other.angle2 and self.angle2 == other.angle1))

    def __ne__(self, other):
        return not self == other

    def difference(self, other):
        saved_length = Length(0, 0)
        if self.angle1 == other.angle1 or self.angle1 == other.angle2:
            saved_length = angle1.opposite_length
        if self.angle2 == other.angle1 or self.angle2 == other.angle2:
            saved_length = angle2.opposite_length

        other_length = other.length.difference(saved_length)
        return self.length.difference(other_length)

    def sum(self, other):
        saved_length = Length(0, 0)
        if self.angle1 == other.angle1 or self.angle1 == other.angle2:
            saved_length = angle1.opposite_length
        if self.angle2 == other.angle1 or self.angle2 == other.angle2:
            saved_length = angle2.opposite_length

        other_length = other.length.difference(saved_length)
        return self.length.sum(other_length)

    def minus(self, other):
        self.length = self.difference(other)

    def add(self, other):
        self.length = self.sum(other)

        
from functools import total_ordering

@total_ordering
class Length():
    def __init__(self, inches, sixty_fourths=None):
        if sixty_fourths != None: #specifying length in inches, six_fourths
            self.inches = inches
            self.sixty_fourths = sixty_fourths
        else: 
            if type(inches) == type(1.0): #specifying length in decimal
                self.inches = int(inches)
                self.sixty_fourths = int(int("{0:.2f}".format(inches).split(".")[-1])*64/100)
            elif type(inches) == type(""): #specifying length with a string notation (feet)'-(inches) (numerator)/(denominator)" where only (inches) is required, and leaving out the final " indicateds demensional lumber sizes
                self.inches = 0
                self.sixty_fourths = 0

                if '-' in inches: #feet specified
                    self.inches += int(inches.split('-')[0])*12
                    inches = inches.split('-')[-1] #remove feet from inches string

                if "/" in inches: #fractional inches specified
                    numerator = int(inches.split('/')[0].split(' ')[-1])
                    denominator = int(inches.split('/')[1].split('"')[0])
                    self.sixty_fourths += numerator*(64//denominator)
                    inches = inches.replace(' ' + inches.split(' ')[1].split('"')[0], '') #remove fraction from inches string, but keep possible " at the end

                self.inches += int(inches.split('"')[0])

                if not inches[-1] == '"': #dimensional lumber
                    if self.inches == 1:
                        self.minus(Length(0, 16))
                    else:
                        self.minus(Length(0, 32))

            else:
                print(inches, sixty_fourths)
                raise ValueError("inches parameter not of valid type. ", type(inches))


    def __repr__(self):
        if self.sixty_fourths > 0:
            numerator = self.sixty_fourths
            denominator = 64
            while numerator%2 == 0:
                numerator = numerator // 2
                denominator = denominator // 2
            
            return str(self.inches) + " " + str(numerator) + '/' + str(denominator) + '"'
        return str(self.inches) + '"'

    def __hash__(self):
        return hash((self.inches, self.sixty_fourths))

    def __eq__(self, other):
        return self.inches == other.inches and self.sixty_fourths == other.sixty_fourths

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if self.inches == other.inches:
            return self.sixty_fourths < other.sixty_fourths
        else:
            return self.inches < other.inches

    def get_float(self):
        return self.inches + self.sixty_fourths/64

    def difference(self, other):
        inches_remaining = self.inches - other.inches
        sixty_fourths_remaining = self.sixty_fourths - other.sixty_fourths

        if sixty_fourths_remaining < 0:
            inches_remaining -= 1
            sixty_fourths_remaining += 64
        
        if inches_remaining < 0 and sixty_fourths_remaining > 0:
            inches_remaining += 1
            sixty_fourths_remaining -= 64

        return Length(inches_remaining, sixty_fourths_remaining)

    def sum(self, other):
        inches_total = self.inches + other.inches
        sixty_fourths_total = self.sixty_fourths + other.sixty_fourths

        if sixty_fourths_total >= 64:
            sixty_fourths_total -= 64
            inches_total += 1

        return Length(inches_total, sixty_fourths_total)

    def minus(self, other):
        new = self.difference(other)
        self.inches = new.inches
        self.sixty_fourths = new.sixty_fourths

    def add(self, other):
        new = self.sum(other)
        self.inches = new.inches
        self.sixty_fourths = new.sixty_fourths

class Angle:

    def __init__(self, degrees, adjacent_length):
        self.degrees = degrees
        self.opposite_length = Length(tan(radians(90 - self.degrees))*adjacent_length.get_float())
    
    def __eq__(self, other):
        return self.degrees == other.degrees and self.opposite_length == other.opposite_length

    def __ne__(self, other):
        return not self == other
    
    def __repr__(self):
        if self.degrees < 90:
            return str(self.degrees) + ": " + str(self.opposite_length)
        return ""
        
