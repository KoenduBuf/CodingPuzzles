#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>

/////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////// Debugging stuffs ///////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////

#define debug(d...)     fprintf(stderr, d)
#define fatal(d...)     { debug("\nFATAL: "); debug(d); debug("\n"); exit(1); }
#define DEBUG_MODE

/////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////// Some game settings and the predicate struct ////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////

#define SECRET_RADIX        10      // The amount of options for each digit (max 10)
#define MAX_NUM_LEN         10      // The max amount of digits we ever run with

int NUM_LEN = 0; // Actual digits to guess (based on stdin)
int AT_TURN = 0; // Current turn in the game

typedef int8_t digit;               // Max radix is 10, so 1 byte is fine (need signed)
typedef struct {                    // A guess and its result
    digit guessDigits[MAX_NUM_LEN];
    u_int8_t digitInGuess[SECRET_RADIX];
    u_int8_t exact, inThere;
} Predicate;

/////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////// Knowledge base implementation and helpers /////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////

/* This tree structure will represent all options that are still possible
 * One of these structs will represent the options of every digit at one location.
 * The options for that digit still are represented in the 'options' array.
 *  - When the pointer at location D in the array is NULL, then the digit D is not possible.
 *  - When the pointer points to another of these structs, then this digit is possible
 *    but only with the next digits that are represented in the referenced struct.
 *  - For memory efficiency, we reuse trees, this is what the referencedBy counter is for,
 *    it is however forbidden to create a cycle, it should still be a tree, this means
 *    that trees can mostly (if not only) be reused at the same tree depth.
 */
#define CACHE_INDEX(ex, in) ( (((ex) - (MAX_NUM_LEN * 2 + 3)) * (ex) / -2) + (in))
typedef struct dot {
    struct dot *options[SECRET_RADIX];
    int64_t referencedBy; bool leaf;
    // What if we could cache the prune results? MAX_NUM_LEN options for exact and inThere
    // Thinking of it as a triangular matrix: len(row) = 11 - row,
    // start should be '0 11 21 30 38' start(0) = 0, start(1) = start(0) + (12 - 1)
    // start(n) = start(n-1) + (12 - n), thus start(n) = -1/2 (n - 23) n
    struct dot *pruneCache[CACHE_INDEX(MAX_NUM_LEN+1, 0)];
    u_int8_t pruneCacheInputTurn[CACHE_INDEX(MAX_NUM_LEN+1, 0)];
} DOptionsTree;

// A node used at the end of trees as the leaf
DOptionsTree NO_OPTS_LEAF = { .leaf = true,
    .options = { 0 }, .referencedBy = 1,
    .pruneCacheInputTurn = { 0 }
};

int getOptionCount(DOptionsTree *tree) {
    if (tree == NULL) return 0;
    int total = 0;
    for (int d = 0; d < SECRET_RADIX; d++) {
        if (tree->options[d] == NULL) continue;
        if (tree->options[d]->leaf) total += 1;
        total += getOptionCount(tree->options[d]);
    }
    return total;
}

void printOptionsTree(DOptionsTree *tree, int depth, int tabbed) {
    if (debug("%*s", tabbed, "") < 0) return;
    debug("DOT[%d](", getOptionCount(tree));
    if (depth != 0) debug("\n");
    if (tree == NULL) {
        debug(" NULL )");
        return;
    }
    for (int d = 0; d < SECRET_RADIX; d++) {
        // Check what we should display
        char toDisplay = '\0';
        if (tree->options[d] == NULL) toDisplay = '.';
        else if (tree->options[d]->leaf) toDisplay = 'O';
        else if (depth == 0) toDisplay = 't';
        // Display a letter or a subtree
        if (toDisplay != '\0') {
            if (depth != 0) debug("%*s", tabbed+4, "");
            debug("%c", toDisplay);
        } else printOptionsTree(tree->options[d],
            depth - 1, tabbed + 4);
        // Add nice spacing of things:
        if (d != SECRET_RADIX-1) {
            debug(depth == 0 ? "," : ",\n");
        }
    }
    if (depth != 0) debug("\n%*s", tabbed, "");
    debug(")");
}

void freeOptionsTree(DOptionsTree *toFree) {
    if (toFree == NULL) return;
    if (--(toFree->referencedBy) > 0) return;
    if (toFree == &NO_OPTS_LEAF) //return;
        fatal("ReferencedBy flaw, tried to free NO_OPTS_LEAF");
    for (int i = 0; i < SECRET_RADIX; i++)
        freeOptionsTree(toFree->options[i]);
    free(toFree);
}

