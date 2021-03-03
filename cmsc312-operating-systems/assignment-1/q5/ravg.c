#include "avg.h" /* header file generated by rpcgen */
#include <stdlib.h>

/* local routine client */
/* prototype can be whatever you want */
void averageprog_1(char *host, int argc, char *argv[])
{
	CLIENT *clnt; /* client handle, rpc.h included in avg.h from rpcgen */
	int i;
	char f, *dp, *endptr, **result;

	result = &argv[2];
	clnt = clnt_create(host, AVERAGEPROG, AVERAGEVERS, "udp");

	/* check if error */
	if (clnt == NULL)
	{
		clnt_pcreateerror(host);
		exit(1);
	}

	result = average_1(result, clnt);

	if (result == NULL)
	{
		clnt_perror(clnt, "call failed:");
	}

	clnt_destroy(clnt);

	printf("%s\n", *result);
}

/* here is main */
main(int argc, char *argv[])
{
	char *host;

	/* check correct syntax */
	if (argc < 3)
	{
		printf("usage: %s server_host value ...\n", argv[0]);
		exit(1);
	}

	if (argc > MAXAVGSIZE + 2)
	{
		printf("Two many input values\n");
		exit(2);
	}

	/* host name is in first parameter (after program name) */
	host = argv[1];
	averageprog_1(host, argc, argv);
}