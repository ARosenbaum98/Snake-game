import random as r
import os
from subprocess import call 
import time
from threading import Thread


class uni:
  SNAKE = "🔴"
  HEAD = "🟣"
  GRID = "⬜"
  FOOD = "🟡"

class direction:
  dir_list = ["w","a","s","d"]
  UP = "w"
  DOWN = "s"
  LEFT = "a"
  RIGHT = "d"

class GameSpace:
  def __init__(self, size):
    self.size = size
    self.game_over = False

    self.init_board()
    self.init_snake()
    self.place_food()

    self.direction = direction.DOWN

    self.print_board()

  def init_board(self):
    i = 0
    grid = []
    while(i<self.size):
      row = []
      j = 0
      while(j<self.size):
        row.append(uni.GRID)
        j+=1
      grid.append(row)
      i+=1
    self.board = grid

  def init_snake(self):
    x = r.randrange(0, self.size-1)
    y = r.randrange(2, self.size-1)

    self.snake_len = 3

    self.snake = [[x,y],[x,y-1],[x,y-2]]
    self.update_snake_on_board()

  def update(self):
    if self.direction == direction.UP:
      self.move_snake(0,-1)
    elif self.direction == direction.DOWN:
      self.move_snake(0,1)
    elif self.direction == direction.LEFT:
      self.move_snake(-1,0)
    elif self.direction == direction.RIGHT:
      self.move_snake(1,0)
    else:
      print("ERROR")

    self.print_board()

  def move_snake(self, x, y):
    
    i = self.snake_len-1

   #clear the last space the snake was at on the board 
    self.append_board(self.snake[i][0],self.snake[i][1],uni.GRID)

    while(i>0): 
      # Update x
      self.snake[i][0] = self.snake[i-1][0]
      # Update y
      self.snake[i][1] = self.snake[i-1][1]
      i=i-1
    
    
    #Move snake head after rest of body
    old_x = self.snake[0][0]
    old_y = self.snake[0][1]
    self.snake[0] = [old_x + x, old_y + y]

    
    self.check_snake_collision()
    self.check_wall_collision()
    self.check_food_collision()

    if(not self.game_over):
       self.update_snake_on_board()

  def check_snake_collision(self):
    head = self.snake[0]
    i=1
    while i<self.snake_len:
      if self.snake[i][0] == head[0] and self.snake[i][1] == head[1]:
        self.end_game()
      i+=1

  def check_wall_collision(self):
    x = self.snake[0][0]
    y = self.snake[0][1]
    if x<0 or x>=self.size or y<0 or y>=self.size:
      self.end_game()

  def print_board(self):
    call('clear' if os.name =='posix' else 'cls')
    i = 0
    while(i<self.size):
      string = ""
      j = 0
      while(j<self.size):
        string += self.board[i][j]+" "
        j+=1
      print(string)
      i+=1

  def take_input(self,inpt):
    if inpt in direction.dir_list and not inpt == self.direction:
      self.direction = inpt

  def place_food(self):

    #Initialize food at snake head
    x = self.snake[0][0]
    y = self.snake[0][1]

    while(self.coord_in_snake(x,y)): 
      x = r.randrange(0,self.size-1)
      y = r.randrange(0,self.size-1)
  
    self.food = [x,y]
    self.append_board(x,y,uni.FOOD)

  def check_food_collision(self):
    for coord in self.snake:
      x = coord[0]
      y = coord[1]

      if (self.food[0] == x and self.food[1] == y):
        self.place_food()

        #append snake tail
        local_direction = self.get_local_tail_direction()

        tail = self.snake[self.snake_len-1]
        if(local_direction == direction.DOWN):
          self.append_tail(tail[0],tail[1]-1)
        if(local_direction == direction.UP):
          self.append_tail(tail[0],tail[1]+1)
        if(local_direction == direction.LEFT):
          self.append_tail(tail[0]+1,tail[1])
        if(local_direction == direction.RIGHT):
          self.append_tail(tail[0]-1,tail[1])
          
  def append_tail(self, x, y):
    self.snake.append([x,y])
    self.snake_len+=1

  def get_local_tail_direction(self):
    tail = self.snake[self.snake_len-1]
    body = self.snake[self.snake_len-2]

    #Moving vertically
    if tail[0] == body[0]:
      if tail[1]>body[1]:
        return direction.UP
      if tail[1]<body[1]:
        return direction.DOWN

    #Moving Horrizontal
    if tail[1] == body[1]:
      if tail[0]>body[0]:
        return direction.LEFT
      if tail[0]<body[0]:
        return direction.RIGHT

  def update_snake_on_board(self):
    for coord in self.snake:
      x = coord[0]
      y = coord[1]
      if(self.coord_in_range(x,y)):
        self.append_board(x,y,uni.SNAKE)
    self.append_board(self.snake[0][0], self.snake[0][1], uni.HEAD)

  def append_board(self, x, y, char):
    self.board[y][x] = char

  def coord_in_snake(self,x,y):
    for part in self.snake:
      if part[0] == x and part[1] == y:
        return True
    return False

  def coord_in_range(self,x,y):
    return x>=0 and x < self.size and y>=0 and y < self.size

  def end_game(self):
    self.game_over = True



gs = GameSpace(20)
print()

while(not gs.game_over):
  print("Use the a, w, s, d keys to move the snake")
  print("Press enter to advance the keyframe")
  gs.take_input(input())
  gs.update()
