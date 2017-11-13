# import xml.etree.ElementTree as etree
import lxml
from lxml import etree
import codecs
import os
from datetime import datetime
import csv
from tqdm import tqdm
# from neo4j.v1 import GraphDatabase
# uri = 'bolt://127.0.0.1:7687'
# driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"))

# with driver.session() as session:
#     with session.begin_transaction() as tx:
#         statement = 'CREATE (a:Comment {id:{id},postid:{postid}, score:{score},' \
#                     'text:{text}, creationdate:{creationdate}, userid:{userid}})'
#         for event, elem in tqdm(etree.iterparse('../data/Comments.xml')):
#             epoch_dt = ''
#             print(elem.items())
#             if elem.get('CreationDate') != None:
#                 epoch_dt = datetime.strptime(elem.get('CreationDate'), '%Y-%m-%dT%H:%M:%S.%f').timestamp()
#             tx.run(statement, id=elem.get('Id'), postid=elem.get('PostId'), score=elem.get('Score'),
#                    text=elem.get('Text'), creationdate=epoch_dt, userid=elem.get('UserId'))
#     tx.commit()
# driver.close()

MAX_LINES = 100000 # write 100 at a time.
# MAX_REC = 50000000

# Helper methods
def clean(x):
    #neo4j-import doesn't support: multiline (coming soon), quotes next to each other and escape quotes with '\""'
    if x == None:
        return ''
    return x.replace('\n','').replace('\r','').replace('\\','').replace('"','')

def open_csv(name):
    return csv.writer(open('../csvs/{}.csv'.format(name), 'w'), doublequote=False, escapechar='\\')

