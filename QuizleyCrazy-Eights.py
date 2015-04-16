import itertools, random

def printRules():
  print("The goal of Quizley is to be the first player\n to get rid of all the cards in your hand.")
  print()
  print("Each turn, the player has the choice of either\n playing one card that matches the number or suit of the top card of\n the discard pile or drawing another card if no action\n can be taken.")
  print("Certain cards also have special effects when played:")
  print("*"*80)
  print("  Playing a King makes the next player draw 4 cards,")
  print("  Playing a Queen makes the next player draw 2 cards,")
  print("  Playing a Jack makes all other players draw 1 card,")
  print("  Playing a 10 skips the next person’s turn,")
  print("  Playing a 9 reverses the player order.")
  print("In order to use these cards, the player must answer\n a trivia question correctly about the Python programming language.")
  print("If answered incorrectly, the effect of the card is\n turned on the player, e.g. now the player has to draw 4 cards.")
  print("Good luck and have fun!")
  print("*"*80)
  userInput =""
  while(userInput!="Y"):
    userInput = input("Enter \'Y\' when ready to play the game: ")
    if (userInput == "Y"):
      break

def createDeck():

  deck = list(itertools.product(range(2,11),['\u2660','\u2764','\u2666','\u2663'])) * 2  #create two decks of 4 suit numerical cards
  deck += list(itertools.product(['King', 'Jack', 'Queen', 'A'],['\u2660','\u2764','\u2666','\u2663']))*2   #create two decks of royals and Aces

  random.shuffle(deck)      #shuffle the deck
  return deck

def drawCard(game):
  game["temp"] = tuple(game["cardDeck"][0])     #set the temp holding variable to the card at the top of the deck
  del game["cardDeck"][0]         #remove card from the top of the deck
  return game

def drawHands(game):
  for i in range(3):         #Draw 7 cards for the 3 different players
    game = drawCard(game)     
    temp = tuple(game["temp"])
    if i%3 == 0:        #For player 1
      game["p1hand"].append(temp) #add the most recently drawn card to player 1's hand
    if i%3 == 1:        #And so on for every other player
      game["p2hand"].append(temp)
    if i%3 == 2:
      game["p3hand"].append(temp)
  return game
#End drawHands

def printHand(game):
  i=1
  print("*" * 20)
  print("Player %d's hand" % game["currentPlayer"])
  print("*" * 20)
  if (game["currentPlayer"]==1):
    for card in range(0,len(game["p1hand"])):   #Print the cards in the hand of player 1
      print("Card", i, " : ", game["p1hand"][i-1][0],game["p1hand"][i-1][1])
      i+=1      #increment the counter to iterate through the list of tuples
  if (game["currentPlayer"]==2):
    for card in game["p2hand"]:
      print("Card", i, " : ", game["p2hand"][i-1][0],game["p2hand"][i-1][1])
      i+=1
  if (game["currentPlayer"]==3):
    for card in game["p3hand"]:
      print("Card", i, " : ", game["p3hand"][i-1][0],game["p3hand"][i-1][1])
      i+=1
  print("*" * 20)
  pass
#End printHand

def playGame(game, quiz): 
  gameOver = False        #Initialize the variables of the game
  previousHand = "p3hand"
  currentHand = "p1hand"
  nextHand = "p2hand"
  while(gameOver==False): #loop until game is over
    printHand(game)       #Print the game
    temp= getPlay(game, game["currentPlayer"], previousHand, currentHand, nextHand,quiz)       #Get the play from current player
    game = temp[0]
    gameOver= temp[1]
    if(gameOver==True):
      break
    temp = getInfo(game["currentPlayer"], previousHand, currentHand, nextHand)   #Changes the players hand order
    previousHand = temp[0]
    currentHand = temp[1]
    nextHand = temp[2]
    for i in range(101):  #Print 100 empty lines so next player can't see the previous players turn
      print()

  print("Thanks for playing! :)")
#End playGame

