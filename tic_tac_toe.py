from os import system
from tabulate import tabulate
import random

# global variables
table = [
        ["[1]","[2]","[3]"],
        ["[4]","[5]","[6]"],
        ["[7]","[8]","[9]"],
    ]
position = {
            "1":"00",
            "2":"01",
            "3":"02",
            "4":"10",
            "5":"11",
            "6":"12",
            "7":"20",
            "8":"21",
            "9":"22",
        }
name_dic = {}
logged_in = ''

# account handling
class account():
    def __init__(self,name):
        '''
        initiate account object with given name and append that name - object pair in name_dic
        '''
        global name_dic
        self.name = name
        name_dic[name] = self
        self.wins = 0
        self.loses = 0
        self.draws = 0

    # functions of winning, losing and drawing
    def win(self):
        self.wins += 1

    def lose(self):
        self.loses += 1

    def draw(self):
        self.draws += 1

# main body
def main():
    global table
    global position
    global logged_in

    # sign up and login menu. will repeat if user enter 1(go back)
    while True:
        if (logged_in := sign_log()) != 'go back':
            break
    # main menu loop
    while True:
        clear_screen()
        main_value = main_menu()
        # profile menu
        if main_value == '2':
            profile()
            continue
        # score board
        if main_value == '3':
            score_board()
            continue
        # log out(recursively call main)
        if main_value == '4':
            main()

        # ask user whose turn will be first
        turn_value = turn_menu()
        # game and play again code
        while True:
            # re assigned table and position to reset its values after a game
            table = [
                    ["[1]","[2]","[3]"],
                    ["[4]","[5]","[6]"],
                    ["[7]","[8]","[9]"]
                    ]
            position = {
                        "1":"00",
                        "2":"01",
                        "3":"02",
                        "4":"10",
                        "5":"11",
                        "6":"12",
                        "7":"20",
                        "8":"21",
                        "9":"22"
                        }
            # game code
            game_loop(turn_value)
            # endgame msg(play again or return to main menu)
            if endgame_msg() == "1":
                continue
            else:
                break

def clear_screen():
    '''
    clear the terminal screen by typing "clear" in terminal
    '''
    system("clear")

def sign_log():
    global name_dic
    # sign_log menu
    sign_log_menu = [
                    ['1','Sign Up'],
                    ['2','Log In'],
                    ]
    sign_log_value = '0'
    while sign_log_value not in "12":
        clear_screen()
        print(tabulate(sign_log_menu, tablefmt="simple_grid"))
        sign_log_value = input()
    # name entering
    clear_screen()
    # sign in(create an account of unique name and return account object)
    if sign_log_value == '1':
        name = input('Enter Name To Sign Up \n Or Enter 1 to Go Back >').lower()
        if name == '1':
            return 'go back'
        while name in name_dic or name == '':
            clear_screen()
            name = input('Name Already Exist Pick A New One \n OR Enter 1 to Go Back >').lower()
            if name == '1':
                return 'go back'
        name = account(name)
        return name
    # login(return account object which was signed in before)
    else:
        name = input('Enter Name To Login In \n OR Enter 1 to Go Back >').lower()
        if name == '1':
            return 'go back'
        while name not in name_dic:
            clear_screen()
            name = input('Enter Correct Name \n OR Enter 1 to Go Back >').lower()
            if name == '1':
                return 'go back'
        return name_dic[name]

def main_menu():
    main_menu = [
        ['1','New Game'],
        ['2','Profile'],
        ['3','Score Board'],
        ['4','Log Out'],
    ]
    # defining main_menu_value so that it can be used in while loop condition
    main_menu_value = '0'
    # returning 1, 2, 3 or, 4
    while main_menu_value not in '1234':
        print(tabulate(main_menu, tablefmt="simple_grid"))
        main_menu_value = input()
    return main_menu_value

