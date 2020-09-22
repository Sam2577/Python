from random import randint

def get_user_choice() -> int:
    CR = '\n'
    message = "enter your choice 1-10{}"
    user_choice = int(input(message.format(CR)))
    while user_choice not in set(range(1,11)):
        print("OUTSIDE OF THE RANGE OF ONE TO TEN")
        user_choice = int(input(message.format(CR)))
    return user_choice

def play(user_choice=None, hidden_number=None):
    if not hidden_number:
        hidden_number = randint(1,10)
    if user_choice == hidden_number:
        print("YOU WIN")
        return
    user_choice = get_user_choice()
    if user_choice != hidden_number:
        print('higher' if user_choice < hidden_number else 'lower')
    #recursive call and passing state instead of mutating global variables
    play(user_choice, hidden_number)
        
play()
