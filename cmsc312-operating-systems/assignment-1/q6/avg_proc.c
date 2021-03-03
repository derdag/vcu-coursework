#include <rpc/rpc.h>
#include "avg.h"
#include <stdio.h>
#include <stdlib.h>

static double sum_avg;
static double median_val;

// compare helper function for qsort
int compare(const void *x, const void *y)
{
	return (*(double *)x - *(double *)y);
}

input_data *average_1(input_data *input, CLIENT *client)
{
	double *dp = input->input_data.input_data_val;
	int n = input->input_data.input_data_len;
	double arr[n];
	u_int i, j;

	for (i = 0; i < n; i++)
	{
		arr[i] = *dp;
		dp++;
	}

	qsort(arr, n, sizeof(arr[0]), compare);

	dp = input->input_data.input_data_val;

	for (j = 1; j < n; j++)
	{
		*dp = arr[j];
		dp++;
	}

	return (input);
}

input_data *average_1_svc(input_data *input, struct svc_req *svc)
{
	CLIENT *client;
	return (average_1(input, client));
}
