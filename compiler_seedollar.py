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

def nativetype(typelabel):
    if typelabel in ["short", "int", "long", "float", "double", "char"]:
        return 1
    return 0

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

class BluePrint(object):
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.methodes = []
        self.constructor_extensions = ""
        self.constructor_arguments = ""
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
        c += self.constructor_extensions + "\n}\n"
        c += self.name + "* $None_" + self.name + "(" + self.name + "* obj){\n"
        c += "\tfree(obj);\n\treturn (" + self.name + "*) NULL;\n"
        c += "}\n"
        return c

argv = sys.argv
argc = len(argv)

if argc <= 2:
    print("Too few arguments! [usage:] seedollar path/to/c_code")
    exit(1)
path_to_file = argv[1]
write_to_path = argv[2]
cdo_file = open(path_to_file, "r")
code = cdo_file.read()
cdo_file.close()

code = re.sub(
    r"//.*\n",
    "",
    code
)

#code = input(">>> ")

classes = []
def compile_to_c(code):
    global classes
    code = code.replace("$", " $ ")
    code = code.replace("(", " ( ")
    code = code.replace(")", " ) ")
    code = code.replace("{", " { ")
    code = code.replace("}", " } ")
    code = code.replace(";", " ; ")
    sc = Scanner(code.strip().split())
    blueprint = None
    c_code = ""
    while sc.hasNext():
        command = sc.next()
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
                                blueprint.constructor_extensions = sc.readCurlyBreaket()
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
c_code = compile_to_c(code)
c_code = "void $throw(char* exception, char* message, int line, char* function_name);" + c_code + """
void $throw(char* exception, char* message, int line, char* function_name){
    fprintf(stderr, "\\n[Exception:%s] %s \\nReference -> line: %i, function:%s\\n\\n", exception, message, line, function_name);
}
"""

print("Compiling is done!")
output_file = open(write_to_path, "w")
output_file.write(c_code)
output_file.close()
print("Writing to '"+write_to_path+"' is done!")