void setDOpts(DOptionsTree *parent, digit d, DOptionsTree *newv) {
    if (newv != NULL) newv->referencedBy++;
    freeOptionsTree(parent->options[d]);
    parent->options[d] = newv;
}

DOptionsTree *decouple(DOptionsTree *parent, digit d) {
    // If you are going to edit your child, then use this
    // this decouples your child and returns it, it is your
    // responsibility to put it back later! Failing to do this
    // will lead to a memory leak...
    // If you don't want to put it back, call freeOptionsTree
    // You can even think of this method as a setDOpts(., ., NULL)
    // but then without the 'freeOptionsTree' call
    DOptionsTree *child = parent->options[d];
    parent->options[d] = NULL;
    return child;
}

DOptionsTree *copyNode(DOptionsTree *tree) {
    if (tree == &NO_OPTS_LEAF) fatal("Someone trying to copy NO_OPTS_LEAF...");
    // Copy and update some references, no need to -1 on tree
    DOptionsTree *newtree = malloc(sizeof(DOptionsTree));
    memcpy(newtree, tree, sizeof(DOptionsTree));
    // memset(newtree->pruneCache, 0, sizeof(newtree->pruneCacheInputTurn));
    for (int i = 0; i < SECRET_RADIX; i++) {
        if (newtree->options[i] == NULL) continue;
        newtree->options[i]->referencedBy++;
    }
    return newtree;
}

DOptionsTree *copyIfUsed(DOptionsTree *tree) {
    if (tree == &NO_OPTS_LEAF) fatal("Copy on NO_OPTS_LEAF...");
    if (tree->referencedBy < 0) fatal("Copy on referencedBy < 0");
    return (tree->referencedBy < 2) ? tree : copyNode(tree);
}

/////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////// Easy functions for creating and changing trees //////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////

/**
 * The first main function for handling complicated options manipulation.
 * This function adds the options of some tree to another tree, basically
 * creating the union or the intersection of 2 trees (based on the boolean
 * "intersection") complexity: as fast as all nodes in the smallest tree.
 */
DOptionsTree *mergeOptionTrees(DOptionsTree *toTree, DOptionsTree *other,
    bool intersection) {
    if (toTree == NULL || other == NULL) fatal("Intersection but trees were NULL");

    int childrenNotNull = 0;
    for (int i = 0; i < SECRET_RADIX; i++) {
        // What to do if 1 side has nothing
        if (toTree->options[i] == NULL) {
            if (intersection || other->options[i] == NULL) continue;
            toTree = copyIfUsed(toTree); // If union: add from other tree
            setDOpts(toTree, i, other->options[i]);
            childrenNotNull += 1;
            continue;
        }
        if (other->options[i] == NULL) {
            if (!intersection) continue;
            toTree = copyIfUsed(toTree); // If intersection: set to null
            setDOpts(toTree, i, NULL);
            continue;
        }
        // If both have actual information, merge those!
        toTree = copyIfUsed(toTree);
        DOptionsTree *childi = decouple(toTree, i);
        DOptionsTree *merged = mergeOptionTrees(childi,
            other->options[i], intersection);
        if (merged != childi) freeOptionsTree(childi);
        if (merged != NULL) childrenNotNull += 1;
        setDOpts(toTree, i, merged);
    }

    if (childrenNotNull == 0) return NULL;
    return toTree;
}

/**
 * This genius level function creates a DOptionsTree that contains
 * all unique combinations of digits, now you would think 'but wait,
 * that would mean a huge amount of trees!' and you would be right if
 * we did not reuse trees (i.e. tree with 0 and 1 crossed out is the
 * same one as 1 and 0 crossed out). 'But then how did you do that so
 * efficiently?' the answer to that is simple: binary is super cool.
 */
