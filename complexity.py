import nltk

class Complexity:

	def __init__(self,corpora):
		self.corpora = corpora
		self.freq = nltk.FreqDist(self.corpora)

	def complexityVowel(self,word):
		points = 0.0001

		vowel = 'aeiou'
		for index in xrange(1,len(word)):
			A = word[index-1]
			B = word[index]

			if A in vowel:
				points += 1
				if B in vowel:
					points -= 0.2

		return points

	def complexityConsoant(self,word):
		points = 0.0001

		consoant = 'bcdfghjklmnpqrstvxyzw'

		for index in xrange(1,len(word)):
			A = word[index-1]
			B = word[index]

			if A in consoant:
				points += 2
				if B in consoant:
					points += 0.3

		return points

	def complexityLetter(self,word):
		wheigths = {'a': 3, 'c': 7, 'b': 2, 'e': 3, 'd': 2, 'g': 3, 'f': 4,
					 'i': 3, 'h': 4, 'k': 2, 'j': 4, 'm': 1, 'l': 3, 'o': 2,
					  'n': 1, 'q': 2, 'p': 3, 's': 4, 'r': 2, 'u': 2, 't': 2,
					   'w': 5, 'v': 4, 'y': 3, 'x': 4}
		points = 0

		for letter in word:
			points += wheigths[letter]

		return points/float(len(word))

	def complexitySize(self,word):
		return len(word)

	def complexityPatterns(self,word):
		patterns = {'th':-0.2,'ph':-0.2,'nt':-0.2}
		points = 0.0001

		if word[-1] in 'ms':
			points -= 0.4

		if word[-1] in 'aeiou':
			points -= 0.2

		for index in xrange(1,len(word)):
			P = word[index-1:index+1]
			if P in patterns:
				points += patterns[P]
			elif P[0]=='s' and P[1] not in 'aeiou':
				points -= 0.3

		return points

	def complexityFrequency(self,word):
		return self.freq.freq(word)

	def compute(self,word):
		f = self.complexityPatterns(word)/self.freq.freq(self.freq.most_common(1)[0][0])
		frequency = min(1,1.0/f)

		if word[0] not in 'abcdefghijklmnopqrstuvxyzw':
			return 1-f

		vowel    = min(1,1.0/self.complexityVowel(word))
		consoant = min(1,1.0/self.complexityConsoant(word))	
		letter   = min(1,1.0/self.complexityLetter(word))
		size     = min(1,1.0/self.complexitySize(word))
		patterns = max(0.5,self.complexityPatterns(word))
		
		return 1- ((vowel+consoant*2+letter*1.5+size*3+patterns*.5+frequency*2.0)/10.0)

# f = open('corpora.txt').read().lower()
# dicionary = nltk.word_tokenize(f.decode('utf-8'))

# C = Complexity(dicionary)


# print 'gigger',C.compute('gigger')
# print 'thougth',C.compute('thought')
# print 'differing',C.compute('differing')
# print C.compute('sweet')
# print C.compute('summer')
# print 'triggered',C.compute('triggered')
# print 'electrified',C.compute('electrified')
# print 'james',C.compute('james')
# print 'he',C.compute('he')
# print 'the',C.compute('the')
# print 'they',C.compute('they')


