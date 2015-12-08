#include <stdlib.h>
#include <iostream>
#include <iomanip>
#include "EventFilter/EMTFRawToDigi/include/mtf7/block_operator.h"
#include "EventFilter/EMTFRawToDigi/include/mtf7/emutf_debug.h"


//----------------------------------------------------------------------
mtf7::block_operator::block_operator( mtf7::error_value *error_status ):
  _buffer_start_ptr(0), _i_own_buffer(false), _error_status(error_status)
{}

//----------------------------------------------------------------------
const mtf7::word_64bit *mtf7::block_operator::get_buffer_start_ptr()
{ return _buffer_start_ptr; }

//----------------------------------------------------------------------
void mtf7::block_operator::free_own_buffer()
{  
  if (!_i_own_buffer    ) return;
  if (!_buffer_start_ptr) return;
  
  void *ptr = (void *) _buffer_start_ptr;
  
  free( ptr );
  
  _buffer_start_ptr = 0;
  _i_own_buffer = false;
}

//----------------------------------------------------------------------
mtf7::error_value mtf7::block_operator::get_error_status()
{ return *_error_status; }

//----------------------------------------------------------------------
void mtf7::block_operator::break_into_abcd_words( word_64bit input_value ){

  MTF7_DEBUG( std::cout, input_value);

  // AWB 04.12.15
  std::cout << std::hex // Numbers in hexidecimal 
            << std::showbase // Show the 0x prefix
            << std::internal // Fill between the prefix and the number
            << std::setfill('0'); // Fill with 0s

  std::cout << "Inside break_into_abcd_words in src/block_operator.cpp" << std::endl;
  std::cout << "Word abcd: " << std::setw(18) << input_value << std::endl;

/*
  _16bit_word_a = input_value & 0xffff; input_value >>= 16;
  _16bit_word_b = input_value & 0xffff; input_value >>= 16;
  _16bit_word_c = input_value & 0xffff; input_value >>= 16;
  _16bit_word_d = input_value & 0xffff; 
*/

  _16bit_word_d = input_value & 0xffff; input_value >>= 16;
  _16bit_word_c = input_value & 0xffff; input_value >>= 16;
  _16bit_word_b = input_value & 0xffff; input_value >>= 16;
  _16bit_word_a = input_value & 0xffff;
  
    // AWB 04.12.15
  std::cout << "Word a: " << std::setw(6) << _16bit_word_a << std::endl;
  std::cout << "Word b: " << std::setw(6) << _16bit_word_b << std::endl;
  std::cout << "Word c: " << std::setw(6) << _16bit_word_c << std::endl;
  std::cout << "Word d: " << std::setw(6) << _16bit_word_d << std::endl;

  std::cout << std::dec // Numbers in hexidecimal 
            << std::noshowbase; // Show the 0x prefix

}

//----------------------------------------------------------------------
mtf7::word_64bit mtf7::block_operator::merge_abcd_words(){

  mtf7::word_64bit merged_word = 0;

  merged_word |= _16bit_word_d & 0xffff; merged_word <<= 16;
  merged_word |= _16bit_word_c & 0xffff; merged_word <<= 16;
  merged_word |= _16bit_word_b & 0xffff; merged_word <<= 16;
  merged_word |= _16bit_word_a & 0xffff;

  MTF7_DEBUG( std::cout, merged_word);

  return merged_word;

}

mtf7::word_64bit *mtf7::block_operator::create_buffer( unsigned long buffer_size ){

  free_own_buffer();

  if ( buffer_size == 0 ) return 0;

  mtf7::word_64bit *buffer = (mtf7::word_64bit*) calloc( sizeof( mtf7::word_64bit ), buffer_size );

  _buffer_start_ptr = buffer;
  _i_own_buffer = true;

  return buffer;

}
     
