import heapq
import copy
import pygame
import time
import itertools
from collections import deque 
import random
import math


WIDTH, HEIGHT =800, 400
TILE_SIZE = 80
FONT_SIZE = 40
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (100, 200, 100)
BUTTON_TEXT_COLOR = (0, 0, 0)


class Puzzle: 
    def __init__(self,state,parent=None,move="",cost=0):
        self.state=state
        self.parent=parent
        self.move=move # buoc di tu cha den dday 
        self.cost=cost

    def __lt__(self,other): 
        return self.cost<other.cost
    
def find_blank(state): 
    for i in range(3): 
        for j in range(3): 
            if state[i][j]==0: 
                return i,j
    return None

def move_black(state,direct): 
    i,j=find_blank(state)
    if i is None or j is None:
        return None
    new_state=copy.deepcopy(state)

    moves = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
    if direct not in moves:
        return None
    di,dj=moves[direct]
    ni,nj=i+di,j+dj

    if 0<=ni<3 and 0<=nj<3: 
        new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
        return new_state
    return None 

def bfs(start,goal): 
    queue=deque([Puzzle(start)])
    visited =set()
    max_space = 1
    while queue: 
        node=queue.popleft()
        if node.state==goal: 
            path=[]
            while node.parent: 
                path.append(node.move)
                node=node.parent
            return path[::-1],len(path),max_space
        visited.add((tuple(map(tuple,node.state))))

        for move in ["U", "D", "L", "R"]:
            new_state=move_black(node.state,move)
            if new_state and tuple(map(tuple,new_state)) not in visited:
                queue.append(Puzzle(new_state,node,move))
                max_space = 1
                max_space = max(max_space, len(queue) + len(visited))
    
    return None,-1,max_space

def dfs(start,goal): 
    stack=[Puzzle(start)]
    visited=set()
    max_space = 1
    while stack: 
        node=stack.pop()
        if node.state==goal:
            path=[] # duong di cua node
            while node.parent: 
                path.append(node.move)
                node=node.parent

            return path[::-1],len(path),max_space
        
        visited.add(tuple(map(tuple,node.state)))

        for move in ["U", "D", "L", "R"]:
            new_state=move_black(node.state,move)    
            if new_state and tuple(map(tuple,new_state)) not in visited:
                stack.append(Puzzle(new_state,node,move))
                max_space = max(max_space, len(stack) + len(visited))


    return None ,-1,max_space

# Thuat toan UCS 

# tim gia cua cac trang thai la so o sai so voi goal
def misplaced_tiles(state,goal): 
    return sum(1 for i in range(3) for j in range(3) if state[i][j]!=goal[i][j] and state[i][j]!=0)
# thuat toan ucs
def ucs(start,goal): 
    priority_queue=[]
    initial_cost = misplaced_tiles(start,goal)
    heapq.heappush(priority_queue,(0,Puzzle(start,cost=0))) # them vao hang doi uu tien
    visited=set()
    max_space = 1
    while priority_queue: 
        cost,node=heapq.heappop(priority_queue)
        if node.state==goal: 
            path=[]
            while node.parent: 
                path.append(node.move)
                node=node.parent
            return path[::-1],cost,max_space
        
        visited.add(tuple(map(tuple,node.state)))

        for move in ["U", "D", "L", "R"]:
            new_state=move_black(node.state,move)
            if new_state and tuple(map(tuple,new_state)) not in visited: 
                new_cost=node.cost+1
                heapq.heappush(priority_queue,(new_cost,Puzzle(new_state,node,move,new_cost)))
                max_space = max(max_space, len(priority_queue) + len(visited))
    return None,-1,max_space


#ham mahatan cua gbfs

def mahatan_puzzle(start,goal):
    cost=0
    start_1D=[start[i][j] for i in range(3) for j in range(3)]
    goal_1D=[goal[i][j] for i in range(3) for j in range(3)]

    for i in range(3*3): 
        if start_1D[i]!=0: 
            goal_pos=goal_1D.index(start_1D[i])
            curr_x,curr_y=i//3,i%3
            goal_x,goal_y=goal_pos//3,goal_pos%3
            cost = cost + abs(curr_x-goal_x) + abs(curr_y - goal_y)
    return cost

