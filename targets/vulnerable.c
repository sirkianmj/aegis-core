#include <stdio.h>
#include <string.h>
#include <unistd.h>

// The "Sink" - We want the AI to reach this function
void critical_system_access() {
    printf("SUCCESS_ACCESS_GRANTED_LEVEL_9\n");
}

void secure_gate() {
    char buffer[64];
    
    printf("AEGIS SECURITY GATE. ENTER PASSCODE: ");
    
    // Read input from user
    read(0, buffer, 64);
    
    // Strip newline if present
    buffer[strcspn(buffer, "\n")] = 0;

    // The "Branch" - The AI must mathematically solve this constraint
    if (strcmp(buffer, "AegisTopSecret") == 0) {
        critical_system_access();
    } else {
        printf("ACCESS DENIED. LOCKING DOWN.\n");
    }
}

int main() {
    secure_gate();
    return 0;
}