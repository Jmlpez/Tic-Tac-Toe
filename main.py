import os

SIZE = 3
INF = 1000
USER_PLAYER = "X"  # maximize
IA_PLAYER = "O"  # minimize


def print_table(table):
    for r in range(SIZE):
        for c in range(SIZE):
            print(table[r][c], end=" ")
        print(end="\n")


def is_free_cell(posr, posc, table):
    return table[posr][posc] == "-"


def player_win(player="", table=[]):
    win_condition = [player] * SIZE

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
    for r in range(SIZE):
        if "-" in table[r]:
            return False
    return True


def check_final_state(table):
    if player_win("X", table):
        return 10
    elif player_win("O", table):
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
            if is_free_cell(r, c, table):
                table[r][c] = player
                next_player = IA_PLAYER if player == USER_PLAYER else USER_PLAYER
                score = get_best_score(table, next_player, depth + 1)
                if player == USER_PLAYER:
                    best_score = max(best_score, score)
                elif player == IA_PLAYER:
                    best_score = min(best_score, score)
                table[r][c] = "-"
    return best_score


def get_best_move(table):
    move = (0, 0)
    best_score = INF
    for r in range(SIZE):
        for c in range(SIZE):
            if is_free_cell(r, c, table):
                table[r][c] = IA_PLAYER
                score = get_best_score(table, USER_PLAYER, 1)
                if score < best_score:
                    best_score = score
                    move = (r, c)
                table[r][c] = "-"
    return move


def user_move(table):
    posr, posc = map(int, input().split(" "))

    if (
        posr >= 0
        and posr < SIZE
        and posc >= 0
        and posc < SIZE
        and is_free_cell(posr, posc, table)
    ):
        table[posr][posc] = USER_PLAYER
        return True
    return False


def IA_move(table):
    move = get_best_move(table)
    table[move[0]][move[1]] = IA_PLAYER


def get_empty_table():
    table = [["-"] * SIZE for _ in range(SIZE)]
    return table


def print_result(table, win_player=None):
    print_table(table)
    if win_player not in [USER_PLAYER, IA_PLAYER]:
        print("DRAW!")
    else:
        print("IA WIN!. OF COURSE BABY")


def run():
    initial_table = get_empty_table()

    game_over = False

    while not game_over:
        os.system("clear")
        print_table(initial_table)

        # User Move
        if not user_move(initial_table):
            continue

        if draw(initial_table):
            print_result(initial_table)
            game_over = True
            continue
        # IA Move
        IA_move(initial_table)
        if player_win(IA_PLAYER, initial_table):
            print_result(initial_table, IA_PLAYER)
            game_over = True


if __name__ == "__main__":
    run()
