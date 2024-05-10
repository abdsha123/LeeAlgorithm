import tkinter as tk
from collections import deque

class Maze:
    def __init__(self, master, rows, cols, size):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.size = size
        self.matrix = [[0 for _ in range(cols)] for _ in range(rows)]
        self.start = None
        self.end = None
        self.draw_grid()
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<Button-3>", self.on_erase)
        self.canvas.bind("<B3-Motion>", self.on_erase_drag)
        self.canvas.bind("<Button-2>", self.on_clear)
        self.canvas.bind("<Button-4>", self.on_zoom_in)
        self.canvas.bind("<Button-5>", self.on_zoom_out)
        self.canvas.pack()
        self.zoom = 1
        
    def draw_grid(self):
        self.canvas = tk.Canvas(self.master, width=self.cols*self.size, height=self.rows*self.size, bg="white")
        for i in range(self.cols):
            self.canvas.create_line(i*self.size, 0, i*self.size, self.rows*self.size)
        for j in range(self.rows):
            self.canvas.create_line(0, j*self.size, self.cols*self.size, j*self.size)
            
    def on_click(self, event):
        col = event.x // self.size
        row = event.y // self.size
        if self.matrix[row][col] == 0:
            if self.start is None:
                self.start = (row, col)
                self.canvas.create_rectangle(col*self.size+1, row*self.size+1, (col+1)*self.size-1, (row+1)*self.size-1, fill="green")
            elif self.end is None:
                self.end = (row, col)
                self.canvas.create_rectangle(col*self.size+1, row*self.size+1, (col+1)*self.size-1, (row+1)*self.size-1, fill="red")
            else:
                self.matrix[row][col] = 1
                self.canvas.create_rectangle(col*self.size+1, row*self.size+1, (col+1)*self.size-1, (row+1)*self.size-1, fill="black")
                
    def on_drag(self, event):
        col = event.x // self.size
        row = event.y // self.size
        if self.matrix[row][col] == 0:
            self.matrix[row][col] = 1
            self.canvas.create_rectangle(col*self.size+1, row*self.size+1, (col+1)*self.size-1, (row+1)*self.size-1, fill="black")
            
    def on_erase(self, event):
        col = event.x // self.size
        row = event.y // self.size
        if self.start == (row, col):
            self.start = None
        elif self.end == (row, col):
            self.end = None
        elif self.matrix[row][col] == 1:
            self.matrix[row][col] = 0
            self.canvas.create_rectangle(col*self.size+1, row*self.size+1, (col+1)*self.size-1, (row+1)*self.size-1, fill="white")
            
    def on_erase_drag(self, event):
        col = event.x // self.size
        row = event.y // self.size
        if self.matrix[row][col] == 1:
            self.matrix[row][col] = 0
            self.canvas.create_rectangle(col*self.size+1, row*self.size+1, (col+1)*self.size-1, (row+1)*self.size-1, fill="white")
            
    def on_clear(self, event):
        self.canvas.delete("all")
        self.start = None
        self.end = None
        self.matrix = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.draw_grid()
        
    def on_zoom_in(self, event):
        if self.zoom < 3:
            self.zoom += 1
            self.size *= 2
            self.canvas.config(width=self.cols*self.size, height=self.rows*self.size)
            self.canvas.scale(tk.ALL, 0, 0, 2, 2)
            
    def on_zoom_out(self, event):
        if self.zoom > 1:
            self.zoom -= 1
            self.size //= 2
            self.canvas.config(width=self.cols*self.size, height=self.rows*self.size)
            self.canvas.scale(tk.ALL, 0, 0, 0.5, 0.5)
            
    def lee_algorithm(self):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        visited = set()
        parent = {}
        queue = deque([(self.start, 0)])
        visited.add(self.start)

        while queue:
            curr_pos, curr_dist = queue.popleft()
            if curr_pos == self.end:
                return curr_dist, parent
            for direction in directions:
                new_pos = (curr_pos[0] + direction[0], curr_pos[1] + direction[1])
                if new_pos[0] < 0 or new_pos[0] >= self.rows or new_pos[1] < 0 or new_pos[1] >= self.cols or new_pos in visited or self.matrix[new_pos[0]][new_pos[1]] == 1:
                    continue
                visited.add(new_pos)
                parent[new_pos] = curr_pos
                queue.append((new_pos, curr_dist + 1))
        return -1, None
        
    def solve(self):
        if self.start is None or self.end is None:
            return
        distance, parent = self.lee_algorithm()
        if distance != -1:
            self.canvas.create_text((self.end[1]+0.5)*self.size, (self.end[0]+0.5)*self.size, text=str(distance), fill="blue")
            curr_pos = self.end
            while curr_pos != self.start:
                prev_pos = parent[curr_pos]
                self.canvas.create_line((curr_pos[1]+0.5)*self.size, (curr_pos[0]+0.5)*self.size, (prev_pos[1]+0.5)*self.size, (prev_pos[0]+0.5)*self.size, fill="blue", width=2)
                curr_pos = prev_pos
            
def main():
    root = tk.Tk()
    root.title("Lee Algorithm with GUI")
    maze = Maze(root, 20, 20, 20)
    button = tk.Button(root, text="Solve", command=maze.solve)
    button.pack()
    root.mainloop()

if __name__ == '__main__':
    main()
