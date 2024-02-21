#include <algorithm> 
#include <fstream>
#include <iostream>
#include <iterator>
#include <math.h>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

char map[16][16] = {
                    {0x8, 0x9, 0xb, 0xa, 0xe, 0xf, 0xd, 0xc, 0x4, 0x5, 0x7, 0x6, 0x2, 0x3, 0x1, 0x0 },
                    {0x9, 0xb, 0xa, 0xe, 0xf, 0xd, 0xc, 0x4, 0x5, 0x7, 0x6, 0x2, 0x3, 0x1, 0x0, 0x8 },
                    {0xb, 0xa, 0xe, 0xf, 0xd, 0xc, 0x4, 0x5, 0x7, 0x6, 0x2, 0x3, 0x1, 0x0, 0x8, 0x9 },
                    {0xa, 0xe, 0xf, 0xd, 0xc, 0x4, 0x5, 0x7, 0x6, 0x2, 0x3, 0x1, 0x0, 0x8, 0x9, 0xb },
                    {0xe, 0xf, 0xd, 0xc, 0x4, 0x5, 0x7, 0x6, 0x2, 0x3, 0x1, 0x0, 0x8, 0x9, 0xb, 0xa },
                    {0xf, 0xd, 0xc, 0x4, 0x5, 0x7, 0x6, 0x2, 0x3, 0x1, 0x0, 0x8, 0x9, 0xb, 0xa, 0xe },
                    {0xd, 0xc, 0x4, 0x5, 0x7, 0x6, 0x2, 0x3, 0x1, 0x0, 0x8, 0x9, 0xb, 0xa, 0xe, 0xf },
                    {0xc, 0x4, 0x5, 0x7, 0x6, 0x2, 0x3, 0x1, 0x0, 0x8, 0x9, 0xb, 0xa, 0xe, 0xf, 0xd },
                    {0x4, 0x5, 0x7, 0x6, 0x2, 0x3, 0x1, 0x0, 0x8, 0x9, 0xb, 0xa, 0xe, 0xf, 0xd, 0xc },
                    {0x5, 0x7, 0x6, 0x2, 0x3, 0x1, 0x0, 0x8, 0x9, 0xb, 0xa, 0xe, 0xf, 0xd, 0xc, 0x4 },
                    {0x7, 0x6, 0x2, 0x3, 0x1, 0x0, 0x8, 0x9, 0xb, 0xa, 0xe, 0xf, 0xd, 0xc, 0x4, 0x5 },
                    {0x6, 0x2, 0x3, 0x1, 0x0, 0x8, 0x9, 0xb, 0xa, 0xe, 0xf, 0xd, 0xc, 0x4, 0x5, 0x7 },
                    {0x2, 0x3, 0x1, 0x0, 0x8, 0x9, 0xb, 0xa, 0xe, 0xf, 0xd, 0xc, 0x4, 0x5, 0x7, 0x6 },
                    {0x3, 0x1, 0x0, 0x8, 0x9, 0xb, 0xa, 0xe, 0xf, 0xd, 0xc, 0x4, 0x5, 0x7, 0x6, 0x2 },
                    {0x1, 0x0, 0x8, 0x9, 0xb, 0xa, 0xe, 0xf, 0xd, 0xc, 0x4, 0x5, 0x7, 0x6, 0x2, 0x3 },
                    {0x0, 0x8, 0x9, 0xb, 0xa, 0xe, 0xf, 0xd, 0xc, 0x4, 0x5, 0x7, 0x6, 0x2, 0x3, 0x1 }
                  };

/*                                      KEY LENGTH FUNCTIONS                                                            */

int findFrequentDivisor(std::vector <std::vector <int>> divisors){

    std::unordered_map <int, int> divisorCounts;
    std::vector <int> tempDiv;
    for (unsigned int i = 0; i < divisors.size(); i++){
        tempDiv = divisors[i];
        for (unsigned int j = 0; j < tempDiv.size(); j++){
            if ( !divisorCounts[tempDiv[j]] ){
                divisorCounts[tempDiv[j]] = 1;
            } 
            else{
                divisorCounts[tempDiv[j]] ++;
            }
        }
    }
    std::vector <std::pair <int, int> > divisorFreq;
    for ( auto i : divisorCounts ){
        divisorFreq.push_back( std::pair <int, int> (i.first, i.second) );
    } 
    std::sort(divisorFreq.begin(), divisorFreq.end(), [](std::pair <int, int> &left, std::pair <int, int> &right){
            return left.second > right.second;
            });
    
    int mostCommonDivisor = divisorFreq[0].first;
    return mostCommonDivisor;
}

