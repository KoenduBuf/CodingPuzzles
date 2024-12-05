#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <math.h>

//////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////// Structs & Defs

#define WIDTH      30
#define HEIGHT     20
#define DEATH_MAX  SHRT_MIN + 10
#define DEATH(p)   DEATH_MAX - p

typedef struct {
    short x, y;
} Loc;

typedef struct {
    short dx, dy;
    char* name;
} Dir;

//////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////// Variables & Macros

Dir no_direction = { 0, 0, NULL };
Dir directions[] = {
    {  0, -1, "UP" },
    {  0,  1, "DOWN" },
    {  1,  0, "RIGHT"},
    { -1,  0, "LEFT" }
};

double d_grid[WIDTH][HEIGHT] = { };
short s_grid[WIDTH][HEIGHT] = { };

int amount_players = 0;
Loc players[4] = { };
int my_id = -1;

#define my_player           players[my_id]
#define print(d)            (printf("%s\n", d))

#define infield(x, y)       (x >= 0 && y >= 0 && x < WIDTH && y < HEIGHT)
#define s_value(x, y)       (infield(x, y) ? s_grid[x][y] : SHRT_MIN)
#define death(x, y)         (s_value(x, y) <= DEATH_MAX)
#define deathl(loc)         death(loc.x, loc.y)
#define deathd(dir)         death(my_player.x + dir.dx, my_player.y + dir.dy)

#define loc_eq(loc1, loc2)     (loc1.x == loc2.x && loc1.y == loc2.y)
#define loc_dist(loc1, loc2)   (abs(loc1.x - loc2.x) + abs(loc1.y - loc2.y))

//////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////// Debug

#define debug(...) fprintf(stderr, __VA_ARGS__);
char num_to_debug_char(short num) {
    if (num == SHRT_MIN) return '#';
    if (num < 0) return '-';
    if (num > 9) return '+';
    return num + '0';
}

void debug_grid() {
    char rowStr[WIDTH * 2 + 1] = { };
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            rowStr[x * 2] = ' ';
            rowStr[x * 2 + 1] = num_to_debug_char(s_grid[x][y]);
        }
        debug("%s\n", rowStr);
    }
    debug("We: (%d, %d), against %d\n", my_player.x, my_player.y, amount_players - 1);
    for (int i = 0; i < amount_players; i++) {
        if (i == my_id) continue;
        debug("{ %d: (%d, %d) } ", i, players[i].x, players[i].y);
    }
    debug("\n");
}

//////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////// Some helpful things

// Very basic bit map for square marking, int represents a row
u_int32_t sharedSquareMap[HEIGHT] = { };
#define munsetall() for (int y = 0; y < HEIGHT; y++) sharedSquareMap[y] = 0
#define mlookup(x, y)   ( sharedSquareMap[y] & (1 << x) )
#define mset(x, y)      ( sharedSquareMap[y] |= (1 << x) )
#define munset(x, y)    ( sharedSquareMap[y] &= ~(1 << x) )
#define mlookupl(loc)   mlookup(loc.x, loc.y)
#define munsetl(loc)    munset(loc.x, loc.y)
#define msetl(loc)      mset(loc.x, loc.y)

// Very basic pre allocated queue
#define sharedQueueSize (WIDTH * 3)
Loc sharedQueueData[sharedQueueSize];
typedef struct {
    Loc* data;
    int size;
    int w, r;
} Queue;
Queue sharedQueue = { sharedQueueData, sharedQueueSize };
void push(Queue* queue, Loc val) {
    queue->data[queue->w] = val;
    queue->w = (queue->w + 1) % queue->size;
}
Loc* pop(Queue* queue) {
    if (queue->r == queue->w) return NULL;
    Loc* r = queue->data + queue->r;
    queue->r = (queue->r + 1) % queue->size;
    return r;
}
int size(Queue* queue) {
    return (queue->w - queue->r + queue->size) % queue->size;
}
void clear(Queue* queue) {
    queue->w = queue->r;
}

//////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////// Basic functions

#define death_not_me(lx, ly)  (death(lx, ly) && (my_player.x != lx || my_player.y != ly))
#define alley_hor(x, y)       (death_not_me(x+1, y) && death_not_me(x-1, y))
#define alley_ver(x, y)       (death_not_me(x, y-1) && death_not_me(x, y+1))
#define alley(x, y)           (alley_ver(x, y) || alley_hor(x, y))
#define alleyl(loc)           alley(loc.x, loc.y)

Dir directionTo(Loc from, Loc to) {
    if (from.y > to.y) return directions[0]; // Up
    if (from.y < to.y) return directions[1]; // Down
    if (from.x < to.x) return directions[2]; // Right
    if (from.x > to.x) return directions[3]; // Left
    return no_direction;
}

