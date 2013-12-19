'''
Created on May 18, 2013

@package: superdesk desk
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Ioan v. Pocol

Contains the SQL alchemy meta for desk API.
'''

from ..api.task_type import TaskType
from sqlalchemy.dialects.mysql.base import INTEGER
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Boolean
from superdesk.meta.metadata_superdesk import Base
from superdesk.desk.meta.task_status import TaskStatusMapped

# --------------------------------------------------------------------

class TaskTypeMapped(Base, TaskType):
    '''
    Provides the mapping for TaskType.
    '''
    __tablename__ = 'desk_task_type'
    __table_args__ = dict(mysql_engine='InnoDB', mysql_charset='utf8')

    Name = Column('key', String(255), nullable=False, unique=True)
    Active = Column('active', Boolean, nullable=False, default=True)
    # None REST model attribute --------------------------------------
    id = Column('id', INTEGER(unsigned=True), primary_key=True)

# --------------------------------------------------------------------

class TaskTypeTaskStatusMapped(Base):
    '''
    Provides the connecting of TaskType and TaskStatus.
    '''
    __tablename__ = 'desk_task_type_status'
    __table_args__ = dict(mysql_engine='InnoDB', mysql_charset='utf8')

    id = Column('id', INTEGER(unsigned=True), primary_key=True)
    taskType = Column('fk_task_type_id', ForeignKey(TaskTypeMapped.id, ondelete='CASCADE'), nullable=False)
    taskStatus = Column('fk_task_status_id', ForeignKey(TaskStatusMapped.id, ondelete='CASCADE'), nullable=False)