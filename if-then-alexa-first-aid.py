#burns
if userBurned:
	if severe:
		if ask(callHelp):
			call('emerg', 'severe burn')
			#take further instructions from emergency services
	else:
		instruct(set([coldWater, nonstickBandage]))
	lastCheck()

cuts
sprain ankle
FLU

#chest pain
if chestPain:
	if ask(callHelp):
		call('emerg', 'chest pain')
	else:
		heartThreat = check(heartSymptoms)
		if heartThreat > 2:
			if ask(callHelpRetry):
				call('emerg', 'chest pain and other symptoms suggestive of myocardial infarction')
			else:
				instruct(rest)
	lastCheck()

#non-emergency
if nonEmerg:
	if ask(callEMT):
		reason = ask(why)
		comments = ask(details)
		call('EMT', reason, comments)
	else:
		#book dr appt?
	lastCheck()

def instruct(setOfInstructns):
	pass

def check(symptoms):
	symptomCount = 0
	if symptoms == heartSymptoms:
		for symptom in ['left arm or jaw in pain or tingling','heaviness or pressure on chest','dizzy, cold, nauseous, or sweaty']:
			if ask(symptom):
				symptomCount += 1
	return symptomCount

def lastCheck():
	#ask user if there is anything else we can do to help

def ask(query):
	if query == callHelp:
		#ask user if we should call emergency services and request prompt medical assistance
			#if they say yes, return True
	elif query == callHelpRetry:
		#ask user to confirm that they do not want help. it seems serious!
			#if they say yes, return True
	elif query == callEMT:
		#ask user if we should call EMT and ask for a (non-time sensitive) drop by when they are in the area
			#if they say yes, return True

def call(toWhom, why):
	if toWhom == 'emerg':
		#place call to emergency services, stating why