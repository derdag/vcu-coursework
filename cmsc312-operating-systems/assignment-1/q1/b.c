#include <sys/types.h>
#include <sys/shm.h>
#include <stdlib.h>
#include <string.h>

#include <unistd.h>

// integers are 4 bytes, char 1 byte
#define INTSHMSZ 1    // maybe this should be more than one, its just supposed to hold 1 int
#define STRINGSHMSZ 6 //double check this length too

// process B

int main()
{

    int intshmid, stringshmid;
    key_t intkey, stringkey;
    char *stringshm, *s; //idk what the second parameter is?? or first?
    int *intshm, *i;     //maybe make this a string too for the int shared memory

    // create key for memory segments
    intkey = 3456;
    stringkey = 4567;

    // here we create/locate the segment
    // can consider wrapping these statement in an if () < 0, to check if error with shmget, then exit(1)
    intshmid = shmget(intkey, INTSHMSZ, IPC_CREAT | 0666);
    stringshmid = shmget(stringkey, STRINGSHMSZ, IPC_CREAT | 0666);

    // attach segment to dataspace
    intshm = shmat(intshmid, NULL, 0);
    stringshm = shmat(stringshmid, NULL, 0);

    i = intshm; // idk what this does tbh

    // process B waits to see '1' in integer shared memory.
    while (*intshm != '1')
        sleep(1);

    // writes string "shared" to string shared memory
    s = stringshm;

    strcpy(s, "shared");

    // wait for a to print string
    while (*intshm != '*')
        sleep(1);

    // process B writes '2' in integer shared memory, signalling it is complete

    *i = '2';

    return 0;
}
