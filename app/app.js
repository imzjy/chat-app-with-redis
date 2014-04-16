function FriendsListCtrl ($scope, $http) {

	$http.get('/users/1/friends').success(function(data) {
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