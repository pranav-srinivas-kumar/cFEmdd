/*
** $Id: cfe_fs_decompress.h 1.7 2012/01/13 12:11:28GMT-05:00 acudmore Exp  $
**
**   File: cfe_fs_decompress.h
**
**      Copyright (c) 2004-2012, United States government as represented by the 
**      administrator of the National Aeronautics Space Administration.  
**      All rights reserved. This software(cFE) was created at NASA's Goddard 
**      Space Flight Center pursuant to government contracts.
**
**      This is governed by the NASA Open Source Agreement and may be used, 
**      distributed and modified only pursuant to the terms of that agreement.
** 
**
**   Author:   A. Cudmore,    NASA/GSFC Code 582
**             Ported from JWST, which was ported from Swift/BAT, 
**             which was ported from the public domain *zip sources.
**  Original Credit:
**
** inflate.c -- Not copyrighted 1992 by Mark Adler version c10p1, 10 January
** 1993
**
** You can do whatever you like with this source file, though I would prefer
** that if you modify it and redistribute it that you include comments to
** that effect with your name and the date.  Thank you. [The history has been
** moved to the file ChangeLog.]
**
** $Log: cfe_fs_decompress.h  $
** Revision 1.7 2012/01/13 12:11:28GMT-05:00 acudmore 
** Changed license text to reflect open source
** Revision 1.6 2012/01/10 18:37:52EST aschoeni 
** CFE return codes set directly; FS_gz_huft_build return code is now properly redefined
** Revision 1.5 2011/01/20 10:49:04EST lwalling 
** Add file ID and change history log to file header
**
*/

#ifndef CFE_FS_decompress_H
#define CFE_FS_decompress_H

#include "cfe.h"
#include "cfe_fs_priv.h"

#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/*
** Defines
*/
#define SH2(p) ((uint16)(uint8)((p)[0]) | ((uint16)(uint8)((p)[1]) << 8))
#define LG(p) ((uint32)(SH2(p)) | ((uint32)(SH2((p)+2)) << 16))
#define NEXTBYTE()  (uint8)( gz_inptr<gz_insize ? gz_inbuf[gz_inptr++] : FS_gz_fill_inbuf() )
#define DUMPBITS(n) { b>>=(n); k-=(n); }
#define NEEDBITS(n) {								\
	while(  k < (n)  )	{								\
		b |= ( (uint32)NEXTBYTE() ) << k;				\
		if ( gGuzError != CFE_SUCCESS ) return gGuzError;	\
		k += 8;									\
	}											\
}
#define BMAX 16
#define N_MAX 288
#define WSIZE 0x8000
#define WSIZE_X2 0x10000L
#define INBUFSIZ 0x8000
#define INBUFSIZ_EXTRA 0x8040
#define OUTBUFSIZ_EXTRA 0x4800
#define MAX_HUF_TABLES 1000
#define EXTHDR 16

/*
** Gzip header information
*/
#define GZIP_MAGIC     "\037\213"   /* Magic header for gzip files, 1F 8B              */
#define OLD_GZIP_MAGIC "\037\236"   /* Magic header for gzip 0.5 = freeze 1.x          */

#define CONTINUATION   0x02         /* bit 1 set: continuation of multi-part gzip file */
#define EXTRA_FIELD    0x04         /* bit 2 set: extra field present                  */
#define ORIG_NAME      0x08         /* bit 3 set: original file name present           */
#define COMMENT        0x10         /* bit 4 set: file comment present                 */
#define ENCRYPTED      0x20         /* bit 5 set: file is encrypted                    */
#define RESERVED       0xC0         /* bit 6,7:   reserved                             */


/*
** Typedefs
*/
typedef struct
{
   uint16 n;
   uint16 t;
   
} HufTableV;

typedef struct
{
   uint8     e;
   uint8     b;
   HufTableV v;
   
} HufTable;



/*
** Fundtion Prototypes
*/
void   FS_gz_clear_bufs( void );
int32  FS_gz_eat_header( void );
int16  FS_gz_fill_inbuf( void );
void   FS_gz_flush_window( void );
int32  FS_gz_huft_build( uint32 * b, uint32 n, uint32 s, uint16 * d, uint16 * e, int32 * m );
int32  FS_gz_inflate( void );
int32  FS_gz_inflate_block( int32 * e );
int32  FS_gz_inflate_codes( HufTable * tl, HufTable * td, int32 bl, int32 bd );
int32  FS_gz_inflate_dynamic( void );
int32  FS_gz_inflate_fixed( void );
int32  FS_gz_inflate_stored( void );
int32  FS_gz_unzip( void );
uint32 FS_gz_updcrc( uint8 * s, uint32 n );


#endif /* CFE_FS_decompress_H */
