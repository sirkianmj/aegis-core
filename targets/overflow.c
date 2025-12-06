#include <stdio.h>
#include <unistd.h>
#include <string.h>

// The goal: Jump here!
void hacker_win() {
    printf("\n[!!!] PWNED! YOU HIJACKED CONTROL FLOW! [!!!]\n");
}

void vulnerable_function() {
    char buffer[64];
    
    printf("Waiting for input: ");
    // VULNERABILITY: Reads 200 bytes into 64 byte buffer
    // This allows us to overwrite the Return Address on the stack.
    read(0, buffer, 200); 
}

int main() {
    vulnerable_function();
    printf("Normal exit.\n");
    return 0;
}