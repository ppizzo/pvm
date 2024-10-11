#include "stdio.h"
#include "string.h"
#include "unistd.h"
#include "fcntl.h"
#include "errno.h"
#include "sys/types.h"
#include "sys/stat.h"
#include "stdlib.h"
#include "stdarg.h"
#include "termios.h"
#include "linux/serial.h

#define TIOCSRS485 0x542F

int main(void) {
	char txBuffer[130];
	char rxBuffer[130];
	int fd;
	struct termios tty_attributes;
	struct serial_rs485 rs485conf;

	if ((fd = open("/dev/ttyACM0",O_RDWR|O_NOCTTY|O_NONBLOCK))<0) {
		fprintf (stderr,"Open error on %s\n", strerror(errno));
		exit(EXIT_FAILURE);
	} else {
		tcgetattr(fd,&tty_attributes);

		// c_cflag
		// Enable receiver
		tty_attributes.c_cflag |= CREAD;

		// 8 data bit
		tty_attributes.c_cflag |= CS8;

		// c_iflag
		// Ignore framing errors and parity errors.
		tty_attributes.c_iflag |= IGNPAR;

		// c_lflag
		// DISABLE canonical mode.
		// Disables the special characters EOF, EOL, EOL2,
		// ERASE, KILL, LNEXT, REPRINT, STATUS, and WERASE, and buffers by lines.

		// DISABLE this: Echo input characters.
		tty_attributes.c_lflag &= ~(ICANON);

		tty_attributes.c_lflag &= ~(ECHO);

		// DISABLE this: If ICANON is also set, the ERASE character erases the preceding input
		// character, and WERASE erases the preceding word.
		tty_attributes.c_lflag &= ~(ECHOE);

		// DISABLE this: When any of the characters INTR, QUIT, SUSP, or DSUSP are received, generate the corresponding signal.
		tty_attributes.c_lflag &= ~(ISIG);

		// Minimum number of characters for non-canonical read.
		tty_attributes.c_cc[VMIN]=1;

		// Timeout in deciseconds for non-canonical read.
		tty_attributes.c_cc[VTIME]=0;

		// Set the baud rate
		cfsetospeed(&tty_attributes,B9600);
		cfsetispeed(&tty_attributes,B9600);

		tcsetattr(fd, TCSANOW, &tty_attributes);

		// Set RS485 mode:
		rs485conf.flags |= SER_RS485_ENABLED;
		/*		if (ioctl (fd, TIOCSRS485, &rs485conf) < 0) {
			printf("ioctl error\n");
			}*/

		txBuffer[0]='#';
		txBuffer[1]='0';
		txBuffer[2]='1';
		txBuffer[3]='0';
		txBuffer[4]='\r';

		// Read a char
		while (read(fd,&rxBuffer,1)==1) {
			printf("%c",rxBuffer[0]);
		}
		printf("\n");
	}

	close(fd);
	return EXIT_SUCCESS;
}
