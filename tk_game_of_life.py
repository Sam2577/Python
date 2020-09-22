import tkinter

block_size = 15
canvas_width = 800
canvas_height = 500
grid_width = int(canvas_width/block_size)
grid_height = int(canvas_height/block_size)

dirs = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]

## gosper glider gun
board_set = set(((3, 8),(3, 9),(4, 8),(4, 9),(13, 8),(13, 9),(13, 10),(14, 7),
(14, 11),(15, 6),(16, 6),(15, 12),(16, 12),(18, 7),(18, 11),
(19, 8),(19, 9),(19, 10),(17, 9),(20, 9),(23, 8),(23, 7),
(23, 6),(24, 8),(24, 8),(24, 7),(24, 6),(25, 5),(25, 9),
(27, 5),(27, 4),(27, 9),(27, 10),(37, 6),(37, 6),(37, 7),
(38, 6),(38, 7)))

##board_set = set()

def checkered():
    for x in range(0,canvas_width,block_size):
        canvas.create_line(x, 0, x, canvas_height)
    for y in range(0,canvas_height,block_size):
        canvas.create_line(0, y, canvas_width, y)

def add_block(event):
    global canvas, board_set
    x = event.x - (event.x % block_size)
    y = event.y - (event.y % block_size)
    location = (int(x / block_size),int(y / block_size))
    if location not in board_set:
        board_set.add(location)
        canvas.create_rectangle(x,y, x + block_size, y + block_size, fill="black")
        canvas.create_rectangle(x + 1, y + 1, x + (block_size -1), y + (block_size -1), fill="green")

def get_neighbors(coord, board_set_copy, all_possible_neighbors):
    result = []
    for d in dirs:
        n_cell = (coord[0] + d[0], coord[1] + d[1])
        if n_cell in all_cells and n_cell not in result:
            result.append(n_cell)
            if n_cell not in all_possible_neighbors:
                all_possible_neighbors.add(n_cell)
    return get_num_neighbors(result, board_set_copy)

def get_all_cells():
    return [(x, y) for y in range(grid_height) for x in range(grid_width)]

def get_num_neighbors(nbs, board_set_copy):
    num = 0
    for n in nbs:
        if n in board_set_copy: num += 1
    return num

def go(event):
    global board_set, canvas
    canvas.delete("all")
    checkered()
    board_set_copy = board_set.copy()

    for item in board_set_copy:
        x = item[0] * block_size
        y = item[1] * block_size
        canvas.create_rectangle(x,y, x + block_size, y + block_size, fill="black")
        canvas.create_rectangle(x + 1, y + 1, x + (block_size -2), y + (block_size -2), fill="green")
        
        all_possible_neighbors = set()
        num_neighbors = get_neighbors(item, board_set_copy, all_possible_neighbors)

        if num_neighbors < 2 or num_neighbors > 3:
            board_set.remove(item)
            
        apn = all_possible_neighbors.copy()
        for n in apn:
            apn_copy = all_possible_neighbors.copy()
            num_nbs = get_neighbors(n, board_set_copy, apn_copy)
            if num_nbs == 3:
                if n not in board_set:
                    board_set.add(n)                 
    root.after(250, go, event)
   
                     
root = tkinter.Tk()
canvas = tkinter.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()
button1 = tkinter.Button(root, text='step')
button1.pack()
checkered()
all_cells = get_all_cells()
button1.bind('<Button-1>', go)
canvas.bind('<Button-1>', add_block)
for item in board_set:
    x = item[0] * block_size
    y = item[1] * block_size
    canvas.create_rectangle(x,y, x + block_size, y + block_size, fill="black")
    canvas.create_rectangle(x + 1, y + 1, x + (block_size -2), y + (block_size -2), fill="green")
tkinter.mainloop()
