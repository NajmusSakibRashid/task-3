import sys
from prettytable import PrettyTable
import random
import hmac
import hashlib

args = sys.argv[1:]

if len(args) < 3:
    print("Please provide at least 3 commands")
    sys.exit(1)
elif len(args)%2==0:
    print("Please provide an odd number of commands")
    sys.exit(1)
elif len(set(args))!=len(args):
    print("Please provide unique commands")
    sys.exit(1)

class Help:
    def __init__(self,args):
        self.moves=args
        self.table=PrettyTable()
        self.results=[]
        self.table=PrettyTable()
        self.table.field_names=[r'v PC\User >']+self.moves
        results=['Draw']+['Win' for _ in range(len(self.moves)//2)]+['Lose' for _ in range(len(self.moves)//2)]
        for move in self.moves:
            self.table.add_row([move]+results)
            self.results.append(results)
            results=[results[-1]]+results[:-1]
    def print(self):
        print(self.table)
    def getResult(self,computer,user):
        # print(computer,user,self.results)
        return self.results[computer][user]

class ComputerMove:
    def __init__(self,args):
        self.moves=args
        self.move=None
        self.key=None
    def generateKey(self):
        string='ABCDEF0123456789'
        key=''
        for _ in range(64):
            key+=string[random.randint(0,len(string)-1)]
        self.key=key
    def getKey(self):
        return self.key
    def setMove(self):
        self.move=random.randint(0,len(self.moves)-1)
    def getMove(self):
        return self.moves[self.move]
    def generateHMAC(self):
        self.setMove()
        self.generateKey()
        return hmac.new(self.getKey().encode(),self.getMove().encode(),hashlib.sha256).hexdigest().upper()
    
class Game:
    def __init__(self,args):
        self.moves=args
        self.computer=ComputerMove(self.moves)
        self.help=Help(self.moves)
    def run(self):
        print(f'HMAC: {self.computer.generateHMAC()}')
        print('Available moves:')
        for idnex,move in enumerate(self.moves):
            print(f'{idnex+1} - {move}')
        print('0 - exit')
        print('? - help')
        user=input('Enter your move: ')
        try:
            if user=='?':
                self.help.print()
            elif int(user)==0:
                return
            else:
                user=int(user)-1
                if user<0 or user>=len(self.moves):
                    print('Invalid move')
                else:
                    print(f'Your move: {self.moves[user]}')
                    print(f'Computer move: {self.computer.getMove()}')
                    result=self.help.getResult(self.computer.move,user)
                    print(f'Result: {result}')
                    print(f'HMAC Key: {self.computer.getKey()}')
        except:
            print('Invalid move')
        self.run()
        
        
game=Game(args)

game.run()