/* Check the PR's exact code (pr_helpers.h, made by extract.py) against a
   per-byte reference.

   Build with -DCHECK_COUNT_WORDS=0 (byte-stepping loop, used outside MSVC)
   or =1 (word-counting loop, used by MSVC); without it, the loop the
   compiler would get in CPython is used.

   1. The word helper: every byte value at every position of a word on all
      256 fill values, and every pair of values at every pair of positions
      on 16 fills, for lower and upper.
   2. pr_bytes_lower/upper: every byte value at every position for lengths
      0..80 and at 27 positions of lengths around word multiples up to
      4,097; every pair of byte values at every pair of positions for
      lengths 2..9; random bytes at lengths 0..1,100 with source and
      destination offsets 0..15.  The destination's neighbours and the
      source must be left alone. */
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef ptrdiff_t Py_ssize_t;
#if SIZE_MAX == 0xFFFFFFFFu
#  define SIZEOF_SIZE_T 4
#else
#  define SIZEOF_SIZE_T 8
#endif
#if defined(_MSC_VER)
#  define Py_ALWAYS_INLINE __forceinline
#  define Py_NO_INLINE __declspec(noinline)
#else
#  define Py_ALWAYS_INLINE __attribute__((always_inline))
#  define Py_NO_INLINE __attribute__((noinline))
#endif
#ifndef CHECK_COUNT_WORDS
#  if defined(_MSC_VER) && !defined(__clang__)
#    define CHECK_COUNT_WORDS 1
#  else
#    define CHECK_COUNT_WORDS 0
#  endif
#endif
#define PyDoc_STRVAR_shared(name, str) static const char name[] = str
#if defined(__clang__) || (defined(__GNUC__) && __GNUC__ >= 7)
#  define _Py_FALLTHROUGH __attribute__((fallthrough))
#else
#  define _Py_FALLTHROUGH do { } while (0)
#endif

static unsigned char tolower_tab[256], toupper_tab[256];
#define Py_TOLOWER(c) (tolower_tab[(unsigned char)(c)])
#define Py_TOUPPER(c) (toupper_tab[(unsigned char)(c)])

#include "pr_helpers.h"

static unsigned char ref_lower(unsigned char c) { return c >= 'A' && c <= 'Z' ? c + 32 : c; }
static unsigned char ref_upper(unsigned char c) { return c >= 'a' && c <= 'z' ? c - 32 : c; }

static long long checked, bad;
static uint64_t rng_state = 161155;
static unsigned char rnd(void)
{
    rng_state = rng_state * 6364136223846793005ULL + 1442695040888963407ULL;
    return (unsigned char)(rng_state >> 56);
}

static void check_word(const unsigned char *in)
{
    const size_t ones = (size_t)-1 / 0xff;
    size_t x, lo, up;
    unsigned char ol[SIZEOF_SIZE_T], ou[SIZEOF_SIZE_T];
    memcpy(&x, in, sizeof(x));
    /* the constants as ascii_case_words computes them */
    lo = x ^ ascii_case_bits(x, (0x80 - 'A') * ones, (0x80 - 'A' - 26) * ones);
    up = x ^ ascii_case_bits(x, (0x80 - 'a') * ones, (0x80 - 'a' - 26) * ones);
    memcpy(ol, &lo, sizeof(lo));
    memcpy(ou, &up, sizeof(up));
    for (int i = 0; i < SIZEOF_SIZE_T; i++) {
        if (ol[i] != ref_lower(in[i]) || ou[i] != ref_upper(in[i])) {
            if (bad++ < 10) {
                printf("word mismatch at byte %d: in %02x lower %02x upper %02x\n",
                       i, in[i], ol[i], ou[i]);
            }
        }
    }
    checked++;
}

#define PAD 16
static unsigned char srcbuf[4200 + 2 * PAD], dstbuf[4200 + 2 * PAD];
static unsigned char want[4200], saved[4200 + 2 * PAD];

