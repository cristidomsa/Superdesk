'''
Created on Aug 23, 2012

@package: superdesk media archive
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Ioan v. Pocol

SQL Alchemy based implementation for the video data API. 
'''

from ally.container.ioc import injected
from ally.container.support import setup
from superdesk.media_archive.core.spec import QueryIndexer
from ally.container import wire
from superdesk.media_archive.api.video_info import IVideoInfoService, QVideoInfo
from superdesk.media_archive.core.impl.meta_service_base import MetaInfoServiceBaseAlchemy
from superdesk.media_archive.api.video_data import QVideoData
from superdesk.media_archive.meta.video_data import VideoDataMapped,\
    VideoDataEntry, META_TYPE_KEY
from superdesk.media_archive.meta.video_info import VideoInfoMapped,\
    VideoInfoEntry


# --------------------------------------------------------------------

@injected
@setup(IVideoInfoService)
class VideoInfoServiceAlchemy(MetaInfoServiceBaseAlchemy, IVideoInfoService):
    '''
    @see: IVideoInfoService
    '''
    
    queryIndexer = QueryIndexer;wire.entity('queryIndexer')

    def __init__(self):
        MetaInfoServiceBaseAlchemy.__init__(self, VideoInfoMapped, QVideoInfo, VideoDataMapped, QVideoData)
        self.queryIndexer.register(VideoInfoEntry, QVideoInfo, VideoDataEntry, QVideoData, META_TYPE_KEY)
        
