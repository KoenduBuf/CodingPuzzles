#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

/////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////// Most basic macros and structs ///////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////

int NUM_LEN = -1;                               // Actual digits to guess
#define debug(d...)     fprintf(stderr, d);     // Debug print something
#define debugNl(n, l)   for (int d=0; d<l; d++) debug("%d",n[d]);
#define debugN(d)       debugNl(d, NUM_LEN);

typedef int8_t digit;

typedef struct {
    digit nums[10];
} Digits;

typedef struct {
    Digits guess;
    u_int8_t exact, inThere;
} Predicate;

/////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////// Integer set implementation and helpers //////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////

typedef struct {
    u_int16_t data;
    int8_t size;
} IntSet;

#define FULL_SET(until)         { .data=(1<<(until+1))-1, .size=until }
#define setInt(set, d)          { set.data |= (1 << d); set.size++; }
#define unsetInt(set, d)        { set.data ^= (1 << d); set.size--; }
#define add(set, d)             if (!contains(set, d)) setInt(set, d);
#define remove(set, d)          if (contains(set, d)) unsetInt(set, d);
#define setOnly(set, d)         { set.data = (1 << d); set.size = 1; }
#define contains(set, d)        (((set.data >> d) & 1) == 1)
#define debugSet(set)           for (int d=0; d<10; d++) if (contains(set, d)) debug("%d",d);

IntSet FULL_SET_10 = FULL_SET(10);

IntSet intSetOf(Digits digits) {
    IntSet result = { };
    for (int i = 0; i < NUM_LEN; i++) {
        add(result, digits.nums[i]);
    }
    return result;
}

IntSet subtractSet(IntSet set, IntSet set2) {
    IntSet result = set;
    for (digit i = 0; i < 10; i++) {
        if (!contains(set2, i)) continue;
        remove(result, i);
    }
    return result;
}

int getAny(IntSet fromSet) {
    for (digit i = 9; i >= 0; i--)
        if (contains(fromSet, i)) return i;
    return -1;
}

/////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////// Knowledge base implementation and helpers /////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////

typedef struct {
    IntSet numsNotInThere;      // This will contain digit X if X is not in the final digits.
    IntSet numsInThere;         // This will contain digit X if X is definitely in the final digits.
    IntSet locCanBe[10];        // This will say for every location which digits it can still be.
    Predicate predicates[100];  // All the predicates that have been returned from query so far.
    int predicatesSize;         // The amount of predicates that have been returned from query so far.
} Knowledge;

#define mPredicatesSize     knowledge->predicatesSize
#define savePredicate(p)    knowledge->predicates[mPredicatesSize++] = p;
#define getPredicate(p)     knowledge->predicates[p < 0 ? mPredicatesSize-p : p]

void updateLocationHasToBe(Knowledge *knowledge, int location, digit d) {
    add(knowledge->numsInThere, d);
    setOnly(knowledge->locCanBe[location], d);
    for (int loc = 0; loc < NUM_LEN; loc++) {
        if (loc == location) continue;
        remove(knowledge->locCanBe[loc], d);
    }
}

void updateLocationCannotBe(Knowledge *knowledge, int location, digit d) {
    remove(knowledge->locCanBe[location], d);
    if (knowledge->locCanBe[location].size == 1) {
        updateLocationHasToBe(knowledge, location,
            getAny(knowledge->locCanBe[location]));
    }
}

void updateDigitInThere(Knowledge *knowledge, digit d);
void updateDigitNotInThere(Knowledge *knowledge, digit d);
void updateDigitInThere(Knowledge *knowledge, digit d) {
    add(knowledge->numsInThere, d);

    // If we know a digit has to be in there, and it can only be in 1 spot, it has to go there!
    int locThatCanBeThisDigit = -1;
    for (int loc = 0; loc < NUM_LEN; loc++) {
        if (!contains(knowledge->locCanBe[loc], d)) continue;
        if (locThatCanBeThisDigit != -1) {
            locThatCanBeThisDigit = -2;
            break;
        }
        locThatCanBeThisDigit = loc;
    }
    if (locThatCanBeThisDigit >= 0) {
        updateLocationHasToBe(knowledge, locThatCanBeThisDigit, d);
        debug("[ UPDATE ] We know that digit %d has to be in there, so loc %d has to be that digit!\n",
            d, locThatCanBeThisDigit);
    }

    // If we know about so many digits that they are in there to fill the number, then the rest is not!
    if (knowledge->numsInThere.size == NUM_LEN && knowledge->numsNotInThere.size < 10-NUM_LEN) {
        debug("[ LEARN! ] We know enough digits to fill the number, so the rest is not in there!\n");
        for (int digit = 0; digit < 10; digit++) {
            if (contains(knowledge->numsInThere, digit)) continue;
            updateDigitNotInThere(knowledge, digit);
        }
    }
}