std::vector <int> findDivisors(int number){
    std::vector <int> divisors;
    /* Don't consider 1, 2, or 3 as divisors since they're too common and too trivial as key lengths */
    for ( unsigned int i = 4; i < sqrt(number); i++ ){
        if ( number % i == 0 ) divisors.push_back(i);
    }
    return divisors;
}

int findKeyLength(std::vector <char>  ciphertextArray){

    std::unordered_map <std::string, int> repeatedStrings;
    std::vector <int> charDistance;
    std::string ciphertext (ciphertextArray.begin(), ciphertextArray.end());

    std::string subString;
    const int SUBSTRLEN = 4;

    for ( unsigned int i = 0; i < ciphertext.length(); i++ ){
        subString = ciphertext.substr(i, SUBSTRLEN);
        if ( !repeatedStrings[subString] ){
            repeatedStrings[subString] = i;
        }
        else{
            charDistance.push_back( i - repeatedStrings[subString] );
            repeatedStrings[subString] = i;
        }
    }

    /* Find the most frequent divisor among all the character lengths */
    std::vector <int> divisors;
    std::vector <std::vector <int> > allDivisors;
    for (unsigned int i = 0; i < charDistance.size(); i++){
        divisors = findDivisors(charDistance[i]);
        allDivisors.push_back(divisors);
    }

    int keyLen = findFrequentDivisor(allDivisors);
    return keyLen;
}



/*                            DECIPHERING FUNCTIONS                                                                           */


/* Description: divideCipherText() will take in a string of ciphertexts, and will divide the ciphertexts 
 * into n portions, where n = keyLength.
 *
 * Input: 
 *  ciphertext: array of cipherbytes
 *  keyLength: length of the key
 * Returns:
 *  Array of strings divided into n entries, where n = keyLength
 * */
std::vector <std::string> divideCipherText(std::vector <char> ciphertext, int keyLength){
    std::vector <std::string> cipherColumns (keyLength, std::string(""));
    std::string tempStr;
    int idx = 0;

    for ( unsigned int i = 0; i < ciphertext.size(); i++ ){
        idx = i % keyLength;
        tempStr = cipherColumns[idx];
        tempStr += ciphertext[i];
        cipherColumns[idx] = tempStr;
    }

    return cipherColumns;
}
/* Converts a cipherbyte to ASCII using the map
 * Input:
 *  Cyberbyte: The byte to the translated to ASCII
 *  key: The byte used to index the map
 *Returns:
    The tranlsated ASCII byte
 */