DOptionsTree *fullUniqueTree() {
    const u_int32_t needTrees = (1 << SECRET_RADIX);
    DOptionsTree **cache = malloc(needTrees * sizeof(DOptionsTree *));
    // First we create all the trees that we need
    // the 0th has all options open, 1 won't have 0, etc
    for (u_int32_t bitmask = 0; bitmask < needTrees; bitmask++) {
        // we dont need trees that are more than MAX_NUM_LEN-1 deep
        // thus trees with more than MAX_NUM_LEN-1 bits to 1
        // We use black magic to get the amount of set bits
        // Completely from (https://stackoverflow.com/questions/109023/)
        u_int32_t setbits = bitmask - ((bitmask >> 1) & 0x55555555);
        setbits = (setbits & 0x33333333) + ((setbits >> 2) & 0x33333333);
        setbits = (((setbits + (setbits >> 4)) & 0x0F0F0F0F) * 0x01010101) >> 24;
        if (setbits >= NUM_LEN) {
            cache[bitmask] = &NO_OPTS_LEAF;
            continue;
        }
        cache[bitmask] = calloc(1, sizeof(DOptionsTree));
    }
    // 0 should point to 0 + [ 1 2 4 8 16 ... ]
    // 1 should point to 1 + [ x 2 4 8 16 ... ]
    // 2 should point to 2 + [ 1 x 4 8 16 ... ]
    // 3 should point to 3 + [ x x 4 8 16 ... ] etc.
    for (int32_t tree = needTrees-1; tree >= 0; tree--) {
        if (cache[tree] == &NO_OPTS_LEAF) continue;
        for (int d = 0; d < SECRET_RADIX; d++) {
            setDOpts(cache[tree], d, ((tree >> d) & 1)
                ? NULL : cache[tree + (1 << d)]);
        }
    }
    DOptionsTree *finaltree = cache[0];
    free(cache);
    return finaltree;
}

DOptionsTree *extendTemplateTree(DOptionsTree *templateTree, int depth) {
    if (depth <= 0) fatal("Cannot extend a template tree to depth < 1");
    if (depth == 1) return templateTree;

    DOptionsTree *lowerTree = extendTemplateTree(templateTree, depth-1);
    templateTree = copyNode(templateTree);

    for (int d = 0; d < SECRET_RADIX; d++) {
        // If some place in the template tree is NULL, leave it
        if (templateTree->options[d] == NULL) continue;
        // If some place in the template tree is NO_OPTS_LEAF, extend it
        if (templateTree->options[d] != &NO_OPTS_LEAF)
            fatal("Template contained things...");
        setDOpts(templateTree, d, lowerTree);
    }
    return templateTree;
}

DOptionsTree *treeWithoutDigits(digit* digits, int ndigits, int depth) {
    DOptionsTree *tree = calloc(1, sizeof(DOptionsTree));
    for (int d = 0; d < SECRET_RADIX; d++) {
        // If 'd' in the 'without' digits, then continue
        for (int dd = 0; dd < ndigits; dd++)
            if (d == digits[dd]) goto is_in_digits;
        // If 'd' not in those digits, it should be in the tree
        setDOpts(tree, d, &NO_OPTS_LEAF);
        is_in_digits:;
    }
    return extendTemplateTree(tree, depth);;
}

DOptionsTree *baseOptionsTree(bool firstNot0, bool uniqueDigits) {
    DOptionsTree *tree;
    // Create either a unique or a full tree
    if (uniqueDigits) tree = fullUniqueTree();
    else tree = treeWithoutDigits(NULL, 0, NUM_LEN);
    // If needed, remove options starting with 0.
    if (firstNot0) setDOpts(tree, 0, NULL);
    return tree;
}

/////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////// Calculating possible options and such ///////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////

DOptionsTree *pruneOptions(DOptionsTree *options, Predicate predicate, int at);
DOptionsTree *pruneOptionsAndSet(DOptionsTree *parent, int d, Predicate predicate, int at) {
    DOptionsTree *was = parent->options[d], *new = NULL;

    // If we have the solution in the cache, use it
    int cacheIndex = CACHE_INDEX(predicate.exact, predicate.inThere);
    if (was->pruneCacheInputTurn[cacheIndex] == AT_TURN) {
        new = was->pruneCache[cacheIndex];
    } else {
        new = pruneOptions(was, predicate, at+1);
        // We just computed it, store the result in the cache for later
        was->pruneCache[cacheIndex] = new;
        was->pruneCacheInputTurn[cacheIndex] = AT_TURN;
    }

    // Finally, set the thing if needed
    if (new != was) {
        parent = copyIfUsed(parent);
        setDOpts(parent, d, new);
    }
    return parent;
}