void updateDigitNotInThere(Knowledge *knowledge, digit d) {
    add(knowledge->numsNotInThere, d);

    // If a digit is not in the number, it can also not be in any location!
    for (int loc = 0; loc < NUM_LEN; loc++) {
        remove(knowledge->locCanBe[loc], d);
    }

    // If we know about all digits that are not in there, then we can decude which ones are!
    if (knowledge->numsNotInThere.size == 10-NUM_LEN && knowledge->numsInThere.size < NUM_LEN) {
        debug("[ LEARN! ] We know enough digits that are not in there to figure out which are!\n");
        for (int digit = 0; digit < 10; digit++) {
            if (contains(knowledge->numsNotInThere, digit)) continue;
            updateDigitInThere(knowledge, digit);
        }
    }
}




/////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////// Random definitions for ease of use /////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////

#define swapInt(l1, l2)     { int t = l1; l1 = l2; l2 = t; }
#define numsFrom(guess, f)  for (int d=0; d<NUM_LEN; d++) guess.nums[d] = (d+f)%10;
#define copyN(l1, l2, n)    for (int l=0; l<n; l++) l1[l] = l2[l];

/**
 * Do a guess, then scan for the results and return a predicate.
 */
Predicate queryGuess(Digits guessed) {
    for (int i = 0; i < NUM_LEN; i++) {         // Print
        printf("%d", guessed.nums[i]);
        if (guessed.nums[i] < 0 || guessed.nums[i] > 9) {
            debug("Tried to guess a digit %d\n", guessed.nums[i]);
            printf("\n");
            fflush(stdout);
            exit(EXIT_FAILURE);
        }
    }
    printf("\n");
    fflush(stdout);
    Predicate p = { .guess = guessed };         // Scan
    int r = scanf("%hhu%hhu", &p.exact, &p.inThere);
    if (r != 2) exit(EXIT_FAILURE);
    if (p.exact == NUM_LEN) exit(EXIT_SUCCESS);
    debug("Queried: [ G: ");                    // Debug
    debugN(p.guess.nums);
    debug(" -> exact: %d, inThere: %d ]\n",
        p.exact, p.inThere);
    return p;                                   // Return
}

IntSet filterSet(IntSet set, Digits keep) {
    IntSet result = { };
    for (int i = 0; i < NUM_LEN; i++) {
        if (!contains(set, keep.nums[i])) continue;
        add(result, keep.nums[i]);
    }
    return result;
}

int unknownInThereDigits(Knowledge *knowledge, Digits guess) {
    // Aka from how many digits do we not know if it is in the result or not.
    return NUM_LEN - (filterSet(knowledge->numsInThere, guess).size
        + filterSet(knowledge->numsNotInThere, guess).size);
}

bool equalDigits(Digits d1, Digits d2) {
    for (int i = 0; i < NUM_LEN; i++)
        if (d1.nums[i] != d2.nums[i]) return false;
    return true;
}

bool alreadyGuessed(Knowledge *knowledge, Digits guess) {
    for (int p = 0; p < mPredicatesSize; p++)
        if (equalDigits(guess, getPredicate(p).guess)) return true;
    return false;
}

void rotateExceptKnown(digit nums[], Knowledge *knowledge) {
    int rightMostVal = -1, prev;
    for (int d = NUM_LEN-1; d >= 0; d--) {
        if (knowledge->locCanBe[d].size == 1) continue;
        if (rightMostVal == -1) rightMostVal = nums[d];
        else nums[prev] = nums[d];
        prev = d;
    }
    nums[prev] = rightMostVal;
}





/////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////// Complete solvers for specific cases /////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////

