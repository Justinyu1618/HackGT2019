
art_lines = []
f = open("pong.txt", "r")
f1 = f.readlines()
for line in f1:
  art_lines.append(line)

for i in range(len(art_lines)):
  print(art_lines[i])
  print(len(art_lines[i])//2)