static void check_func(const unsigned char *data, Py_ssize_t n, int soff, int doff)
{
    for (int upper = 0; upper < 2; upper++) {
        /* the source with PAD bytes after it, and the destination with
           PAD guard bytes on each side */
        unsigned char *src = srcbuf + soff, *dst = dstbuf + PAD + doff;
        size_t srcwin = soff + n + PAD;
        memcpy(src, data, n);
        memcpy(saved, srcbuf, srcwin);
        memset(dst - PAD, 0xA5, n + 2 * PAD);
        for (Py_ssize_t i = 0; i < n; i++) {
            want[i] = upper ? ref_upper(data[i]) : ref_lower(data[i]);
        }
        if (upper) {
            pr_bytes_upper((char *)dst, (const char *)src, n);
        }
        else {
            pr_bytes_lower((char *)dst, (const char *)src, n);
        }
        int ok = memcmp(dst, want, n) == 0
                 && memcmp(srcbuf, saved, srcwin) == 0;
        for (int k = 1; ok && k <= PAD; k++) {
            ok = dst[-k] == 0xA5 && dst[n - 1 + k] == 0xA5;
        }
        if (!ok && bad++ < 10) {
            printf("%s mismatch: len %ld, src offset %d, dst offset %d\n",
                   upper ? "upper" : "lower", (long)n, soff, doff);
        }
        checked++;
    }
}

static void every_value_at(Py_ssize_t n, Py_ssize_t pos)
{
    unsigned char data[4200];
    for (Py_ssize_t i = 0; i < n; i++) {
        data[i] = rnd();
    }
    for (int v = 0; v < 256; v++) {
        data[pos] = (unsigned char)v;
        check_func(data, n, v % PAD, (v / PAD) % PAD);
    }
}

int main(void)
{
    unsigned char w[SIZEOF_SIZE_T];
    for (int c = 0; c < 256; c++) {
        tolower_tab[c] = ref_lower((unsigned char)c);
        toupper_tab[c] = ref_upper((unsigned char)c);
    }

    /* 1. the word helper */
    for (int fill = 0; fill < 256; fill++)
        for (int p = 0; p < SIZEOF_SIZE_T; p++)
            for (int a = 0; a < 256; a++) {
                memset(w, fill, sizeof(w));
                w[p] = (unsigned char)a;
                check_word(w);
            }
    for (int fill = 0; fill < 256; fill += 17)
        for (int p = 0; p < SIZEOF_SIZE_T; p++)
            for (int q = p + 1; q < SIZEOF_SIZE_T; q++)
                for (int a = 0; a < 256; a++)
                    for (int b = 0; b < 256; b++) {
                        memset(w, fill, sizeof(w));
                        w[p] = (unsigned char)a;
                        w[q] = (unsigned char)b;
                        check_word(w);
                    }
    long long words = checked;

    /* 2. the functions */
    for (Py_ssize_t n = 0; n <= 80; n++)
        for (Py_ssize_t pos = 0; pos < n; pos++)
            every_value_at(n, pos);
    for (Py_ssize_t n = 2; n <= 9; n++)
        for (Py_ssize_t p = 0; p < n; p++)
            for (Py_ssize_t q = p + 1; q < n; q++) {
                unsigned char data[9];
                for (Py_ssize_t i = 0; i < n; i++) {
                    data[i] = rnd();
                }
                for (int a = 0; a < 256; a++)
                    for (int b = 0; b < 256; b++) {
                        data[p] = (unsigned char)a;
                        data[q] = (unsigned char)b;
                        check_func(data, n, (a + b) % PAD, b % PAD);
                    }
            }
    static const int mults[] = {3, 4, 8, 16, 32, 64, 128, 512};
    for (size_t m = 0; m < sizeof(mults) / sizeof(mults[0]); m++)
        for (int d = -1; d <= 1; d++) {
            Py_ssize_t n = (Py_ssize_t)mults[m] * SIZEOF_SIZE_T + d;
            Py_ssize_t mid = n / 2 - 4;
            for (Py_ssize_t pos = 0; pos < n; pos++)
                if (pos < 9 || (pos >= mid && pos < mid + 9) || pos >= n - 9)
                    every_value_at(n, pos);
        }
    for (Py_ssize_t n = 0; n <= 1100; n++)
        for (int soff = 0; soff < PAD; soff++)
            for (int doff = 0; doff < PAD; doff += 5) {
                unsigned char data[1100];
                for (Py_ssize_t i = 0; i < n; i++) {
                    data[i] = rnd();
                }
                check_func(data, n, soff, doff);
            }

    printf("%s: word %d bytes, %s loop: %lld word checks, %lld call checks, %lld bad\n",
           bad ? "FAIL" : "ok", SIZEOF_SIZE_T,
           CHECK_COUNT_WORDS ? "word-counting (MSVC)" : "byte-stepping",
           words, checked - words, bad);
    return bad != 0;
}