void solveLen1() {                          // Lets hardcode optimally for length 1 (avg 5) (because too easy)
    if (NUM_LEN != 1) return;
    Digits guess = { };
    for (int i = 3; i < 12; i++) {
        guess.nums[0] = (i % 9) + 1;
        queryGuess(guess);
    }
}


void solveLen2(Knowledge *knowledge) {      // Lets hardcode optimally for length 2 (avg 5) (because too easy)
    if (NUM_LEN != 2) return;
    Digits guess = { };
    Predicate pred = { };
    for (int i = 1; i < 10; i += 2) {
        numsFrom(guess, i);
        pred = queryGuess(guess);
        if (pred.inThere + pred.exact == 0) continue;
        if (pred.exact == 0) { // Swap makes exact
            swapInt(pred.guess.nums[0], pred.guess.nums[1]);
            swapInt(pred.exact, pred.inThere);
        }
        if (pred.exact == 2) {
            queryGuess(pred.guess);
            return;
        }
        savePredicate(pred); // was exact = 1
        if (mPredicatesSize == 2) break;
    } // Predicates 1 and 2 have 'exact = 1'
    guess.nums[0] = getPredicate(0).guess.nums[0];
    guess.nums[1] = getPredicate(1).guess.nums[1];
    pred = queryGuess(guess);
    guess.nums[0] = getPredicate(1).guess.nums[0];
    guess.nums[1] = getPredicate(0).guess.nums[1];
    pred = queryGuess(guess);
}



Digits swapFindFirst(Knowledge *knowledge) {
    Predicate pred = { }, preRotPred = { };
    Digits guess = { };

    // First off we just guess 1234...
    numsFrom(guess, 1);
    preRotPred = queryGuess(guess);

    // If there is inThere is not equal to NUM_LEN, then go over digits outside our number first

    int rememberT = -1;
    for (int r = 1; r < 9; r++) {
        numsFrom(guess, 1);
        swapInt(guess.nums[0], guess.nums[r]);
        pred = queryGuess(guess);
        savePredicate(pred);

        if (pred.exact == preRotPred.exact) continue;   // This means 0 and r were not correct in both

        if (pred.exact == preRotPred.exact - 1) {       // This means one of 0 and r was correct before
            if (r == 1) continue;

            if (r == 2) {
                if (getPredicate(-1).exact == preRotPred.exact - 1) {
                    // if first 2 swaps get -1, then swap 2 and 3 to learn things!
                    numsFrom(guess, 1);
                    swapInt(guess.nums[1], guess.nums[2]);
                    pred = queryGuess(guess);
                    if (pred.exact == preRotPred.exact - 2) {
                        // So 2 and 3 were correct, also 1 is wrong!
                        setOnly(knowledge->locCanBe[1], preRotPred.guess.nums[1]);
                        setOnly(knowledge->locCanBe[2], preRotPred.guess.nums[2]);
                    } else {
                        setOnly(knowledge->locCanBe[0], preRotPred.guess.nums[0]);
                        return preRotPred.guess;
                    }
                }
            }
        }

        if (pred.exact == preRotPred.exact + 1) {       // Getting here means 0 was not correct in both
            if (rememberT == -1) {
                rememberT = r;
                continue;
            } // This will only happen twice EVER
            numsFrom(guess, 1);
            swapInt(guess.nums[0], guess.nums[rememberT]);
            swapInt(guess.nums[rememberT], guess.nums[r]);
            if (guess.nums[0] != 0) {
                pred = queryGuess(guess);
                if (pred.exact == preRotPred.exact + 2) {
                    setOnly(knowledge->locCanBe[0], guess.nums[0]);
                    setOnly(knowledge->locCanBe[r], guess.nums[r]);
                    return guess;
                }
            }
            numsFrom(guess, 1);
            swapInt(guess.nums[0], guess.nums[r]);
            swapInt(guess.nums[rememberT], guess.nums[r]);
            if (guess.nums[0] == 0) {
                debug("Wait... Something is wrong... (@10, 1)\n");
            }
            pred = queryGuess(guess);
            if (pred.exact == preRotPred.exact + 2) {
                setOnly(knowledge->locCanBe[0], guess.nums[0]);
                setOnly(knowledge->locCanBe[rememberT], guess.nums[rememberT]);
                return guess;
            }
            debug("Wait... Something is wrong... (@10, 2)\n");
            return guess;
        }

        // If from a swap the value changes by 2, we know 0 and r!
        if (pred.exact == preRotPred.exact - 2) guess = preRotPred.guess;
        if (pred.exact == preRotPred.exact + 2) guess = pred.guess;
        setOnly(knowledge->locCanBe[0], guess.nums[0]);
        setOnly(knowledge->locCanBe[r], guess.nums[r]);
        return guess;
    }
    return guess;
}