char cipherToASCII(unsigned char cipherByte, char key){
    int kl = (key & 0x0F);
    int kh = (unsigned int)(key & 0xF0) >> 4;

    unsigned char  cl = (cipherByte & 0x0F);
    unsigned char  ch = (cipherByte & 0xF0) >> 4;

    char pl = 0;
    char ph = 0;

    for ( int i = 0; i < 16; i++ ){
        if ( map[i][kl] == ch ) ph = i;
        if ( map[i][kh] == cl ) pl = i;
    }
    return (ph << 4) | pl;

}
/* Determines if the given byte is ASCII printable or not. */
bool isPrintableASCII(unsigned char byte){
    unsigned char byteH = (unsigned char)(byte & 0xF0) >> 4;
    /* Check if upperbits of byte is printable character or newline (0x0A)*/
    if ((byteH >= 0x02 && byteH <= 0x07) || byte == 0x0A ) return true;
    return false;
}
/* Given the character frequecies of a string, will determine if its is human intelligible */
bool isEnglish(std::vector <std::pair <char, int>> charFrequency){
    if (charFrequency.size() < 2) return false;
    /* Sort array based on character frequency in descending order to get most frequently occuring first in array */
    std::sort(charFrequency.begin(), charFrequency.end(), [](std::pair <char, int> &left, std::pair <char, int> &right){
            return left.second > right.second;
            });

    /* By checking the two most frequently occuring characters, we see if it is a lowercase letter or a space */
    int invalidChars = 0;
    for (unsigned int i = 0; i < 2; i++){
        std::pair <char, int> charPair = charFrequency[i];
        if ((charPair.first < 'a' || charPair.first > 'z') && charPair.first != ' '){
            invalidChars ++;
        } 
    }
    return (invalidChars == 0);
}
/* Counts the occurences of a character in the string */
std::vector <std::pair <char, int>> frequencyAnalysis(std::string plaintext){
    std::unordered_map <char, int> charCount;
    std::vector <std::pair <char, int>> allCharCounts;
    for (char c : plaintext){
        if (!charCount[c]){
            charCount[c] = 1;
        }
        else{
            charCount[c] ++;
        }
    }
    for (auto i : charCount){
        allCharCounts.push_back(std::pair <char, int> (i.first, i.second));
    }
    return allCharCounts;
} 
/* For each possible key in the range of printable keys, 
 *      First decipher the plaintext by translating each cipherbyte to ASCII.
 *          If is not a printable ASCII, then stop and use a different key
 *      Second, count the frequency of the characters.
 *      Third, determine if the frequency counts of the characters is similar to human language.
 * */
std::string decipherCaesar(std::string ciphertext){
    std::string plaintext = "";

    bool canPrint = false;
    for ( int kh = 0x0; kh <= 0x07; kh++ ){
        for ( int kl = 0x0; kl <= 0x0F; kl++ ){

            char tryKey = (kh << 4) | kl;
            plaintext = "";
            for (unsigned char c : ciphertext){
                unsigned char byte = cipherToASCII(c, tryKey);
                if (isPrintableASCII(byte)){
                    plaintext += byte;
                    canPrint = true;
                }
                else{
                    canPrint = false;
                    plaintext = "";
                    break;
                }
            }

            if (canPrint){
                std::vector <std::pair <char, int>>charFrequency = frequencyAnalysis(plaintext);
                if (isEnglish(charFrequency)){
                    std::cout << "KEY " << tryKey << std::endl;
                    return plaintext;
                }
            }

        }
    }
    return plaintext;
}

std::string decipherVignere(std::vector <char> ciphertext){
    /* Get length of key */
    int keyLen = findKeyLength(ciphertext);

    /* Divide ciphertext into n length segments, where n = key length */
    std::vector <std::string> cipherColumns;
    cipherColumns = divideCipherText(ciphertext, keyLen); 

    std::vector <std::string>  plaintextColumns;
    std::string DECRYPTED = "";
    std::string  tempDecrypt;

    /* For each portion, decrypt using caesapr analysis and combien the results together*/
    for (unsigned int i = 0; i < cipherColumns.size(); i++){
        tempDecrypt = decipherCaesar(cipherColumns[i]);
        plaintextColumns.push_back(tempDecrypt);
    }
    
    /* Combine all the deciphered plaintext segments together*/
    unsigned int colLength = plaintextColumns[0].length();
    for ( unsigned int i = 0; i < colLength; i++ ){
        for ( unsigned int j = 0; j < plaintextColumns.size(); j++ ){
            if ( i < plaintextColumns[j].length() )
                DECRYPTED += plaintextColumns[j][i];
        }
    } 
    return DECRYPTED;
}

int main(){

    std::ifstream cipherInput("ciphertext2", std::ios::binary);
    std::vector<char> ciphertextRaw((std::istreambuf_iterator<char>(cipherInput)),(std::istreambuf_iterator<char>()));
    cipherInput.close();

    /* Try to read only the first 2000 bytes to get the file signature. */
    std::vector <char> ciphertext;
    for (unsigned int i = 0; i < 2000; i++){
        ciphertext.push_back(ciphertextRaw[i]);
    }

    std::string plaintext = decipherVignere(ciphertext);
    std::cout << "\nDecrypted message:\n" << plaintext << std::endl;

    std::cout << std::endl;
    return 0;
}
