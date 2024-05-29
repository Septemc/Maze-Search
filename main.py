from tkinter import *
import random
import time
from queue import PriorityQueue

SIZE = 41
dire = ((1, 0), (-1, 0), (0, 1), (0, -1))


def maze_generate(SIZE):
    data = [[0 for i in range(SIZE)] for j in range(SIZE)]
    for i in range(SIZE - 1):
        for j in range(SIZE - 1):
            if i % 2 and j % 2:
                data[i][j] = 1
    p = 0
    s = [[random.randint(0, SIZE // 2), random.randint(0, SIZE // 2)]]
    while p >= 0:
        d = random.randint(0, 3)
        nothave = 1
        for i in range(4):
            if 0 <= s[p][0] + dire[d][0] <= SIZE // 2 and 0 <= s[p][1] + dire[d][1] <= SIZE // 2 and \
                    data[2 * (s[p][0] + dire[d][0]) - 1][2 * (s[p][1] + dire[d][1]) - 1] == 1:
                nothave = 0
                p += 1
                if len(s) == p:
                    s.append([s[p - 1][0] + dire[d][0], s[p - 1][1] + dire[d][1]])
                else:
                    s[p][0] = s[p - 1][0] + dire[d][0]
                    s[p][1] = s[p - 1][1] + dire[d][1]
                data[2 * s[p][0] - 1][2 * s[p][1] - 1] = 2
                data[2 * s[p - 1][0] - 1 + dire[d][0]][2 * s[p - 1][1] - 1 + dire[d][1]] = 2
                break
            if d == 3:
                d = 0
            else:
                d += 1
        if nothave:
            p -= 1
    for i in range(SIZE):
        data[0][i] = 0
        data[i][0] = 0
        data[SIZE - 1][i] = 0
        data[i][SIZE - 1] = 0
    data[0][1] = 2
    data[SIZE - 1][SIZE - 2] = 2
    return data


def dfs(x, y, data, visited, path):
    if x == SIZE - 1 and y == SIZE - 2:
        return True

    for d in dire:
        nx = x + d[0]
        ny = y + d[1]
        if 0 <= nx < SIZE and 0 <= ny < SIZE and data[nx][ny] == 2 and visited[nx][ny] == 0:
            visited[nx][ny] = 1
            path.append([nx, ny])
            t.update()  # 刷新界面
            t.after(5)  # 延迟
            l.place(x=30 * nx + 2, y=30 * ny + 2)
            Label(t, bg="yellow", relief="raised", padx=12, pady=4).place(x=30 * nx, y=30 * ny)
            if dfs(nx, ny, data, visited, path):
                return True
            path.pop()

    return False


def bfs(x, y, data, visited, path):
    queue = [(x, y)]
    while queue:
        x, y = queue.pop(0)
        if x == SIZE - 1 and y == SIZE - 2:
            return True

        for d in dire:
            nx = x + d[0]
            ny = y + d[1]
            if 0 <= nx < SIZE and 0 <= ny < SIZE and data[nx][ny] == 2 and visited[nx][ny] == 0:
                visited[nx][ny] = 1
                path.append([nx, ny])
                t.update()  # 刷新界面
                t.after(5)  # 延迟
                l.place(x=30 * nx + 2, y=30 * ny + 2)
                Label(t, bg="yellow", relief="raised", padx=12, pady=4).place(x=30 * nx, y=30 * ny)
                if bfs(nx, ny, data, visited, path):
                    return True
                path.pop()

    return False


def manhattan_dist(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


def a_star(start, end, data):
    queue = PriorityQueue()
    queue.put((manhattan_dist(start, end), 0, start, []))

    while not queue.empty():
        _, dist, curr, path = queue.get()

        if curr == end:
            return path + [curr]

        for d in dire:
            nx, ny = curr[0] + d[0], curr[1] + d[1]
            if 0 <= nx < SIZE and 0 <= ny < SIZE and data[nx][ny] == 2 and visited[nx][ny] == 0:
                visited[nx][ny] = 1
                t.update()  # 刷新界面
                t.after(5)  # 延迟
                l.place(x=30 * nx + 2, y=30 * ny + 2)
                Label(t, bg="yellow", relief="raised", padx=12, pady=4).place(x=30 * nx, y=30 * ny)
                queue.put((dist + 1 + manhattan_dist((nx, ny), end), dist + 1, (nx, ny), path + [curr]))

    return []


dist = [[SIZE * SIZE for _ in range(SIZE)] for _ in range(SIZE)]  # 存储从起点到每个点的距离


def dijkstra(start, end, data):
    queue = PriorityQueue()
    queue.put((0, start))
    dist[start[0]][start[1]] = 0

    while not queue.empty():
        _, (x, y) = queue.get()

        if (x, y) == end:
            return True, dist[x][y]

        for d in dire:
            nx, ny = x + d[0], y + d[1]
            if 0 <= nx < SIZE and 0 <= ny < SIZE and data[nx][ny] == 2 and not visited[nx][ny]:
                visited[nx][ny] = True
                cost = dist[x][y] + 1  # 假设移动成本为1
                if cost < dist[nx][ny]:
                    dist[nx][ny] = cost
                    t.update()  # 刷新界面
                    t.after(5)  # 延迟
                    l.place(x=30 * nx + 2, y=30 * ny + 2)
                    Label(t, bg="yellow", relief="raised", padx=12, pady=4).place(x=30 * nx, y=30 * ny)
                    queue.put((cost, (nx, ny)))

    return False, dist[end[0]][end[1]]


if __name__ == "__main__":
    SIZE = 41
    data = maze_generate(SIZE)
    for a_idx in range(3, 5):
        t = Tk()
        t.geometry(f"{30 * SIZE}x{30 * SIZE}")
        t.configure(bg="mintcream")

        solve_path = [[0, 1]]
        visited = [[0 for i in range(SIZE)] for j in range(SIZE)]
        visited[0][1] = 1

        l = Label(t, bg="red", relief="sunken", padx=10, pady=2)
        l.place(x=2, y=32)
        start = (0, 1)
        paths = []
        end = (SIZE - 1, SIZE - 2)

        for i in range(SIZE):
            for j in range(SIZE):
                if not data[i][j]:
                    Label(t, bg="black", relief="raised", padx=12, pady=4).place(x=30 * i, y=30 * j)

        if a_idx == 1:
            # 开始时间
            start_time = time.perf_counter()
            dfs(0, 1, data, visited, solve_path)
            # 结束时间
            end_time = time.perf_counter()
            time_need = end_time - start_time
        elif a_idx == 2:
            # 开始时间
            start_time = time.perf_counter()
            bfs(0, 1, data, visited, solve_path)
            # 结束时间
            end_time = time.perf_counter()
            time_need = end_time - start_time
        elif a_idx == 3:
            # 开始时间
            start_time = time.perf_counter()
            paths = a_star(start, end, data)
            # 结束时间
            end_time = time.perf_counter()
            time_need = end_time - start_time
        elif a_idx == 4:
            # 开始时间
            start_time = time.perf_counter()
            found, dist = dijkstra(start, end, data)
            # 结束时间
            end_time = time.perf_counter()
            time_need = end_time - start_time

        if len(solve_path) != 1:
            for path in solve_path:
                nx, ny = path
                Label(t, bg="red", relief="raised", padx=12, pady=4).place(x=30 * nx, y=30 * ny)
        elif paths:
            for path in paths:
                nx, ny = path
                Label(t, bg="red", relief="raised", padx=12, pady=4).place(x=30 * nx, y=30 * ny)
        else:
            print("此算法不显示路径")

        # 打印代码执行时间
        print(f"算法{a_idx}执行时间为: {time_need:.10f} 秒")
        l.focus_set()
        t.mainloop()