def gbfs(start,goal): 
    priority_queue=[]
    # initial_cost = misplaced_tiles(start,goal)
    initial_cost=mahatan_puzzle(start,goal)
    heapq.heappush(priority_queue,(initial_cost,Puzzle(start,cost=initial_cost))) # them vao hang doi uu tien
    visited=set()
    max_space = 1
    while priority_queue: 
        _,node=heapq.heappop(priority_queue)
        if node.state==goal: 
            path=[]
            cost=0
            while node.parent:
                cost+=1
                path.append(node.move)
                node=node.parent
            return path[::-1],cost,max_space
        
        visited.add(tuple(map(tuple,node.state)))

        for move in ["U", "D", "L", "R"]:
            new_state=move_black(node.state,move)
            if new_state and tuple(map(tuple,new_state)) not in visited: 
                # new_cost=misplaced_tiles(new_state,goal)
                new_cost=mahatan_puzzle(new_state,goal)
                heapq.heappush(priority_queue,(new_cost,Puzzle(new_state,node,move,new_cost)))
                max_space = max(max_space, len(priority_queue) + len(visited))
    return None,-1,max_space


def A_start(start,goal): 
    priority_queue = []
    initial_h = mahatan_puzzle(start, goal)
    initial_f = 0 + initial_h
    heapq.heappush(priority_queue, (initial_f, Puzzle(start, cost=0)))
    visited_cost = {tuple(map(tuple, start)): 0}  # Lưu chi phí g(n) tốt nhất đến mỗi trạng thái
    counter = 0
    max_space = 1
    while priority_queue: 
        f_cost,node=heapq.heappop(priority_queue)
        if node.state==goal: 
            path=[]
            cost=0
            while node.parent:
                path.append(node.move)
                node=node.parent
            print('return')
            return path[::-1],len(path),max_space
        state_tuple = tuple(map(tuple, node.state))
        if f_cost>visited_cost.get(state_tuple,float('inf')) + mahatan_puzzle(node.state,goal): 
            continue
        for move in ["U", "D", "L", "R"]:
            new_state = move_black(node.state, move)
            if new_state: 
                new_g = node.cost + 1
                new_h = mahatan_puzzle(new_state, goal)
                new_f = new_g + new_h
                new_state_tuple = tuple(map(tuple, new_state))
                if new_state_tuple not in visited_cost or new_g < visited_cost[new_state_tuple]:
                    visited_cost[new_state_tuple] = new_g
                    counter += 1
                    heapq.heappush(priority_queue, (new_f, Puzzle(new_state, node, move, new_g)))
                max_space = max(max_space, len(priority_queue) + len(visited_cost))
    print('none')
    return None,-1,max_space


def ida_start(start,goal): 
    def search(node,g,threshold,visited_cost,path): 
        state_tuple=tuple(map(tuple,node.state))
        h=mahatan_puzzle(node.state,goal)
        f=g+h

        if f > threshold: 
            return f,False,path
        if node.state==goal:
            return f,True,path
        
        min_next_threshold = float('inf')
        for move in ["U", "D", "L", "R"]:
            new_state=move_black(node.state,move)
            if new_state:
                new_state_tuple=tuple(map(tuple,new_state))
                new_g=node.cost+1
                if new_state_tuple not in visited_cost or new_g<visited_cost[new_state_tuple]: 
                    visited_cost[new_state_tuple]=new_g
                    new_node=Puzzle(new_state,node,move,new_g)
                    new_path=path+[move]
                    next_f,found,result_path=search(new_node,new_g,threshold,visited_cost,new_path)
                    if found: 
                        return next_f,True,result_path
                    min_next_threshold=min(min_next_threshold,next_f)
        return min_next_threshold,False,path
    
    initial_h=mahatan_puzzle(start,goal)
    threshold=initial_h
    visited_cost={tuple(map(tuple,start)):0}
    max_space=1
    while True: 
        path=[]
        node=Puzzle(start,cost=0)
        visited_cost={tuple(map(tuple,start)): 0}
        new_threshold,found,final_path=search(node,0,threshold,visited_cost,path)
        max_space=max(max_space,len(visited_cost))

        if found:
            return final_path,len(final_path),max_space
        
        if new_threshold==float('inf'): 
            return None,-1,max_space
        threshold=new_threshold


