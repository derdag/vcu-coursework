#include <rpc/rpc.h>
#include "avg.h"
#include <stdio.h>
#include <stdlib.h>

static double sum_avg;
static double median_val;

char **average_1(char **input, CLIENT *client)
{
	// printf("%s\n", *input); // uncomment this line if we would like server to print the message as well
	return (input);
}

char **average_1_svc(char **input, struct svc_req *svc)
{
	CLIENT *client;
	return (average_1(input, client));
}
