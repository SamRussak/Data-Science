import pandas as pd
import sys
import csv
import string
from itertools import chain, combinations
from collections import defaultdict

#Get user inputs from command line
userInput = sys.argv
input_filename = userInput[1]
output_filename = userInput[2]
min_support_percentage = userInput[3]
min_confidence = userInput[4]

#initiate variable sets and lists for apriori
transactionList = list()
itemSet = set()
freqSet = defaultdict(int)
finalSet = dict()
sets = list()
rules = list()

#print out sets
def printSet():
	with open(output_filename, 'w') as fp:
		a = csv.writer(fp)       
		for item, supp in sorted(sets, key=len):
			item = sorted(item, key=lambda item: item[0])
			data = "Set, {}, {}".format(supp, ",".join(item))
			a.writerow([data])		
#print out rules
def printRule():
	with open(output_filename, 'a') as fp:
		a = csv.writer(fp)       
		for left, right, supp, conf in sorted(rules, key=lambda item: item[0]):		
			data = "Rule, {}, {}, {} => {}".format(supp, conf, ",".join(left), ",".join(right))
			a.writerow([data])				

#find if items have min supports
def getMinSupp(item_set):
	try:
		temp_set = set()
		tempFreqSet = defaultdict(int)
		for i in item_set:
		    for transaction in transactionList:
		        if i.issubset(transaction):
		            freqSet[i] += 1
		            tempFreqSet[i] += 1

		for i, count in tempFreqSet.items():
		    support = float(count)/float(len(transactionList))
		    if(support >= float(min_support_percentage)):
		        temp_set.add(i)  
		return temp_set      
	except:
		print("Unable to get Minimum Support")
		sys.exit()

#union sets to create K+1 size elements
def unionSets():
	try:		
		return set([x.union(y) for x in loopSet for y in loopSet if len(x.union(y)) == counter])
	except:
		print("Unable to union sets")
		sys.exit()

#gets supset of itemset
def getSubset(itemset):
	#for i, a in enumerate(itemset):
		#print("{} {}".format(i,a))
	try:
		return chain(*[combinations(itemset, i + 1) for i, a in enumerate(itemset)])
	except:
		print("Unable to get subsets")
		sys.exit()

#create list of transactions
try:
	with open(input_filename, "r") as f:
		reader = csv.reader(f, delimiter=",")	
		for record in reader:
			transaction = frozenset(record[1:])
			transactionList.append(transaction)
			for item in transaction:
				itemSet.add(frozenset([item]))
except:
	print("Unable to read input file") 
	sys.exit()
        
#get all items with min support percentage
try:
	loopSet = getMinSupp(itemSet)
	counter = 2
	while(True):
		finalSet[counter-1] = loopSet
		loopSet = unionSets()
		temp_set = getMinSupp(loopSet)
		if(temp_set == set([])):
			break
		loopSet = temp_set
		counter += 1
except:
	print("unable to loop through list to get minsupp")
	sys.exit()

try:
	#Generate Rules
	for i, support in finalSet.items():
		for value in support:
			temp_set = [frozenset(x) for x in getSubset(value)]
			#for i in temp_set:
				#print(i)
			for left in temp_set:
				#print(left)
				right = value.difference(left)
				if(len(right) > 0):
					left = frozenset(left)
					combine = left.union(right)# right				
					supp = float(freqSet[combine])/len(transactionList)
					#print(supp)
					conf = float(freqSet[combine]) / float(freqSet[left])
					#print(conf)
					if(conf >= float(min_confidence)):
						rules.append((sorted(left, key=lambda item: item[0]), sorted(right, key=lambda item: item[0]), supp, conf))
except:
	print("Unable to get association rules")
	sys.exit()
	
#put itemsets into list for print out
for key, value in finalSet.items():
	for item in value:
		supp = float(freqSet[item])/len(transactionList)	
		#print(supp)
		sets.extend([(tuple(item), supp)])

#call print methods
printSet()
printRule()