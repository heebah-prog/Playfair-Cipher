from unittest import FunctionTestCase
import numpy as np
from matplotlib.pyplot import flag

# Create a 5x5 matrix using a secret key
def create_matrix(key):
    key = key.upper()
    matrix = [[0 for i in range (5)] for j in range(5)]
    letters_added = []
    row = 0
    col = 0
    # add the key to the matrix
    for letter in key:
        if letter not in letters_added:
            matrix[row][col] = letter
            letters_added.append(letter)
        else:
            continue
        if (col==4):
            col = 0
            row += 1
        else:
            col += 1
    #Add the rest of the alphabet to the matrix
    # A=65 ... Z=90
    for letter in range(65,91):
        if letter==74: # I/J are in the same position
                continue
        if chr(letter) not in letters_added: # Do not add repeated letters
            letters_added.append(chr(letter))
            
    #print (len(letters_added), letters_added)
    index = 0
    for i in range(5):
        for j in range(5):
            matrix[i][j] = letters_added[index]
            index+=1
    return matrix


#Add fillers 'X' if the same letter is in a pair
def separate_same_letters(message):
    index = 0
    while (index<len(message)):
        letter1 = message[index]
        if index == len(message)-1:
            message = message + 'X'
            index += 2
            continue
        letter2 = message[index+1]
        if letter1==letter2:
            message = message[:index+1] + "X" + message[index+1:]
        index +=2   
    return message

#Return the index of a letter in the matrix
#This will be used to know what rule (1-4) to apply
def indexOf(letter,matrix):
    for i in range (5):
        try:
            index = matrix[i].index(letter)
            return (i,index)
        except:
            continue

#Implementation of the playfair cipher
#If encrypt=True the method will encrypt the message
# otherwise the method will decrypt
def playfair(key, message, encrypt=True):
    inc = 1
    if encrypt==False:
        inc = -1
    matrix = create_matrix(key) #create a matrix
    message = message.upper() # Capitalized each letters
    message = message.replace(' ','')  # Remove spaces betweeen letters  
    message = separate_same_letters(message) # Add filler X if letters appear in pairs

    cipher_text=''
    for (letter1, letter2) in zip(message[0::2], message[1::2]):
        row1,col1 = indexOf(letter1,matrix)
        row2,col2 = indexOf(letter2,matrix)
        if row1==row2: #Rule 2, the letters are in the same row
            cipher_text += matrix[row1][(col1+inc)%5] + matrix[row2][(col2+inc)%5]
        elif col1==col2:# Rule 3, the letters are in the same column
            cipher_text += matrix[(row1+inc)%5][col1] + matrix[(row2+inc)%5][col2]
        else: #Rule 4, the letters are in a different row and column
            cipher_text += matrix[row1][col2] + matrix[row2][col1]
    
    return cipher_text

def displayOperation():
    print("\nPlease choose Operation :")
    print("1 to Encrypt")
    print("2 to Decrypt")
    print("3 to Enter a new Key")
    print("4 to Exit")


if __name__=='__main__':
    # a sample of encryption and decryption
    
    # Keep application running until user exit
    flag = True
    while flag:

        # Get user key
        userKey = input("Please enter your key > ")

        print("\nPlayfair application will use following key 5x5 matrix\n")
        print(np.array(create_matrix(userKey)))
        
        repeatOperationFlag = True
        while repeatOperationFlag:
            try:
                displayOperation()
                userOperation = int(input("> "))
        
                # Encrypt Operation
                if(userOperation == 1):
                    plainInput = input("Enter plain input > ")
                    encryptedOutput = playfair(userKey, plainInput) 
                    print("Cipher Output : ",encryptedOutput)

                # Decrypt operation
                elif (userOperation == 2):
                    cipherInput = input("Enter cipher input > ")
                    decryptedOutput = playfair(userKey, cipherInput, False) 
                    print("Plaintext output : ",decryptedOutput)
                
                # Enter new key operation
                elif (userOperation == 3):
                    repeatOperationFlag = False

                # Exit operation
                elif (userOperation == 4):
                    exit()

                else:
                    print("Invalid option selected")

            except ValueError:
                print("Invalid Input, Integer expected")

