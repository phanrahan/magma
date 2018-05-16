import shutil
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

test_pairs = [
    ("test_circuit/build/test_add8cin.json", "test_circuit/gold/test_add8cin.json"),
    ("test_coreir/mapParallel_test.json", "test_coreir/mapParallel_test_gold.json")
]

for output, gold in test_pairs:
    output = os.path.join(dir_path, output)
    gold = os.path.join(dir_path, gold)
    shutil.copy(output, gold)