def getPlay(game, currentPlayer, previousHand, currentHand, nextHand, quiz):
  while(True):  #Infinite loop
    print("last card played was : ", game["lastCardPlayed"][0], game["lastCardPlayed"][1])  #Print the last card played
    userInput=input("Select a play (\'Play\' or \'Draw\'): ").strip(' \t\n\r^?')  #Get stripped user input
    if(userInput == "Play"):  #If user decides to play a card
      while(True):    #infinite loop
        userInput= int(input("Select a card from 1 to %d, or \'0\' to quit: " % len(game[currentHand])).strip(' \t\n\r^?'))   #Get stripped user input on which card to play
        if(userInput==0):   #Zero breaks the loop, returns to the outer loop
              print("Returning to main menu!")
              break
        if(userInput>0 and userInput<= len(game[currentHand])):   #If user input is valid
          if(str(game[currentHand][userInput-1][0])=="King" or str(game[currentHand][userInput-1][0])=="Queen" or str(game[currentHand][userInput-1][0])=="Jack"):  #If the card is a royal
            if(checkValid(game, game["currentPlayer"], userInput)==False):  #Check to see if the card matches suit or rank of last played card
              continue
            if(str(game[currentHand][userInput-1][0]) == "King"):   #If the card is a king
              userAnswer = askQuestion(quiz)    #Ask a trivia question 
              if(userAnswer==True):       #If they got it right, make the next player draw 4 cards
                if (len(game[currentHand])==1):
                  print("Congratulations, you win!")
                  return ((game, True))
                if(game["direction"]=="clockwise"):   #Increment the current player to next or previous player
                  game["currentPlayer"]+=1
                  if (game["currentPlayer"]>3):
                    game["currentPlayer"]=1
                  for i in range(4):
                    game=drawCard(game)
                    game[nextHand].append(game["temp"])
                  return (game, False)
                else:     #If the direction of play is counter clockwise, forces the previous player to draw
                  game["currentPlayer"]-=1
                  if (game["currentPlayer"]<=0):
                    game["currentPlayer"]=3
                  for i in range(4):
                    game=drawCard(game)
                    game[previousHand].append(game["temp"])
                  return (game, False)
              else:   #If the answered the trivia question incorrectly, they keep the king and draw 4 extra cards
                if (game["direction"]=="clockwise"):
                  game["currentPlayer"]+=1
                  if (game["currentPlayer"]>3):
                    game["currentPlayer"]=1
                if (game["direction"] == "counterclockwise"):
                  game["currentPlayer"]-=1
                  if (game["currentPlayer"]<=0):
                    game["currentPlayer"]=3
                game["cardDeck"].append(game[currentHand][userInput-1])
                for i in range(5):
                  game=drawCard(game)
                  game[currentHand].append(game["temp"])
                return (game, False)
            elif(str(game[currentHand][userInput-1][0]) == "Queen"):  #Same as king, except draw two cards
              userAnswer = askQuestion(quiz)
              if(userAnswer==True):
                if (len(game[currentHand])==1):
                  print("Congratulations, you win!")
                  return (game, True)
                if(game["direction"]=="clockwise"):
                  game["currentPlayer"]+=1
                  if (game["currentPlayer"]>3):
                    game["currentPlayer"]=1
                  for i in range(2):
                    game=drawCard(game)
                    game[nextHand].append(game["temp"])
                  return (game, False)
                else:
                  game["currentPlayer"]-=1
                  if (game["currentPlayer"]<=0):
                    game["currentPlayer"]=3
                  for i in range(2):
                    game=drawCard(game)
                    game[previousHand].append(game["temp"])
                  return (game, False)
              else:
                if(game["direction"]=="clockwise"):
                  game["currentPlayer"]+=1
                  if (game["currentPlayer"]>3):
                    game["currentPlayer"]=1
                else:
                  game["currentPlayer"]-=1
                  if (game["currentPlayer"]<=0):
                    game[1]=3
                for i in range(3):
                  game=drawCard(game)
                  game[currentHand].append(game["temp"])
                return (game, False)
            elif(str(game[currentHand][userInput-1][0]) == "Jack"):   #Jack forces both opponents to draw one card each
              userAnswer = askQuestion(quiz)
              if(userAnswer==True):
                if (len(game[currentHand])==1):
                  print("Congratulations, you win!")
                  return (game, True)
                game=drawCard(game)
                game[previousHand].append(game["temp"])
                game=drawCard(game)
                game[nextHand].append(game["temp"])
                if(game["direction"]=="clockwise"):
                  game["currentPlayer"]+=1
                  if (game["currentPlayer"]>3):
                    game["currentPlayer"]=1
                else:
                  game["currentPlayer"]-=1
                  if (game["currentPlayer"]<=0):
                    game["currentPlayer"]=3
                game["cardDeck"].append(game["lastCardPlayed"])
                game["lastCardPlayed"]= game[currentHand][userInput-1]
                del game[currentHand][userInput-1]
                return (game, False)
              else:     #Player draws two cards if they miss the trivia questions
                if (game["direction"]=="clockwise"):
                  game["currentPlayer"]+=1
                  if (game["currentPlayer"]>3):
                    game["currentPlayer"]=1
                if (game["direction"] == "counterclockwise"):
                  game["currentPlayer"]-=1
                  if (game["currentPlayer"]<=0):
                    game["currentPlayer"]=3
                  game["cardDeck"].append(game[currentHand][userInput-1])
                  for i in range(3):
                    game=drawCard(game)
                    game[currentHand].append(game["temp"])
                  return (game, False)
          elif( int(game[currentHand][userInput-1][0]) == 10):  #10 is the skip player card
            if(checkValid(game, currentPlayer, userInput)==False):  #check that the card the user chose is valid first
              continue
            if(len(game[currentHand])==1):    #Last card check
              userAnswer = askQuestion(quiz)
              if(userAnswer==False):
                for i in range(2):
                  game=drawCard(game)
                  game[currentHand].append(game["temp"])
                return (game, False)
              else:
                print("Congratulations, you win!")
                return (game, True)
            game["cardDeck"].append(game["lastCardPlayed"]) #put the last card at the end of the deck
            if(game["direction"] == "clockwise"):
              game["currentPlayer"]-=1  #Skip the next player
              if (game["currentPlayer"]<=0):
                game["currentPlayer"]=3
              game["lastCardPlayed"]= game[currentHand][userInput-1]
              del game[currentHand][userInput-1]
              return (game, False)
            else:
              game["currentPlayer"]+=1  #Skips the next player if the direction of play is counter clockwise
              if (game["currentPlayer"]>3):
                game["currentPlayer"]=1
              game["lastCardPlayed"]= game[currentHand][userInput-1]
              del game[currentHand][userInput-1]
              return (game, False)
          elif( int(game[currentHand][userInput-1][0]) == 9):   #Reverses the direction if a 9 is played
            if(checkValid(game, currentPlayer, userInput)==False):
              continue
            if(len(game[currentHand])==1):
              userAnswer = askQuestion(quiz)
              if(userAnswer==False):
                for i in range(2):
                  game=drawCard(game)
                  game[currentHand].append(game["temp"])
                  return (game, False)
              else:
                print("Congratulations, you win!")
                return (game, True)
            game["cardDeck"].append(game["lastCardPlayed"])
            if(game["direction"] == "clockwise"):
              game["currentPlayer"]-=1
              if (game["currentPlayer"]<=0):
                game["currentPlayer"]=3
              game["direction"]= "counterclockwise"   #Reverse the direction of play
              game["lastCardPlayed"]= game[currentHand][userInput-1]  #Puts the user's card as last card played, then remove that card from the player's hand
              del game[currentHand][userInput-1]
              return (game, False)
            else:
              game["direction"]= "clockwise"
              game["currentPlayer"]+=1
              if (game["currentPlayer"]>3):
                game["currentPlayer"]=1
              game["lastCardPlayed"]= game[currentHand][userInput-1]
              del game[currentHand][userInput-1]
              return (game, False)
          elif(int(game[currentHand][userInput-1][0])<9 and int(game[currentHand][userInput-1][0])>0):  #If the card has no action related to it, run through checks then play the card
            if(checkValid(game, currentPlayer, userInput)==False):
              print("fails validity for 2-")
              continue
            if(len(game[currentHand])==1):
              userAnswer = askQuestion(quiz)
              if(userAnswer==False):
                for i in range(2):
                  game=drawCard(game)
                  game[currentHand].append(game["temp"])
                  return (game, False)
              else:
                print("Congratulations, you win!")
                return (game, True)
            if (game["direction"]=="clockwise"):
              game["currentPlayer"]+=1
              if (game["currentPlayer"]>3):
                game["currentPlayer"]=1
            if (game["direction"] == "counterclockwise"):
              game["currentPlayer"]-=1
              if (game["currentPlayer"]<=0):
                game["currentPlayer"]=3
            game["cardDeck"].append(game["lastCardPlayed"])
            game["lastCardPlayed"]= game[currentHand][userInput-1]
            del game[currentHand][userInput-1]
            return (game, False)
          else:   #If user inputs unrecognized information
            print("Unrecognized command.")
            continue
    elif(userInput == "Draw"):  #If user decides to draw
      if (game["direction"]=="clockwise"):
        game["currentPlayer"]+=1
        if (game["currentPlayer"]>3):
          game["currentPlayer"]=1
      else:
        game["currentPlayer"]-=1
        if (game["currentPlayer"]<=0):
          game["currentPlayer"]=3
      print("You draw another card: "), #draw a card 
      game= drawCard(game)
      print(game["temp"][0],game["temp"][1])
      game[currentHand].append(game["temp"])
      return (game, False)
    else:   #If unrecognized command
      print("Unrecognized command, please enter \'Play\' or \'Draw\'")
      continue


