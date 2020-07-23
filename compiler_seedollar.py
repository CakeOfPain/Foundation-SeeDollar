#!/usr/bin/python

# Autor: Leo Englert
# describtion: Compiles c$-code to pure c-code
import sys
import re

# Steps:
#       1. Load the content of the target file
#       2. split it up in words (TODO: Make sure string and new-lines doesn't get destructed)
#       3. interpret all words, keyword is the dollarsign
#       4. compile the classes into structs and functions
#       5. build file.c

# This function checks if the type is a numeric type or a pointer, if so it returns 1 for numeric or 0 for pointer
def nativetype(typelabel):
    if typelabel in ["short", "int", "long", "float", "double", "char"]:
        return 1
    return 0

# This class is a scanner which finds codeblocks and other structures in the code
class Scanner(object):
    def __init__(self, code):
        self.code = code
        self.size = len(code)
        self.counter = 0
    def hasNext(self):
        if self.counter < self.size:
            return True
        return False
    def next(self):
        self.counter += 1
        return self.code[self.counter-1]
    def back(self):
        self.counter -= 1
        return self.code[self.counter+1]
    def peek(self):
        return self.code[self.counter]
    def peeknext(self):
        return self.code[self.counter+1]
    def readCurlyBreaket(self):
        if(self.next() != "{"):
            print("[Seedolar] Syntax Error! Missing {")
            exit(1)
        are_open = 0
        content = ""
        while self.hasNext():
            command = self.next()
            if(command == "{"):
                are_open += 1
                content += " { "
            elif(command == "}"):
                if(are_open == 0):
                    break
                else:
                    are_open -= 1
                    content += " } "
            else:
                content += " " + command
        return content
    def readBreaket(self):
        if(self.next() != "("):
            print("[Seedolar] Syntax Error! Missing (")
            exit(1)
        are_open = 0
        content = ""
        while self.hasNext():
            command = self.next()
            if(command == "("):
                are_open += 1
                content += " ( "
            elif(command == ")"):
                if(are_open == 0):
                    break
                else:
                    are_open -= 1
                    content += " ) "
            else:
                content += " " + command
        return content

def typeindex(index):
    if index == 0:
        return "NULL"
    elif index == 1:
        return "0"

# This class is a type of form, to compile the class-definition into pure c (functions and structs)
class BluePrint(object):
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.methodes = []
        self.constructor_extension = ""
        self.constructor_arguments = ""
        self.destructor_extension = ""
    # This method compiles the values of the form into pure c
    def build_c(self):
        global typeindex
        c = ""
        c += "typedef struct " + self.name + " {\n"
        for x in self.attributes:
            c += "\t" + x[1] + " " + x[2] + ";\n"
        for x in self.methodes:
            if x[2] != "":
                c += "\t" + x[0] + " (*" + x[1] + ")(struct " + self.name + "* self, " + x[2] + ");\n"
            else:
                c += "\t" + x[0] + " (*" + x[1] + ")(struct " + self.name + "* self);\n"
        c += "} " + self.name + ";\n"
        for x in self.methodes:
            c += x[0] + " " #type
            if x[2] == "":
                c += self.name + "__" + x[1] + "(" + self.name + "* self" #name
            else:
                c += self.name + "__" + x[1] + "(" + self.name + "* self, " #name
            c += x[2] + "){\n" # arguments
            c += x[3] + "\n}\n" # content
        c += self.name + "* $" + self.name + "(" + self.constructor_arguments + "){\n"
        c += "\t" + self.name + "* self = ("+self.name+"*) malloc(sizeof("+self.name+"));\n"
        c += '\tif(self==NULL) $throw("Build ' + self.name + '", "Out of Memory", __LINE__, "$'+self.name+'");\n'
        for x in self.attributes:
            c += "\tself->" + x[2] + "=" + typeindex(x[0]) + ";\n" #1 = Name, 0 = type
        for x in self.methodes:
            c += "\tself->" + x[1] + "=" + self.name + "__" + x[1] + ";\n"
        c += self.constructor_extension + "\n return self; \n}\n"
        c += self.name + "* $None_" + self.name + "(" + self.name + "* obj){\n"
        c += self.destructor_extension + "\n"
        c += "\tfree(obj);\n\treturn (" + self.name + "*) NULL;\n"
        c += "}\n"
        return c

