#include <iostream>
#include <stdlib.h>
#include <time.h>

#define SECRET_RADIX        10      // The amount of options for each digit (max 10)
#define MAX_NUM_LEN         10      // The max amount of digits we ever run with
#define FIRST_NOT_0         true    // If true, the first digit cannot be 0
#define UNIQUE_DIGITS       true    // If true, digits in the secret are unique
//#define DEBUG_MODE

/////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////// Some game settings and the predicate struct ////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////

class DOptionsTrie;

int NUM_LEN = -1;                   // Actual digits to guess (based on stdin)
typedef int8_t digit;               // Max radix is 10, so 1 byte is fine (need signed)
class Predicate {                   // A guess and its result
public:
    digit guessDigits[MAX_NUM_LEN];
    bool digitInGuess[SECRET_RADIX];
    u_int8_t exact, inThere;

    void queryGuess() {
        for (int i = 0; i < NUM_LEN; i++) {         // Print & Set
            digit d = this->guessDigits[i];
            if (d < 0 || d >= SECRET_RADIX) {
                std::cerr << "WTF, guessed a digit "
                    << (int)d << std::endl;
                exit(EXIT_FAILURE);
            }
            this->digitInGuess[d] = true;
            std::cout << ((int) d);
        }
        std::cout << std::endl;                     // Response
        // int exact, inThere;
        // std::cin >> exact >> inThere;
        // this->exact = exact;
        // this->inThere = inThere;
        scanf("%hhu%hhu", &this->exact, &this->inThere);
        if (this->exact == NUM_LEN) exit(EXIT_SUCCESS);
#ifdef DEBUG_MODE
        std::cerr << "Queried: [ G: ";               // Debug
        for (int i=0; i<NUM_LEN; i++)
            std::cerr << this->guessDigits[i];
        std::cerr << " -> exact: " << this->exact;
        std::cerr << ", inThere: " << this->inThere;
        std::cerr << " ]" << std::endl;
#endif
    }

    static Predicate *random(DOptionsTrie *tree);
};

extern DOptionsTrie NO_OPTS_LEAF;

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
class DOptionsTrie {
private:
    void expandTemplate(int toDepth) {
        if (toDepth == 1) return;
        if (toDepth <= 0) {
            std::cerr << "Cannot extend a template tree to depth < 1" << std::endl;
            exit(EXIT_FAILURE);
        }

        DOptionsTrie *lowerTree = new DOptionsTrie(this);
        lowerTree->expandTemplate(toDepth - 1);

        for (int d = 0; d < SECRET_RADIX; d++) {
            // If some place in the template tree is NULL, leave it
            if (this->options[d] == NULL) continue;
            // If some place in the template tree is NO_OPTS_LEAF, extend it
            if (this->options[d] != &NO_OPTS_LEAF) {
                std::cerr << "Template contained things" << std::endl;
                exit(EXIT_FAILURE);
            }
            this->setOption(d, lowerTree);
        }
    }

    void initAsFullUniqueTree() {
        /**
         * This genius level function creates a DOptionsTrie that contains
         * all unique combinations of digits, now you would think 'but wait,
         * that would mean a huge amount of trees!' and you would be right if
         * we did not reuse trees (i.e. tree with 0 and 1 crossed out is the
         * same one as 1 and 0 crossed out). 'But then how did you do that so
         * efficiently?' the answer to that is simple: binary is super cool.
         */
        const u_int32_t needTrees = (1 << SECRET_RADIX);
        DOptionsTrie *cache[needTrees];
        // First we create all the trees that we need
        // the 0th has all options open, 1 won't have 0, etc
        cache[0] = this;
        for (u_int32_t bitmask = 1; bitmask < needTrees; bitmask++) {
            // we dont need trees that are more than MAX_NUM_LEN-1 deep
            // thus trees with more than MAX_NUM_LEN-1 bits to 1
            // We use black magic to get the amount of set bits
            // Completely from (https://stackoverflow.com/questions/109023/)
            u_int32_t setbits = bitmask - ((bitmask >> 1) & 0x55555555);
            setbits = (setbits & 0x33333333) + ((setbits >> 2) & 0x33333333);
            setbits = (((setbits + (setbits >> 4)) & 0x0F0F0F0F) * 0x01010101) >> 24;
            if (((int) setbits) >= NUM_LEN) {
                cache[bitmask] = &NO_OPTS_LEAF;
                continue;
            }
            cache[bitmask] = new DOptionsTrie();
        }

        // 0 should point to 0 + [ 1 2 4 8 16 ... ]
        // 1 should point to 1 + [ x 2 4 8 16 ... ]
        // 2 should point to 2 + [ 1 x 4 8 16 ... ]
        // 3 should point to 3 + [ x x 4 8 16 ... ] etc.
        for (int32_t tree = needTrees-1; tree >= 0; tree--) {
            if (cache[tree] == &NO_OPTS_LEAF) continue;
            for (int d = 0; d < SECRET_RADIX; d++) {
                cache[tree]->setOption(d, ((tree >> d) & 1)
                    ? NULL : cache[tree + (1 << d)]);
            }
        }
    }

