var app = angular.module("myApp", ["ngRoute", "ja.qr"])
app.config(function($routeProvider) {
    $routeProvider
    .when("/form/create", {
        templateUrl : "static/components/create_new_form.html",
        controller: 'create_new_form_ctrl'
    })
    .when("/form/lists", {
        templateUrl : "static/components/form_list.html",
        controller: 'form_lists_ctrl'
    })
    .when("/form/:id/edit", {
        templateUrl : "static/components/form_edit.html",
        controller: 'form_edit_ctrl'
    })
    .when("/form/:id", {
        templateUrl : "static/components/question_form.html",
        controller: 'question_form_ctrl'
    })
    .when("/student", {
        templateUrl : "static/components/student_manament.html",
        controller: 'student_list_ctrl'
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
        answers: answer_interface(),
        correct: ""
    })

    const answer_interface = () => {
        const answers = []
        for(let i = 0; i < answer_amount; i++) {
            answers.push({
                name: ''
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

app.controller('question_form_ctrl',  ['$scope', '$http', '$routeParams', '$location', function ($scope, $http, $routeParams, $location) {
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

        if(JSON.stringify($scope.questions).indexOf('""') >= 0 || JSON.stringify($scope.form).indexOf('""') >= 0) {
            $scope.error = 'กรุณาใส่คำตอบ และเลือกคำตอบให้ครบทุกข้อ'
        } else {
            $http.put('/question/update', data).then((res) => {
                console.log('[submit] update ', res)
            }).then(() => {
                $location.url('/form/lists')
            })
        }
    }

    $scope.changeAnswer = () => {
        console.log($scope.questions)
    }
}])

app.controller('form_lists_ctrl',  ['$scope', '$http', '$routeParams', '$location', function ($scope, $http, $routeParams, $location) {

    const init = () => {
        $http.get('/forms').then((res) => {
            $scope.forms = res.data
        })
    }
    init()

    $scope.update = (id) => {
        $location.url('/form/'+ id +'/edit')
    }

    $scope.delete = (id) => {
        $http.delete('/question/delete?slug='+ id).then((res) => {
            console.log('[submit] delete ', res)
        }).then(() => {
            init()
        })
    }
}])

app.controller('form_edit_ctrl',  ['$scope', '$http', '$routeParams', '$location', function ($scope, $http, $routeParams, $location) {
    $("#datepicker").datepicker()

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

        if(JSON.stringify($scope.questions).indexOf('""') >= 0 || JSON.stringify($scope.form).indexOf('""') >= 0) {
            $scope.error = 'กรุณาใส่คำตอบ และเลือกคำตอบให้ครบทุกข้อ'
        } else {
            $http.put('/question/update', data).then((res) => {
                console.log('[submit] update ', res)
            }).then(() => {
                $location.url('/form/lists')
            })
        }
    }

    $scope.changeAnswer = () => {
        console.log($scope.questions)
    }
}])

app.controller('student_list_ctrl',  ['$scope', '$http', '$routeParams', '$location', function ($scope, $http, $routeParams, $location) {
    $scope.year = ""
    $scope.level = ""
    $scope.grade = ""
    $scope.room = ""
    $scope.firstname = ""
    $scope.lastname = ""

    $scope.search = () => {
        $http.get(`/student/?year=${$scope.year}&level=${$scope.level}&grade=${$scope.grade}&room=${$scope.room}&firstname=${$scope.firstname}&lastname=${$scope.lastname}`).then((res) => {
            $scope.students = res.data
            $scope.check_all = false
            console.log('[student_list_ctrl] ', res.data)
        })
    }

    $scope.on_click_all = () => {
        if($scope.check_all) {
            $scope.students = $scope.students.map((student) => {
                return Object.assign(student, { is_checked: true }, {})
            })
        } else {
            $scope.students = $scope.students.map((student) => {
                return Object.assign(student, { is_checked: false }, {})
            })
        }
    }

    $scope.on_click_one = (is_checked) => {
        if(!is_checked) {
            $scope.check_all = false
        } else {
            const students = $scope.students.filter((student) => {
                return !!student.is_checked
            })

            if(students.length == $scope.students.length) {
                $scope.check_all = true
            }
        }
    }
}])
