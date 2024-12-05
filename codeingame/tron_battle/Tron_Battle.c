#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>

//////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////// Structs & Vars

#define WIDTH    30
#define HEIGHT   20

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
#define mlookup(x, y) ( squareMap[y] & (1 << x) )
#define mlookupl(loc) mlookup(loc.x, loc.y)
#define mset(x, y) ( squareMap[y] |= (1 << x) )
#define msetl(loc) mset(loc.x, loc.y)
#define munsetall() for (int y = 0; y < HEIGHT; y++) squareMap[y] = 0 

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
#define death(x, y) (val(x, y) == SHRT_MIN)
#define alley(x, y) ( (death(x+1, y) && death(x-1, y)) || (death(x, y-1) && death(x, y+1)) )
#define death_loc(loc) death(loc.x, loc.y)
#define val_move(loc, dir) val(loc.x + dir.dx, loc.y + dir.dy)

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

Dir highest_award_move(int moves) {
    Loc playLoc = { players[0].x, players[0].y };
    

    for (int d = 0; d < 4; d++) {
        Dir try = directions[d];
        if (val_move(playLoc, try) > 0) {
            
        }
    }
}



//////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////// Alone

void moveAlone() {

}

//////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////// Together

void moveTogether() {
    for (int i = 1; i < alive_players; i++) {
        
    }
    printf("LEFT\n"); // A single line with UP, DOWN, LEFT or RIGHT
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
                if (grid[x][y] != SHRT_MIN)
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
        debug("%d\n", alone);
        // if (alone == 0) {
            moveTogether();
        // } else {
            // moveAlone();
        // }
    }
    return 0;
}


// Quick maths
// 1 turn can have 256 possible moves
// a state can be represented in 4*20 byes +some = 100 ish bytes
// 1) 256 KB
// 2) 65 MB
// 3) 16 GB xd
// a game can be at most 30 * 20 / 2 = 300 turns
// 
