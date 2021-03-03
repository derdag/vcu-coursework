#include <sys/types.h>
#include <sys/shm.h>
#include <stdlib.h>
#include <stdio.h>

#include <unistd.h>

#define INTSHMSZ 1    // maybe this should be more than one, its just supposed to hold 1 int
#define STRINGSHMSZ 6 //double check this length too

// process A writes '1' to integer shared memory location, then waits until B & C complete

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

    // write '1' to integer shared memory location
    i = intshm;
    *i = '1';

    pid_t b, c;

    b = fork();

    if (b == 0)
    {
        // b code
    }
    else
    {
        c = fork();

        if (c == 0)
        {
            // c code
        }
        else
        {
            // a code
        }
    }

    // poll for int shared memory = '1'
    while (*intshm != '1')
        sleep(1);

    // poll for int shared memory = '2'
    while (*intshm != '2')
        sleep(1);

    printf("%s\n", stringshm); //print string from shared memory, should be string "shared"

    // poll for int shared memory = '3'
    while (*intshm != '3')
        sleep(1);

    printf("%s\n", stringshm); //print string from shared memory, should be string "memory"

    //process A is the last one to quit and prints out a 'Goodbye' message before quitting
    printf("Goodbye!\n");

    shmdt(stringshm); //this detaches from shared memory
    shmdt(intshm);
    shmctl(intshmid, IPC_RMID, NULL); //this destroys shared memory
    shmctl(stringshmid, IPC_RMID, NULL);

    return 0;
}
