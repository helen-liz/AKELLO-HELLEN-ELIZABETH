#using lambda with sorted(), using length of words
words=['cherry','Banana','Aate','Apple','Mango','DragonFruit']
sorted_words=sorted(words, key=lambda x: len(x))
print(sorted_words)

