from datetime import datetime, timedelta


lundi = '2022-11-14'
mardi = '2022-11-15'
mercredi = '2022-11-16'
jeudi = '2022-11-17'
vendredi = '2022-11-18'
samedi = '2022-11-19'
dimanche = '2022-11-20'

day_of_the_week = datetime.strptime(lundi, '%Y-%m-%d').weekday()
print('lundi', day_of_the_week)

day_of_the_week = datetime.strptime(mardi, '%Y-%m-%d').weekday()
print('mardi', day_of_the_week)

day_of_the_week = datetime.strptime(mercredi, '%Y-%m-%d').weekday()
print('mercredi', day_of_the_week)

day_of_the_week = datetime.strptime(jeudi, '%Y-%m-%d').weekday()
print('jeudi', day_of_the_week)

day_of_the_week = datetime.strptime(vendredi, '%Y-%m-%d').weekday()
print('vendredi', day_of_the_week)

day_of_the_week = datetime.strptime(samedi, '%Y-%m-%d').weekday()
print('samedi', day_of_the_week)

day_of_the_week = datetime.strptime(dimanche, '%Y-%m-%d').weekday()
print('dimanche', day_of_the_week)

print('LUNDI')
date = datetime.strptime(lundi, '%Y-%m-%d')
day_of_the_week = date.weekday()
l = date - timedelta(days=day_of_the_week)
d = date + timedelta(days=(6 - day_of_the_week))
print('lundi', l)
print('dimanche', d)

print('MARDI')
date = datetime.strptime(mardi, '%Y-%m-%d')
day_of_the_week = date.weekday()
l = date - timedelta(days=day_of_the_week)
d = date + timedelta(days=(6 - day_of_the_week))
print('lundi', l)
print('dimanche', d)

print('MERCREDI')
date = datetime.strptime(mercredi, '%Y-%m-%d')
day_of_the_week = date.weekday()
l = date - timedelta(days=day_of_the_week)
d = date + timedelta(days=(6 - day_of_the_week))
print('lundi', l)
print('dimanche', d)

print('JEUDI')
date = datetime.strptime(jeudi, '%Y-%m-%d')
day_of_the_week = date.weekday()
l = date - timedelta(days=day_of_the_week)
d = date + timedelta(days=(6 - day_of_the_week))
print('lundi', l)
print('dimanche', d)

print('VENDREDI')
date = datetime.strptime(vendredi, '%Y-%m-%d')
day_of_the_week = date.weekday()
l = date - timedelta(days=day_of_the_week)
d = date + timedelta(days=(6 - day_of_the_week))
print('lundi', l)
print('dimanche', d)

print('SAMEDI')
date = datetime.strptime(samedi, '%Y-%m-%d')
day_of_the_week = date.weekday()
l = date - timedelta(days=day_of_the_week)
d = date + timedelta(days=(6 - day_of_the_week))
print('lundi', l)
print('dimanche', d)

print('DIMANCHE')
date = datetime.strptime(dimanche, '%Y-%m-%d')
day_of_the_week = date.weekday()
l = date - timedelta(days=day_of_the_week)
d = date + timedelta(days=(6 - day_of_the_week))
print('lundi', l)
print('dimanche', d)