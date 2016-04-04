// Class for Resistive Plate Chamber (RPC) Data Record

#ifndef __l1t_emtf_RPC_h__
#define __l1t_emtf_RPC_h__

#include <boost/cstdint.hpp> 

namespace l1t {
  namespace emtf {
    class RPC {
    public:
      
      explicit RPC(uint64_t dataword);
    
    RPC() : 
      prt_delay(-99), partition_num(-99), partition_data(-99), bcn(-99), lb(-99), link_number(-99), 
	bxn(-99), tbin(-99), eod(-99), bc0(-99), format_errors(0), dataword(-99) 
	{};
      
    RPC(int int_prt_delay, int int_partition_num, int int_partition_data, int int_bcn, int int_lb, int int_link_number, 
	int int_bxn, int int_tbin, int int_eod, int int_bc0) :
      prt_delay(int_prt_delay), partition_num(int_partition_num), partition_data(int_partition_data), bcn(int_bcn), lb(int_lb), link_number(int_link_number), 
	bxn(int_bxn), tbin(int_tbin), eod(int_eod), bc0(int_bc0), format_errors(0), dataword(-99)
    	{};
      
      virtual ~RPC() {};
      
      void set_prt_delay(int bits)      {  prt_delay = bits; };
      void set_partition_num(int bits)  {  partition_num = bits; };
      void set_partition_data(int bits) {  partition_data = bits; };
      void set_bcn(int bits)            {  bcn = bits; };
      void set_lb(int bits)             {  lb = bits; };
      void set_link_number(int bits)    {  link_number = bits; };
      void set_bxn(int bits)            {  bxn = bits; };
      void set_tbin(int bits)           {  tbin = bits; };
      void set_eod(int bits)            {  eod = bits; };
      void set_bc0(int bits)            {  bc0 = bits; };
      void add_format_error()           { format_errors += 1; };
      void set_dataword(uint64_t bits)  { dataword = bits;  };

      const int PRT_delay()      { return  prt_delay ; };
      const int Partition_num()  { return  partition_num ; };
      const int Partition_data() { return  partition_data ; };
      const int BCN()            { return  bcn ; };
      const int LB()             { return  lb ; };
      const int Link_number()    { return  link_number ; };
      const int BXN()            { return  bxn ; };
      const int Tbin()           { return  tbin ; };
      const int EOD()            { return  eod ; };
      const int BC0()            { return  bc0 ; };      
      const int Format_Errors()  { return format_errors; };
      const uint64_t Dataword()  { return dataword;  };      
      
    private:
      int  prt_delay;
      int  partition_num;
      int  partition_data;
      int  bcn; 
      int  lb;
      int  link_number;
      int  bxn; 
      int  tbin;
      int  eod; 
      int  bc0; 
      int  format_errors;
      uint64_t dataword;
      
    }; // End of class RPC

    // Define a vector of RPC
    typedef std::vector<RPC> RPCCollection;

  } // End of namespace emtf
} // End of namespace l1t

#endif /* define __l1t_emtf_RPC_h__ */
