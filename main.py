import os

SIZE = 3
INF = 1000
USER_PLAYER = 'X'  # maximize
IA_PLAYER = 'O'  # minimize


def print_table(table):
    for r in range(SIZE):
        for c in range(SIZE):
            print(table[r][c], end=" ")
        print(end="\n")


def player_win(player='', table=[]):
    win_condition = [player for _ in range(SIZE)]

    # row check
    for row in range(SIZE):
        if table[row] == win_condition:
            return True

    # col check
    for col in range(SIZE):
        current = [table[i][col] for i in range(SIZE)]
        if current == win_condition:
            return True

    # diagonal check
    main_diag = [table[i][i] for i in range(SIZE)]
    secun_diag = [table[i][SIZE - i - 1] for i in range(SIZE)]

    if main_diag == win_condition or secun_diag == win_condition:
        return True

    return False


def draw(table):
    result = [table[r][c]
              for r in range(SIZE) for c in range(SIZE) if table[r][c] == '-']

    return len(result) == 0


def check_final_state(table):
    if player_win('X', table):
        return 10
    elif player_win('O', table):
        return -10
    elif draw(table):
        return 0
    return


def get_best_score(table, player, depth):
    curr_state = check_final_state(table)
    if curr_state is not None:
        if curr_state > 0:
            return curr_state - depth
        elif curr_state < 0:
            return curr_state + depth
        return 0

    best_score = INF if player == IA_PLAYER else -INF
    for r in range(SIZE):
        for c in range(SIZE):
            if table[r][c] == '-':
                table[r][c] = player
                next_player = IA_PLAYER if player == USER_PLAYER else USER_PLAYER
                score = get_best_score(table, next_player, depth + 1)
                if player == USER_PLAYER:
                    best_score = max(best_score, score)
                elif player == IA_PLAYER:
                    best_score = min(best_score, score)
                table[r][c] = '-'
    return best_score


def get_best_move(table):
    move = (0, 0)
    best_score = INF
    for r in range(SIZE):
        for c in range(SIZE):
            if table[r][c] == '-':
                table[r][c] = IA_PLAYER
                score = get_best_score(table, USER_PLAYER, 1)
                if score < best_score:
                    best_score = score
                    move = (r, c)
                table[r][c] = '-'
    return move


def user_move(table):
    posr, posc = map(int, input().split(" "))
    table[posr][posc] = USER_PLAYER


def IA_move(table):
    move = get_best_move(table)
    table[move[0]][move[1]] = IA_PLAYER


def run():
    initial_table = [['-', '-', '-'],
                     ['-', '-', '-'],
                     ['-', '-', '-']]
    # print(initial_table)
    while True:
        os.system("clear")
        print_table(initial_table)

        user_move(initial_table)
        if (draw(initial_table)):
            print("DRAW!. That's IMPOSSIBLE XD")
            break

        IA_move(initial_table)
        if (player_win(IA_PLAYER, initial_table)):
            print_table(initial_table)
            print("IA WIN!. OF COURSE BABY")
            break


if __name__ == '__main__':
    run()
