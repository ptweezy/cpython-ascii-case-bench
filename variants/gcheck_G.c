/* Variant G (with G2's Py_ALWAYS_INLINE) against a per-byte reference: lengths 0..80, offsets 0..15, random
   bytes (all 256 values), copying and in place, lower and upper. */
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef ptrdiff_t Py_ssize_t;
#define SIZEOF_SIZE_T ((Py_ssize_t)sizeof(size_t))
#ifdef _MSC_VER
#define Py_NO_INLINE __declspec(noinline)
#define Py_ALWAYS_INLINE __forceinline
#else
#define Py_NO_INLINE __attribute__ ((noinline))
#define Py_ALWAYS_INLINE __attribute__((always_inline))
#endif
static unsigned char lo(unsigned char c){return (c>='A'&&c<='Z')?c+32:c;}
static unsigned char up(unsigned char c){return (c>='a'&&c<='z')?c-32:c;}
#define Py_TOLOWER(c) lo(c)
#define Py_TOUPPER(c) up(c)
static inline Py_ALWAYS_INLINE size_t
ascii_case_bits(size_t x, unsigned char first)
{
    const size_t ones = (size_t)-1 / 0xff;  /* 0x01 in every byte */
    size_t b = x & (0x7f * ones);
    size_t ge_first = b + (0x80 - first) * ones;
    size_t gt_last = b + (0x80 - first - 26) * ones;
    return (ge_first & ~gt_last & ~x & (0x80 * ones)) >> 2;
}
/* Convert the word at cptr + i into result + i. */
static inline Py_ALWAYS_INLINE void
ascii_case_word(char *result, const char *cptr, Py_ssize_t i,
                unsigned char first)
{
    size_t x;
    memcpy(&x, cptr + i, sizeof(x));
    x ^= ascii_case_bits(x, first);
    memcpy(result + i, &x, sizeof(x));
}

/* Convert len >= SIZEOF_SIZE_T bytes a word at a time.  If len is not a
   multiple of the word size, the last word overlaps the one before it;
   converting a byte twice gives the same result as converting it once.
   Kept out of line so that short strings don't pay for its setup. */
static Py_NO_INLINE void
ascii_case_words(char *result, const char *cptr, Py_ssize_t len,
                 unsigned char first)
{
    Py_ssize_t i;
    for (i = 0; i < len - SIZEOF_SIZE_T; i += SIZEOF_SIZE_T) {
        ascii_case_word(result, cptr, i, first);
    }
    ascii_case_word(result, cptr, len - SIZEOF_SIZE_T, first);
}

void _Py_bytes_lower(char *result, const char *cptr, Py_ssize_t len)
{
    Py_ssize_t i;

    if (len >= SIZEOF_SIZE_T) {
        ascii_case_words(result, cptr, len, 'A');
        return;
    }
    for (i = 0; i < len; i++) {
        result[i] = Py_TOLOWER((unsigned char) cptr[i]);
    }
}
void _Py_bytes_upper(char *result, const char *cptr, Py_ssize_t len)
{
    Py_ssize_t i;

    if (len >= SIZEOF_SIZE_T) {
        ascii_case_words(result, cptr, len, 'a');
        return;
    }
    for (i = 0; i < len; i++) {
        result[i] = Py_TOUPPER((unsigned char) cptr[i]);
    }
}
int main(void){
  unsigned char src[128], dst[128], ref[128]; long bad = 0, n = 0;
  srand(1);
  for (int rep = 0; rep < 200; rep++)
  for (int off = 0; off < 16; off++)
  for (int len = 0; len <= 80; len++)
  for (int up_ = 0; up_ < 2; up_++)
  for (int inplace = 0; inplace < 2; inplace++) {
    for (int i = 0; i < 128; i++) src[i] = rand() & 0xff;
    for (int i = 0; i < len; i++) ref[i] = up_ ? up(src[off+i]) : lo(src[off+i]);
    unsigned char *out = inplace ? src + off : dst + 16 + (15 - off);
    if (!inplace) { out[-1] = 0x5a; out[len] = 0xa5; }
    if (up_) _Py_bytes_upper((char *)out, (char *)src + off, len);
    else     _Py_bytes_lower((char *)out, (char *)src + off, len);
    if (memcmp(out, ref, len)) bad++;
    if (!inplace && (out[-1] != 0x5a || out[len] != 0xa5)) bad++;
    n++;
  }
  printf("G check: %ld cases, %ld bad\n", n, bad); return bad != 0;
}
