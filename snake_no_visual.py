import random
import numpy as np
import pickle

# a copy of visualsnake.py but without the PyGame

class LearnSnake:
    def __init__(self):         
        self.screen_width = 600
        self.screen_height = 400
         
        self.snake_size = 10
        self.snake_speed = 15
                 
        self.snake_coords = []
        self.snake_length = 1
        self.dir = "right"
        self.board = np.zeros((self.screen_height // self.snake_size, self.screen_width // self.snake_size))
        
        self.game_close = False
     
        self.x1 = self.screen_width / 2
        self.y1 = self.screen_height / 2
        
        self.r1, self.c1 = self.coords_to_index(self.x1, self.y1)
        self.board[self.r1][self.c1] = 1
             
        self.c_change = 1
        self.r_change = 0
        
        self.door1_r, self.door1_c = 2, 2  # Tọa độ cửa sổ 1
        self.door2_r, self.door2_c = 35, 35  # Tọa độ cửa sổ 2

        self.food_r, self.food_c = self.generate_food()
        self.board[self.food_r][self.food_c] = 2

        self.bomb_r, self.bomb_c = self.generate_bomb()
        self.board[self.bomb_r][self.bomb_c] = 3

        self.board[self.door1_r][self.door1_c] = 4  # Mã cho cửa sổ 1
        self.board[self.door2_r][self.door2_c] = 4

        self.survived = 0

        self.step()
    
    def get_state(self):
        head_r, head_c = self.snake_coords[-1]
        state = []
        state.append(int(self.dir == "left"))
        state.append(int(self.dir == "right"))
        state.append(int(self.dir == "up"))
        state.append(int(self.dir == "down"))
        state.append(int(self.food_r < head_r))
        state.append(int(self.food_r > head_r))
        state.append(int(self.food_c < head_c))
        state.append(int(self.food_c > head_c))
        state.append(self.is_unsafe(head_r + 1, head_c))
        state.append(self.is_unsafe(head_r - 1, head_c))
        state.append(self.is_unsafe(head_r, head_c + 1))
        state.append(self.is_unsafe(head_r, head_c - 1))
        return tuple(state)
    
    def is_unsafe(self, r, c):
        if self.valid_index(r, c):
          if self.board[r][c] == 1:
              return 1
          return 0
        else:
          return 1
        
    
    def get_dist(self, r1, c1, r2, c2):
        return ((r2 - r1) ** 2 + (c2 - c1) ** 2) ** 0.5
        
                
    def valid_index(self, r, c):
        return 0 <= r < len(self.board) and 0 <= c < len(self.board[0])
        
    def coords_to_index(self, x, y):
        r = int(y // 10)
        c = int(x // 10)
        return (r, c)
    
    def check_door(self, r, c):
        if (r == self.door1_r and c == self.door1_c):
            return self.door2_r, self.door2_c  # Di chuyển đến cửa số 1
        elif (r == self.door2_r and c == self.door2_c):
            return self.door1_r, self.door1_c  # Di chuyển đến cửa số 2
        return None
    
    def is_near_door(self, r, c):
    # Kiểm tra xem (r, c) có nằm trong khoảng gần cổng không (1 ô xung quanh)
        return (abs(r - self.door1_r) <= 1 and abs(c - self.door1_c) <= 1) or \
            (abs(r - self.door2_r) <= 1 and abs(c - self.door2_c) <= 1)


    def generate_food(self):
        while True:
            food_c = random.randint(0, self.board.shape[1] - 1)  # Giới hạn cột
            food_r = random.randint(0, self.board.shape[0] - 1)  # Giới hạn hàng
            
            # Kiểm tra xem có bị trùng với rắn, cửa hay gần cửa không
            if self.board[food_r][food_c] == 0 and not self.is_near_door(food_r, food_c):
                return food_r, food_c  # Trả về tọa độ hợp lệ
    
    def generate_bomb(self):
        bomb_c = random.randint(0, self.board.shape[1] - 1)  # Giới hạn cột
        bomb_r = random.randint(0, self.board.shape[0] - 1)  # Giới hạn hàng
        if self.board[bomb_r][bomb_c] != 0:  # Đảm bảo không trùng với rắn hoặc thức ăn
            return self.generate_bomb()  # Tạo lại nếu trùng
        return bomb_r, bomb_c

    def is_in_bomb_range(self, r, c):
        return (self.bomb_r == r and self.bomb_c == c)

    def game_over(self):
        return self.game_close
        
        
        
    def step(self, action="None"):
        if action == "None":
            action = random.choice(["left", "right", "up", "down"])
        else:
            action = ["left", "right", "up", "down"][action]
        
        reward = 0
 
        if action == "left" and (self.dir != "right" or self.snake_length == 1):
            self.c_change = -1
            self.r_change = 0
            self.dir = "left"
        elif action == "right" and (self.dir != "left" or self.snake_length == 1):
            self.c_change = 1
            self.r_change = 0
            self.dir = "right"
        elif action == "up" and (self.dir != "down" or self.snake_length == 1):
            self.r_change = -1
            self.c_change = 0
            self.dir = "up"
        elif action == "down" and (self.dir != "up" or self.snake_length == 1):
            self.r_change = 1
            self.c_change = 0
            self.dir = "down"

 
        if self.c1 >= self.screen_width // self.snake_size or self.c1 < 0 or self.r1 >= self.screen_height // self.snake_size or self.r1 < 0:
            self.game_close = True
        self.c1 += self.c_change
        self.r1 += self.r_change
        
        #Lưu tọa độ con rắn
        self.snake_coords.append((self.r1, self.c1))
        
        if self.valid_index(self.r1, self.c1):
            self.board[self.r1][self.c1] = 1
        
        #Duy trì độ dài con rắn vs update bảng
        if len(self.snake_coords) > self.snake_length:
            rd, cd = self.snake_coords[0]
            del self.snake_coords[0]
            if self.valid_index(rd, cd):
                self.board[rd][cd] = 0
 
        #Ktra rắn có va chạm vs thân k
        for r, c in self.snake_coords[:-1]:
            if r == self.r1 and c == self.c1:
                self.game_close = True
 
        new_pos = self.check_door(self.r1, self.c1)
        if new_pos:
            self.r1, self.c1 = new_pos  # Di chuyển đến cửa còn lại
        if self.c1 == self.food_c and self.r1 == self.food_r:
            self.food_r, self.food_c = self.generate_food()
            self.board[self.food_r][self.food_c] = 2
            self.snake_length += 1
            reward = 1 # food eaten, so +1 reward
        if self.is_in_bomb_range(self.r1, self.c1):
            self.game_close = True
        else:
            rh1, ch1 = self.snake_coords[-1]
            if len(self.snake_coords) == 1:
                rh2, ch2 = rh1, ch1
            else:
                rh2, ch2 = self.snake_coords[-1]
        
        # death = -10 reward
        if self.game_close:
            reward = -10
        self.survived += 1
        
        return self.get_state(), reward, self.game_close
            
        
    # run game using given episode (from saved q tables)
    # no visual - just returns snake length
    def run_game(self, episode):
        filename = f"pickle/{episode}.pickle"
        with open(filename, 'rb') as file:
            table = pickle.load(file)
        current_length = 2
        steps_unchanged = 0
        while not self.game_over():
            state = self.get_state()
            action = np.argmax(table[state])
            if steps_unchanged == 1000:
                break
            self.step(action)
            if self.snake_length != current_length:
                steps_unchanged = 0
                current_length = self.snake_length
            else:
                steps_unchanged += 1
                
        return self.snake_length
            
        