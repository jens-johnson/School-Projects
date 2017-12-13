#include <stdio.h>

/*
Christopher Johnson

A simple implementation of a 64B direct-mapped cache.
*/


struct cache_block{
	/*
	Cache block struct, contains valid (1 for valid, 0 for invalid), tag (first 26b of an address),
	and value(a 4B hex string)
	*/
	unsigned int valid;
	unsigned int tag;
	unsigned char value[4];
};


struct cache_block cache[16]; // Our 64B, 16-set cache represented by an array of cache_blocks


void eviction(unsigned set){
	/*
	Called by main to 'evict' a block from the cache [in reality this procedure is simply a print
	procedure as we are changing the tag and value in main]
	*/
	unsigned tag = cache[set].tag;
	unsigned valid = cache[set].valid;
	printf("evicting block - set: %d - tag: %d - valid: %d - value: %02x %02x %02x %02x\n", set, tag, valid, cache[set].value[0], cache[set].value[1], cache[set].value[2], cache[set].value[3]);
}

int main(){
	char action[1];
	action[0] = ' ';
	while (action[0] != 'q'){
		printf("Enter 'r' for read, 'w' for write, 'p' to print, 'q' to quit: ");
		scanf("%s", &action[0]);
		if (action[0] == 'r'){
			/*
			Read case
			*/
			unsigned read_address;
			printf("Enter a 32-bit unsigned hex address: ");
			scanf(" %x", &read_address);
			unsigned set = (read_address << 26) >> 28; // Set: The 27th-30th bits of the address
			unsigned tag = read_address >> 6; // Tag: The first 26 bits of the address
			unsigned offset = (read_address << 30)>>30; // Offest: the last 2 bits of the address
			printf("looking for set: %d - tag: %d\n", set, tag);
			if (cache[set].valid == 0){
				printf("no valid set found - miss!\n"); // Set is invalid
			}
			if (cache[set].valid != 0){ // Case where set is valid and found
				printf("found set: %d - tag: %d - offset: %d - valid: 1 - value: %02x\n", set, tag, offset, cache[set].value[offset]);
				if (cache[set].tag == tag){ // If tags match, we have a hit
					printf("hit!\n");
				}
				else{
					printf("tags don't match - miss!\n");
				}
			}
		}
		if (action[0] == 'w'){
			/*
			Write case
			*/
			unsigned write_address;
			unsigned write_value;
			printf("Enter a 32-bit unsigned hex address: ");
			scanf(" %x", &write_address);
			printf("Enter a 32-bit unsigned hex value: ");
			scanf(" %x", &write_value);
			unsigned set = (write_address << 26) >> 28; // Set: The 27th-30th bits of the address
			unsigned tag = write_address >> 6; // Tag: The first 26 bits of the address
			if (cache[set].valid != 0){ // Evict the block if necessary
				eviction(set);
			}
			cache[set].valid = 1;
			cache[set].tag = tag;
			for (int i = 0; i < 4; i++){
				cache[set].value[i] = (write_value >> (i << 3)) & 0xff; // Isolate a single byte of the block value
			}
			printf("wrote set: %d - tag: %d - valid: 1 - value: %02x %02x %02x %02x\n", set, tag, cache[set].value[0], cache[set].value[1], cache[set].value[2], cache[set].value[3]);
		}
		if (action[0] == 'p'){
			/*
			Print case
			*/
			for (int n=0; n<16; n++){
				if (cache[n].valid != 0){
					/*
					Print every valid set in the cache
					*/
					printf("set: %d - tag: %d - valid: 1 - value: %02x %02x %02x %02x\n", n, cache[n].tag, cache[n].value[0], cache[n].value[1], cache[n].value[2], cache[n].value[3]);
				}
			}
		}
	}
}