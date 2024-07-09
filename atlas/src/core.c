#include <stdio.h>
#include <string.h>
#include <unistd.h>

const char* whitelist[] = {"2F9916ED54D1A55ADC45847647DA63C3CEBBA334E8F91038E532019B4544C190", "E071119BFC83EF5C84AF01DEC888940CB191B8C006A10F130E7D0D5CF34D6C8A", "2A6A7975816C168689FCB74B651F3A76FDBBD2F4F93953C19CF34A61512C9A12", "C3C84DF024DD1EBB14B9FA616D7D765394A85DE9519E363F7E5184C4EFF436AF"};
const int whitelistSize = 4;

void generateAndPrintStrings(int base) {
    for (int i = 0; i < 50; i++) {
        char output[33];
        int seed = base + i;
        
        for (int j = 0; j < 32; j++) {
            int charType = seed % 3;
            int charIndex;
            
            if (charType == 0) {
                charIndex = (seed % 10) + '0';
            } else if (charType == 1) {
                charIndex = (seed % 26) + 'A';
            } else {
                charIndex = (seed % 26) + 'a';
            }
            
            output[j] = charIndex;
            seed = (seed * 31 + j) % 1000;
        }

        output[32] = '\0';
        printf("Habitable island identified (2%% reliability): %s\n", output);

    }
}

int main(int argc, char** argv) {
    if (argc != 2) {
        printf("./core <identifier>\n", argv[0]);
        return 1;
    }
    
    for (int i = 0; i < whitelistSize; i++) {
        if (strcmp(argv[1], whitelist[i]) == 0) {

			printf("\nAES ECB 256 recognized.\n");

			printf("Identifier Accepted. Welcome Dave.\n");

			printf("Processing the AI instructions...\n");

            generateAndPrintStrings(i+1);
            return 0;
        }
    }

    printf("\n0\n");
    return 1;
}
