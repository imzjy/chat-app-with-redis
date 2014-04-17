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
    	$scope.users = data;
  	});

	/*
	$scope.users = [
		{"id":2,"name":"zhangsan"},
		{"id":3,"name":"lisi"},
		{"id":1,"name":"jerryzhou"}
	];
	*/

	$scope.orderProp = "id";
}