    void initAsTreeWithoutDigits(digit* digits, int ndigits, int depth) {
        // Creates a tree containing all options except the ones in 'digits'
        for (int d = 0; d < SECRET_RADIX; d++) {
            // If 'd' in the 'without' digits, then continue
            for (int dd = 0; dd < ndigits; dd++)
                if (d == digits[dd]) goto is_in_digits;
            // If 'd' not in those digits, it should be in the tree
            this->setOption(d, &NO_OPTS_LEAF);
            is_in_digits:;
        }
        this->expandTemplate(depth);
    }

public:
    DOptionsTrie *options[SECRET_RADIX];
    int64_t referencedBy; bool leaf;

    // Firstly, constructors

    DOptionsTrie(bool firstNot0, bool uniqueDigits) {
        // Create either a unique or a full tree
        if (uniqueDigits) initAsFullUniqueTree();
        else initAsTreeWithoutDigits(NULL, 0, NUM_LEN);
        // If needed, remove options starting with 0.
        if (firstNot0) this->setOption(0, NULL);
    }

    DOptionsTrie(DOptionsTrie *copyFrom) {
        if (copyFrom == &NO_OPTS_LEAF) {
            std::cerr << "Someone trying to copy NO_OPTS_LEAF" << std::endl;
            exit(EXIT_FAILURE);
        }
        // Copy and update some references, no need to -1 on this
        this->referencedBy = 0;
        this->leaf = copyFrom->leaf;
        for (int i = 0; i < SECRET_RADIX; i++) {
            this->options[i] = copyFrom->options[i];
            if (this->options[i] == NULL) continue;
            this->options[i]->referencedBy++;
        }
    }

    DOptionsTrie() : options { 0 } {
        this->referencedBy = 0;
        this->leaf = 0;
    }

    // Just some things for debugging

    int optionCount() {
        int total = 0;
        for (int d = 0; d < SECRET_RADIX; d++) {
            if (this->options[d] == NULL) continue;
            if (this->options[d]->leaf) total += 1;
            total += this->options[d]->optionCount();
        }
        return total;
    }

    void debugPrint(int depth, int tabbed) {
        // Tab in and print the header of the thing
        for (int i=0;i<tabbed;i++) std::cerr << ' ';
        std::cerr << "DOT[" << this->optionCount() << "](";
        if (depth != 0) std::cerr << std::endl;

        for (int d = 0; d < SECRET_RADIX; d++) {
            // Check what we should display
            char toDisplay = '\0';
            if (this->options[d] == NULL) toDisplay = '.';
            else if (this->options[d]->leaf) toDisplay = 'O';
            else if (depth == 0) toDisplay = 't';
            // Display a letter or a subtree
            if (toDisplay == '\0') {
                this->options[d]->debugPrint(depth-1, tabbed+4);
            } else {
                if (depth != 0) {
                    for (int i=0;i<tabbed+4;i++) std::cerr << ' ';
                }
                std::cerr << toDisplay;
            }
            // Add nice spacing of things:
            if (d != SECRET_RADIX-1) {
                std::cerr << ',';
                if (depth != 0) std::cerr << std::endl;
            }
        }
        for (int i=0;i<tabbed;i++) std::cerr << ' ';
        std::cerr << ')';
    }

    // Things to keep track of references and memory stuff

    void freeTree() {
        if (--(this->referencedBy) > 0) return;
        if (this == &NO_OPTS_LEAF) {
            std::cerr << "ReferencedBy flaw, free on NO_OPTS_LEAF" << std::endl;
            exit(EXIT_FAILURE);
        }
        for (int i = 0; i < SECRET_RADIX; i++)
            if (this->options[i] != NULL) this->options[i]->freeTree();
        delete this;
    }

    void setOption(digit d, DOptionsTrie *newv) {
        if (newv != NULL) newv->referencedBy++;
        if (this->options[d] != NULL)
            this->options[d]->freeTree();
        this->options[d] = newv;
    }

    DOptionsTrie *decouple(digit d) {
        // If you are going to edit your child, then use this
        // this decouples your child and returns it, it is your
        // responsibility to put it back later! Failing to do this
        // will lead to a memory leak...
        // If you don't want to put it back, call freeOptionsTree
        // You can even think of this method as a .->setOption(., NULL)
        // but then without the 'freeOptionsTree' call
        DOptionsTrie *child = this->options[d];
        this->options[d] = NULL;
        return child;
    }