int amountKnown(Knowledge *knowledge) {
    int total = 0;
    for (int i = 0; i < 10; i++)
        if (knowledge->locCanBe[i].size == 1) total++;
    return total;
}

void rotateSolve(Knowledge *knowledge, Digits guess) {
    /*
    * If we have a guess with all correct digits (though not in the right place), and we know any digit K exactly we can:
    * - Find out in worst 'not-exact' turns which numbers of any guess are correct, by swapping each digit with K.
    * - Solve by rotating, then check using swap, then lock correct digits
    *      Worst case (len 10): (rot, lock 1, repeat) 9 + 8 + 7 + 6 + 5 + 4 + 3 + 2                     =  44 turns
    *      Avg case   (len 10): (we find digit before searching all, and sometimes 2 fall in place)     = <22 turns
    */
    Digits baseGuess = guess;
    while (true) {
        debug("Okay, rotation: We have: ");
        debugN(guess.nums);
        rotateExceptKnown(guess.nums, knowledge);
        debug("  --R1->  ");
        debugN(guess.nums);
        debug("\n");
        Predicate pred = queryGuess(guess);

        if (pred.exact > amountKnown(knowledge)) { // Some fell into place? lock them
            for (int r = 1; r < 10; r++) {
                if (knowledge->locCanBe[r].size == 1) continue;
                copyN(guess.nums, pred.guess.nums, 10);
                if (guess.nums[r] == 0) continue;
                swapInt(guess.nums[0], guess.nums[r]);
                Predicate pred2 = queryGuess(guess);
                if (pred2.exact == pred.exact - 2) {
                    setOnly(knowledge->locCanBe[r], pred.guess.nums[r]);
                    debug("Boom, we now know something more");
                    if (pred.exact <= amountKnown(knowledge)) break;
                }
            }
            copyN(guess.nums, pred.guess.nums, 10);
        }
    }
}













/////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////// I guess the main solver stuff ////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////

