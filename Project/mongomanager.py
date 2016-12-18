from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.code import Code
import redis
import pickle  #???
import random

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
        return blog

    # def getClientsList(self):
    #     clients = list(self.db.clients.find())
    #     return clients

    # def getMenuList(self):
    #     menu = list(self.db.menu.find())
    #     return menu

    # def getCouriersList(self):
    #     couriers = list(self.db.couriers.find())
    #     return couriers

    def removeBlog(self, id):
        blog = self.db.blog.find_one({'_id': ObjectId(id)})

        self.db.blogs.delete_one({'_id': ObjectId(id)})
        # self.r.delete(blog["name"]["_id"])

    def saveBlog(self, info):
        name = info['name']
        text = info['text']
        # author = self.db.users.find_one({'_id': ObjectId("boris-t")})
        author = "boris-t"
        comments = []
        topic = info['topic']
        blog_post = {'name': name, 'text': text, 'author': author, 'topic': topic,'comments': comments, 'likes': 0}
        self.db.blogs.insert(blog_post)
        # self.r.delete(ObjectId(info['name']))

    def generate(self):
        topics = ["Competitions", "Lifehacks", "Journeys", "Descriptions", "Technique", "Events", "Other"]
        for i in range (0,50000):
            text = "This is " + str(i) + " blogs post"
            rand_author = random.randint(0,5)
            name = "Blog#" + str(i)
            rand_topic = random.randint(0,5)
            comments = []
            author = self.db.users.find().skip(rand_author).next()
            topic = topics[rand_topic]

            blog_post = {'name': name, 'text': text, 'author': author, 'topic': topic, 'comments': comments, 'likes': 0}
            self.db.blogs.insert(blog_post)
        print "Data generated!"


    def getBlogsByTopic(self,request):
        query = {}
        if request.GET['search_str'] != "":
            query["name"] = str(request.GET['search_str'])
        if request.GET['topic_name'] != "All":
            query["topic"] = str(request.GET['topic_name'])
        print query
        blogs = list(self.db.blogs.find(query))
        return list(blogs)

    def updateBlog(self, info):
        print info
        name = info['name']
        text = info['text']
        author = self.db.users.find_one({'_id': ObjectId(info['author'])})
        comments = []

        blog_post = {'name': name, 'text': text, 'author': author, 'comments': comments, 'likes': 0}

        # last_post = self.db.orders.find_one({'_id': ObjectId(info['name'])})
        # self.r.delete(last_post["name"]["_id"])

        # self.db.orders.update_one({'_id': ObjectId(info['order'])}, {'$set': order})

        # self.r.delete(ObjectId(info['name']))


    # def status(self,request):
    #     if self.r.exists(request.GET['name']) != 0:
    #         return 0
    #     else: return 1

    # def search(self, request):
    #     if self.r.exists(request.GET['name']) != 0:
    #         order = pickle.loads(self.r.get(request.GET['name']))
    #     else:
    #         query = {}
    #         if request.GET['name'] != 0:
    #             query["plate._id"] = ObjectId(request.GET['plate_id'])
    #         order = list(self.db.orders.find(query))
    #         self.r.set(request.GET['plate_id'], pickle.dumps(order))
    #     return list(order)

# db = DataBase()
# db.generate()

