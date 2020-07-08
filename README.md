![Seedollar Logo](Logo.png)
# It's C with classes, but gets compiled to pure c
Defined classes, will be compiled into structs and functions.

## In which cases is Seedollar helpful?
Seedollar is not everyone's thing, especially if you're used to code in C++ or Java.
But if you have to switch from these languages into C, then it might be the right thing for you.
The problem is that C doesn't like classes like in OOP languages. C only accepts structs that cannot contain any functions (except function-pointers).
C-structs are complexe, especially it comes to dynamic created structs which you need in order to use dynamic lists and other data-structures.
So if you're not used to c-structs and you don't want to deal with these things, then Seedollar is
for you.

## Aims:
* Code like in c, but with classes based on structs. 
* Memory management, included garbage collection. 
* Simple error handling. 
* does not replace most of c

## Program code like this:
```
$Name_of_class 
{
  char* attribute1;
  int attribute2;
  $(char* attr1, int attr2)
  {
    self->attribute1 = attr1;
    self->attribute2 = attr2;
  }
  
  $void method1(int arg1)
  {
    self->attribute2 = arg1;
  }
}

int main(int argc, const char **argv)
{
  Name_of_class* obj = $Name_of_class("String", 0);
  obj->method1(obj, 2);
  obj = $None_Name_of_class(obj);
  return 0;
}
```

## Usage (Things that Seedollar don't like yet)
* If you're about to define an array in a class, than you better define it like this: `char* string;` or `int* integer_array;`
* If you want to use a reference of the class in which you define, you do it like this: `this name_of_reference;`
* don't define unions and other structs in a class
* Don't use Seedollar, if you don't use it in your code

## Compile to c
### Windows
`python compiler_seedollar.py file.sdo file.c`
or if you rename the compiler: `python <name of compiler>.py file.sdo file.c`
### Linux
`./compiler_seedollar.py file.sdo file.c`
or if you rename the compiler: `./<name of compiler>.py file.sdo file.c`

# Please report bugs and help to improve Seedollar