import tkinter as tk
from collections import deque
import random  # <-- لإضافة العشوائية

class MazeSolverGUI:
    def __init__(self, root):
        self.root = root
        root.title("Maze Solver")

        # إعداد الاعمدة و الصفوف لبداية للمتاهة
        self.rows = 6
        self.cols = 8
        self.cell_size = 60

        self.start = (0, 0)
        self.end = (self.rows - 1, self.cols - 1)

        width = self.cols * self.cell_size
        height = self.rows * self.cell_size
        root.config(background='black')
        self.canvas = tk.Canvas(root, width=width, height=height, bg='black')
        self.canvas.pack(pady=20)

        # ازرار التحكم
        tk.Button(root, text="Solve Maze", command=self.solve_and_display, cursor='heart', width='30').pack(pady=5)
        tk.Button(root, text="Generate Random Maze", command=self.generate_random_maze, cursor='heart', width='30').pack(pady=5)

        self.result_label = tk.Label(root, text="Click ", font=('Arial', 12))
        self.result_label.pack()

        # توليد المتاهة في البداية
        self.generate_random_maze()

    def generate_random_maze(self):
        # توليد متاهة عشوائية
        self.maze = [
            [0 if random.random() > 0.3 else 1 for _ in range(self.cols)]
            for _ in range(self.rows)
        ]
        self.maze[self.start[0]][self.start[0]] = 0
        self.maze[self.end[0]][self.end[1]] = 0
        self.result_label.config(text="maze generated")
        self.draw_maze()

    def draw_maze(self):

        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                if (i, j) == self.start:
                    color = 'green'
                elif (i, j) == self.end:
                    color = 'red'
                elif self.maze[i][j] == 1:
                    color = 'black'
                else:
                    color = 'white'

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='blue')
                self.canvas.create_text(x1 + self.cell_size//2, y1 + self.cell_size//2, text=f"{i},{j}")

    def draw_path(self, path):
        for index, (i, j) in enumerate(path):
            if (i, j) == self.start or (i, j) == self.end:
                continue
            x1 = j * self.cell_size
            y1 = i * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size

            green = int(200 * (1 - index / len(path)))
            blue = int(200 * (index / len(path)))
            color = f'#{green:02x}{150:01x}{blue:02x}'

            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')
            self.canvas.create_text(x1 + self.cell_size//2, y1 + self.cell_size//2, text=f"{i},{j}")

        self.draw_start_end()

    def draw_start_end(self):
        for point, color in [(self.start, 'green'), (self.end, 'red')]:
            i, j = point
            x1 = j * self.cell_size
            y1 = i * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size

            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='yellow')
            self.canvas.create_text(x1 + self.cell_size//2, y1 + self.cell_size//2, text=f"{i},{j}")

    def bfs(self):
        rows, cols = len(self.maze), len(self.maze[0])
        visited= set()
        queue = deque([(self.start, [])])

        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == self.end:
                return path + [(x, y)]

            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    if self.maze[nx][ny] == 0 and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append(((nx, ny), path + [(x, y)]))
        return None

    def solve_and_display(self):
        path = self.bfs()
        if path:
            self.result_label.config(text="Path found!", fg='green')
            self.draw_maze()
            self.draw_path(path)
        else:
            self.result_label.config(text="No path exists.", fg='red')



if __name__ == "__main__":
    root = tk.Tk()
    app = MazeSolverGUI(root)
    root.mainloop() #ده امر تشغيل البرنامج