def profile():
    '''
    display account info of currently logged in account
    '''
    global logged_in
    clear_screen()
    profile_menu = [
        ['Name',logged_in.name],
        ['Wins',logged_in.wins],
        ['Loses',logged_in.loses],
        ['Draws',logged_in.draws],
    ]
    print(tabulate(profile_menu, tablefmt="simple_grid"))
    input('Press Enter to return to Main Menu')

def score_board():
    '''
    make a sorted by wins 2D list for the table
    '''
    board = [
        ['Rank','Names','Wins'],
    ]
    # sorting
    rank = 1
    for k_v_pair in sorted(name_dic.items(), key = lambda x : x[1].wins , reverse = True):
        board.append([rank , k_v_pair[0] , k_v_pair[1].wins])
        rank += 1
    # printing
    clear_screen()
    print(tabulate(board, tablefmt="simple_grid"))
    input('Press Enter to return to Main Menu')

def turn_menu():
    '''
    return 1(user 1st turn) or 2(computer first turn)
    '''
    turn_menu = [
                ["1","User Turn"],
                ["2","Computer Turn"],
                ["3","Random"],
    ]
    # defining turn_value so that it can be used in while loop condition
    turn_value = '0'
    while turn_value not in "123":
        clear_screen()
        print('Whose Turn Should Be First')
        print(tabulate(turn_menu, tablefmt="simple_grid"))
        turn_value = input()
    # handling random option
    if turn_value == "3":
        turn_value = random.choice(["1","2"])
    return turn_value

def game_loop(turn_value):
    '''
    do first turn
    loop through each cycle of user and computer turn and checking if someone has won or is it a draw
    '''
    global table
    global position
    # first turn of computer(optional)
    if turn_value == "2":
        clear_screen()
        marking(random.choice(list(position.keys()))," O ")
    # loop
    while True:
        clear_screen()
        #input for user turn
        posi = '0'
        while posi not in position:
            print(tabulate(table, tablefmt="simple_grid"))
            posi = input("Enter Postion >")
            clear_screen()
        #marking user turn
        marking(posi," X ")
        if who_won() == " X " or len(position) == 0:
            break

        #opponent turn
        marking(random.choice(list(position.keys()))," O ")
        if who_won() == " O " or len(position) == 0:
            break

def marking(cor,turn):
        '''
        make markings in the table
        take numeric digit and turn(X or O) as input
        mark the respective position with X or O
        '''
        global table
        global position
        first_cor , sec_cor = position[cor]
        position.pop(cor)
        table[int(first_cor)][int(sec_cor)] = turn

def who_won():
    '''
    return X(user has won) or O(user has lost)
    '''
    global table
    # main diagonal check
    if table[0][0] == table[1][1] == table[2][2]:
        return table[1][1]
    # secondary diagonal check
    if table[0][2] == table[1][1] == table[2][0]:
        return table[1][1]
    for i in range(3):
        #horizontal check
        if table[i][0] == table[i][1]  == table[i][2]:
            return table[i][0]
        #vertical check
        if table[0][i] == table[1][i] == table[2][i]:
            return table[0][i]

def endgame_msg():
    '''
    increment win, lose, or draw of logged in account object
    display endgame msg and ask if play again or return to main menu
    return 1(play again) or 2(return to main menu)
    '''
    global table
    global position
    global logged_in
    if who_won() == " X ":
        logged_in.win()
        end_msg = 'You Won'
    elif who_won() == " O ":
        logged_in.lose()
        end_msg = "You Lose"
    else:
        logged_in.draw()
        end_msg = "Draw"
        
    play_again_menu =[
                    ["1","Play Again"],
                    ['2','Main Menu'],
                    ]
    # defining play_again_value so that it can be used in while loop condition
    play_again_value = '0'
    while play_again_value not in "12":
        clear_screen()
        print(end_msg)
        print(tabulate(play_again_menu, tablefmt="simple_grid"))
        play_again_value = input()
    return play_again_value

if __name__ == "__main__":
    main()