bool learnThings(Knowledge *knowledge) {
    for (int p = 0; p < mPredicatesSize; p++) {
        Predicate pred = getPredicate(p);

        // First get as much info about this predicate as possible
        int totalInThere = pred.exact + pred.inThere;
        int digitsWeKnowAreInR = 0;
        int digitsWeKnowNotInR = 0;
        int digitsWeKnowInR_ButKnownNotExact = 0;
        int digitsWeKnowInR_AndKnownAreExact = 0;
        int digitsThatCannotBeExact = 0;
        int digitsThatCouldBeExact = 0;
        for (int i = 0; i < NUM_LEN; i++) {
            u_int8_t digit = pred.guess.nums[i];
            if (!contains(knowledge->locCanBe[i], digit)) digitsThatCannotBeExact++;
            else digitsThatCouldBeExact++;
            if (contains(knowledge->numsNotInThere, digit)) {
                digitsWeKnowNotInR++;
            } else if (contains(knowledge->numsInThere, digit)) {
                digitsWeKnowAreInR++;
                if (!contains(knowledge->locCanBe[i], digit)) digitsWeKnowInR_ButKnownNotExact++;
                else if (knowledge->locCanBe[i].size == 1) digitsWeKnowInR_AndKnownAreExact++;
            }
        }


        // If we already know everything about if there numbers are in R
        bool weKnowAboutInThere = digitsWeKnowAreInR + digitsWeKnowNotInR == NUM_LEN;

        if (!weKnowAboutInThere) {
            // In case we don't know about all the digits in this predicate whether they
            // are in the final number or not, then find that out first!

            if (totalInThere == digitsWeKnowAreInR) {
                debug("[ LEARN! ] Predicate guess '");
                debugN(pred.guess.nums);
                debug("' should have %d YES, we know %d YES (and %d NO), so rest is NO\n",
                    totalInThere, digitsWeKnowAreInR, digitsWeKnowNotInR);
                for (int i = 0; i < NUM_LEN; i++) {
                    int d = pred.guess.nums[i];
                    if (contains(knowledge->numsInThere, d)) continue;
                    updateDigitNotInThere(knowledge, d);
                }
                return true;
            }

            if (totalInThere + digitsWeKnowNotInR == NUM_LEN) {
                debug("[ LEARN! ] Predicate guess '");
                debugN(pred.guess.nums);
                debug("' should have %d YES, we know %d NO (and %d YES), so rest is YES\n",
                    totalInThere, digitsWeKnowNotInR, digitsWeKnowAreInR);
                for (int i = 0; i < NUM_LEN; i++) {
                    int d = pred.guess.nums[i];
                    if (contains(knowledge->numsNotInThere, d)) continue;
                    updateDigitInThere(knowledge, d);
                }
                return true;
            }

            if (totalInThere == 0) {
                debug("[ LEARN! ] Predicate guess '");
                debugN(pred.guess.nums);
                debug("' has 0 digits in there, so none are in the result\n");
                for (int i = 0; i < NUM_LEN; i++) {
                    int d = pred.guess.nums[i];
                    updateDigitNotInThere(knowledge, d);
                }
                return true;
            }



            u_int16_t thisHash = intSetOf(pred.guess).data; // Same hash this way = same digits used
            for (int p2 = 0; p2 < mPredicatesSize; p2++) {
                if (p == p2) continue;
                Predicate otherPred = getPredicate(p2);
                if (intSetOf(otherPred.guess).data != thisHash) continue;

                int digitsInDifferentLocation = 0;
                for (int l = 0; l < NUM_LEN; l++) {
                    if (otherPred.guess.nums[l] == pred.guess.nums[l]) continue;
                    digitsInDifferentLocation++;
                }


                if (pred.exact > 0 && pred.inThere == 0) {

                    if (otherPred.inThere == pred.inThere && pred.exact == otherPred.exact) {
                        // Then all digits that are different are wrong!
                        bool learnt = false;
                        for (int i = 0; i < NUM_LEN; i++) {
                            if (otherPred.guess.nums[i] == pred.guess.nums[i]) continue;
                            if (contains(knowledge->numsNotInThere, pred.guess.nums[i])) continue;
                            updateDigitNotInThere(knowledge, pred.guess.nums[i]);
                            learnt = true;
                        }
                        if (learnt) {
                            debug("[ LEARN! ] Predicate guess '");
                            debugN(pred.guess.nums);
                            debug("' together with '");
                            debugN(otherPred.guess.nums);
                            debug("' same digits in different places, so eliminating some digits (1)\n")
                            return true;
                        }
                    }
                    if (otherPred.inThere == pred.exact && otherPred.exact == pred.inThere) {
                        // Then all digits that are the same are wrong!
                        bool learnt = false;
                        for (int i = 0; i < NUM_LEN; i++) {
                            if (otherPred.guess.nums[i] != pred.guess.nums[i]) continue;
                            if (contains(knowledge->numsNotInThere, pred.guess.nums[i])) continue;
                            updateDigitNotInThere(knowledge, pred.guess.nums[i]);
                            learnt = true;
                        }
                        if (learnt) {
                            debug("[ LEARN! ] Predicate guess '");
                            debugN(pred.guess.nums);
                            debug("' together with '");
                            debugN(otherPred.guess.nums);
                            debug("' same digits in different places, so eliminating some digits (2)\n")
                            return true;
                        }
                    }
                    if (digitsInDifferentLocation == (pred.exact - otherPred.exact)) {
                        // If this is the case, then all different digits are exactly right in pred!
                        bool learnt = false;
                        for (int i = 0; i < NUM_LEN; i++) {
                            if (otherPred.guess.nums[i] == pred.guess.nums[i]) continue;
                            if (!contains(knowledge->numsInThere, pred.guess.nums[i])) {
                                updateDigitInThere(knowledge, pred.guess.nums[i]);
                                learnt = true;
                            }
                            if (knowledge->locCanBe[i].size > 1) {
                                updateLocationHasToBe(knowledge, i, pred.guess.nums[i]);
                                learnt = true;
                            }
                        }
                        if (learnt) {
                            debug("[ LEARN! ] Predicate guess '");
                            debugN(pred.guess.nums);
                            debug("' together with '");
                            debugN(otherPred.guess.nums);
                            debug("' same digits in different places, so eliminating some digits (3)\n")
                            return true;
                        }
                    }

                }

            }





        } else {
            // In case we do know for all the digits in this predicate whether they are in
            // the final number, we can learn some things extra sometimes.
            if (pred.exact > digitsWeKnowInR_AndKnownAreExact
            && digitsWeKnowInR_ButKnownNotExact == pred.inThere) {
                debug("[ LEARN! ] Predicate guess '");
                debugN(pred.guess.nums);
                debug("' has some exactly right, and we know which digits\n");
                debug("           'inThere' corresponds to, so we can fill in exacts\n");
                for (int i = 0; i < NUM_LEN; i++) {
                    u_int8_t d = pred.guess.nums[i];
                    if (contains(knowledge->numsNotInThere, d)) continue;
                    if (!contains(knowledge->locCanBe[i], d)) continue;
                    updateLocationHasToBe(knowledge, i, d);
                }
                return true;
            }
        }

        if (pred.exact + digitsThatCannotBeExact == NUM_LEN
        && digitsWeKnowInR_AndKnownAreExact < pred.exact) {
            debug("[ LEARN! ] Predicate guess '");
            debugN(pred.guess.nums);
            debug("' has %d exactly right, and %d digits we know cannot be, so rest is!\n",
                pred.exact, digitsThatCannotBeExact);
            for (int i = 0; i < NUM_LEN; i++) {
                int d = pred.guess.nums[i];
                if (!contains(knowledge->locCanBe[i], d)) continue;
                updateLocationHasToBe(knowledge, i, d);
            }
            return true;
        }

        if (pred.exact == 0 && digitsThatCouldBeExact > 0) {
            debug("[ LEARN! ] Predicate guess '");
            debugN(pred.guess.nums);
            debug("' has 0 exactly right, so none in right place\n");
            for (int i = 0; i < NUM_LEN; i++) {
                int d = pred.guess.nums[i];
                updateLocationCannotBe(knowledge, i, d);
            }
            return true;
        }


    }
    return false;
}

