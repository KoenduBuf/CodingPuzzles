#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>

//////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////// Structs & Vars

#define WIDTH    30
#define HEIGHT   20

#define DEATH         SHRT_MIN + 10
#define DEATH_VAL(p)  DEATH - p

typedef struct {
    short x, y;
} Loc;
typedef struct {
    short dx, dy;
    char* name;
} Dir;

Dir directions[] = {
    { 0, -1, "UP" },
    { 1, 0, "RIGHT"},
    { 0, 1, "DOWN" },
    { -1, 0, "LEFT" }
};

short grid[WIDTH][HEIGHT] = { };
int alive_players = 0;
Loc players[4] = { };

//////////////////////////////////////////////////////////////////////
////////////////// tiny C array queue imp, and cheeky bit square map

Loc queueData[WIDTH*3];
typedef struct {
    Loc* data;
    int size;
    int w, r;
} Queue;

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

u_int32_t squareMap[HEIGHT] = { }; // int represents a row
#define munsetall() for (int y = 0; y < HEIGHT; y++) squareMap[y] = 0 

#define mlookup(x, y) ( squareMap[y] & (1 << x) )
#define mset(x, y) ( squareMap[y] |= (1 << x) )
#define munset(x, y) ( squareMap[y] &= ~(1 << x) )

#define mlookupl(loc) mlookup(loc.x, loc.y)
#define msetl(loc) mset(loc.x, loc.y)
#define munsetl(loc) munset(loc.x, loc.y)

// #define mset_move(loc, dir) mset((loc.x + dir.dx), (loc.y + dir.dy))
// #define mlookup_move(loc, dir) mlookup((loc.x + dir.dx), (loc.y + dir.dy))
// #define munset_move(loc, dir) munset((loc.x + dir.dx), (loc.y + dir.dy))


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
            rowStr[x * 2 + 1] = num_to_debug_char(grid[x][y]);
        }
        debug("%s\n", rowStr);
    }
    debug("We: (%d, %d), against %d\n", players[0].x, players[0].y, alive_players - 1);
    for (int i = 1; i < alive_players; i++) {
        debug("{ %d: (%d, %d) } ", i, players[i].x, players[i].y);
    }
    debug("\n");
}

//////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////// General

#define infield(x, y) (x >= 0 && y >= 0 && x < WIDTH && y < HEIGHT)
#define val(x, y) (infield(x, y) ? grid[x][y] : SHRT_MIN)
#define death(x, y) (val(x, y) <= DEATH)
#define alley(x, y) ( (death(x+1, y) && death(x-1, y)) || (death(x, y-1) && death(x, y+1)) )
#define set_if_possible(x, y, val) if (infield(x, y) && !death(x, y)) grid[x][y] = val

#define death_loc(loc)        death(loc.x, loc.y)
#define death_move(loc, dir)  death(loc.x + dir.dx, loc.y + dir.dy)
#define val_loc(loc)          val(loc.x, loc.y)
#define val_move(loc, dir)    val(loc.x + dir.dx, loc.y + dir.dy)

int playerAt(Loc loc) {
    for (int i = 1; i < alive_players; i++) {
        if (players[i].x == loc.x && players[i].y == loc.y) return i;
    }
    return 0;
}

int spaceAlone(Loc loc) {
    int totalalone = 0;
    Queue queue = { queueData, WIDTH*2, 0, 0 };
    push(&queue, loc);
    munsetall();
    while (size(&queue) > 0) {
        Loc* next = pop(&queue);
        for (int d = 0; d < 4; d++) {
            Dir try = directions[d];
            Loc l = { next->x + try.dx, next->y + try.dy };
            if (playerAt(l)) return 0;
            if (!death_loc(l) && !mlookupl(l)) {
                msetl(l);
                push(&queue, l);
                totalalone++;
            }
        }
    }
    return totalalone;
}

int highest_award_move(Loc location, int moves) {
    if (moves == 0) return 0;
    if (death_loc(location)) return SHRT_MIN;

    int bestValue = SHRT_MIN;
    for (int d = 0; d < 4; d++) {
        Dir try = directions[d];
        Loc new_loc = { location.x + try.dx, location.y + try.dy };
        if (!death_loc(new_loc) && !mlookupl(new_loc)) {
            msetl(new_loc);
            int thisMove = highest_award_move(new_loc, moves - 1);
            if (thisMove > bestValue) bestValue = thisMove;
            munsetl(new_loc);
        }
    }
    return bestValue + val_loc(location);
}

Dir should_move_to_highest(Loc location, int moves) {
    int bestValue = SHRT_MIN;
    Dir bestDirection = {};
    munsetall();
    for (int d = 0; d < 4; d++) {
        Dir try = directions[d];
        Loc new_loc = { location.x + try.dx, location.y + try.dy };
        msetl(new_loc);
        int dirVal = highest_award_move(new_loc, moves - 1);
        munsetl(new_loc);
        if (dirVal > bestValue) {
            bestValue = dirVal;
            bestDirection = try;
        }
    }
    return bestDirection;
}

//////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////// Alone

void moveAlone() {

}

//////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////// Together

#define min(a, b)   (a < b ? a : b)
#define max(a, b)   (a > b ? a : b)
#define abs(x)      (x > 0 ? x : -x)

void moveTogether() {
    for (int i = 1; i < alive_players; i++) {
        for (int px = -5; px <= 5; px++) {
            for (int py = -5; py <= 5; py++) {

                set_if_possible(players[i].x - px, players[i].y - py, max(5 - abs(px), 5 - abs(py)));
            }
        }
    }
    Dir d = should_move_to_highest(players[0], 10);
    printf("%s\n", d.name);
}



//////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////// Main

int main() {
    // Setup some variables, P = your id
    int N, P, pStartX, pStartY, pCurX, pCurY;
    while (1) {
        // Clear the grid (except death squares)
        for (int x = 0; x < WIDTH; x++) {
            for (int y = 0; y < HEIGHT; y++) {
                if (grid[x][y] > DEATH)
                    grid[x][y] = 1;
            }
        }
        // Get the new information and store it
        alive_players = 1;
        scanf("%d%d", &N, &P);
        for (int i = 0; i < N; i++) {
            scanf("%d%d%d%d", &pStartX, &pStartY, &pCurX, &pCurY);
            if (pStartX == -1 && grid[pCurX][pCurY] == SHRT_MIN) {
                continue;
            }
            if (i == P) {
                players[0].x = (short) pCurX;
                players[0].y = (short) pCurY;
            } else {
                players[alive_players].x = (short) pCurX;
                players[alive_players].y = (short) pCurY;
                alive_players++;
            }
            grid[pCurX][pCurY] = SHRT_MIN;
        }
        // Play together or alone
        int alone = spaceAlone(players[0]);
        // if (alone == 0) {
            moveTogether();
        // } else {
            // moveAlone();
        // }
    }
    return 0;
}

