var app = angular.module("myApp", ["ngRoute"])
app.config(function($routeProvider) {
    $routeProvider
    .when("/form/create", {
        templateUrl : "static/components/create_new_form.html",
        controller: 'create_new_form_ctrl'
    })
    .when("/form/:id", {
        templateUrl : "static/components/question_form.html",
        controller: 'question_form_ctrl'
    })
});

app.controller('create_new_form_ctrl', ['$scope', '$location', '$http', function ($scope, $location, $http) {
    $( "#datepicker" ).datepicker()
    const question_amount = 10
    const answer_amount = 4

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

    const question_interface = (id) => ({
        id: id,
        name: '',
        answers: answer_interface()
    })

    const answer_interface = () => {
        const answers = []
        for(let i = 0; i < answer_amount; i++) {
            answers.push({
                name: '',
                check: false
            })
        }
        return answers
    }

    const get_questions = () => {
        const questions = []
        for(let i = 0; i < $scope.question_amount; i++) {
            questions.push(question_interface(i))
        }
        return questions
    }

    $scope.submit = () => {
        const slug = ID(8)

        const data = {
                slug: slug,
                name : $scope.name,
                description : $scope.description,
                time : $scope.time,
                question_amount : $scope.question_amount,
                subject : $scope.subject,
                date : $scope.date,
                answers: JSON.stringify(get_questions())
        }

        $http.post('/question/create', data).then((res) => {
            console.log('[submit] success ', res)
            const new_id = $location.url('/form/' + slug)
        })
    }
}])

app.controller('question_form_ctrl',  ['$scope', '$http', '$routeParams', function ($scope, $http, $routeParams) {
    $scope.question_label = {
        '0': 'ก',
        '1': 'ข',
        '2': 'ค',
        '3': 'ง',
        '4': 'จ'
    }

    $http.get('/question?slug='+ $routeParams.id).then((res) => {
        $scope.form = res.data
        $scope.questions = JSON.parse(res.data.answers)
    })

    $scope.update = () => {
        const data = Object.assign({}, $scope.form, {
            answers: JSON.stringify($scope.questions)
        })

        $http.put('/question/update', data).then((res) => {
            console.log('[submit] update ', res)
        })
    }
}])