def getInfo(currentPlayer, previousHand, currentHand, nextHand):
  if (currentPlayer==1):  #If current player is 1, sets the previous and next hands 
    currentHand = "p1hand"
    previousHand = "p3hand"
    nextHand = "p2hand"
  if (currentPlayer==2):
    currentHand = "p2hand"
    previousHand = "p1hand"
    nextHand = "p3hand"
  if (currentPlayer==3):
    currentHand = "p3hand"
    previousHand = "p2hand"
    nextHand = "p1hand"
  return (previousHand, currentHand, nextHand)

def checkValid(game, currentPlayer, userInput):   #Checks to see if suits or rank match
  if (game["currentPlayer"]==1):
    if(game["p1hand"][userInput-1][0]== game["lastCardPlayed"][0] or game["p1hand"][userInput-1][1]== game["lastCardPlayed"][1]):
      return True
    else:
      print("Invalid play. Try again.")
      return False
  if (game["currentPlayer"]==2):
    if(game["p2hand"][userInput-1][0]== game["lastCardPlayed"][0] or game["p2hand"][userInput-1][1]== game["lastCardPlayed"][1]):
      return True
    else:
      print("Invalid play. Try again.")
      return False
  else:
    if(game["p3hand"][userInput-1][0]== game["lastCardPlayed"][0] or game["p3hand"][userInput-1][1]== game["lastCardPlayed"][1]):
      return True
    else:
      print("Invalid play. Try again.")
      return False

