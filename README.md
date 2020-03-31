# MT19937

Implementing and breaking the MT19937 Mersenne Twister pseudorandom number generator; based on the challenges #21 to #23 of [cryptopals](https://github.com/anneouyang/cryptopals)

- [Part I: Implement the MT19937 Mersenne Twister RNG](https://github.com/anneouyang/MT19937#part-i-implement-the-mt19937-mersenne-twister-rng)
- [Part II: Crack an MT19937 seed](https://github.com/anneouyang/MT19937#part-ii-crack-an-mt19937-seed)
- [Part III: Clone an MT19937 RNG from its output](https://github.com/anneouyang/MT19937#part-iii-clone-an-mt19937-rng-from-its-output)



<br />

## Overview

The Mersenne Twister is a pseudorandom number generator using a Mersenne prime (a prime number one less than a power of two: ![formula](https://render.githubusercontent.com/render/math?math=2%5E%7Bn%7D%20-%201)) as its period length. MT19937 uses the Mersenne prime ![formula](https://render.githubusercontent.com/render/math?math=2%5E%7B19937%7D%20-%201).

C++11 provides an implementation of  [`std::mt19937`](http://www.cplusplus.com/reference/random/mt19937/) designed to replace `rand()` for several reasons:

1. MT19937 provides better pseudorandomness.
2. MT19937 has a longer period, which is ![formula](https://render.githubusercontent.com/render/math?math=2%5E%7B19937%7D%20-%201).
3. MT19937 is able to generate random numbers from a larger range.



<br />

## Part I: Implement the MT19937 Mersenne Twister RNG

### A Simplified Explanation of the Algorithm

#### High Level Overview

A state of a Mersenne Twister is an array of *n* values of *w* bits each. 

The array is initialized with a *w*-bit seed value to obtain *state_0*. Note that *state_0* does not produce any outputs. 

State transitions are achieved by a twist function. At each state, an output (a random number) can be obtained by . A state allows you to output *n* numbers before transitioning to the next state.

In the 32-bit MT19937, *w* = `32` and *n* = `624`.

#### Initialization

The initialization function takes in a seed and generates the first state. Let

- *f* be a constant parameter; *f* = `1812433253`
- *X* be the state array

![Equation](https://render.githubusercontent.com/render/math?math=X_0) = seed

![Equation](https://render.githubusercontent.com/render/math?math=X_i)= lowest *w* bits of (![Equation](https://render.githubusercontent.com/render/math?math=f%20%2A%20%28X_%7Bi-1%7D%20%5Coplus%20%28X_%7Bi-1%7D%20%5Cgg%20%28w-2%29%29%29%20%2B%20i)) for ![Equation](https://render.githubusercontent.com/render/math?math=i%20%5Cin%20%5C%7B1..n-1%5C%7D)

#### Twist Function

The twist function is called every *n* numbers to achieve the state transition. Let

- *m* be an offset where 1 <= *m* < *n*; *m* = `397`
- *r* be the number of bits of the lower bitmask where 0 <= *r* <= *w* - 1; *r* = `31`
- *a* be the coefficients of the rational normal form twist matrix; a = `0x9908B0DF`
- *A* be the twist transformation in the rational normal form ![Equation](https://render.githubusercontent.com/render/math?math=%5Cleft%5B%20%7B%5Cbegin%7Barray%7D%7Bcc%7D%200%20%26%20I_%7Bw-1%7D%20%5C%5C%20a_%7Bw-1%7D%20%26%20%28a_%7Bw-2%7D%2C%20...%20%2Ca_0%29%20%5C%5C%20%5Cend%7Barray%7D%20%7D%20%5Cright%5D)

The series is defined by the recurrence relation

![Equation](https://render.githubusercontent.com/render/math?math=X_%7Bi%7D%20%3D%20X_%7Bi%2Bm%7D%20%5Coplus%20%28%28%5Ctext%7Bupper%20w%20-%20r%20bits%7D%20%28X_i%29%20%7C%7C%20%5Ctext%7Blower%20r%20bits%7D%28X_%7Bi%2B1%7D%29%29%20A%29) where![Equation](https://render.githubusercontent.com/render/math?math=i%20%5Cin%20%5C%7B0..n-1%5C%7D)

Note because *A* is in the rational normal form, the multiplication can be efficiently expressed as ![Equation](https://render.githubusercontent.com/render/math?math=%5Cboldsymbol%7Bx%7DA%20%3D%20%5Cbegin%7Bcases%7D%5Cboldsymbol%7Bx%7D%20%5Cgg%201%20%26%20x_0%20%3D%200%5C%5C%28%5Cboldsymbol%7Bx%7D%20%5Cgg%201%29%20%5Coplus%20%5Cboldsymbol%7Ba%7D%20%26%20x_0%20%3D%201%5Cend%7Bcases%7D) where ![Equation](https://render.githubusercontent.com/render/math?math=x_0) Is the lowest order bit of x

#### Temper Function

The tempering function returns a random number from a state and calls the twist function every *n* numbers. Let

- *y* be a temporary intermediate value
- *x* be the next value from the series
- *z* be the value returned from the algorithm
- *d, b, c* be TGFSR(R) tempering bitmasks; *d* = `0xFFFFFFFF`, *b* = `0x9D2C5680`, *c* = `0xEFC60000`
- *u, s, t, l* be TGFSR(R) tempering bit shifts; *u* = `11`, *s* = `7`, *t* = `15`, l = `18`

The tempering operations are defined as 

*y* = *x* ![Equation](https://render.githubusercontent.com/render/math?math=\oplus)((*x* >> *u*) & *d*)

*y* = *y* ![Equation](https://render.githubusercontent.com/render/math?math=\oplus)((*y*  << *s*) & *b*)

*y* *=* y ![Equation](https://render.githubusercontent.com/render/math?math=\oplus)((*y*  << *t*) & *c*)

*z* = *y* ![Equation](https://render.githubusercontent.com/render/math?math=\oplus)(*y* >> *l*) 

### Implementation

The code can be found [here](/code/implement_mt19937).



<br />

## Part II: Crack an MT19937 seed

### The Setup

- Wait a random number of seconds between `min_sleep_time` and `max_sleep_time`.
- Seeds the RNG with the current Unix timestamp.
- Waits a random number of seconds again.
- Returns the first 32 bit output of the RNG.

Guess the seed from the output of the RNG.

### Idea

Try all the possible seed values from (current time - max time) to (current time - min time). If the seed produces an RNG that generates the same output as the given RNG, it's likely that the seed has been recovered. 

This example illustrates a vulnerability from using an imprecise clock as the seed, and it has an easy fix by seeding with a more precise clock. In C++, for example, the use of`std::chrono::system_clock::now().time_since_epoch().count()` is preferable to `time(NULL)` as the seed of an RNG.

### Implementation

See code [here](/code/crack_seed_mt19937) for an implementation of the set up and a comparison of the two seeds (actual & guessed).



<br />

## Part III: Clone an MT19937 RNG from its output

### Idea

After observing *n* numbers, it is possible to predict all future iterations by reconstructing the internal state of the RNG, since the tempering function used to produce outputs is bijective and *invertible*.

Inverting the temper transform involves applying the inverse of each operation of the tempering function in reverse order. Examine the code segment from the tempering function:

```python
y = y ^ ((y >> MT19937.u) & MT19937.d)
y = y ^ ((y << MT19937.s) & MT19937.b)
y = y ^ ((y << MT19937.t) & MT19937.c)
y = y ^ (y >> MT19937.l)
```

Note that there are essentially two types of operations:

- Shift left + bitwise and
- Shift right + bitwise and

### Inverting the (shift left + bitwise and) operation

For an operation ![Equation](https://render.githubusercontent.com/render/math?math=y%20%3D%20x%20%5Coplus%20%28%20%28x%20%5Cll%20a%29%20%5Cland%20b%29%0A) rewrite the forward operation in terms of individual bits ![Equation](https://render.githubusercontent.com/render/math?math=x_i).

There are two cases:

- Case 1, *if i + a >= w*: ![Equation](https://render.githubusercontent.com/render/math?math=y_i%3Dx_i)
- Case 2, *if i + a < w:* ![Equation](https://render.githubusercontent.com/render/math?math=y_i%20%3D%20x_i%20%5Coplus%20%28x_%7Bi%20%2B%20a%7D%20%5Cland%20b_i%29)

The inverses for the two cases are then:

- Case 1: ![Equation](https://render.githubusercontent.com/render/math?math=x_i%3Dy_i)
- Case 2: ![Equation](https://render.githubusercontent.com/render/math?math=x_i%20%3D%20y_i%20%5Coplus%20%28x_%7Bi%20%2B%20a%7D%20%5Cland%20b_i%29)

Inverse the operation bit by bit starting from the trivial bits in Case 1.

### Inverting the (shift right + bitwise and) operation

The inverse of the right shift operation ![Equation](https://render.githubusercontent.com/render/math?math=y%20%3D%20x%20%5Coplus%20%28%20%28x%20%5Cgg%20a%29%20%5Cland%20b%29%0A) is symmetrical:

- Case 1, *if i < a*: ![Equation](https://render.githubusercontent.com/render/math?math=x_i%3Dy_i)
- Case 2, *if i >= a*: ![Equation](https://render.githubusercontent.com/render/math?math=x_i%20%3D%20y_i%20%5Coplus%20%28x_%7Bi%20-%20a%7D%20%5Cland%20b_i%29)

### Implementation

See an efficient implementation that uses the symmetry and operations on bits [here](/code/clone_mt19937.py).



<br />

## References

- https://en.wikipedia.org/wiki/Mersenne_Twister
- http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/ARTICLES/mt.pdf