import functions as f


def main():
    f.pygame.init()

    win_side_length = 800
    window = f.pygame.display.set_mode((win_side_length, win_side_length))
    f.pygame.display.set_caption("A* Pathfinding Algorithm")

    ROWCOUNT = 50
    grid = f.make_grid(ROWCOUNT, win_side_length)
    algo_started = False
    del_key = False
    run = True
    start = None
    end = None
    while run:
        f.draw_window(ROWCOUNT, win_side_length, window, grid)
        for event in f.pygame.event.get():
            if event.type == f.pygame.QUIT:
                run = False
            if algo_started:
                continue

            # LEFT MOUSE BUTTON
            if f.pygame.mouse.get_pressed()[0]:
                cursor_pos = f.pygame.mouse.get_pos()
                row, col = f.get_mouse_pos(
                    ROWCOUNT, win_side_length, cursor_pos)
                cell = grid[row][col]
                if not start and cell != end:
                    start = cell
                    start.make_start()
                elif not end and cell != start:
                    end = cell
                    end.make_end()
                elif cell != end and cell != start:
                    cell.make_barrier()

            # ANY KEY IS PRESSED
            elif event.type == f.pygame.KEYDOWN:
                if event.key == f.pygame.K_BACKSPACE:  # HOLDING BACKSPACE = DELETING MODE
                    del_key = True
                elif event.key == f.pygame.K_SPACE and not algo_started and start and end:
                    for row in grid:
                        for cell in row:
                            cell.update_neighbours(grid)
                    f.pathfinder(lambda: f.draw_window(
                        ROWCOUNT, win_side_length, window, grid), grid, start, end)
                elif event.key == f.pygame.K_c:
                    start = None
                    end = None
                    grid = f.make_grid(ROWCOUNT, win_side_length)

            elif event.type == f.pygame.KEYUP:  # ANY KEY HAS STOPPED BEING PRESSED
                if event.key == f.pygame.K_BACKSPACE:
                    del_key = False

        # HANDLE DELETING CELLS
        if del_key:
            cursor_pos = f.pygame.mouse.get_pos()
            row, col = f.get_mouse_pos(
                ROWCOUNT, win_side_length, cursor_pos)
            cell = grid[row][col]
            cell.reset()
            if cell == start:
                start = None
            elif cell == end:
                end = None

    f.pygame.quit()


if __name__ == "__main__":
    main()
