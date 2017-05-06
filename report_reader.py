import pymongo as pm

def connectDB():
	conn = pm.MongoClient('localhost', 27017)
	db = conn.get_database('report_db')
	return db

def getColList(db):
	return db.collection_names()

def getDocNum(col):
	return col.find().count()

def match(col, matchDict):
	return list(col.find(matchDict))

def main():
	db = connectDB()
	print(getColList(db))
	col = db['col20170503']
	print(getDocNum(col))
	print(match(col, {'school':'HFUT'}))

if __name__ == '__main__':
	main()