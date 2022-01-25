

counts = {3: 1515, 5: 3429, 4: 3527, 7: 1110, 6: 2089, 9: 279, 8: 576, 10: 155, 11: 85, 2: 144, 14: 8, 12: 32, 1: 1, 13: 18, 15: 3, 16: 1}
num = 0
for key, value in counts.items():
    if key >= 7:
        num += value
total = sum(counts.values())
print(total)
print(num)
print(num / total)
# words = []
# with open('input/only_solutions.txt', 'r') as infile:
#     for line in infile.readlines():
#         words.extend(line.replace("\"", "").replace("[", "").replace("]", "").split(", "))
#
# words = sorted(list(set(words)))
#
# with open("input/words_v5.txt", 'w') as outfile:
#     for word in words:
#         word = word.strip()
#         outfile.write(word + "\n")