    DOptionsTrie *copyIfUsed() {
        if (this->referencedBy < 0) {
            std::cerr << "Copy on referencedBy < 0" << std::endl;
            exit(EXIT_FAILURE);
        }
        return (this->referencedBy < 2) ? this : new DOptionsTrie(this);
    }

};

DOptionsTrie NO_OPTS_LEAF;

// The star of this program: pruning the tree

DOptionsTrie *pruneOptions(DOptionsTrie *options, Predicate *predicate, int at);
DOptionsTrie *pruneForDigit(DOptionsTrie *options, Predicate *predicate, int at, int optionDigit) {
    if (predicate->guessDigits[at] == optionDigit) {     // For the exact right digit:
        if (predicate->exact == 0) {
            // If nothing in here is exact, remove exact right options
            options = options->copyIfUsed();
            options->setOption(optionDigit, NULL);
        } else {
            // If something is exact, then leave this one, but recurse
            // 'but we don't know if it is exact!'
            // don't worry, we only apply it for this option
            predicate->exact--;
            DOptionsTrie *was = options->options[optionDigit];
            DOptionsTrie *p = pruneOptions(was, predicate, at+1);
            if (p != was) {
                options = options->copyIfUsed();
                options->setOption(optionDigit, p);
            }
            predicate->exact++;
        }
    } else if (predicate->digitInGuess[optionDigit]) { // If digit is in there somewhere
        if (predicate->inThere == 0) {
            // If this digit is in there, but inThere is 0, this is not an option
            options = options->copyIfUsed();
            options->setOption(optionDigit, NULL);
        } else {
            // If this digit is in there, and it actually can be, recurse
            predicate->inThere--;
            DOptionsTrie *was = options->options[optionDigit];
            DOptionsTrie *p = pruneOptions(was, predicate, at+1);
            if (p != was) {
                options = options->copyIfUsed();
                options->setOption(optionDigit, p);
            }
            predicate->inThere++;
        }
    } else { // If this digit is not in our predicate anywhere...
        if (predicate->inThere + predicate->exact == NUM_LEN - at) {
            // If this digit is not in there, but we have inThere == NUM_LEN ...
            options = options->copyIfUsed();
            options->setOption(optionDigit, NULL);
        }  else {
            // If it could be that this digit is wrong, pretend it is,
            // which means it can still be 'optionDigit', so recurse
            DOptionsTrie *was = options->options[optionDigit];
            DOptionsTrie *p = pruneOptions(was, predicate, at+1);
            if (p != was) {
                options = options->copyIfUsed();
                options->setOption(optionDigit, p);
            }
        }
    }
    return options;
}

DOptionsTrie *pruneOptions(DOptionsTrie *options, Predicate *predicate, int at) {
    if (at >= NUM_LEN) return options;
    if (options == &NO_OPTS_LEAF) {
        std::cerr << "Pruning NO_OPTS_LEAF, at: " << at << std::endl;
        exit(EXIT_FAILURE);
    }
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


Predicate* Predicate::random(DOptionsTrie *tree) {
    // Just follows the tree to create a random but possible guess
    Predicate *pred = new Predicate();
    DOptionsTrie *atTree = tree;
    for (int di = 0; di < NUM_LEN; di++) {
#ifdef DEBUG_MODE
        std::cerr << "Choosing from: ";
        atTree->debugPrint(0, 0);
#endif
        // Create a random digit for this guess
        int total = 0, i, c;
        for (i = 0; i < SECRET_RADIX; i++)
            if (atTree->options[i] != NULL) total++;
        if (total == 0) {
            std::cerr << "Sorry, this is impossible" << std::endl;
            exit(EXIT_FAILURE);
        }
        for (i = 0, c = (rand() % total); c >= 0; i++)
            if (atTree->options[i] != NULL) c--;
        digit digit = i - 1;
#ifdef DEBUG_MODE
        std::cerr << " --> Chose " << ((int)digit) << std::endl;
#endif
        // Add this digit to our guess
        pred->guessDigits[di] = digit;
        atTree = atTree->options[digit];
    }
    pred->queryGuess();
    return pred;
}

int main() {
    srand(time(NULL));          // Set the random generator
    NO_OPTS_LEAF.referencedBy = 1;
    NO_OPTS_LEAF.leaf = true;

    std::cin >> NUM_LEN;        // Scan single int number length
    DOptionsTrie *options = new DOptionsTrie(FIRST_NOT_0, UNIQUE_DIGITS);
    scanf("%*d%*d");            // Discard some things when reading in

    while (true) {
#ifdef DEBUG_MODE
        // Print some debug stuffs
        std::cerr << "Main loop!" << std::endl;
        options->debugPrint(1, 0);
        std::cerr << std::endl;
#endif
        // Do a guess, and see what is still possible
        Predicate *pred = Predicate::random(options);
        options = pruneOptions(options, pred, 0);
    }
    return 0;
}
