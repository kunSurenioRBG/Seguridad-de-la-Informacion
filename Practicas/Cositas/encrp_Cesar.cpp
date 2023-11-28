#include <iostream>

using namespace std;

void encriptar(char mensaje[100], int n);

// alfabeto ingles (26 letras)
char ABC[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
char abc[] = "abcdefghijklmnopqrstuvwxyz";
int n = 0;

int main()
{
    cout << "introduce una cadena de caracteres: ";
    char cadena[100];
    cin.getline(cadena, 100);
    cout << "introduce un numero: ";
    cin >> n;
    encriptar(cadena, n);
    cout << cadena;
    return 0;
}

void encriptar(char mensaje[100], int n)
{
    int i = 0;
    while (mensaje[i] != '\0')
    {
        mensaje[i] += n;
        if (mensaje[i] >= 'A' && mensaje[i] <= 'Z')
        {
            if (mensaje[i] < 'A')
            {
                mensaje[i] += 26;
            }
            else if (mensaje[i] > 'Z')
            {
                mensaje[i] -= 26;
            }
        }
        else if (mensaje[i] >= 'a' && mensaje[i] <= 'z')
        {
            if (mensaje[i] < 'a')
            {
                mensaje[i] += 26;
            }
            else if (mensaje[i] > 'z')
            {
                mensaje[i] -= 26;
            }
        }
        
        i++;
    }
}