#!/usr/bin/env python3

from blog.models import Post, UserProfile, Category

#u = User(name="Erik Perillo", role="admin")
#u.save()
#u = User(name="Maria Eugenia", role="author")
#u.save()

c = Category(title="Random")
c.save()
c = Category(title="Robotics")
c.save()
c = Category(title="Computer Vision")
c.save()

#p = Post(title="ey b0ss", body="This is a test post.",
#        author=User.objects.filter(name="Erik Perillo")[0],
#        category=Category.objects.filter(title="Random")[0])
#p.save()
#p = Post(title="what a great time to be alive", body="Right?",
#        author=User.objects.filter(name="Erik Perillo")[0],
#        category=Category.objects.filter(title="Robotics")[0])
#p.save()
#p = Post(title="shiiit", body="Whaaat the hell?",
#        author=User.objects.filter(name="Maria Eugenia")[0],
#        category=Category.objects.filter(title="Random")[0])
#p.save()
