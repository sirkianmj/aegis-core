
        #include <stdio.h>
        #include <unistd.h>
        int main() {
            char buf[10];
            read(0, buf, 10);
            if (buf[0] == 'A') {
                if (buf[1] == 'E') {
                    if (buf[2] == 'G') {
                        if (buf[3] == 'I') {
                            if (buf[4] == 'S') {
                                printf("SUCCESS_ACCESS_GRANTED");
                            }
                        }
                    }
                }
            }
            return 0;
        }
        