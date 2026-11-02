/* Like word_exhaustive.c, for the size_t version: every pair of byte values
   at every pair of positions in a size_t word (4 or 8 bytes), on 16 fill
   patterns, for both lower and upper, against a per-byte reference. */
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <stddef.h>
static inline size_t
ascii_case_bits(size_t x, unsigned char first)
{
    const size_t ones = (size_t)-1 / 0xff;  /* 0x01 in every byte */
    size_t b = x & (0x7f * ones);
    size_t ge_first = b + (0x80 - first) * ones;
    size_t gt_last = b + (0x80 - first - 26) * ones;
    return (ge_first & ~gt_last & ~x & (0x80 * ones)) >> 2;
}
static unsigned char lo(unsigned char c){return (c>='A'&&c<='Z')?c+32:c;}
static unsigned char up(unsigned char c){return (c>='a'&&c<='z')?c-32:c;}
int main(void){
  enum { W = sizeof(size_t) };
  long bad=0, n=0;
  for (int fill=0; fill<256; fill+=17)
  for (int p=0;p<W;p++) for (int q=0;q<W;q++)
  for (int a=0;a<256;a++) for (int b=0;b<256;b++){
    unsigned char in[W]; memset(in,fill,W); in[p]=a; in[q]=b;
    size_t x; memcpy(&x,in,W);
    size_t l = x ^ ascii_case_bits(x,'A'), u = x ^ ascii_case_bits(x,'a');
    unsigned char ol[W], ou[W]; memcpy(ol,&l,W); memcpy(ou,&u,W);
    for(int i=0;i<W;i++){ if(ol[i]!=lo(in[i])||ou[i]!=up(in[i])) bad++; }
    n++;
  }
  printf("word=%d bytes words=%ld bad_bytes=%ld\n", (int)W, n, bad); return bad!=0;
}
