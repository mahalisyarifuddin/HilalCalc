CC ?= cc
CFLAGS ?= -O3 -march=native -DNDEBUG -Wall -Wextra -std=c11
AE_DIR := scripts/vendor/astronomy-engine

.PHONY: astronomy-c-10k astronomy-c-global astronomy-c-baseline land-binary clean

astronomy-c-10k: scripts/astronomy_c_10k
astronomy-c-global: scripts/astronomy_c_global_10k land-binary
astronomy-c-baseline: scripts/astronomy_c_baseline_10k
land-binary: land_polygons.bin

scripts/astronomy_c_10k: scripts/astronomy_c_10k.c $(AE_DIR)/astronomy.c $(AE_DIR)/astronomy.h
	$(CC) $(CFLAGS) -I$(AE_DIR) $< $(AE_DIR)/astronomy.c -lm -o $@

scripts/astronomy_c_global_10k: scripts/astronomy_c_global_10k.c $(AE_DIR)/astronomy.c $(AE_DIR)/astronomy.h
	$(CC) $(CFLAGS) -D_GNU_SOURCE -fopenmp -I$(AE_DIR) $< $(AE_DIR)/astronomy.c -lm -o $@

scripts/astronomy_c_baseline_10k: scripts/astronomy_c_baseline_10k.c $(AE_DIR)/astronomy.c $(AE_DIR)/astronomy.h
	$(CC) $(CFLAGS) -fopenmp -I$(AE_DIR) $< $(AE_DIR)/astronomy.c -lm -o $@

land_polygons.bin: ne_110m_land.geojson scripts/prepare_land_binary.py
	python3 scripts/prepare_land_binary.py $< $@

clean:
	rm -f scripts/astronomy_c_10k scripts/astronomy_c_global_10k scripts/astronomy_c_baseline_10k
