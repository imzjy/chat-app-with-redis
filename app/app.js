var webchatApp = angular.module('webchat', ['ngRoute']);

webchatApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/login', {
        templateUrl: 'partials/login.html',
        controller: LoginCtrl
      }).
      when('/users/:id', {
        templateUrl: 'partials/chat.html',
        controller: ChatCtrl
      }).
      otherwise({
        redirectTo: '/login'
      });
  }]);


function LoginCtrl ($scope, $location) {
	$scope.goChat = function (user_id) {
		$location.path('/users/' + user_id);
	}
}

function ChatCtrl ($scope, $http, $routeParams, $interval) {
	var get_friends_path = '/users/' + $routeParams.id + '/friends';
	$http.get(get_friends_path).success(function(data) {
    	$scope.friends = data;
      console.log(data)
	});


  $scope.checkFriendMessage = function (friend_id) {
    if ( angular.isDefined($scope.checkFriendMessageTimer) ) return;
    $scope.checkFriendMessageTimer = $interval(function () {

      console.log('check message from: ' + friend_id)
      $http.get('/users/' + $routeParams.id + '/messages/' + friend_id + '/unread').success(function(data) {
        if(angular.isDefined(data.text)){
          data.owner = 'friend';
          $scope.dialog.message_histories.push(data);
        }
      });

    }, 1000);
  }

  $scope.checkNewMessages = function () {
    if ( angular.isDefined($scope.checkNewMessagesTimer) ) return;
    $scope.checkNewMessagesTimer = $interval(function () {

      console.log('check new message')
      $http.get('/users/' + $routeParams.id + '/messages/new').success(function(data) {
        if(angular.isArray(data) && data.length > 0){
          angular.forEach($scope.friends, function(friend, idx){
              if (data.indexOf(friend.id) > -1) {
                $scope.friends[idx].active = true;
              }
          });
        }
      });

    }, 5000);
  }

  $scope.$on('$destroy', function() {
      if (angular.isDefined($scope.checkFriendMessageTimer)) {
        $interval.cancel($scope.checkFriendMessageTimer);
      }
      if (angular.isDefined($scope.checkNewMessages)) {
        $interval.cancel($scope.checkNewMessages);
      }
  });

  $scope.checkNewMessages();

  $scope.talkTo = function (friend_id) {
    $scope.dialog = {};

    $scope.closeDialog();

    $scope.dialog.friend = (function (friend_id) {
      for (var i = 0; i < $scope.friends.length; i++) {
        if($scope.friends[i].id == friend_id){
          return $scope.friends[i];
        }
      };
    })(friend_id);
    $scope.dialog.show = true;
    $scope.dialog.templateUrl = "partials/chat-dialog-window.html";
    $scope.dialog.message_histories = []
    $scope.checkFriendMessage(friend_id);
  }

  $scope.closeDialog = function () {
    $scope.dialog.show = false;
    if ( angular.isDefined($scope.checkFriendMessageTimer) ) {
      $interval.cancel($scope.checkFriendMessageTimer);
      delete $scope.checkFriendMessageTimer;
    }
  }

  $scope.sendMessage = function(friend_id) {
    var newMessage,
      msgEntry;
    
    newMessage = this.new_messsage;
    if (!newMessage) {
      return;
    };
    
    msgEntry = {
      from: $routeParams.id,
      to: friend_id,
      text: this.new_messsage
    }

    console.log(msgEntry);
    $http.post('/message/in', msgEntry).success(function(data, status) {
      console.log(status + " : " +data );
      if (status === 200) {
        $scope.dialog.message_histories.push(
          {"owner": "me",
            "text": data });
      };
    });
  }

	$scope.orderProp = "id";
}