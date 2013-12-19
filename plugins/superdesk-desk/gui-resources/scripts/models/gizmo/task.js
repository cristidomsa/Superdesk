define
([
    'gizmo/superdesk',
    config.guiJs('superdesk/user', 'models/user'),
    'desk/models/gizmo/desk',
    'desk/models/gizmo/task-status'
], 
function(giz, User, Desk, Status)
{ 
    var Task = giz.Model.extend
    ({
        url: new giz.Url('Desk/Task'),
    }),
    Subtasks = giz.Collection.extend({ model: Task });
    
    Task = Task.extend
    ({ 
        defaults: 
        { 
            Desk: Desk,
            User: User,
            Task: Subtasks,
            Parent: Task,
            Status: Status
        } 
    });
    
    return Task;
});
