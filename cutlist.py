from data_classes import Board, Length

class Cutlist:
# Algorithim adapted from https://en.wikipedia.org/wiki/Knapsack_problem#Dynamic_programming_in-advance_algorithm

    def __init__(self, boards, stock_board_length, saw_kerf):
        self.boards = boards
        self.stock_board_length = stock_board_length
        self.saw_kerf = saw_kerf
        self.min = [{} for i in range(len(self.boards)+1)] #stores waste, used_boards tuples for each number of boards used (i), stock length pairs. 
        #   Ex. min[1, Length(15,0)] could give (Length(2,12), [Board(Length(12, 48), 90, 90)]) 

    def minimum_waste(self, i, stock_length): #return the minimum waste when cutting a stock board using i number of boards
        board = self.boards[i-1]

        # print("(", i, ",", stock_length, ")\t", board)

        if i == 0 or stock_length == Length(0,0): #if we aren't using any boards, or if there is no stock board left to cut from, the minimum waste would be the whole length of the stock board, and no boards would cut from it
            return stock_length, []
        if stock_length < Length(0,0): #parent call created a negative stock_length when subtracting a board
            raise OverflowError("stock_length is negative", stock_length) #should never happen?

        #have we already calculated the minimum waste for using one less board when cutting a stock board of the same length?
        if stock_length not in self.min[i-1]: #no
            self.min[i-1][stock_length] = self.minimum_waste(i-1, stock_length) #need to calculate that minimum waste
       
        #is this board longer than the stock board
        if board.length.sum(self.saw_kerf) > stock_length and board.length != stock_length: #yes, it could never be cut from the stock board
            self.min[i][stock_length] = self.min[i-1][stock_length] #this stock board is all waste, so cutting with this board would have the same waste as cutting with one less
        
        else: #no, we could cut it from the stock board
            #is this board a perfect fit?
            if board.length == stock_length: #yes, so we won't have to subtract a saw kerf for the following cut
                removal_length = board.length
            else: #no, so we have to account for the saw kerf for the following cut
                removal_length = board.length.sum(self.saw_kerf)
            
            #have we already calculated the minimum waste for using one less board when cutting a stock board exactly this board's length (plus a saw kerf) shorter?
            if stock_length.difference(removal_length) not in self.min[i-1]: #no
                self.min[i-1][stock_length.difference(removal_length)] = self.minimum_waste(i-1, stock_length.difference(removal_length)) #need to calculate that minimum waste

            self.min[i][stock_length] = self.min[i-1][stock_length.difference(removal_length)][0], self.min[i-1][stock_length.difference(removal_length)][1] + [board]
        
        # print("Solved:(", i, ",", stock_length, ") =", self.min[i][stock_length][0], self.min[i][stock_length][1])
        return self.min[i][stock_length]

    def solve(self):
        needed_stock_boards = 0
        total_waste = Length(0,0)
        used_boards_lists = []
        quantities = []
        wastes = []
        while len(self.boards) > 0:
            waste, used_boards = self.minimum_waste(len(self.boards), self.stock_board_length)
            needed_stock_boards += 1
            total_waste = total_waste.sum(waste)

            if used_boards not in used_boards_lists:
                used_boards_lists.append(used_boards)
                quantities.append(1)
                wastes.append(waste)
            else:
                quantities[used_boards_lists.index(used_boards)] += 1

            # for board in self.boards:
            #     print("\t",board)

            for used_board in used_boards:
                # print("Removing", used_board)
                self.boards.remove(used_board)

            self.min = [{} for i in range(len(self.boards)+1)]
        
        return needed_stock_boards, total_waste, zip(quantities, wastes, used_boards_lists)