# Gets the arguments from the system (console) and the number of arguments. It's like in the main function of c
argv = sys.argv
argc = len(argv)

# Checks that we have at least two (actually three) arguments
if argc <= 2:
    print("Too few arguments! [usage:] seedollar path/to/c_code")
    exit(1)

path_to_file = argv[1] # target file (path)
write_to_path = argv[2] # build file (path)
# Reads whole content of target file
cdo_file = open(path_to_file, "r")
code = cdo_file.read()
cdo_file.close()

# Removes all line-comments of the code
code = re.sub(
    r"//.*\n",
    "",
    code
)

# List of classes that were created (At the moment unused, maybe later on)
classes = []

# Function which compiles Seedollar-code into pure c
def compile_to_c(code):
    global classes
    # splits all operators that are relevant for compiling with spaces
    code = code.replace("$", " $ ")
    code = code.replace("(", " ( ")
    code = code.replace(")", " ) ")
    code = code.replace("{", " { ")
    code = code.replace("}", " } ")
    code = code.replace(";", " ; ")
    # Creates a scanner for going through all words in the code
    sc = Scanner(code.strip().split())
    # placeholder blueprint reference
    blueprint = None
    # string which gets returned as c-code at the end of the function
    c_code = ""
    while sc.hasNext(): # loops through all words in the code (if scanner has no word left, sc.hasNext() returns False)
        command = sc.next() # command is a placeholder for the current word

        # goes through all the syntax and builds for defined classes blueprints (blueprints gets compiled into c structs and functions)
        if command == "{":
            sc.back()
            c_code += "{" + sc.readCurlyBreaket() + "}"
        elif command == "$":
            if sc.peek() == "(":
                include_path = sc.readBreaket().strip()
                include_file = open(include_path, "r")
                include_code = include_file.read()
                include_file.close()
                include_code = compile_to_c(include_code)
                c_code += "\n " + include_code + "\n"
            else:
                blueprint = BluePrint(sc.next())
                if sc.next() != "{":
                    print("Syntax Error: excepts {")
                    exit(1)
                else:
                    token = ""
                    methodes = []
                    attributes = []
                    while sc.hasNext():
                        token = sc.next()
                        if token == "$":
                            if sc.peek() == "(":
                                blueprint.constructor_arguments = sc.readBreaket()
                                blueprint.constructor_extension = sc.readCurlyBreaket()
                            elif sc.peek() == "{":
                                blueprint.destructor_extension = sc.readCurlyBreaket()
                            else:
                                methodes.append(
                                        [sc.next(), sc.next(), sc.readBreaket(), sc.readCurlyBreaket()]
                                    )
                        elif token == "}":
                            break
                        elif token == "this":
                            attributes.append(
                                [0, "struct " + blueprint.name + "* ", sc.next()]
                            )
                            if sc.next() != ";":
                                        print("Syntax Error: excepts ;")
                                        exit(1)
                        else:
                            attributes.append(
                                    [nativetype(token), token, sc.next()]
                                )
                            if sc.next() != ";":
                                        print("Syntax Error: excepts ;")
                                        exit(1)
                    blueprint.methodes = methodes
                    blueprint.attributes = attributes
                    classes.append(blueprint)
                    c_code += blueprint.build_c()
        else:
            c_code += command + " "
    c_code = c_code.replace("#", "\n#")
    c_code = c_code.replace("typedef", "\ntypedef")
    c_code = c_code.replace("$ ", "$")
    return c_code
c_code = compile_to_c(code) # code of target-file gets compiled into pure c

# Adds throw function for simple error handling (specialy for "Out of Memory")
c_code = "void $throw(char* exception, char* message, int line, char* function_name);" + c_code + """
void $throw(char* exception, char* message, int line, char* function_name){
    fprintf(stderr, "\\n[Exception:%s] %s \\nReference -> line: %i, function:%s\\n\\n", exception, message, line, function_name);
}
"""

# Sends a message to the user that all is compiled
print("Compiling is done!")

# Writes c-code to build-file that the user has defined before
output_file = open(write_to_path, "w")
output_file.write(c_code)
output_file.close()

# Sends a message to the user that everything is completed
print("Writing to '"+write_to_path+"' is done!")