void learnUntilTired(Knowledge *knowledge) {
    while (learnThings(knowledge)) { };
    // Print everything we know:
    debug("\nAfter a good day of learning, we now know:\n");
    debug(" - Digits ARE in there:");
    debugSet(knowledge->numsInThere);
    debug("\n - Digits NOT in there:");
    debugSet(knowledge->numsNotInThere);
    debug("\n - Every location can still be:");
    for (int loc = 0; loc < NUM_LEN; loc++) {
        debug("\n    \\_  Loc %d: (%d) ", loc, knowledge->locCanBe[loc].size);
        debugSet(knowledge->locCanBe[loc]);
    }
    debug("\n");
}

Predicate guessSaveLearn(Digits guess, Knowledge *knowledge, const char *msg) {
    Predicate newPred = queryGuess(guess);
    debug("[ Guess. ] %s\n", msg);
    savePredicate(newPred);
    learnUntilTired(knowledge);
    return newPred;
}

bool randomGuess(Knowledge *knowledge, Digits *guess, IntSet used, int setDigit) {
    if (setDigit == NUM_LEN) return !alreadyGuessed(knowledge, *guess); // True if new guesss

    digit startFrom = (mPredicatesSize*7+31*setDigit)%10;
    for (digit optD = startFrom; optD < startFrom+10; optD++) {
        if (!contains(knowledge->locCanBe[setDigit], optD%10)) continue;
        if (contains(used, optD % 10)) continue;
        add(used, optD % 10);
        guess->nums[setDigit] = optD % 10;

        bool possible = true;
        for (int i = setDigit+1; i < NUM_LEN; i++) {
            if (subtractSet(knowledge->locCanBe[i], used).size == 0) possible = false;
        }

        if (possible && randomGuess(knowledge, guess, used, setDigit+1)) return true;
        remove(used, optD % 10);
    }
    return false;
}

