yosys -p 'synth_ecp5 -top Tile -blif build/Tile.blif' build/Tile.v | tee yosys.log
# arachne-pnr -d 8k -o build/Tile.txt build/Tile.blif | tee arachne.log
# icetime -itmd hx4k build/Tile.txt | tee icetime.log
