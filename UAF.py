# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 14:46:14 2020

@author: TRIETLAM, Marc Boyer
"""

from fractions import Fraction

######################################################################
##  Exceptions for error handling

class UAFInputError(Exception):
     def __init__(self, expression, message):
        self.expression = expression
        self.message = message
    
######################################################################
##  Class Point and related functions

def is_int(value):
    """Check if the parameter is an integer"""
    return value.lstrip('+- ').isdigit()
    # Source:
    # https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except

def str_to_int_if_possible(value):
    """If the parameter is an int or an str representing an int, convert into int, otherwise, keep string"""
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return value
    if is_int(value):
        return int(value)
    return value

def test_str_to_int_if_possible():
    assert( str_to_int_if_possible(1) == 1 )
    assert( str_to_int_if_possible(1.1) == float(1.1) )
    assert( str_to_int_if_possible("+12") == 12 )
    assert( str_to_int_if_possible("13/25") == "13/25")
    assert( str_to_int_if_possible("abc") == "abc")
    assert( str_to_int_if_possible("+12a") == "+12a" )
    
def checkValue(value):
    """Return True if the parameter value is either an integer, a fraction, a float, +Infinity or -Infinity"""
    # Is it infinity ?
    if (value == "+Infinity") or (value == "-Infinity"):
        return True
    # Is it a valid fraction ?
    divPos= value.find("/")
    if divPos != -1:
        return is_int( value[0:divPos] ) and is_int( value[divPos+1:] )
    # Is it a float or an integer
    try:
        value= float(value)
        return True
    except ValueError:
        return False

# Definition of points
class Point:
    """ 
    The Point class is to identify the point following the Cartesian 
    coordinate system.
    Ex: Point(4,5) means x=4 and y=5 
    __init__ function: allows the class to initialize the attributes of a class.
    __eq__ function: compares itself to an int.
    __str__ function: is useful for a string representation of the object.
    """
    def __init__(self, x, y):
        self.x= str_to_int_if_possible(x)
        self.y= str_to_int_if_possible(y)
    def __eq__(self, other):
        if (self.x == other.x) and (self.y == other.y):
            return True
        else:
            return False
    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+")"

######################################################################
##  Class Segment and related functions    

# Definition of Segment
class Segment():
    """
    Segment is a component in the uaf function which defined by:
        (left_open,p1,slope,p2,right_open)
        Ex: [(0,1)0(4,5)[ means a line from point (0,1) to point (4,5) with 
        the slope equals 0 and left-closed, right-open.
    """
    def __init__(self,left_open,p1,slope,p2,right_open):
        self.left_open= left_open
        self.p1= p1
        self.slope=slope
        self.p2=p2
        self.right_open=right_open


    def __eq__(self, other):
        """ This function is to compare the values themvelves """
        if isinstance(other, Segment):
            if ( (other.left_open == self.left_open) and
              (other.p1 == self.p1 ) and
              (other.slope == self.slope ) and
              (other.p2 == self.p2 ) and
              (other.right_open== self.right_open) ):
                return True
        
        return False

    def debug_eq(self, other):
        """This function print debug informations for equality"""
        print(" isinstance(other, Segment)= ",  isinstance(other, Segment) )
        if not isinstance(other, Segment):
            return
        print(" other.left_open == self.left_open=", other.left_open == self.left_open)
        print(" other.right_open == self.right_open=", other.right_open == self.right_open)
        print(" other.p1 == self.p1=", other.p1 == self.p1)
        if other.p1 != self.p1:
            print(" other.p1 ", other.p1)
            print(" self.p1 ", self.p1)
        print(" other.p2 == self.p2=", other.p2 == self.p2)
        print(" other.slope == self.slope=", other.slope == self.slope)

        
        
# Consider the intervals  
        """ 
        We have four states of the interval: 
            - Open:]a,b[
            - Closed: [a,b]
            - Left-closed, right-open: [a,b[
            - Left-open, right-closed: ]a,b]
                """
    def __str__(self):
        if self.left_open:
            result= ']'
        else:
            result= '['
        result= result + self.p1.__str__() + str( self.slope) + str(self.p2)
        if self.right_open:
            result= result + '['
        else:
            result= result + ']'
        return result
        

def readSegment(input_string):    
    """ 
    Construct a Segment object from a string.
    input example:  '[(0,2)1(+Infinity,+Infinity)['
    To do that, we need to indentify:
        - The first square bracket 
        - The first Cartesian coordinate point
        - The value of slope
        - The second Cartesian coordinate point
        - The second square bracket
    This function only reads one segment.
    """
    # Respect la syntaxe
    """Check the syntaxe of the function at the first paren"""
    if input_string[1]!='(':
        print("Error in parsing ", input_string)
        print("  First opening paren is missing")
        return None
        
    """"Check the syntaxe of the function at the last paren"""
    if input_string[-2]!=')':
        print("Error in parsing ", input_string)
        print("  Last opening paren is missing")
        return None
    
    """Check the number of comma"""
    if input_string.count(',')!=2:
        print("Error in parsing ", input_string)
        print("  The number of comma is not correct")
        return None
        
    """Check the number of left paren"""
    if input_string.count('(')!=2:
        print("Error in parsing ", input_string)
        print("  The number of left paren is not correct")
        return None
        
    """Check the number of right paren"""
    if input_string.count(')')!=2:
        print("Error in parsing ", input_string)
        print("  The number of right paren is not correct")
        return None
    
    """
    Read the syntaxe of the uaf function
    We define a syntaxe included 5 parts: first square bracket, first point, 
    slope, second point and second square bracket.
    """
        
    "Read the first square bracket to identify the first point is opened or closed"
    if input_string[0]==']':
        left_open= True
    else:
        left_open= False
        
    """
    Read the first point
    first_paren is the opened paren "(" to start 
    the value of the first point (x1,y1)
    first_comma is the comma "," in the syntaxe of the first point
    second_paren is the closed paren ")" of the syntaxe of the first point
    """
    first_paren= input_string.find("(")
    # print("a", type(first_paren))
    # print("b", first_paren)    
    # [(0,1)1(+Infinity,+Infinity)[
        
    first_comma= input_string.find(",")
    x1= input_string[first_paren+1:first_comma]
    # if checkValue(x1) == False:
    #     print("   Not a valid value:" + x1 )
    #     return None
    second_paren= input_string.find(")")    
    y1= input_string[first_comma+1:second_paren]
    # if checkValue(y1) == False:
    #     print("   Not a valid value:" + y1 )
    #     return None
    
    """
    Read the slope
    third_paren is the opened paren "(" to start 
    the value of the second point (x2,y2)
    second_comma is the comma "," in the syntaxe of the second point
    fourth_paren is the closed paren ")" of the syntaxe of the second point
    """
    third_paren= input_string.find("(",first_paren+1)
    slope= input_string[second_paren+1:third_paren] 
    if checkValue(slope) == False:
         print("   Not a valid value:" + slope )
         return None
    else:
        slope= str_to_int_if_possible( slope )
    
    "Read the second point"
    second_comma= input_string.find(",",first_comma+1)
    fourth_paren= input_string.find(")",second_comma+1)
    x2= (input_string[third_paren+1:second_comma])
    if checkValue(x2) == False:
        print("   Not a valid value:" + x2 )
        return None
    
    y2= (input_string[second_comma+1:fourth_paren])
    if checkValue(y2) == False:
        print("   Not a valid value:" + y2 )
        return None
    
    "Read the first square bracket to identify the second point is opened or closed"
    if input_string[-1]=='[':
        right_open= True
    else:
        right_open= False
 
    """
    Check the number of the comma inside one a couple of paren
    x3 is the value of the Point1 including (x1,y1)
    x4 is the value of the Point2 including (x2,y2)
    """       
    x3=input_string[first_paren:second_paren]
    x4=input_string[third_paren:fourth_paren]
    if (x3.count(",")!=1) and (x4.count(",")!=1):
        print("Error in parsing ", input_string)
        print("  The value of points is not correct")
        return None
     
    """
    Check the order of the paren
    It should be () and ()
    z1  contains the characters from the first paren to the second paren
    """     
    z1=input_string[first_paren+1:second_paren-1]
    z2=input_string[third_paren+1:fourth_paren-1]
    if (z1.count("(")!=0) and (z2.count(")")!=0):
        print("The order of the paren () is not correct", input_string)
        return None
        
    return Segment(left_open, Point(x1,y1), slope, Point(x2,y2),right_open)


def test_one_segment(name, input_string, expected_value):
    seg= readSegment( input_string ) 
    if seg == expected_value:
        print( "Test OK:", name)
    else:
        print("Test failed ",name)
        print("  Input string: ", input_string)
        print("  Result:   ", seg)
        print("  Expected: ", expected_value)
        seg.debug_eq(expected_value)
        

    
def test_readSegment():
    """Unitary tests of readSegment function"""

    # Check nominal behavior
    test_one_segment("N1",
                     "[(0,1)1(+Infinity,+Infinity)[",
                     Segment(False, Point('0','1'),1,Point("+Infinity","+Infinity"),True))
    test_one_segment("N2",
                     "](21,1)1(+Infinity,+Infinity)[",
                     Segment(True, Point(21,1),1,Point("+Infinity","+Infinity"),True))
    test_one_segment( "N3",
                      "](31/71,1)1(+Infinity,+Infinity)[" ,
                      Segment(True, Point('31/71',1),1,Point("+Infinity","+Infinity"),True) )
    test_one_segment( "N4",
                      "[(31/71,1)1(+Infinity,+Infinity)[",
                      Segment(False, Point('31/71',1),1,Point("+Infinity","+Infinity"),True))
    test_one_segment("N5",
                     "[(31/71,1)1(+Infinity,+Infinity)]",
                     Segment(False, Point('31/71',1),1,Point("+Infinity","+Infinity"),False))
    test_one_segment("N6",
                     "[(0,1)21(+Infinity,-Infinity)[",
                     Segment(False, Point(0,1),21,Point("+Infinity","-Infinity"),True))
    test_one_segment("N7",
                     "[(+Infinity,21/45)21(+Infinity,-Infinity)[",
                     Segment(False, Point("+Infinity",'21/45'),21,Point("+Infinity","-Infinity"),True))
    test_one_segment("N8",
                     "[(.5,21/45)21(+Infinity,-Infinity)[",
                     Segment(False, Point('.5','21/45'),21,Point("+Infinity","-Infinity"),True))
    test_one_segment("N9",
                     "[(.5,21/45)21(1/2,298)[",
                     Segment(False, Point('.5','21/45'),21,Point("1/2",298),True))
    test_one_segment("N10",
                     "[(0,1)21(12,-Infinity)]",
                     Segment(False, Point(0,1),21,Point(12,"-Infinity"),False))
    test_one_segment("N11",
                     "](-7080,+Infinity)21(+Infinity,+Infinity)[",
                     Segment(True, Point(-7080,"+Infinity"),21,Point("+Infinity","+Infinity"),True))
    # Check errors
    test_one_segment("Missing first comma",
                     "](-7080+Infinity)21(+Infinity,+Infinity)[",
                     None)
    
    test_one_segment("Missing second comma",
                     "](-7080,+Infinity)21(+Infinity+Infinity)[",
                     None)
    test_one_segment("Missing first opening paren",
                     "]-7080,+Infinity)21(+Infinity,+Infinity)[",
                     None)
    test_one_segment("Missing first closing paren",
                     "](-7080,+Infinity21(+Infinity,+Infinity)[",
                     None)
    test_one_segment("Missing second opening paren",
                     "](-7080,+Infinity21)+Infinity,+Infinity)[",
                     None)
    test_one_segment("Syntax 1",
                     "](-7080,+Infinity)21)+Infinity,+Infinity)[",
                     None)
    test_one_segment("Syntax 2",
                     "](0,1(2)+Infinity,+Infinity)[",
                     None)

######################################################################
##  Class UAF and related functions    

class UAF:
    def __init__(self):
        self.seg_list= []
        
    def addSegment(self,s):
        self.seg_list.append(s)
        return self

    def addSegmentList(self,l):
        self.seg_list.extend(l)
        return self

    def __eq__(self,other):
        if not isinstance(other, UAF):
            return False
        s_len= len( self.seg_list )
        o_len= len( other.seg_list )
        if s_len != o_len:
            return False
        for i in range(s_len):
            if self.seg_list[i] != other.seg_list[i]:
                return False
        return True

    def __str__(self):
        res= 'uaf('
        for i in self.seg_list:
            res+= str( i )
        return res+ ')'
        
        
def readUAF( input_string ):
    """ Construct a UAF object from a string.
    input examples:  
       'uaf(](0,2)1(+Infinity,+Infinity)]'
       'uaf([(0,1)2(1,3)]](1,3)1(+Infinity,+Infinity)[)'
       'uaf([(0,1)2(1,3)]](1,3)1(5,7)]](5,+Infinity)0(+Infinity,+Infinity)[)'
    """
    if (len( input_string ) < 5) or (input_string[0:4] != 'uaf('):
        return None
    
    return UAF().addSegmentList( readSegList( input_string[4:-1] ) )
    

def readSegList( input_string ):
    """ Construct a list of segment object from a string.
    input examples:  
       '](0,2)1(+Infinity,+Infinity)]'
       '[(0,1)2(1,3)]](1,3)1(+Infinity,+Infinity)['
       '[(0,1)2(1,3)]](1,3)1(5,7)]](5,+Infinity)0(+Infinity,+Infinity)['
    """

    if (input_string[-1] != '[') and (input_string[-1] != ']'):
        raise UAFInputError(input_string, "End of segment list must be ']' or '['")

    # start: index of the start of the current segment
    start= 0
    i_len= len( input_string )

    
    L= []

    while start < i_len:
        # end: end of the current segment
        n1= input_string.find("]", start+1)
        n2= input_string.find("[", start+1)
        if n1 != -1 and n2 != -1:
            end= min(n1,n2)
        elif n1 != -1:
            end= n1
        else:
            end= n2
#        print("start=", start)
#        print("end=", end)
#        print(" input_string[start:end+1]=", input_string[start:end+1] )        
        seg = readSegment( input_string[start:end+1] )
        L.append(seg)
        start= end+1
    return L

def test_readUAF():
    uaf1= UAF().addSegment( readSegment( "[(0,2)1(3,5)]" ) ).\
          addSegment( readSegment( '](3,5)-1/2(5,4)[') ).\
          addSegment( readSegment( '[(5,4)12(+Infinity,+Infinity)]') )
    assert( uaf1 == uaf1 )
    uaf2= UAF().addSegment( readSegment( "[(0,2)1(3,5)]" ) ).\
          addSegment( readSegment( '](3,5)-1/2(5,4)[') ).\
          addSegment( readSegment( '[(5,4)15(+Infinity,+Infinity)]') )
    assert( uaf2 == uaf2 )
    assert( uaf2 != uaf1 )
    uaf3= UAF().addSegment( readSegment( "[(0,0)1(+Infinity,+Infinity)]" ) )
    assert( uaf3 == uaf3 )
    assert( uaf1 != uaf3 )
    assert( uaf2 != uaf3 )

    print( uaf1 )
    uaf1_str= 'uaf([(0,2)1(3,5)]](3,5)-1/2(5,4)[[(5,4)12(+Infinity,+Infinity)])'
    assert( str( uaf1 ) == uaf1_str )
    
    print( uaf2 )
    uaf2_str= 'uaf([(0,2)1(3,5)]](3,5)-1/2(5,4)[[(5,4)15(+Infinity,+Infinity)])'
    assert( str( uaf2 ) == uaf2_str )
    
    print( uaf3 )
    uaf3_str= 'uaf([(0,0)1(+Infinity,+Infinity)])'
    assert( str( uaf3 ) == uaf3_str )

    if readUAF(  uaf3_str ) == uaf3:
        print("Test OK: UAF1")
    else:
        print("Test failed: UAF1")
        print("   Result    :", readUAF( uaf3_str ) )
        print("   Expected  :", uaf3 )
                            
    if readUAF(  uaf1_str ) == uaf1:
        print("Test OK: UAF2")
    else:
        print("Test failed: UAF2")
        print("   Result    :", readUAF( uaf1_str ) )
        print("   Expected  :", uaf1 )

    if readUAF(  uaf2_str ) == uaf2:
        print("Test OK: UAF3")
    else:
        print("Test failed: UAF3")
        print("   Result    :", readUAF( uaf2_str ) )
        print("   Expected  :", uaf2 )

######################################################################
##  Class UPP and related functions
##
## An UPP has a prefix and an periodic part. The periodic part has a
## period and an increment.
##
##  The prefix and the suffix are list of segment
##  The increment and the period are  either an integer or a fraction

class UPP:
     def __init__(self,prefix,suffix,period,increment):
          self.prefix= prefix
          self.suffix= suffix
          self.period= period
          self.increment= increment
                 
     def addSegment(self,s):
        self.seg_list.append(s)
        return self

     def addSegmentList(self,l):
        self.seg_list.extend(l)
        return self

     def __eq__(self,other):
        if not isinstance(other, UPP):
            return False
        s_len= len( self.seg_list )
        o_len= len( other.seg_list )
        if s_len != o_len:
            return False
        for i in range(s_len):
            if self.seg_list[i] != other.seg_list[i]:
                return False
        return True

     def __str__(self):
        res= 'upp('
        for i in self.seg_list:
            res+= str( i )
        return res+ ')'
      
  
     
        
        
def main():
    """
    Create a function main() which has the code to be run.
    """
    # print(Segment(False, Point(str(0),str(1)),str(1),Point("+Infinity","+Infinity"),True))
    #](0,1)2(+Infinity,+Infinity)[
    # print(Segment(True, Point(0,1),2,Point("+Infinity","+Infinity"),True))
    # print( Segment( False, Point(11,-2), 1, Point("+Infinity","+Infinity"), True ) )
    test_str_to_int_if_possible()
    test_readSegment()
    test_readUAF()


main()

