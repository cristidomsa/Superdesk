'''
Created on May 18, 2013

@package: superdesk desk
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Ioan v. Pocol

API specifications for card (Kanban column).
'''

from ally.api.config import service, call, query, DELETE, UPDATE, \
    GET
from ally.api.criteria import AsLikeOrdered, AsEqualOrdered
from ally.api.type import Iter
from ally.support.api.entity_ided import Entity, IEntityService, QEntity
from superdesk.api.domain_superdesk import modelDesk
from superdesk.desk.api.desk import Desk
from superdesk.desk.api.task_status import TaskStatus

# --------------------------------------------------------------------

@modelDesk
class Card(Entity):
    '''
    Provides the card model.
    '''
    Desk = Desk
    Order = int
    Name = str
    Description = str
    UpperLimit = int
    Color = str
    
# --------------------------------------------------------------------

@query(Card)
class QCard(QEntity):
    '''
    Provides the query for desk model.
    '''
    order = AsEqualOrdered
    name = AsLikeOrdered
    description = AsLikeOrdered
    color = AsLikeOrdered

# --------------------------------------------------------------------

@service((Entity, Card), (QEntity, QCard))
class ICardService(IEntityService):
    '''
    Provides the service methods for the desk.
    '''
    
    @call(method=GET)
    def getByDesk(self, deskId:Desk.Id, detailed:bool=True, q:QCard=None) -> Iter(Card.Id):
        '''
        Provides the list of cards related to a desk.
        '''
        
    @call(method=GET)
    def getStatuses(self, cardId:Card.Id, detailed:bool=True) -> Iter(TaskStatus.Name):
        '''
        Provides all statuses assigned to the card.
        '''

    @call(method=GET, webName="Unassigned")
    def getUnassignedStatuses(self, cardId:Card.Id, detailed:bool=True) -> Iter(TaskStatus.Name):
        '''
        Returns a list of statuses that are not assigned to any board of the correspondent board desk.
        '''

    @call(method=UPDATE)
    def attachTaskStatus(self, cardId:Card.Id, statusKey:TaskStatus.Name):
        '''
        Attach a status to a card.
        '''

    @call(method=DELETE)
    def detachTaskStatus(self, cardId:Card.Id, statusKey:TaskStatus.Name) -> bool:
        '''
        Detach a status from a card.
        '''

    @call
    def insert(self, card:Card) -> Card.Id: 
        '''
        Overwrite default insert in order to set a value for order
        '''

    @call
    def update(self, card:Card): 
        '''
        Overwrite default update in order to not set a value for order directly
        '''
        
    @call(method=UPDATE, webName="Up")
    def moveUp(self, cardId:Card.Id):
        '''
         Move the card up in the list of desks cards.
        '''

    @call(method=UPDATE, webName="Down")
    def moveDown(self, cardId:Card.Id):
        '''
        Move the card down in the list of desks cards.
        '''       

    @call(method=UPDATE, webName="Jump")
    def makeJump(self, cardId:Card.Id, jump:int):
        '''
        Move the card to the specified position in the list of desks cards.
        Negative jump goes Up, positive jump goes Down.
        '''
