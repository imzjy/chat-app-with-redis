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

function ChatCtrl ($scope, $http, $routeParams) {
	var get_friends_path = '/users/' + $routeParams.id + '/friends';
	$http.get(get_friends_path).success(function(data) {
    	$scope.friends = data;
	});


  $scope.talkTo = function (friend_id) {
    console.log(friend_id);
    $scope.dialog = {};
    $scope.dialog.friend = (function (friend_id) {
      for (var i = 0; i < $scope.friends.length; i++) {
        if($scope.friends[i].id == friend_id){
          return $scope.friends[i];
        }
      };
    })(friend_id);
    $scope.dialog.show = true;
    $scope.dialog.templateUrl = "partials/chat-dialog-window.html";
  }

  $scope.closeDialog = function () {
    $scope.dialog.show = false;
  }

  $scope.sendMessage = function(friend_id) {
    console.log(friend_id + ":" + this.new_messsage);
  }

	$scope.orderProp = "id";
}