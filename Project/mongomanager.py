from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.code import Code
import redis
import pickle  #???
import random
import datetime

class DataBase:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.globedb
        self.r = redis.StrictRedis()

    def saveUser(self, info):
        login = str(info['login'])
        email = str(info['email'])
        first_name = str(info['name'])
        second_name = str(info['surname'])

        user = {'login': login, 'email' : email, 'first_name': first_name, 'second_name': second_name}

        self.db.users.insert(user)

    def getAllBlogs(self):
        blogs = [blog for blog in self.db.blogs.find()]
        return blogs

    def getBlog(self, id):
        blog = self.db.blogs.find_one({'_id': ObjectId(id)})
        if self.r.exists(ObjectId(id))!= 0:
            blogs = pickle.loads(self.r.get(ObjectId(id)))
            print "Using cache"
        else:
            query = {}
            if id != 0:
                query["_id"] = ObjectId(id)
            blog = self.db.blogs.find_one({'_id': ObjectId(id)})
            self.r.set(ObjectId(id), pickle.dumps(blog))
            print "Without cache"
        return blog

    def removeBlog(self, id):
        self.db.blogs.delete_one({'_id': ObjectId(id)})
        self.r.delete(ObjectId(id))

    def saveBlog(self, info):
        name = info['name']
        text = info['text']
        # author = self.db.users.find_one({'_id': ObjectId("boris-t")})
        author = "boris-t"
        topic = info['topic']
        blog_post = {'name': name, 'text': text, 'author': author, 'topic': topic, 'likes': 0, 'datetime': datetime.datetime.now()}
        self.db.blogs.insert(blog_post)

        # query = {}
        # if self.r.exists(str(query)) != 0:
        #     print "exist"
        #     self.r.delete(str(query))
        # query['name'] = name
        # if self.r.exists(str(query)) != 0:
        #     print "exist"
        #     self.r.delete(str(query))
        #
        # query = {}
        # query['topic'] = topic
        # if self.r.exists(str(query)) != 0:
        #     print "exist"
        #     self.r.delete(str(query))
        #
        # query = {}
        # query['name'] = name
        # query['topic'] = topic
        # if self.r.exists(query) != 0:
        #     self.r.delete(query)

    def generate(self):
        topics = ["Competitions", "Lifehacks", "Journeys", "Descriptions", "Technique", "Events", "Other"]
        for i in range (0,50000):
            text = "This is " + str(i) + " blogs post"
            rand_author = random.randint(0,5)
            name = "Blog#" + str(i)
            rand_topic = random.randint(0,5)
            author = self.db.users.find().skip(rand_author).next()
            topic = topics[rand_topic]

            blog_post = {'name': name, 'text': text, 'author': author, 'topic': topic, 'likes': 0, 'datetime': datetime.datetime.now()}
            self.db.blogs.insert(blog_post)


    def getBlogsByTopic(self,request):
        query = {}
        if request.GET['search_str'] != "":
            query["name"] = str(request.GET['search_str'])
        if request.GET['topic_name'] != "All":
            query["topic"] = str(request.GET['topic_name'])
        print query
        # blogs = list(self.db.blogs.find(query))
        # return list(blogs)
        return self.search(query)


    def getBlogsByAuthor(self,login):
        blogs = self.db.blogs.find({'author.login': str(login)})
        return blogs

    # def status(self,request):
    #     if self.r.exists(request.GET['name']) != 0:
    #         return 0
    #     else: return 1

    def search(self, query):
        if self.r.exists(query) != 0:
            blogs = pickle.loads(self.r.get(query))
            print "Using cache"
        else:
            blogs = list(self.db.blogs.find(query))
            self.r.set(query, pickle.dumps(blogs))
            print "Without cache"
        return blogs

    def getCommentsByBlog(self, id):
        comments = [comment for comment in self.db.comments.find({'blog_id': ObjectId(id)})]
        return comments

    def addCommentToBlog(self, id, info):
        self.db.comments.insert({'username': info['username'], 'text': info['text'], 'datetime': info['datetime'], 'blog_id': ObjectId(id)})
        print "Success"

    def createTimeInfo(self):
    # def getMostCommented(self):
    #     blogs = list(self.db.comments.aggregate(
    #
    #     ))


    def getMostActiveUsers(self):
        users = list(self.db.comments.aggregate(
            [{"$project": {"username": "$username", "count": {"$add": [1]}}},
             {"$group": {"_id": "$username", "number": {"$sum": "$count"}}}, {"$sort": {"number": -1}}, {"$limit": 5}]))
        print users
        return users

    def getMostWritingUsers(self):
        users = list(self.db.blogs.aggregate(
            [{"$project": {"username": "$author.login", "count": {"$add": [1]}}},
             {"$group": {"_id": "$username", "number": {"$sum": "$count"}}},
             {"$sort": {"number": -1}}, {"$limit": 10}]
        ))
        print users
        return users


    # def getTopClientsAggregate(self):
    #     clients = list(self.db.orders.aggregate(
    #         [{"$unwind": "$client.name"}, {"$project": {"name": "$client.name", "count": {"$add": [1]}}},
    #          {"$group": {"_id": "$name", "number": {"$sum": "$count"}}}, {"$sort": {"number": -1}}, {"$limit": 3}]))
    #     print clients
    #     return clients


    # def getCacheLoadingTime(self):
    #
    #
    # def getMongoLoadingTime(self):



db = DataBase()
# db.generate()
# db.getMostActiveUsers()
db.getMostWritingUsers()