def SimpleHillClimbing(start,goal): 
    current_node=Puzzle(start,cost=mahatan_puzzle(start,goal))
    visited=set()
    visited.add(tuple(map(tuple,current_node.state)))
    max_space=1

    while True: 
        if current_node.state==goal: 
            path=[]
            cost=0
            while current_node.parent: 
                cost+=1 
                path.append(current_node.move)
                current_node=current_node.parent
            return path[::-1],cost,max_space
        
        best_neighbhor=None
        best_cost=current_node.cost

        for move in ["U", "D", "L", "R"]:
            new_state=move_black(current_node.state,move)

            if new_state and tuple(map(tuple,new_state)) not in visited: 
                new_cost=mahatan_puzzle(new_state,goal)
                if new_cost < best_cost: 
                    best_cost = new_cost
                    best_neighbhor=Puzzle(new_state,current_node,move,new_cost)
        if best_neighbhor is None: 
            return None,-1,max_space

        current_node=best_neighbhor
        visited.add(tuple(map(tuple,current_node.state)))
        max_space=max(max_space,len(visited))
                
def StochasticHillClimbing(start,goal): 
    current_node=Puzzle(start,cost=mahatan_puzzle(start,goal))
    visited=set()
    visited.add(tuple(map(tuple,current_node.state)))
    max_space=1

    while True: 
        if current_node.state==goal: 
            path=[]
            cost=0
            while current_node.parent: 
                cost+=1 
                path.append(current_node.move)
                current_node=current_node.parent
            return path[::-1],cost,max_space
        
        neighbors = []
        for move in ["U", "D", "L", "R"]:
            new_state=move_black(current_node.state,move)

            if new_state and tuple(map(tuple,new_state)) not in visited: 
                new_cost=mahatan_puzzle(new_state,goal)
                neighbors.append(Puzzle(new_state, current_node, move, new_cost))
        if not neighbors:
            return None, -1, max_space
        better_neighbors = [n for n in neighbors if n.cost < current_node.cost]
        next_node=None
        for neighbor in better_neighbors: 
            next_node=neighbor
            break

        if next_node is None:
            return None, -1, max_space
        
        # Cập nhật trạng thái
        current_node = next_node
        visited.add(tuple(map(tuple, current_node.state)))
        max_space = max(max_space, len(visited))

def SimulatedAnnealing(start,goal): 
    current_node = Puzzle(start, cost=mahatan_puzzle(start, goal))
    visited = set()
    visited.add(tuple(map(tuple, current_node.state)))
    max_space = 1

    # Thiết lập tham số ban đầu cho Simulated Annealing
    temperature = 10000.0  # Nhiệt độ ban đầu
    cooling_rate = 0.995  # Tỷ lệ làm nguội (0 < cooling_rate < 1)
    min_temperature = 0.01  # Nhiệt độ tối thiểu để dừng


    while True:
        if current_node.state==goal: 
            path=[]
            cost=0
            while current_node.parent: 
                cost+=1 
                path.append(current_node.move)
                current_node=current_node.parent
            return path[::-1],cost,max_space
        
        neighbors = []
        for move in ["U", "D", "L", "R"]:
            new_state=move_black(current_node.state,move)

            if new_state and tuple(map(tuple,new_state)) not in visited: 
                new_cost=mahatan_puzzle(new_state,goal)
                neighbors.append(Puzzle(new_state, current_node, move, new_cost))
        if not neighbors:
            return None, -1, max_space
        
        better_neighbors = [n for n in neighbors if n.cost < current_node.cost]
        next_node=None
        for neighbor in better_neighbors: 
            next_node=neighbor
            break

        probability=0
        if next_node is None:
            for neighbor in neighbors:
                probability_neighbor=math.exp(-(current_node.cost-neighbor.cost)/temperature)
                x=random.random()
                if probability_neighbor >= x:
                    next_node=neighbor
                    break

                # if probability_neighbor>probability: 
                #     next_node=neighbor
        
        # Cập nhật trạng thái và không gian bộ nhớ
        current_node = next_node
        visited.add(tuple(map(tuple, current_node.state)))
        max_space = max(max_space, len(visited))
        
        # Giảm nhiệt độ
        temperature *= cooling_rate
        if temperature < min_temperature:  # Dừng nếu nhiệt độ quá thấp
            return None, -1, max_space


