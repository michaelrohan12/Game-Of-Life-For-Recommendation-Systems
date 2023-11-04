import time
import pygame
import numpy as np
import json
import os
import random
import pyautogui
import cv2

COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170)
COLOR_ALIVE_NEXT = (255, 255, 255)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (1920, 1080))


def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]), dtype=np.dtype(
        [('product_id', int), ('value', int)]))

    for row in range(cells.shape[0]):
        for col in range(cells.shape[1]):
            updated_cells[row, col] = (cells[row, col]['product_id'], 0)

    for row, col in np.ndindex(cells.shape):
        neighborhood = cells[max(row - 1, 0):min(row + 2, cells.shape[0]),
                             max(col - 1, 0):min(col + 2, cells.shape[1])]
        alive = np.sum(neighborhood['value'])
    
        color = COLOR_BG if cells[row, col]['value'] == 0 else COLOR_ALIVE_NEXT

        if cells[row, col]['value'] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = COLOR_DIE_NEXT
            elif 2 <= alive <= 3:
                updated_cells[row, col]['value'] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
        else:
            if alive == 3:
                updated_cells[row, col]['value'] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT

        pygame.draw.rect(screen, color, (col * size,
                         row * size, size - 1, size - 1))

    return updated_cells


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame Recording")
    

    with open(os.path.join('feature-data', 'Mobile_features.json'), 'r') as file:
        sample_data = json.load(file)
    file.close()
    
    with open(os.path.join('inverted-index-ds', 'Mobile_DS.json'), 'r') as file:
        item_id_data = json.load(file)
    file.close()
    
    grid_width = 80
    grid_height = 60 

    cells = np.zeros((grid_height, grid_width), dtype=np.dtype(
        [('product_id', int), ('value', int)]))

    product_ids = []
    for row in range(grid_height):
        key = str(row)
        if type(sample_data[key]) is dict:
            idx1 = list(sample_data[key].keys())[0]
            idx2 = list(sample_data[key].values())[0]
            product_ids = item_id_data[idx1][idx2]
        else:
            product_ids = item_id_data[sample_data[key]]
        for col in range(grid_width):
            cells[row, col] = (random.choice(product_ids), 0)

    screen.fill(COLOR_GRID)
    update(screen, cells, 10)
    pygame.display.flip()
    pygame.display.update()

    running = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                out.release()
                # print(cells)
                
                chosen_product_ids = set()
                for cell in cells:
                    for value in cell:
                        if value[1] != 0:
                            chosen_product_ids.add(value[0])
                
                with open(os.path.join('data_with_ids', 'Mobile.json'), 'r') as file:
                    item_data = json.load(file)
                file.close()
                
                print("Item Details:")
                for product_id in chosen_product_ids:
                    item_dict = item_data[str(product_id)]
                    print("\n\nItem Id: " + str(product_id))
                    for key, value in item_dict.items():
                        print("{} = {}".format(key, value))
                    print("\n")
                    
                print("Chosen Product IDs:")
                for product_id in chosen_product_ids:
                    print(product_id)
                
                print(f"Total product ids for recommendation : {len(chosen_product_ids)}\n\n")
                    
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, 10)
                    pygame.display.update()

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()

                cells[pos[1] // 10, pos[0] // 10]['value'] = 1
                update(screen, cells, 10)
                pygame.display.update()

        screen.fill(COLOR_GRID)

        if running:
            cells = update(screen, cells, 10, with_progress=True)
            pygame.display.update()
            time.sleep(1)

        screenshot = pyautogui.screenshot(region=(0, 0, 1920, 1080))
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        out.write(frame)

        time.sleep(0.001)

if __name__ == "__main__":
    main()