def cal_epoch(datestring):
    if datestring:
        return str(datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%S.%f').timestamp())
    else:
        return ''

def ascii_encode(list):
    return [u''.join(s).encode('ascii', 'ignore').decode('ascii') for s in list]

# Nodes Headers
badgesHeader = ['BadgeID:ID(BadgeId)',':LABEL'] ##!!!!!! Sort this out.
postsHeader = ['PostID:ID(PostId)', 'CreationDate:float', \
               'Score', 'ViewCount', 'Body',  \
               'LastActivityDate:float', 'CommunityOwnedDate:float', 'ClosedDate:float',\
               'Title', 'Tags', 'AnswerCount', 'CommentCount', 'FavoriteCount']

tagsHeader = ['TagId:ID(TagId)',':LABEL'] #tag name
votesHeader = ['VoteId:ID(VoteId)','VoteTypeId','CreationDate','BountyAmount',':LABEL']


# Relationship Headers
badges_rel_header = [':START_ID(UserId)','Date',':END_ID(BadgeId)',':TYPE']
posts_rel_header = [':START_ID(PostId)',':END_ID(PostId)', ':TYPE']
posts_ans_header = [':START_ID(PostId)',':END_ID(PostId)', ':TYPE']
posts_lastedit_header = [':START_ID(UserId)', 'LastEditDate:float',':END_ID(PostId)', ':TYPE']
posts_owner_header = [':START_ID(UserId)',':END_ID(PostId)',':TYPE']
tags_rel_header = [':START_ID(PostId)',':END_ID(TagId)', ':TYPE']
postlinksHeader = [':START_ID(PostId)','CreationDate:float',':END_ID(PostId)',':TYPE']
commentsHeader = [':START_ID(UserId)','Score', 'Text', 'CreationDate:float',':END_ID(PostId)', ':TYPE']
votes_rel_header = [':START_ID(VoteId)',':END_ID(PostId)',':TYPE']
votes_fav_header = [':START_ID(UserId)',':END_ID(VoteId)',':TYPE']
"""
usersHeader = ['UserId:ID(UserId)','Reputation:int','CreationDate:float', 'DisplayName', 'LastAccessDate', \
               'WebsiteUrl', 'Location', 'Age', 'AboutMe', 'Views',':LABEL']
users = open_csv('users')

user_batch = []
users.writerow(usersHeader)
# counter = 0
for event, elem in tqdm(etree.iterparse('../data/Users.xml',encoding="utf-8", recover=True)):
    UserId = clean(elem.get('Id'))
    Reputation = clean(elem.get('Reputation'))
    CreationDate = cal_epoch(elem.get('CreationDate'))
    DisplayName = clean(elem.get('DisplayName'))
    LastAccessDate = cal_epoch(elem.get('LastAccessDate'))
    WebsiteUrl = clean(elem.get('WebsiteUrl'))
    Location = clean(elem.get('Location'))
    Age = clean(elem.get('Age'))
    AboutMe = clean(elem.get('AboutMe'))
    Views = clean(elem.get('Views'))
    LABEL = 'User'
    user_rec = [UserId, Reputation, CreationDate, DisplayName, LastAccessDate, \
                WebsiteUrl, Location, Age, AboutMe, Views, LABEL]
    user_batch.append(ascii_encode(user_rec))
    # counter += 1
    # if counter > MAX_REC:
    #     break
    if len(user_batch) > MAX_LINES:
        users.writerows(user_batch)
        user_batch.clear()

if len(user_batch) > 1:
    users.writerows(user_batch)
    user_batch.clear()
print('User parsing completed')
os.remove('../data/Users.xml')

tags = open_csv('tags')
tags.writerow(tagsHeader)
tags_batch = []
# counter = 0
for event, elem in tqdm(etree.iterparse('../data/Tags.xml',encoding="utf-8", recover=True)):
    TagId = clean(elem.get('TagName'))
    LABEL = 'Tag'
    tags_batch.append(ascii_encode([TagId, LABEL]))

    # counter += 1
    # if counter > MAX_REC:
    #     break
    if(len(tags_batch) > MAX_LINES):
        tags.writerows(tags_batch)
        tags_batch.clear()

if(len(tags_batch) > 1):
    tags.writerows(tags_batch)
    tags_batch.clear()
print('Tags parsing completed')

os.remove('../data/Tags.xml')

comments = open_csv('comments')
comments.writerow(commentsHeader)
batch = []
# counter = 0
for event, elem in tqdm(etree.iterparse('../data/Comments.xml',encoding="utf-8", recover=True)):
    UserId = clean(elem.get('UserId'))
    PostId = clean(elem.get('PostId'))
    Score = clean(elem.get('Score'))
    Text = clean(elem.get('Text'))
    CreationDate = cal_epoch(elem.get('CreationDate'))
    TYPE = 'Comment'
    comment_rec = [UserId, Score, Text, CreationDate, PostId, TYPE]
    batch.append(ascii_encode(comment_rec))
    elem.clear()
    while elem.getprevious() is not None:
        del elem.getparent()[0]
    # counter += 1
    # if counter > MAX_REC:
    #     break
    if len(batch) > MAX_LINES:
        comments.writerows(batch)
        batch.clear()

if len(batch) > 1:
    comments.writerows(batch)
    batch.clear()
print('comments parsing completed')

os.remove('../data/Comments.xml')

votes = open_csv('votes')
votes_rel = open_csv('votes_rel') #rel with posts
votes_fav = open_csv('votes_fav') #user favorites
votes.writerow(votesHeader)
votes_rel.writerow(votes_rel_header)
votes_fav.writerow(votes_fav_header)
votes_batch = []
votes_rel_batch = []
votes_fav_batch = []
# counter = 0
for event,elem in tqdm(etree.iterparse('../data/Votes.xml', encoding="utf-8", recover=True)):
    VoteId = clean(elem.get('Id'))
    VoteTypeId = clean(elem.get('VoteTypeId'))
    CreationDate = cal_epoch(elem.get('CreationDate'))
    BountyAmount = clean(elem.get('BountyAmount'))
    PostId = clean(elem.get('PostId'))
    LABEL = 'Vote' + (';Bounty' if elem.get('BountyAmount') else '')

    votes_batch.append(ascii_encode([VoteId, VoteTypeId, CreationDate, BountyAmount, LABEL]))
    votes_rel_batch.append(ascii_encode([VoteId, PostId, 'VOTES_ON']))
    if elem.get('UserId'):
        UserId = clean(elem.get('UserId'))
        votes_fav_batch.append(ascii_encode([UserId, VoteId, 'FAVORITE']))

    elem.clear()
    while elem.getprevious() is not None:
        del elem.getparent()[0]
    # counter += 1
    # if counter > MAX_REC:
    #     break
    if len(votes_batch) > MAX_LINES:
        votes.writerows(votes_batch)
        votes_batch.clear()
    if len(votes_rel_batch) > MAX_LINES:
        votes_rel.writerows(votes_rel_batch)
        votes_rel_batch.clear()
    if len(votes_fav_batch) > MAX_LINES:
        votes_fav.writerows(votes_fav_batch)
        votes_fav_batch.clear()

if len(votes_batch) > 1:
    votes.writerows(votes_batch)
    votes_batch.clear()
if len(votes_rel_batch) > 1:
    votes_rel.writerows(votes_rel_batch)
    votes_rel_batch.clear()
if len(votes_fav_batch) > 1:
    votes_fav.writerows(votes_fav_batch)
    votes_fav_batch.clear()
print('votes parsing completed')

os.remove('../data/Votes.xml')

badges = open_csv('badges')
badges_rel = open_csv('badges_rel') #UserId, UserId
badges.writerow(badgesHeader)
badges_rel.writerow(badges_rel_header)
badges_batch = []
badges_rel_batch = []
# counter = 0
badge_set = set()
for event,elem in tqdm(etree.iterparse('../data/Badges.xml', encoding="utf-8", recover=True)):
    BadgeId = clean(elem.get('Name'))
    LABEL = 'BADGE'
    UserId = clean(elem.get('UserId'))
    Date = cal_epoch(elem.get('Date'))
    badge_set.add(BadgeId)
    # badges_batch.append(ascii_encode([BadgeId, LABEL]))
    badges_rel_batch.append(ascii_encode([UserId, Date, BadgeId,'HAS_BADGE']))

    elem.clear()
    while elem.getprevious() is not None:
        del elem.getparent()[0]
    # counter += 1
    # if counter > MAX_REC:
    #     break
    # if len(badges_batch) > MAX_LINES:
    #     badges.writerows(badges_batch)
    #     badges_batch.clear()
    if len(badges_rel_batch) > MAX_LINES:
        badges_rel.writerows(badges_rel_batch)
        badges_rel_batch.clear()
# if len(badges_batch) > 1:
#     badges.writerows(badges_batch)
#     badges_batch.clear()
badges_batch = [ascii_encode([x,'BADGE']) for x in badge_set]
badges.writerows(badges_batch)

if len(badges_rel_batch) > 1:
    badges_rel.writerows(badges_rel_batch)
    badges_rel_batch.clear()

os.remove('../data/Badges.xml')



postlinks_ref = open_csv('postlinks_ref')
postlinks_dup = open_csv('postlinks_dup')
postlinks_ref.writerow(postlinksHeader)
postlinks_dup.writerow(postlinksHeader)
postlinksref_batch = []
postlinksdup_batch = []
# counter = 0
for event,elem in tqdm(etree.iterparse('../data/PostLinks.xml', encoding="utf-8", recover=True)):
    PostId = clean(elem.get('PostId'))
    RelatedPostId = clean(elem.get('RelatedPostId'))
    CreationDate = cal_epoch(elem.get('CreationDate'))
    TYPE = 'IS_DUPLICATE_OF' if elem.get('LinkTypeId') == '3' else 'IS_REFERENCED_FROM'

    if elem.get('LinkTypeId') == '3':
        postlinksdup_batch.append(ascii_encode([RelatedPostId,CreationDate,PostId,'IS_DUPLICATE_OF']))
    else:
        postlinksref_batch.append(ascii_encode([RelatedPostId, CreationDate, PostId, 'IS_REFERENCED_FROM']))

    elem.clear()
    while elem.getprevious() is not None:
        del elem.getparent()[0]
    # counter += 1
    # if counter > MAX_REC:
    #     break
    if len(postlinksref_batch) > MAX_LINES:
        postlinks_ref.writerows(postlinksref_batch)
        postlinksref_batch.clear()

    if len(postlinksdup_batch) > MAX_LINES:
        postlinks_dup.writerows(postlinksdup_batch)
        postlinksdup_batch.clear()

if len(postlinksref_batch) > 1:
    postlinks_ref.writerows(postlinksref_batch)
    postlinksref_batch.clear()

if len(postlinksdup_batch) > 1:
    postlinks_dup.writerows(postlinksdup_batch)
    postlinksdup_batch.clear()

os.remove('../data/PostLinks.xml')
"""
posts = open_csv('posts')
posts_rel = open_csv('posts_rel') #parent of contending answers #PostId, PostId
posts_answers = open_csv('posts_answers') #accepted answers #PostId, PostId
posts_lastedit = open_csv('posts_lastedit') # UserId, PostId
posts_owner = open_csv('posts_owner') #UserId, PostId
tags_rel = open_csv('tags_rel')

posts.writerow(postsHeader)
posts_rel.writerow(posts_rel_header)
posts_answers.writerow(posts_ans_header)
posts_lastedit.writerow(posts_lastedit_header)
posts_owner.writerow(posts_owner_header)
tags_rel.writerow(tags_rel_header)

posts_batch = []
posts_rel_batch = []
posts_ans_batch = []
posts_lastedit_batch = []
posts_owner_batch = []
posts_tags_batch = []
# counter = 0

for event, elem in tqdm(etree.iterparse('../data/Posts.xml', encoding="utf-8", recover=True)):
    PostId = clean(elem.get('Id'))
    CreationDate = cal_epoch(elem.get('CreationDate'))
    Score = clean(elem.get('Score'))
    ViewCount = clean(elem.get('ViewCount'))
    Body = clean(elem.get('Body'))
    LastActivityDate = cal_epoch(elem.get('LastActivityDate'))
    CommunityOwnedDate = cal_epoch(elem.get('CommunityOwnedDate'))
    ClosedDate = cal_epoch(elem.get('ClosedDate'))
    Title = clean(elem.get('Title'))
    AnswerCount = clean(elem.get('AnswerCount'))
    CommentCount = clean(elem.get('CommentCount'))
    FavoriteCount = clean(elem.get('FavoriteCount'))
    LABEL = 'Posts' #;Question' if elem.get('PostTypeId') is None or int(elem.get('PostTypeId')) == 1 or None else 'Posts;Answer'
    post_rec = [PostId,CreationDate,Score,ViewCount,Body,LastActivityDate,CommunityOwnedDate, \
                ClosedDate, Title, AnswerCount, CommentCount, FavoriteCount]
    posts_batch.append(ascii_encode(map(str,post_rec)))

    if elem.get('ParentId') is not None:
        posts_rel_batch.append(ascii_encode([clean(elem.get('ParentId')), PostId, 'PARENT_OF']))

    if elem.get('AcceptedAnswerId'):
        posts_ans_batch.append(ascii_encode([clean(elem.get('AcceptedAnswerId')), \
                                             PostId, 'ANSWERS']))
    posts_lastedit_batch.append(ascii_encode(map(str,[clean(elem.get('LastEditorUserId')), \
                                              cal_epoch(elem.get('LastEditDate')), \
                                              PostId, 'LAST_EDITED'])))
    posts_owner_batch.append(ascii_encode([clean('-1' if elem.get('OwnerUserId') is None else elem.get('OwnerUserId')),PostId,'CREATES']))
    Tags = clean(elem.get('Tags')).replace('><', ',').replace('<','').replace('>','').split(',')
    for t in Tags:
        posts_tags_batch.append(ascii_encode([PostId,t,'HAS_TAG']))

    elem.clear()
    while elem.getprevious() is not None:
        del elem.getparent()[0]
    # Optimization code; write in batch instead of line by line.
    # counter += 1
    # if counter > MAX_REC:
    #     break
    if(len(posts_batch) > MAX_LINES):
        posts.writerows(posts_batch)
        posts_batch.clear()

    if (len(posts_rel_batch) > MAX_LINES):
        posts_rel.writerows(posts_rel_batch)
        posts_rel_batch.clear()

    if (len(posts_ans_batch) > MAX_LINES):
        posts_answers.writerows(posts_ans_batch)
        posts_ans_batch.clear()

    if (len(posts_lastedit_batch) > MAX_LINES):
        posts_lastedit.writerows(posts_lastedit_batch)
        posts_lastedit_batch.clear()

    if (len(posts_owner_batch) > MAX_LINES):
        posts_owner.writerows(posts_owner_batch)
        posts_owner_batch.clear()

    if (len(posts_tags_batch) > MAX_LINES):
        tags_rel.writerows(posts_tags_batch)
        posts_tags_batch.clear()

#write remaining lines if left over.
if (len(posts_batch) > 1):
    posts.writerows(posts_batch)
    posts_batch.clear()

if (len(posts_rel_batch) > 1):
    posts_rel.writerows(posts_rel_batch)
    posts_rel_batch.clear()

if (len(posts_ans_batch) > 1):
    posts_answers.writerows(posts_ans_batch)
    posts_ans_batch.clear()

if (len(posts_lastedit_batch) > 1):
    posts_lastedit.writerows(posts_lastedit_batch)
    posts_lastedit_batch.clear()

if (len(posts_owner_batch) > 1):
    posts_owner.writerows(posts_owner_batch)
    posts_owner_batch.clear()

if (len(posts_tags_batch) > 1):
    tags_rel.writerows(posts_tags_batch)
    posts_tags_batch.clear()

print('Posts parsing completed')
# DELETE Posts.xml to make space for other operations.
os.remove('../data/Posts.xml')