void doAGoodGuess(Knowledge *knowledge) {
    int anyNotInDigit = getAny(knowledge->numsNotInThere);
    for (int p = 0; p < mPredicatesSize; p++) {
        Predicate pred = getPredicate(p);
        int predUnknownInThere = unknownInThereDigits(knowledge, pred.guess);

        // If we have any predicates with almost all digits in there, solve!
        if (pred.inThere + pred.exact == NUM_LEN-1 && predUnknownInThere > 0) {

            IntSet digitsNotInPred = subtractSet(FULL_SET_10, intSetOf(pred.guess));
            int anyNotInThisPred = getAny(digitsNotInPred);

            if (anyNotInDigit > 0) {
                for (int swapI = 0; swapI < NUM_LEN-1; swapI++) {
                    Digits guess = pred.guess;
                    guess.nums[swapI] = anyNotInDigit;
                    Predicate newPred = guessSaveLearn(guess, knowledge,
                        "Since we have a predicate with almost all digits, swap solve it!");
                    if (unknownInThereDigits(knowledge, pred.guess) == 0) break;
                }
                return;
            }

        }

        // If we have any predicates with only 'exact' values, solve!
        if (pred.inThere == 0 && (pred.exact == 1 || pred.exact > NUM_LEN/2) && predUnknownInThere == 0) {
            if (predUnknownInThere > 2) {
                for (int i = 0; i < NUM_LEN; i += 2) {
                    Digits guess = pred.guess;
                    swapInt(guess.nums[i], guess.nums[i+1]);
                    Predicate newPred = guessSaveLearn(guess, knowledge,
                        "Since we have a predicate with only exact values, 2-search solve start!");
                    int newUnkownInThere = unknownInThereDigits(knowledge, pred.guess);
                    if (newUnkownInThere <= 2) break;
                }
                return;
            }
            if (predUnknownInThere > 0 && anyNotInDigit > 0) {
                for (int i = 0; i < NUM_LEN; i += 2) {
                    Digits guess = pred.guess;
                    guess.nums[i] = anyNotInDigit;
                    Predicate newPred = guessSaveLearn(guess, knowledge,
                        "Since we have a predicate with only exact values, 2-search solve finish!");
                    int newUnkownInThere = unknownInThereDigits(knowledge, pred.guess);
                    if (newUnkownInThere == 0) break;
                }
                return;
            }
        }

    }

    // If we get here we couldn't come up with anything, so just guess a
    // sort or random but almost maybe possibly correct something.

    Digits random = { 0 };
    IntSet used = { };
    randomGuess(knowledge, &random, used, 0);
    guessSaveLearn(random, knowledge, "Just a random guess");







}










void solve(Knowledge *knowledge) {
    Digits guess = { };

    #define FROM    1
    for (int i = FROM; i < 9+FROM; i += NUM_LEN) {
        numsFrom(guess, i);
        Predicate pred = queryGuess(guess);
        savePredicate(pred);
        learnUntilTired(knowledge);
    }

    int i;
    Digits knowAllGuess = { };
    while (true) {

        for (i = 0; i < NUM_LEN; i++) {
            if (knowledge->locCanBe[i].size != 1) break;
            knowAllGuess.nums[i] = getAny(knowledge->locCanBe[i]);
        }
        if (i == NUM_LEN) {
            debug("WE KNOW THE THING!!!\n");
            guessSaveLearn(knowAllGuess, knowledge, "WE KNOW IT!");
        }

        doAGoodGuess(knowledge);
    }
}




// 46 tests, of which 6 for len 1 and 2
// assuming we can do those in 5ish guesses (which we can), takes 6*5=30
// 40 tests for len >3

// best: 290-30 = 260, so roughly 7 guesses per thing

int main() {
    u_int8_t t;
    scanf("%d", &NUM_LEN);
    debug("Okay, number length is %d\n", NUM_LEN);
    scanf("%hhu%hhu", &t, &t);
    debug("Okay, Got the bs input out of the way\n");

    Knowledge knowledge = { };
    for (int loc = 0; loc < NUM_LEN; loc++) {
        knowledge.locCanBe[loc].data = (1<<11)-1;
        knowledge.locCanBe[loc].size = 10;
    } // All locs can be anything, but first not 0.
    remove(knowledge.locCanBe[0], 0);

    switch (NUM_LEN) {
        case 1:
            solveLen1();
            return 0;
        case 2:
            solveLen2(&knowledge);
            return 0;
    }

    solve(&knowledge);
    return 0;
}
