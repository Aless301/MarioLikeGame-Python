import pygame as pg
import sys
import random

pg.init()

clock = pg.time.Clock()

screen = pg.display.set_mode()
pg.display.set_caption("MarioLike")

SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

score = 0
level = 1

font = pg.font.Font("freesansbold.ttf", 28)
instructions = font.render(
    "Press [R] to reload the level, [X] to quit.", True, (0, 0, 0)
)

subtitle = pg.font.Font("freesansbold.ttf", 50)

end_font = pg.font.Font("freesansbold.ttf", 100)
game_over = end_font.render("GAME OVER", True, (0, 0, 0))
text_width = game_over.get_width()

gravity = 0.5
downspeed = 0
v = 6

is_jumping = False
is_floor = False
dmg_cooldown = False
reload_cooldown = False
reprint_needed = False

enemy_direction = 3

dmg_ticks = 0
reload_ticks = 0

goal_image = pg.image.load("star.png")
resized_image = pg.transform.scale(goal_image, (30, 30))


def drawBlock(obs_x, obs_y, obs_width, obs_height):
    obstacle = pg.draw.rect(
        screen, (0, 0, 255), pg.Rect(obs_x, obs_y, obs_width, obs_height)
    )
    return obstacle


def drawBlockOutline(obs_x, obs_y, obs_width, obs_height):
    block_outline = pg.draw.rect(
        screen, (0, 0, 100), pg.Rect(obs_x, obs_y, obs_width, obs_height), 5
    )
    return block_outline


def drawClouds(cloud_x, cloud_y, cloud_width, cloud_height):
    cloud = pg.draw.rect(
        screen, (255, 255, 255), pg.Rect(cloud_x, cloud_y, cloud_width, cloud_height)
    )
    return cloud


def drawEnemy(enemy_x):
    enemy = pg.draw.rect(
        screen, (0, 255, 0), pg.Rect(enemy_x, SCREEN_HEIGHT - 40 - 40, 40, 40)
    )
    return enemy


def drawEnemyOutline(enemy_x):
    enemy_outline = pg.draw.rect(
        screen, (0, 100, 0), pg.Rect(enemy_x, SCREEN_HEIGHT - 40 - 40, 40, 40), 4
    )
    return enemy_outline


def drawIndicatorLine(x, y, width, height):
    indicator_line = pg.draw.line(
        screen,
        (0, 0, 0),
        (x + width / 2, y + height),
        (x + width / 2, SCREEN_HEIGHT - 40),
        width=2,
    )
    return indicator_line


