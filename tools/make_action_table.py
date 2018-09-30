import csv

def print_array(temp_action):
    temp_action = temp_action[::-1]
    grid = []
    for a in temp_action:
        l = [a.count('0'), a.count('1'), a.count('2'), a.count('3')]
        m = max(l)
        grid.append([i for i, j in enumerate(l) if j == m])


    for n, i in enumerate(grid):
        if len(i) > 1:
            for m, j in enumerate(i):
                if j == 0:
                    grid[n][m] = '↓'
                elif j == 1:
                    grid[n][m] = '←'
                elif j == 2:
                    grid[n][m] = '→'
                elif j == 3:
                    grid[n][m] = 'ｘ'
        else:
            if i == [0]:
                grid[n] = '↓'
            elif i == [1]:
                grid[n] = '←'
            elif i == [2]:
                grid[n] = '→'
            elif i == [3]:
                grid[n] = 'ｘ'

    n = 5
    grid = [grid[i:i+n] for i in range(0, len(grid), n)]
    print('\n'.join(['　　　　'.join([str(cell) for cell in row]) for row in grid]))
    print('　　　　　　　　　　人')



i, j = 0, 0
temp_action = [[0 for x in range(10)] for y in range(20)]
with open('action_remaped.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] in {'0', '1', '2', '3'}:
            for r in row:
                temp_action[i][j] = r
                i += 1
            i = 0
            j += 1

        elif row[0] == '':
            i, j = 0, 0

            print_array(temp_action)
            print(row[0])

        else:
            print(row[0], ':')

print_array(temp_action)
