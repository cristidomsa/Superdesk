'''
Created on May 3, 2012

@package: superdesk posts
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the SQL alchemy implementation for post API.
'''

from ..api.post import IPostService
from ..meta.post import PostMapped
from ..meta.type import PostTypeMapped
from ally.container.ioc import injected
from sql_alchemy.impl.entity import EntityGetCRUDServiceAlchemy
from ally.support.sqlalchemy.util_service import buildQuery, buildLimits
from ally.support.api.util_service import copy
from sqlalchemy.orm.exc import NoResultFound
from ally.exception import InputError, Ref
from ally.internationalization import _
from superdesk.post.api.post import Post, QPostUnpublished, QPostPublished, \
    QPost
from ally.support.sqlalchemy.functions import current_timestamp
from ally.api.extension import IterPart

# --------------------------------------------------------------------

COPY_EXCLUDE = ('Type', 'IsModified', 'AuthorName')

@injected
class PostServiceAlchemy(EntityGetCRUDServiceAlchemy, IPostService):
    '''
    Implementation for @see: IPostService
    '''

    def __init__(self):
        '''
        Construct the post service.
        '''
        EntityGetCRUDServiceAlchemy.__init__(self, PostMapped)

    def getUnpublished(self, creatorId=None, authorId=None, offset=None, limit=None, detailed=False, q=None):
        '''
        @see: IPostService.getUnpublished
        '''
        assert q is None or isinstance(q, QPostUnpublished), 'Invalid query %s' % q
        sql = self._buildQuery(creatorId, authorId, q)
        sql = sql.filter(PostMapped.PublishedOn == None)
        sqlLimit = buildLimits(sql, offset, limit)
        if detailed: return IterPart(sqlLimit.all(), sql.count(), offset, limit)
        return sqlLimit.all()

    def getPublished(self, creatorId=None, authorId=None, offset=None, limit=None, detailed=False, q=None):
        '''
        @see: IPostService.getPublished
        '''
        assert q is None or isinstance(q, QPostPublished), 'Invalid query %s' % q
        sql = self._buildQuery(creatorId, authorId, q)
        sql = sql.filter(PostMapped.PublishedOn != None)
        sqlLimit = buildLimits(sql, offset, limit)
        if detailed: return IterPart(sqlLimit.all(), sql.count(), offset, limit)
        return sqlLimit.all()

    def getAll(self, creatorId=None, authorId=None, offset=None, limit=None, detailed=False, q=None):
        '''
        @see: IPostService.getPublished
        '''
        assert q is None or isinstance(q, QPost), 'Invalid query %s' % q
        sql = self._buildQuery(creatorId, authorId, q)
        sqlLimit = buildLimits(sql, offset, limit)
        if detailed: return IterPart(sqlLimit.all(), sql.count(), offset, limit)
        return sqlLimit.all()

    def insert(self, post):
        '''
        @see: IPostService.insert
        '''
        assert isinstance(post, Post), 'Invalid post %s' % post
        postDb = PostMapped()
        copy(post, postDb, exclude=COPY_EXCLUDE)
        postDb.typeId = self._typeId(post.Type)
        if post.CreatedOn is None: postDb.CreatedOn = current_timestamp()

        self.session().add(postDb)
        self.session().flush((postDb,))
        post.Id = postDb.Id
        return post.Id

    def update(self, post):
        '''
        @see: IPostService.update
        '''
        assert isinstance(post, Post), 'Invalid post %s' % post
        postDb = self.session().query(PostMapped).get(post.Id)
        if not postDb: raise InputError(Ref(_('Unknown post id'), ref=Post.Id))
        if Post.Type in post: postDb.typeId = self._typeId(post.Type)
        if post.UpdatedOn is None: postDb.UpdatedOn = current_timestamp()

        self.session().flush((copy(post, postDb, exclude=COPY_EXCLUDE),))

    # ----------------------------------------------------------------

    def _buildQuery(self, creatorId=None, authorId=None, q=None):
        '''
        Builds the general query for posts.
        '''
        sql = self.session().query(PostMapped)
        if creatorId: sql = sql.filter(PostMapped.Creator == creatorId)
        if authorId: sql = sql.filter(PostMapped.Author == authorId)
        if q: sql = buildQuery(sql, q, PostMapped)
        return sql

    def _typeId(self, key):
        '''
        Provides the post type id that has the provided key.
        '''
        try:
            sql = self.session().query(PostTypeMapped.id).filter(PostTypeMapped.Key == key)
            return sql.one()[0]
        except NoResultFound:
            raise InputError(Ref(_('Invalid post type %(type)s') % dict(type=key), ref=Post.Type))