while True:
    x, y, width, height = 0, SCREEN_HEIGHT - 40, 40, 40

    obs_xPositions = []
    obs_yPositions = []
    obs_Widths = []
    obs_Heights = []

    cloud_xPositions = []
    cloud_yPositions = []
    cloud_Widths = []
    cloud_Heights = []

    enemy_xPositions = []
    enemy_directions = []

    goal_x, goal_y = random.randint(0, SCREEN_WIDTH - 20), random.randint(0, 300)

    dmg_cooldown = True
    reload_cooldown = True

    for i in range(5):
        obs_x = random.randint(0, SCREEN_WIDTH)
        obs_y = random.randint(0, SCREEN_HEIGHT - 200)
        obs_width = random.randint(40, 200)
        obs_height = random.randint(20, 60)

        obs_xPositions.append(obs_x)
        obs_yPositions.append(obs_y)
        obs_Widths.append(obs_width)
        obs_Heights.append(obs_height)

    for i in range(10):
        cloud_x = random.randint(0, SCREEN_WIDTH)
        cloud_y = random.randint(0, SCREEN_HEIGHT - 200)
        cloud_width = random.randint(20, 60)
        cloud_height = random.randint(10, 30)

        cloud_xPositions.append(cloud_x)
        cloud_yPositions.append(cloud_y)
        cloud_Widths.append(cloud_width)
        cloud_Heights.append(cloud_height)

    for i in range(level):
        enemy_x = random.randint(0, SCREEN_WIDTH - 40)

        enemy_xPositions.append(enemy_x)
        enemy_direction = random.choice([3, -3])
        enemy_directions.append(enemy_direction)

    while True:
        screen.fill((135, 206, 235))
        obstacles = []
        enemies = []
        floor = pg.draw.rect(
            screen, (100, 200, 0), pg.Rect(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
        )
        is_floor = False

        for i in range(level):
            enemy = drawEnemy(enemy_xPositions[i])
            enemies.append(enemy)
            enemy_outline = drawEnemyOutline(enemy_xPositions[i])

        score_counter = font.render("Score : " + str(score), True, (0, 0, 0))
        score_width = score_counter.get_width()

        goal = pg.draw.rect(
            screen,
            (135, 206, 235),
            pg.Rect(goal_x, goal_y, 30, 30),
        )

        for i in range(10):
            cloud = drawClouds(
                cloud_xPositions[i],
                cloud_yPositions[i],
                cloud_Widths[i],
                cloud_Heights[i],
            )

        for i in range(5):
            obstacle = drawBlock(
                obs_xPositions[i], obs_yPositions[i], obs_Widths[i], obs_Heights[i]
            )
            obstacles.append(obstacle)
            block_outline = drawBlockOutline(
                obs_xPositions[i], obs_yPositions[i], obs_Widths[i], obs_Heights[i]
            )

        screen.blit(resized_image, (goal_x, goal_y))

        player = pg.draw.rect(screen, (255, 0, 0), pg.Rect(x, y, width, height))
        player_outer_layer = pg.draw.rect(
            screen, (100, 0, 0), pg.Rect(x, y, width, height), 4
        )

        screen.blit(instructions, (10, 10))
        screen.blit(score_counter, (SCREEN_WIDTH - score_width - 10, 10))

        for obs in obstacles:
            if (
                obs.left < goal_x < obs.left + obs.width
                and obs.top < goal_y < obs.top + obs.height
            ):
                reprint_needed = True
                break
            if goal_y + 30 > obs.top and obs.left < goal_x < obs.left + obs.width:
                reprint_needed = True
                break

        if reprint_needed:
            reprint_needed = False
            break

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] and x > 0:
            x -= 5
        if keys[pg.K_RIGHT] and x < SCREEN_WIDTH - width:
            x += 5
        if keys[pg.K_SPACE] and not is_jumping:
            v = 6
            is_jumping = True
        if keys[pg.K_r] and not reload_ticks:
            if score >= 5:
                score -= 5
            reload_ticks = True
            break
        if keys[pg.K_x]:
            pg.quit()
            sys.exit()

        if is_jumping:
            F = (1 / 2) * (v**2)
            y -= F

        for obs in obstacles:
            if (
                obs.left <= x + width
                and x <= obs.left + obs.width
                and obs.top + obs.height >= y + height >= obs.top
            ):
                y = obs.top - height
                is_jumping = False
                downspeed = 0
                v = 0
                is_floor = True

            if (
                obs.left <= x + width
                and x <= obs.left + obs.width
                and obs.top + obs.height > y > obs.top
            ):
                y = obs.top + obs.height
                v = v / 2

        if x <= goal_x <= x + width and y < goal_y < y + height:
            score += 10
            level += 1
            enemy_direction = 3
            break
        if goal_x <= x <= goal_x + 30 and y < goal_y < y + height:
            score += 10
            level += 1
            enemy_direction = 3
            break

        if dmg_cooldown:
            if dmg_ticks < 60:
                dmg_ticks += 1
            else:
                dmg_cooldown = False
                dmg_ticks = 0

        if reload_cooldown:
            if reload_ticks < 180:
                reload_ticks += 1
            else:
                reload_cooldown = False
                reload_ticks = 0

        if not dmg_cooldown:
            for i in range(len(enemy_xPositions)):
                enemy_x = enemy_xPositions[i]
                if enemy_x < x < enemy_x + 40 and y > SCREEN_HEIGHT - 120:
                    x = 0
                    y = SCREEN_HEIGHT - height - 40
                    dmg_cooldown = True
                    if score > 0:
                        score -= 10
                if enemy_x < x + width < enemy_x + 40 and y > SCREEN_HEIGHT - 120:
                    x = 0
                    y = SCREEN_HEIGHT - height - 40
                    dmg_cooldown = True
                    if score > 0:
                        score -= 10

        if y < SCREEN_HEIGHT - height - 40:
            if not is_floor:
                y += downspeed
                downspeed += gravity
                is_jumping = True

        if y >= SCREEN_HEIGHT - height - 40:
            y = SCREEN_HEIGHT - height - 40
            is_jumping = False
            downspeed = 0
            v = 6

        if y + height <= 0:
            indicator_line = drawIndicatorLine(x, y, width, height)

        for i in range(len(enemy_xPositions)):
            enemy_x = enemy_xPositions[i]
            enemy_direction = enemy_directions[i]
            if enemy_x < 0:
                enemy_direction = -3
            if enemy_x + 40 > SCREEN_WIDTH:
                enemy_direction = 3

            enemy_x -= enemy_direction
            enemy_xPositions[i] = enemy_x
            enemy_directions[i] = enemy_direction

        if score <= 0 and level > 1:
            level_reached = subtitle.render(
                "Level reached : " + str(level), True, (0, 0, 0)
            )
            level_width = level_reached.get_width()
            screen.fill((255, 0, 0))
            screen.blit(
                game_over,
                (SCREEN_WIDTH // 2 - text_width // 2, SCREEN_HEIGHT // 2 - 80),
            )
            screen.blit(
                level_reached,
                (SCREEN_WIDTH // 2 - level_width // 2, SCREEN_HEIGHT // 2 + 34),
            )
            pg.display.update()
            pg.time.delay(5000)
            pg.quit()
            sys.exit()

        pg.display.update()
        clock.tick(60)