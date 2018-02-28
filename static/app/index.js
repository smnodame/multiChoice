var app = angular.module("myApp", ["ngRoute"])
app.config(function($routeProvider) {
    $routeProvider
    .when("/", {
        templateUrl : "components/create_new_form.html",
        controller: 'create_new_form_ctrl'
    })
    .when("/:id", {
        templateUrl : "components/question_form.html",
        controller: 'question_form_ctrl'
    })
});

app.controller('create_new_form_ctrl', ['$scope', '$location', function ($scope, $location) {
    $( "#datepicker" ).datepicker()

    const ID = (length) => {
        if (!length) {
            length = 8
        }
        var str = ''
        for (var i = 1; i < length + 1; i = i + 8) {
            str += Math.random().toString(36).substr(2, 10)
        }
        return ('_' + str).substr(0, length)
    }

    $scope.submit = () => {
        $location.url('/' + ID(8))
    }
}])

app.controller('question_form_ctrl',  ['$scope', function ($scope) {
    const at_least = 10

    $scope.question_label = {
        '0': 'ก',
        '1': 'ข',
        '2': 'ค',
        '3': 'ง',
        '4': 'จ'
    }

    const question_interface = (id) => ({
        id: id,
        name: '',
        answers: [
            {
                name: '',
                check: false
            }, {
                name: '',
                check: false
            }, {
                name: '',
                check: false
            }, {
                name: '',
                check: false
            }
        ]
    })

    $scope.questions = [
        question_interface(0),
        question_interface(1),
        question_interface(2),
        question_interface(3),
        question_interface(4),

        question_interface(5),
        question_interface(6),
        question_interface(7),
        question_interface(8),
        question_interface(9)
    ]
}])