def BeamSearch(start, goal, beam_width=2):  
    queue = deque([Puzzle(start, cost=mahatan_puzzle(start,goal))])
    visited = set()
    visited.add(tuple(map(tuple, start)))

    max_space = 1  

    while queue:
        next_level = []  # Danh sách trạng thái cho vòng tiếp theo

        for _ in range(len(queue)):  
            node = queue.popleft()

            # Kiểm tra nếu đã đến trạng thái đích
            if node.state == goal:
                path = []
                while node.parent:
                    path.append(node.move)
                    node = node.parent
                return path[::-1], len(path), max_space

            # Sinh các trạng thái con
            for move in ["U", "D", "L", "R"]:
                new_state = move_black(node.state, move)

                if new_state and tuple(map(tuple, new_state)) not in visited:
                    new_cost=mahatan_puzzle(new_state,goal)
                    new_node = Puzzle(new_state, node, move, cost=new_cost)
                    next_level.append(new_node)
                    visited.add(tuple(map(tuple, new_state)))

        # Nếu không có trạng thái nào để tiếp tục, thuật toán thất bại
        if not next_level:
            return None, -1, max_space

        # Sort `next_level` theo cost (từ thấp đến cao)
        next_level.sort(key=lambda x: x.cost)

        # Thêm thủ công `beam_width` trạng thái tốt nhất vào queue
        for i in range(min(beam_width, len(next_level))):
            queue.append(next_level[i])
        # Cập nhật bộ nhớ tối đa đã sử dụng
        max_space = max(max_space, len(queue) + len(visited))
    
    return None, -1, max_space



# Mỗi hành động có thể có kết quả sai lệch (ngẫu nhiên)
def nondeterministic_results(state, direction):
    alternative = {
        "U": ["U"],
        "D": ["D"],
        "L": ["L"],
        "R": ["R"]
    }
    results = []
    for d in alternative[direction]:
        new_state = move_black(state, d)
        if new_state:
            results.append((d, new_state))
    return results

def and_or_search(start, goal, max_depth=20):
    max_space = 1
    visited = set()

    def recur(node, path, depth,visited):
        nonlocal max_space
        if depth > max_depth:
            return False, []
        state_key = tuple(map(tuple, node.state))
        if state_key in visited:
            return False, []
        if node.state == goal:
            return True, []
        best_path=None
        # visited.add(tuple(map(tuple, node.state)))
        visited.add(state_key)
        for direction in ["U", "D", "L", "R"]:
            successors = nondeterministic_results(node.state, direction)

            all_success = True
            local_paths = []

            for move_dir, result_state in successors:
                if tuple(map(tuple, result_state)) in visited:
                    all_success = False
                    break

                child = Puzzle(result_state, node, move_dir, node.cost + 1)
                success, sub_path = recur(child, path + [move_dir], depth + 1,visited)

                if not success:
                    all_success = False
                    break
                local_paths.append([move_dir] + sub_path)

            if all_success and local_paths:
                candidate_path = local_paths[0]
                if not best_path or len(candidate_path) < len(best_path):
                    best_path = candidate_path

        visited.remove(state_key)
        if best_path:
            max_space = max(max_space, len(best_path) + len(visited))
            return True, best_path
        return False, []

    root = Puzzle(start)
    success, path = recur(root, [], 0,set())
    if success:
        return path, len(path), max_space
    else:
        return None, -1, max_space
    

