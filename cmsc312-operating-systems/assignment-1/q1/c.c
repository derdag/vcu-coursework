#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define INTSHMSZ 1
#define STRINGSHMSZ 6

int main()
{
        int intshmid, stringshmid;
        key_t intkey, stringkey;
        char *stringshm, *intshm, *s, *i;

        intkey = 3412;
        stringkey = 3422;

        if ((intshmid = shmget(intkey, INTSHMSZ, IPC_CREAT | 0666)) < 0)
        {
                perror("shmget");
                exit(1);
        }

        if ((stringshmid = shmget(stringkey, STRINGSHMSZ, IPC_CREAT | 0666)) < 0)
        {
                perror("shmget");
                exit(1);
        }

        if ((intshm = shmat(intshmid, NULL, 0)) == (char *)-1)
        {
                perror("shmat");
                exit(1);
        }
        if ((stringshm = shmat(stringshmid, NULL, 0)) == (char *)-1)
        {
                perror("shmat");
                exit(1);
        }

        i = intshm;

        while (*intshm != '2')
                sleep(1);

        s = stringshm;

        strcpy(s, "memory");

        *i = '3';

        return 0;
}
