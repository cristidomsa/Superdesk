define(['angular', 'https://github.com/enyo/dropzone/raw/master/downloads/dropzone-amd-module.js'],
function(angular, Dropzone) {
    'use strict';

    return function($scope, $q, Task, TaskStatusLoader, TaskService, TaskComment) {
        $scope.statuses = TaskStatusLoader();

        $scope.getEditData = function() {
            var data = $scope.task;

            if (data.DueDate === $scope.orig.DueDate) {
                delete data.DueDate; // TODO api does not accepts data in same format it sends them..
            }

            return data;
        };

        $scope.saveTask = function() {
            var data = $scope.getEditData();
            if ('Id' in $scope.task) {
                Task.update(data, function(task) {
                    angular.extend($scope.orig, $scope.task);
                    $scope.orig.User = $scope.task.User;
                    $scope.orig.Status = {Key: $scope.task.Status.Key};
                    $scope.saveLinks();
                });
            } else {
                Task.save(data, function(response) {
                    Task.get({Id: response.Id}, function(task) {
                        if ($scope.parentTask) {
                            $scope.parentTask.subtasks.push(task);
                        } else {
                            $scope.tasks.push(task);
                        }
                    });
                });
            }
        };

        $scope.deleteTask = function() {
            if ('Id' in $scope.task) {
                Task.remove({Id: $scope.task.Id});
                var index = $scope.tasks.indexOf($scope.orig);
                $scope.tasks.splice(index, 1);
            }
        };

        $scope.saveComment = function(taskComment) {
            if (typeof taskComment === 'string') {
                taskComment = {
                    Task: $scope.task.Id,
                    Text: taskComment
                };
                taskComment.User = localStorage.getItem('superdesk.login.id');
            }
            delete taskComment.CreatedOn;
            delete taskComment.UpdatedOn;

            if ('Id' in taskComment) {
                TaskComment.update(taskComment, function(response) {
                    TaskComment.get({Id: taskComment.Id}, function(taskCommentNew) {
                        taskComment.UpdatedOn = taskCommentNew.UpdatedOn;
                    });
                });
            } else {
                TaskComment.save(taskComment, function(response) {
                    TaskComment.get({Id: response.Id}, function(taskComment) {
                        taskComment.User = {Id: localStorage.getItem('superdesk.login.id'), Name: localStorage.getItem('superdesk.login.name')};
                        $scope.comments.push(taskComment);
                        $scope.commentText = '';
                    });
                });
            }
        };

        $scope.deleteComment = function(index) {
            TaskComment.delete({Id: $scope.comments[index].Id}, function(response) {
                $scope.comments.splice(index, 1);
            });
        };

        $scope.removeFile = function(files, index) {
            TaskService.removeFile($scope.task, files[index]);
            files.splice(index, 1);
        };

        $scope.addLink = function(links, task) {
            links.push({Task: task});
        }

        $scope.removeLink = function(links, index) {
            TaskService.removeLink(links[index]);
            links.splice(index, 1);
        };

        $scope.saveLinks = function() {
            $q.when($scope.task_links, function(links) {
                angular.forEach(links, function(link) {
                    TaskService.saveLink(link);
                });
            });
        };
    };
});