def bfs_Belief(start_belief, goal_belief):
    queue = deque([Puzzle(start_belief)])
    visited = set()
    max_space = 1  # Theo dõi bộ nhớ tối đa

    # Chuyển goal_belief thành tập hợp tuple để kiểm tra nhanh
    goal_set = {tuple(map(tuple, state)) for state in goal_belief}

    while queue:
        node = queue.popleft()
        # Kiểm tra xem tất cả trạng thái trong node.states có trong goal_belief không
        flag = True
        for state in node.states:
            if tuple(map(tuple, state)) not in goal_set:
                flag = False
                break

        if flag:
            # Xây dựng đường đi
            path = []
            while node.parent:
                path.append(node.move)
                node = node.parent
            return True, path[::-1], max_space

        # Chuyển mảng trạng thái thành tuple để thêm vào visited
        state_tuple = tuple(tuple(map(tuple, state)) for state in node.states)
        visited.add(state_tuple)

        # Tạo các mảng trạng thái mới
        for move in ["U", "D", "L", "R"]:
            new_state_belief = []
            valid_move = False
            for state in node.states:
                new_state = move_black(state, move)
                if new_state:
                    new_state_belief.append(new_state)
                    valid_move = True
                else:
                    new_state_belief.append(state)  # Giữ nguyên nếu không di chuyển được
            # Chỉ thêm vào queue nếu có ít nhất một trạng thái thay đổi
            if valid_move:
                new_state_tuple = tuple(tuple(map(tuple, state)) for state in new_state_belief)
                if new_state_tuple not in visited:
                    queue.append(Puzzle(new_state_belief, node, move, node.cost + 1))
                    max_space = max(max_space, len(queue) + len(visited))
    return False, None, max_space
    

def BackTracking(values,visited=None,path=None): 
        visited=set()
        path=[]
        def dfs_BT(depth): 
            if len(visited) == len(values): 
                return True
            for x in values:
                if x not in visited and (not path or x > path[-1]): 
                    path.append(x)
                    visited.add(x)
                    if dfs_BT(depth+1):
                        return True
                    path.pop()
                    visited.remove(x)
            return False
        success=dfs_BT(0)
        return (path,len(path)) if success else (None,-1)


def is_solvable(state):
    """
    Kiểm tra xem trạng thái có thể giải được không bằng cách kiểm tra số nghịch đảo (inversion count).
    """
    flat = [num for row in state for num in row if num != 0]
    inv_count = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inv_count += 1
    return inv_count % 2 == 0

def generate_all_states():
    """
    Sinh tất cả các trạng thái của 8-Puzzle và kiểm tra tính solvable của từng trạng thái.
    """
    values = list(range(9)) 
    all_permutations = itertools.permutations(values)  # Sinh tất cả các hoán vị

    solvable_states = []  # Lưu trữ các trạng thái hợp lệ
    for perm in all_permutations:
        state = [list(perm[i*3:(i+1)*3]) for i in range(3)]
        if checkif(state): 
            solvable_states.append(state)

    return solvable_states

def checkif(state): 
    for i in range(3):
        for j in range(2): 
            if state[i][j+1] != state[i][j] + 1:
                return False

    for i in range(2):  
        for j in range(3):
            if state[i+1][j] != state[i][j] + 3:
                return False

    # Nếu cả hai điều kiện đều thỏa mãn
    return True


# if __name__=="__main__": 
#     values = [2,3,4,1,5,7,6,8]
#     result,len=BackTracking(values)
#     print("ket qua: ",result)

#     array=generate_all_states()
#     for x in array : 
#         print(x)



         


    
    

