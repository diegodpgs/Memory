import time
import random
import nltk
from complexity import Complexity

#@Author: Diego Pedro
#@Date  : April 10, 2016
class Memory:

	def __init__(self,records_file_name,corpora_file_name):
		self.bucket = []
		self.records = []
		self.dictionary = []
		self.parseRecords(records_file_name)
		self.write_records = open(records_file_name,'a')
		self.readCorpora(corpora_file_name)
		self.states = {'1':'Very Good','2':'Good','3':'Some Tired',
					   '4':'Tired','5':'Very Tired','6':'Some Sleep','7':'Sleep','8':'Very Sleep'}
		self.errors = []
		self._complex_ = Complexity(self.dictionary)

	def readCorpora(self,corpora_file_name):
		f = open(corpora_file_name).read().lower()
		self.dictionary = nltk.word_tokenize(f.decode('utf-8'))

	def parseRecords(self,records_file_name):
		file_records = open(records_file_name)
		records_file = file_records.read().split('\n')

		for record in records_file[1:-1]:

			record_time = record.split(',')[0]
			record_date = record.split(',')[1]
			record_days = int(record.split(',')[2])
			record_mark = int(record.split(',')[3])
			record_state = record.split(',')[4]
			record_timing = float(record.split(',')[5])
			record_complexity = float(record.split(',')[6])
			record_word_size = len("".join(record.split(',')[7:]))

			data = (record_mark,record_word_size,record_complexity,record_timing,record_date,record_time,record_days,record_state)
			self.records.append(data)

		file_records.close()

	def getPositionINDEX(self,bucket_size,mark,timing):
		
		records_copy = self.records[:]
		records_copy.append((mark,bucket_size,timing,'mark'))
		records_copy.sort()
		records_copy = records_copy[::-1]
		
		index_mark = 0

		while index_mark < len(records_copy):
			if records_copy[index_mark][3] == 'mark':
				return index_mark

			index_mark += 1

	def getPreviousRecord(self,position):
		self.records.sort()
		return self.records[::-1][position]

	def getAttr(self,record,attr):
		attrs = ['mark','word_size','complexity','timing','date','time','days','state']

		for index in xrange(len(attrs)):
			at = attrs[index]

			if attr == at:
				return record[index]

	def printTable(self,record):
		state = self.states[self.getAttr(record,'state')]
		mark = str(self.getAttr(record,'mark'))
		word_size = str(self.getAttr(record,'word_size'))
		complexity = '%1.2f' % (self.getAttr(record,'complexity'))
		timing = '%1.2f' % (self.getAttr(record,'timing'))
		day = str(time.localtime().tm_yday - self.getAttr(record,'days'))


		print '%s %s %s %s %s   |%s ' % (mark.rjust(4),
													word_size.rjust(4),
													complexity.rjust(8),
													timing.rjust(8),
													day.rjust(5),
													state.rjust(11))

	def printRecord(self,record,table_print=False):

		
		if table_print:
			self.printTable(record)
		else:
			print '\n     %d Days ago   ' % (time.localtime().tm_yday - self.getAttr(record,'days'))
			print 'Mark:        %d' % self.getAttr(record,'mark')
			print 'Word Size:   %d' % self.getAttr(record,'word_size')
			print 'Complexity:  %1.2f' % self.getAttr(record,'complexity')
			print 'Timing:      %1.2f' % self.getAttr(record,'timing')
			print 'Date:        %s' % self.getAttr(record,'date')
			print 'Time:        %s' % self.getAttr(record,'time')
			print 'State:       %s' % self.getAttr(record,'state')

	def printRecords(self):
		self.records.sort()
		
		print '\n\n\nRank|Words|Char|Complexity|Timing|Days Ago|   State'
		for index in xrange(len(self.records)):
			r = self.records[::-1][index]
			print '%s |' % (str(index+1).rjust(3)),
			self.printRecord(r,True	)

	def getMostRecent(self,timing,worst=False):

		recents = []
		
		for r in self.records:
			
			data = (365-r[-2],r[0],r[1],r[2],r[3],r[-1])
			recents.append(data)

		recents.sort()
		

		b = len(self.bucket)-1
		ws = len("".join(self.bucket[0:-1]))
		results = []
		days_mark = 0
		index = 0

		while not ((days_mark != 0 and days_mark !=recents[index][0] and len(results)>0) or index >= len(recents)):
			r_recent = recents[index]
			
		 	actual_data = (b,ws,timing)
		 	recent_data = (r_recent[1],r_recent[2],r_recent[3],r_recent[4],r_recent[5],'%d days ago' % (time.localtime().tm_yday-(365-r_recent[0])))
		 	

			if not worst:
				if actual_data < recent_data:
					results.append(recent_data)
					days_mark = recent_data[-1]
			else:
				if actual_data > recent_data:
					results.append(recent_data)
					days_mark = recent_data[-1]

			index += 1


		print results[-1]

	def printResult(self,timing):
		bucket_size = len("".join(self.bucket[0:-1]))
		mark = len(self.bucket)-1

		position = self.getPositionINDEX(bucket_size,mark,timing)
		

		print '######\n You have achieved %d words\n with total size %d\n timing: %1.2f and complexity %1.2f' % (mark,bucket_size,timing,self.complexity())

		if position == len(self.records):
			print "This is the worst result ever"
		else:
			previousRecord = self.getPreviousRecord(position)

			if position == 0:
				print "This is a new record. The last was" 

			else:
				print "This mark is ranked %d out of %d. The best was from " % (position+1,len(self.records)+1)
				print "The most best recent result is:",
				self.getMostRecent(timing)
				print "The most worst recent result is:",
				self.getMostRecent(timing,True)


			print '\n----------The previous best results was------\n'
			self.printRecord(previousRecord)

	def generateNewWord(self):

		word = self.dictionary[random.randint(0,len(self.dictionary)-1)]

		while word in self.bucket:
			word = self.dictionary[random.randint(0,len(self.dictionary)-1)]

		return word	

	def diferenceTime(self,record_date):
		year = time.localtime().tm_year - int(record_date[1].split('/')[-1])
		day =  time.localtime().tm_yday - int(record_date[2])

		return year*365 + day

	def processWord(self):

		for index in xrange(len(self.bucket)):
			w = self.bucket[index]
			word = raw_input(': ')

			if word != w:
				print 'The correct word is <%s> instead of <%s>' % (w,word)
				print 'TYPE EVERYTHING AGAIN'
				print ' '.join(self.bucket)
				time.sleep(1+len(self.bucket)/2.5)
				print '\n'*120
				self.errors.append((self.bucket[:],index))
				return 'ERROR'

		return 'OK'
	
	def writeRecords(self,timing):
		
		state = raw_input("Type your state:\n\n1:Very Good\n2:Good\n3:Some Tired\n4:Tired\n5:Very Tired\n6:Some Sleep\n7:Sleep\n8:Very Sleep\n\n:: ")
		self.write_records.write('%s,%s,%d,%d,%s,%1.2f,%1.2f,%s\n' % (time.strftime('%H:%M:%S'),
														time.strftime('%d/%m/%Y'),
														time.localtime().tm_yday,
														len(self.bucket)-1,
														state,
														timing,
														self.complexity(),
														','.join(self.bucket[0:-1])))
		self.records.append((len(self.bucket)-1,
							 len(''.join(self.bucket[0:-1])),
							 self.complexity(),
							 timing,
							 time.strftime('%d/%m/%Y'),
							 time.strftime('%H:%M:%S'),
							 time.localtime().tm_yday,
							 state))

	def play(self):

		while True:
			begin = time.time()
			word = self.generateNewWord()
			print 'the first word is <%s>:' % word
			self.bucket = [word]

			errors = 0

			while errors < 5:

				print 'Type the words: '

				if self.processWord() != 'ERROR':
					word = self.generateNewWord()
					
					while not word.isalpha():
						word = self.generateNewWord()

					self.bucket.append(word)
					print 'THE NEW WORD IS:  ',word
					time.sleep(1.5)
					print '\n'*120
				else:
					errors += 1

			if len(self.bucket) == 1:
				print 'You did not get any right words. No data was recorded'
			else:
				timing = 100-(time.time()-begin)/float(len("".join(self.bucket[0:-1])))
				self.printResult(timing)
				self.writeRecords(timing)
			
			option= raw_input('Do you want continue? y/n ')
			

			if option != 'y':
				
				option= raw_input('Do you want see the records? y/n ')
				
				if option == 'y':
					self.printRecords()

				errors_file = open('word_errors.txt','a')
				for line in self.errors:
					errors_file.write('%s;%d\n' % (",".join(line[0]),line[1]))

				break

	def wordComplexity(self,word):
		return self._complex_.compute(word)

	def complexity(self):
		total_complexity = 0

		for word in self.bucket[0:-1]:
			total_complexity += self.wordComplexity(word)

		return  (total_complexity/float(len(self.bucket[0:-1])))*10
		

if "__main__":
	#PROPOSE A BETTER COMPLEXITY USING SPEECH PARSER PRE(she) + VER(is) + ADV(very) + ADJ(pretty) 
	# M = Memory('records.txt','corpora.txt')
	# #M.play()

	# rec = open('records.txt').read().split('\n')
	
	# for r in rec[1:-1]:
	# 	r = r.split(',')
	# 	words =  r[7:]
	# 	words.append('$')
	# 	M.bucket = words
	# 	p1 = r[0:6]
	# 	c = M.complexity()
	# 	p2 = r[7:]

	# 	print '%s,%1.2f,%s' % (",".join(p1),c,",".join(p2))
	# M.printRecords()












