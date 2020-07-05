void $throw(char* exception, char* message, int line, char* function_name);
#include <stdio.h> 
#include <stdlib.h> 
typedef struct Person {
	char* first_name;
	char* last_name;
	int age;
	void (*print)(struct Person* self);
} Person;
void Person__print(Person* self){
 printf ( "First name: %s\n", self->first_name ) ; printf ( "Last name: %s\n", self->last_name ) ; printf ( "Age: %i\n", self->age ) ;
}
Person* $Person( char* first_name, char* last_name, int age){
	Person* self = (Person*) malloc(sizeof(Person));
	if(self==NULL) $throw("Build Person", "Out of Memory", __LINE__, "$Person");
	self->first_name=NULL;
	self->last_name=NULL;
	self->age=0;
	self->print=Person__print;
 self->first_name = first_name ; self->last_name = last_name ; self->age = age ;
}
Person* $None_Person(Person* obj){
	free(obj);
	return (Person*) NULL;
}
int main ( int argc, const char **argv ) { Person* simon = $Person ( "Simon", "Smith", 20 ) ; simon->print ( simon ) ; simon = $None_Person ( simon ) ; return 0 ;}
void $throw(char* exception, char* message, int line, char* function_name){
    fprintf(stderr, "\n[Exception:%s] %s \nReference -> line: %i, function:%s\n\n", exception, message, line, function_name);
}
