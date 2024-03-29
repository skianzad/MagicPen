#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>
#include <bluetooth/hci_lib.h>

int main(int argc, char **argv) {
	inquiry_info* ii = NULL;
	int max_rsp, num_rsp;
	int dev_id, sock, len, flags;
	char addr[19] = { 0 };
	char name[248] = { 0 };

	dev_id = hci_get_route(NULL);
	sock = hci_open_dev(dev_id);

	if (dev_id < 0 || sock < 0) {
		perror("failed to open socket");
		return 1;
	}

	len = 20;

	max_rsp = 255;

	flags = IREQ_CACHE_FLUSH;

	ii = (inquiry_info*)malloc(max_rsp * sizeof(inquiry_info));

	while (1) {
		printf("Scanning...\n");
		num_rsp = hci_inquiry(dev_id, len, max_rsp, NULL, &ii, flags);

		if (num_rsp < 0) {
			perror("hci inquiry failed");
		}

		printf("Num response: %i\n",  num_rsp);

		for (int i = 0; i < num_rsp; i++) {
			ba2str(&(ii + i)->bdaddr, addr);
			memset(name, 0, sizeof(name));

			if (hci_read_remote_name(sock, &(ii + i)->bdaddr, sizeof(name), name, 0) < 0) {
				strcpy(name, "[unknown]");
			}

			printf("%s : %s\n", name, addr);
		}
	}


	free(ii);
	close(sock);
	return 0;
}