def askQuestion(quiz):
  questionNum = random.randint(0,30)  #Create random integer so that each test is assigned it's own value
  print("You must answer the question right, or else draw cards.")
  print(quiz[questionNum]["question"])  #Print the random question
  print("A", quiz[questionNum]["A"])
  print("B", quiz[questionNum]["B"])
  print("C", quiz[questionNum]["C"])
  print("D", quiz[questionNum]["D"])
  userInput = input("The correct answer is: ")
  if( userInput == quiz[questionNum]["correctAnswer"]):
    print("Correct!")
    return True
  else:
    print("False! The correct answer is actually %s You draw cards..." % quiz[questionNum]["correctAnswer"] )
    return False
  
def main():
  printRules()
  game = { "cardDeck": [], "p1hand": [], "p2hand": [], "p3hand": [], "direction" : "clockwise", "isGameOver" : False, "quizQuestions" : [], #Define the properties of the game
    "lastCardPlayed" : (1, '\u2660'), "temp" : (), "currentPlayer" : 1
  }
  quiz = [    #Create a list of dictionaries that each contain a multiple choice question
{
"question" : "_____ are instructions that control the computer",
"A": "Software", 
"B": "Hardware", 
"C": "Emails", 
"D": "Speakers", 
"correctAnswer" : "A"
},
{"question":"Python is a(n)",
"A": "Object oriented language", 
"B": "Interpreted language", 
"C": "Translated language", 
"D": "Dynamic language", 
"correctAnswer" : "B"
},
{"question":	"What will be displayed when eval( 8 - 2*3) is entered?",
"A": "3.0", 
"B": "2.0", 
"C": "1.0", 
"D": "0", 
"correctAnswer" : "B"
},
{"question":"Which one of these lists contain a float, an integer, and a string?",
"A": "[3, 5, ‘this’]", 
"B": "[‘game’, ‘is’, ‘hard’]", 
"C": "[3.14,  9898, ‘hello’]", 
"D": "[1.15, 19.48, 9024]", 
"correctAnswer" : "C"
},
{"question": "If your age is 20, what would appear?\n\nif (age % 3 == 0):\n\tprint(True)\nelse:\n\tprint(False)",
"A": "True", 
"B": "False", 
"correctAnswer" : "B"
},
{"question":"Why are for loops important?",
"A": "They print strings of numbers easily", 
"B": "They are used to repeat a code a number of times", 
"C": "They define a function", 
"D": "They are able to store a lot of information", 
"correctAnswer" : "B"
},
{"question":"A function is a piece of reusable code used to perform",
"A": "A single action", 
"B": "Two actions", 
"C": "An infinite number of actions", 
"D": "Nothing", 
"correctAnswer" : "A"
},
{"question":"What is len(\"Discombobulate\")?",
"A": "5", 
"B": "14", 
"C": "disconcerted", 
"D": "15.13", 
"correctAnswer" : "B"
},
{"question" : "How are computer programs and hardware combed for defects?",
"A": "hunting for bugs", 
"B": "fumigation", 
"C": "debugging", 
"D": "pesticide", 
"correctAnswer" : "C"
},
{"question":"What is the right way to concatenate two strings s1 and s2 into string3?",
"A": "s1 + s3 = string3", 
"B": "s1.adds2 = string3", 
"C": "s1._add(s2) = string3", 
"D": "s1._add_(s2) = string3", 
"correctAnswer" : "D"
},
{"question":"What is list(\"apple\")?",
"A": "[\"apple\"]", 
"B": "[\"elppa\"]", 
"C": "[‘a’,’p’,’p’,’l’,’e’]", 
"D": "[a, p, p, l, e]", 
"correctAnswer" : "C"
},
{"question":"What will be displayed by the following?\n\nlist1 = [4,6]\nlist2 = list1\nlist1[1] = 9\nprint(list2)",
"A": "[4,9]", 
"B": "[9,6]", 
"C": "[4,1]", 
"D": "[1,4]", 
"correctAnswer" : "A"
},
{"question":"Given m = [[25,64,36],[26,98,12], what is print(m[0][1])?",
"A": "36", 
"B": "64", 
"C": "98", 
"D": "25", 
"correctAnswer" : "B"
},
{"question":"Suppose t = (1,2,3,4), t[1 : -1]  is",
"A": "(4,3,2,1)", 
"B": "(2,3,4)", 
"C": "(1,2,3)", 
"D": "(2,3)", 
"correctAnswer" : "D"
},
{"question":"Suppose d = {\"john\":40, \"peter\":45}, d[\"john\"] is __________",
"A": "45", 
"B": "40", 
"C": "john", 
"D": "peter", 
"correctAnswer" : "B"
},
{"question":"How is a tuple different from a list or a dictionary?",
"A": "It’s immutable", 
"B": "It’s mutable", 
"C": "Tuples can be dynamically modified", 
"D": "List and dictionaries are statically defined", 
"correctAnswer" : "A"
},
{"question":"What is the brain of the computer?",
"A": "Monitor", 
"B": "Disk", 
"C": "Memory", 
"D": "CPU", 
"correctAnswer" : "D"
},
{"question":"What will happen when you input 123 in the Python shell?",
"A": "An error will occur", 
"B": "It will return 123", 
"C": "It will add 1 + 2 + 3", 
"D": "It will multiply 1 * 2 * 3", 
"correctAnswer" : "B"
},
{"question":"What is round(15.8943)?",
"A": "10", 
"B": "15", 
"C": "16", 
"D": "20", 
"correctAnswer" : "C"
},
{"question":"_____represents an entity in the real world that can be identified",
"A": "An object", 
"B": "A class", 
"C": "A method", 
"D": "A program", 
"correctAnswer" : "A"
},
{"question":"An object is an instance of a _____",
"A": "function", 
"B": "all of the below", 
"C": "method", 
"D": "class", 
"correctAnswer" : "D"
},
{"question":"The less than or equal to operator is",
"A": "<<", 
"B": "<=", 
"C": "=<", 
"D": "!=", 
"correctAnswer" : "B"
},
{"question" : "2**3 evaluates to",
"A": "8", 
"B": "5", 
"C": "6.0", 
"D": "9", 
"correctAnswer" : "D"
},
{"question":"What is max(4,7,8,9,1,2)?",
"A": "4", 
"B": "8", 
"C": "9", 
"D": "7", 
"correctAnswer" : "C"
},
{"question":"Python comments can be denoted using",
"A": "\\", 
"B": "#", 
"C": "&", 
"D": "//", 
"correctAnswer" : "B"
},
{"question":"What would return an error?",
"A": "int(0134)", 
"B": "eval(0.134)", 
"C": "int(\"hello\")", 
"D": "eval(3.429)", 
"correctAnswer" : "C"
},
{"question":"A variable defined outside function is called a",
"A": "a global variable", 
"B": "a local vairable", 
"C": "a function parameter", 
"D": "a global constraint", 
"correctAnswer" : "A"
},
{"question":"What is \"Programming is fun\"[-1]?",
"A": "Pr", 
"B": "un", 
"C": "n", 
"D": "g", 
"correctAnswer" : "C"
},
{"question":"Convert this into binary code: 135",
"A": "10000111", 
"B": "11101111", 
"C": "1010", 
"D": "1111000", 
"correctAnswer" : "A"
},
{"question":"What is the difference between double and float?",
"A": "float is 64 bit, and double is 32 bit", 
"B": "binary floating is not as accurate as double", 
"C": "float is for numbers with few decimal places", 
"D": "double is not as accurate as float", 
"correctAnswer" : "B"
}]

  game["cardDeck"] = createDeck()   #Create the deck
  game = drawHands(game)    #Draw hands for the players


  playGame(game, quiz)  #play the game
  pass

if __name__ == '__main__':
  main()
