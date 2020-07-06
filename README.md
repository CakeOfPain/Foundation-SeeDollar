![Seedollar Logo](Logo.png =176x186)
# It's c with classes, but gets compiled to pure c
Defined classes, will be compiled into structs and functions.

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
  
  $void methode1(int arg1)
  {
    self->attribute2 = arg1;
  }
}

int main(int argc, const char **argv)
{
  Name_of_class* obj = $Name_of_class("String", 0);
  obj->methode1(obj, 2);
  obj = $None_Name_of_class(obj);
  return 0;
}
```

## Compile to c
### Windows
`python compiler_seedollar.py file.sdo file.c`
or if you rename the compiler: `python <name of compiler>.py file.sdo file.c`
### Linux
`./compiler_seedollar.py file.sdo file.c`
or if you rename the compiler: `./<name of compiler>.py file.sdo file.c`