int playerAt(Loc loc, bool count_me) {
    for (int i = 0; i < amount_players; i++) {
        if (!count_me && i == my_id) continue;
        if (loc_eq(players[i], loc)) return i;
    }
    return -1;
}

int flood_fill(Loc from, int* closestPlayer) {
    int totalalone = 0;
    clear(&sharedQueue);
    push(&sharedQueue, from);
    munsetall();
    if (!deathl(from)) {
        totalalone++;
        msetl(from);
    }
    while (size(&sharedQueue) > 0) {
        Loc* next = pop(&sharedQueue);
        for (int d = 0; d < 4; d++) {
            Dir try = directions[d];
            Loc l = { next->x + try.dx, next->y + try.dy };
            if (closestPlayer != NULL) {
                int player = playerAt(l, false);
                if (player >= 0) {
                    *closestPlayer = player;
                    closestPlayer = NULL;
                }
            }
            if (!deathl(l) && !mlookupl(l)) {
                msetl(l);
                push(&sharedQueue, l);
                totalalone++;
            }
        }
    }
    return totalalone;
}

//////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////// The heart and soul


Dir default_direction() {
    // Try to not go in alleys
    for (int d = 0; d < 4; d++) {
        Dir try = directions[d];
        Loc l = { my_player.x + try.dx, my_player.y + try.dy };
        if (deathl(l) || alleyl(l)) continue;
        return try;
    }
    // Fine we'll go in alleys
    for (int d = 0; d < 4; d++) {
        Dir try = directions[d];
        Loc l = { my_player.x + try.dx, my_player.y + try.dy };
        if (deathl(l)) continue;
        return try;
    }
    // If we get here we die anyway
    debug("Well, RIP us then...\n");
    return directions[0];
}

Dir check_splitsing() {
    bool isSplitsing = false;
    int options[4] = { };

    for (int d = 0; d < 4; d++) {
        Dir try = directions[d];
        Loc l = { my_player.x + try.dx, my_player.y + try.dy };
        if (deathl(l)) continue;
        options[d] = flood_fill(l, NULL);
    }


    int bestOption = 0;
    for (int i = 1; i < 4; i++) {
        if (options[bestOption] > 0 && options[i] > 0
            && options[bestOption] != options[i]) {
            isSplitsing = true; // 2+ with different value
        }
        if (options[i] > options[bestOption]) {
            bestOption = i;
        }
    }

    // debug(" %d, %d, %d, %d  ==> %d\n", options[0], options[1],
            // options[2], options[3], isSplitsing);
    if (isSplitsing) {
        return directions[bestOption];
    } else {
        return no_direction;
    }
}




//////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////// Main loop & basics

void clear_short_grid() {
     // Clear the grid (except death squares)
    for (int x = 0; x < WIDTH; x++) {
        for (int y = 0; y < HEIGHT; y++) {
            if (s_grid[x][y] > DEATH_MAX)
                s_grid[x][y] = 1;
        }
    }
}

void remove_player_ribbon(int p) {
    int REMOVE_DEATH = DEATH(p);
    for (int x = 0; x < WIDTH; x++) {
        for (int y = 0; y < HEIGHT; y++) {
            if (s_grid[x][y] == REMOVE_DEATH)
                s_grid[x][y] = 1;
        }
    }
}


int main() {
    int X0, Y0, pCurX, pCurY;
    while (1) {
        clear_short_grid();
        scanf("%d%d", &amount_players, &my_id);
        for (int i = 0; i < amount_players; i++) {
            scanf("%d%d%d%d", &X0, &Y0, &pCurX, &pCurY);
            if (players[i].x >= 0 && pCurX == -1) {
                remove_player_ribbon(i);
                continue;
            }
            players[i].x = (short) pCurX;
            players[i].y = (short) pCurY;
            s_grid[X0][Y0] = DEATH(i);
            s_grid[pCurX][pCurY] = DEATH(i);
        }
        // debug_grid();

        debug("Starting choice:\n")
        Dir d = check_splitsing();
        if (d.name != NULL) {
            debug(" -> Found this to be a splitsing: %s\n", d.name);
            print(d.name);
            continue;
        }

        int closestPlayer = -1;
        flood_fill(my_player, &closestPlayer);
        if (closestPlayer >= 0) {
            debug(" -> Found player %d to be closest\n", closestPlayer);
            Dir dir = directionTo(my_player, players[closestPlayer]);
            if (dir.name != NULL && !deathd(dir)) {
                print(dir.name);
                continue;
            }
        }

        debug(" -> No special choose, going default\n");
        d = default_direction();
        print(d.name);
    }
    return 0;
}
