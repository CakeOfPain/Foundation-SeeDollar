# It's c with classes, but gets compiled to pure c
Classes which are defined, will be compiled into structs and functions.

# Aims:
* Code like in c, but with classes based on structs. 
* Memory management, included garbage collection. 
* Simple error handling. 
* does not replace most of c

# Program code like this:
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

int main(int argc, const char \*\*argv)
{
  Name_of_class* obj = $Name_of_class("String", 0);
  obj->methode1(obj, 2);
  obj = $None_Name_of_class(obj);
  return 0;
}
´´´