DOptionsTree *pruneForDigit(DOptionsTree *options, Predicate predicate, int at, int optionDigit) {
    if (predicate.guessDigits[at] == optionDigit) {     // For the exact right digit:
        if (predicate.exact == 0) {
            // If nothing in here is exact, remove exact right options
            options = copyIfUsed(options);
            setDOpts(options, optionDigit, NULL);
        } else {
            // If something is exact, then leave this one, but recurse 'but we
            // don't know if it is exact!' don't worry, we only apply it for this option
            predicate.exact--;
            options = pruneOptionsAndSet(options, optionDigit, predicate, at);
            predicate.exact++;
        }
    } else if (predicate.digitInGuess[optionDigit] > 0) { // If digit is in there somewhere
        if (predicate.inThere == 0) {
            // If this digit is in there, but inThere is 0, this is not an option (because unique)
            options = copyIfUsed(options);
            setDOpts(options, optionDigit, NULL);
        } else {
            // If this digit is in there, and it actually can be, recurse
            predicate.inThere--;
            predicate.digitInGuess[optionDigit]--;
            options = pruneOptionsAndSet(options, optionDigit, predicate, at);
            predicate.digitInGuess[optionDigit]++;
            predicate.inThere++;
        }
    } else { // If this digit is not in our predicate anywhere...
        if (predicate.inThere + predicate.exact == NUM_LEN - at) {
            // If this digit is not in there, but we have inThere == NUM_LEN ...
            options = copyIfUsed(options);
            setDOpts(options, optionDigit, NULL);
        }  else {
            // If it could be that this digit is wrong, pretend it is,
            // which means it can still be 'optionDigit', so recurse
            options = pruneOptionsAndSet(options, optionDigit, predicate, at);
        }
    }
    return options;
}

DOptionsTree *pruneOptions(DOptionsTree *options, Predicate predicate, int at) {
    if (at >= NUM_LEN) return options;
    if (options == &NO_OPTS_LEAF) fatal("Pruning NO_OPTS_LEAF, at: %d\n", at);
    int childrenNotNull = 0;

    // For each digit option
    for (int optionDigit = 0; optionDigit < SECRET_RADIX; optionDigit++) {
        if (options->options[optionDigit] == NULL) continue;
        // Now the question is: is digit 'optionDigit' possible?
        options = pruneForDigit(options, predicate, at, optionDigit);
        if (options->options[optionDigit] != NULL)
            childrenNotNull += 1;
    }

    if (childrenNotNull == 0) return NULL;
    return options;
}

/////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////// Creating guesses and the main loop ////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////

void queryGuess(Predicate *p) {
    for (int i = 0; i < NUM_LEN; i++) {         // Print & Set
        if (p->guessDigits[i] < 0 || p->guessDigits[i] >= SECRET_RADIX)
            debug("WTF, guessed a digit %d\n", p->guessDigits[i]);
        printf("%d", p->guessDigits[i]);
        p->digitInGuess[p->guessDigits[i]] += 1;
    }
    printf("\n");
    fflush(stdout);                             // Response
    int r = scanf("%hhu%hhu", &p->exact, &p->inThere);
    if (r != 2) exit(EXIT_FAILURE);
    if (p->exact == NUM_LEN) exit(EXIT_SUCCESS);
#ifdef DEBUG_MODE
    debug("Queried: [ G: ");                    // Debug
    for (int i = 0; i < NUM_LEN; i++) debug("%d", p->guessDigits[i]);
    debug(" -> exact: %d, inThere: %d ]\n", p->exact, p->inThere);
#endif
}

Predicate randomGuess(DOptionsTree *tree) {
    DOptionsTree *atTree = tree;
    Predicate toGuess = { 0 };
    for (int di = 0; di < NUM_LEN; di++) {
#ifdef DEBUG_MODE
        debug("Choosing from: ");
        printOptionsTree(atTree, 0, 0);
#endif
        int total = 0, i, c;
        for (i = 0; i < SECRET_RADIX; i++)
            if (atTree->options[i] != NULL) total++;
        if (total == 0) fatal("Sorry, this is impossible...\n");
        for (i = 0, c = (0); c >= 0; i++) // rand() % total
            if (atTree->options[i] != NULL) c--;
        digit digit = i - 1;
#ifdef DEBUG_MODE
        debug(" --> Chose %d\n", digit);
#endif
        toGuess.guessDigits[di] = digit;
        atTree = atTree->options[digit];
    }
    queryGuess(&toGuess);
    return toGuess;
}

int main() {
    time_t tim; // Init random for guesses
    srand((unsigned) time(&tim));

    scanf("%d", &NUM_LEN);  // Scan single int number length
    DOptionsTree *options = baseOptionsTree(true, true);
    scanf("%*d%*d");        // Scan first inputs before guess

    for (AT_TURN = 1;;AT_TURN++) {
#ifdef DEBUG_MODE
        // Print some debug stuffs
        debug("Main loop!\n");
        printOptionsTree(options, 1, 0);
        debug("\n");
#endif
        // Do a guess, and see what is still possible
        Predicate pred = randomGuess(options);
        options = pruneOptions(options, pred, 0);
    }
    return 0;
}
