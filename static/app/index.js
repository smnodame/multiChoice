var app = angular.module("myApp", ["ngRoute"])
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
    .otherwise({redirectTo : '/form/lists'})
})



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

const question_interface = (id, answer_amount) => ({
    id: id,
    name: '',
    answers: answer_interface(answer_amount),
    correct: ""
})

const answer_interface = (answer_amount) => {
    const answers = []
    for(let i = 0; i < answer_amount; i++) {
        answers.push({
            name: ''
        })
    }
    return answers
}

const get_questions = (question_amount, answer_amount) => {
    const questions = []
    for(let i = 0; i < question_amount; i++) {
        questions.push(question_interface(i, answer_amount))
    }
    return questions
}

app.controller('create_new_form_ctrl', ['$scope', '$location', '$http', function ($scope, $location, $http) {
    $( "#datepicker" ).datepicker()

    $scope.answer_amount = 4

    $scope.submit = () => {
        const slug = ID(8)

        const data = {
                slug: slug,
                name : $scope.name,
                description : $scope.description,
                time : $scope.time,
                question_amount : $scope.question_amount,
                answer_amount : $scope.answer_amount,
                subject : $scope.subject,
                date : $scope.date,
                answers: JSON.stringify(get_questions($scope.question_amount, $scope.answer_amount))
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

app.controller('form_lists_ctrl',  ['$scope', '$http', '$routeParams', '$location', '$compile', function ($scope, $http, $routeParams, $location, $compile) {


    const init = () => {
        $http.get('/forms').then((res) => {
            $scope.forms = res.data

            $scope.forms.forEach((form, index) => {
                 var tblElem = angular.element('<tr id="'+ form.slug +'">'+
                '<th scope="row">'+ (index+1) +'</th>'+
                '<td>'+ form.name + '</td>'+
                '<td>'+ form.subject + '</td>'+
                '<td>'+ form.question_amount + '</td>'+
                '<td>'+ form.time + '</td>'+
                '<td>'+ form.date + '</td>'+
                '<td>'+
                    '<button type="button" class="btn btn-info" ng-click="load_pdf(\''+ form.slug +'\')">PDF</button>'+
                '</td>'+
                '<td>'+
                    '<button type="button" ng-click="update(\''+ form.slug +'\')" class="btn btn-warning">เเก้ไข</button>'+
                    '<button type="button" ng-click="delete(\''+ form.slug +'\')" class="btn btn-danger">ลบ</button>'+
                '</td><'+
                '/tr>')

                //create a function to generate content
                var compileFn = $compile(tblElem);

                //execute the compilation function
                compileFn($scope)

                $( "#tbody" ).append(tblElem)
            })

            $('#example').DataTable()
        })
    }
    init()

    $scope.update = (id) => {
        $location.url('/form/'+ id +'/edit')
    }

    $scope.load_pdf = (slug) => {
        window.open('/send-pdf?slug='+slug)
    }

    $scope.delete = (id) => {
        $http.delete('/question/delete?slug='+ id).then((res) => {
            console.log('[submit] delete ', res)
        }).then(() => {
            $( "#"+id ).remove()
        })
    }


}])

app.controller('form_edit_ctrl',  ['$scope', '$http', '$routeParams', '$location', function ($scope, $http, $routeParams, $location) {
    $("#datepicker").datepicker()
    const answer_amount = 5
    $scope.page = 1

    $scope.click_page = (page) => {
        $scope.page = page
    }

    $scope.show_question = (i) => {
        const index = i + 1
        if($scope.page == 1) {
            if(index >= 1 && index <= 10) {
                return true
            }
        }
        if($scope.page == 2) {
            if(index >= 11 && index <= 20) {
                return true
            }
        }
        if($scope.page == 3) {
            if(index >= 21 && index <= 30) {
                return true
            }
        }
        if($scope.page == 4) {
            if(index >= 31 && index <= 40) {
                return true
            }
        }
        if($scope.page == 5) {
            if(index >= 41 && index <= 50) {
                return true
            }
        }
        if($scope.page == 6) {
            if(index >= 51 && index <= 60) {
                return true
            }
        }
        if($scope.page == 7) {
            if(index >= 61 && index <= 70) {
                return true
            }
        }
        if($scope.page == 8) {
            if(index >= 71 && index <= 80) {
                return true
            }
        }
        if($scope.page == 9) {
            if(index >= 81 && index <= 90) {
                return true
            }
        }
        if($scope.page == 10) {
            if(index >= 91 && index <= 100) {
                return true
            }
        }
        return false
    }

    $scope.change_question_number = () => {
        if(!$scope.new_question_number) {
            alert('จำนวนคำตอบควรควรอยู่ในช่วง 0-100')
            return
        }
        if($scope.new_question_number != $scope.form.question_amount) {
            if($scope.new_question_number > $scope.form.question_amount) {
                const diff = parseInt($scope.new_question_number) - parseInt($scope.form.question_amount)
                const new_questions = get_questions(diff, $scope.form.answer_amount)
                $scope.questions = $scope.questions.concat(new_questions)
                $scope.form.question_amount = $scope.new_question_number
            } else {
                $scope.questions = $scope.questions.filter((d, index) => {
                    return index + 1 <= $scope.new_question_number
                })
                $scope.form.question_amount = $scope.new_question_number
            }
            $scope.page = 1
        }
    }

    $scope.change_answer_number = () => {
        if(!$scope.new_answer_number) {
            alert('จำนวนคำตอบควรควรอยู่ในช่วง 2-5')
            return
        }
        if($scope.new_answer_number != $scope.form.answer_amount) {
            console.log($scope.questions)
            if($scope.new_answer_number > $scope.form.answer_amount) {
                const diff = parseInt($scope.new_answer_number) - parseInt($scope.form.answer_amount)

                $scope.questions = $scope.questions.map((question) => {
                    let new_answer = []
                    for(var i=0;i<diff;i++) {
                        new_answer.push({ name: "" })
                    }
                    const answers = question.answers.concat(new_answer)
                    return Object.assign({}, question, {
                        answers: answers
                    })
                })
                $scope.form.answer_amount = $scope.new_answer_number
            } else {
                $scope.questions = $scope.questions.map((question) => {
                    const answers = question.answers.filter((d, index) => {
                        return index + 1 <= $scope.new_answer_number
                    })
                    if(parseInt(question.correct) > answers.length) {
                        question.correct = ""
                    }
                    return Object.assign({}, question, {
                        answers: answers
                    })
                })
                $scope.form.answer_amount = $scope.new_answer_number
            }
        }
    }

    $scope.question_label = {
        '0': 'ก',
        '1': 'ข',
        '2': 'ค',
        '3': 'ง',
        '4': 'จ'
    }

    $http.get('/question?slug='+ $routeParams.id).then((res) => {
        $scope.form = res.data
        $scope.new_question_number = $scope.form.question_amount
        $scope.new_answer_number = $scope.form.answer_amount
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

app.controller('student_list_ctrl',  ['$scope', '$http', '$routeParams', '$location', '$compile', function ($scope, $http, $routeParams, $location, $compile) {
    $scope.year = ""
    $scope.level = ""
    $scope.grade = ""
    $scope.room = ""
    $scope.firstname = ""
    $scope.lastname = ""

    $scope.view_point = (slug) => {
        $scope.student_slug = slug
        $http.get(`/point_student?slug=${slug}`).then((res) => {
            $scope.points = res.data || []
            $("#myModal").modal()
        })

    }

    $scope.view_paper = (form_slug) => {
        $scope.form_slug = form_slug
        window.open(`/static/mask/${$scope.student_slug}_${$scope.form_slug}-answer.png`,'_blank');
    }

    $scope.search = () => {
        $http.get(`/student/?year=${$scope.year}&level=${$scope.level}&grade=${$scope.grade}&room=${$scope.room}&firstname=${$scope.firstname}&lastname=${$scope.lastname}`).then((res) => {
            $scope.students = res.data
            $scope.check_all = false

            $("#tbody").empty()

            $scope.students.forEach((student, index) => {
                 var tblElem = angular.element('<tr class="even pointer">'+
                    '<td class="a-center ">'+
                    '<input type="checkbox" class="flat" name="table_records" ng-model="students['+index+'].is_checked" ng-change="on_click_one(students['+index+'].is_checked)">'+
                    '</td>'+
                    '<td class=" ">'+ student.slug +'</td>'+
                    '<td class=" ">'+ student.firstname +'</td>'+
                    '<td class=" ">'+ student.lastname +'</td>'+
                    '<td class=" last"><a style="cursor: default" data-toggle="modal" ng-click="view_point(\''+ student.slug  + '\')" >ดูคะแนน</a>'+
                    '</td>'+
                    '</tr>')

                //create a function to generate content
                var compileFn = $compile(tblElem);

                //execute the compilation function
                compileFn($scope)

                $( "#tbody" ).append(tblElem)
            })
            $('#example').DataTable()
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

    $scope.get_qr = () => {
        const students = $scope.students.filter((student) => {
            return !!student.is_checked
        }).map((student) => {
            const obj = {
                slug: student.slug,
                name: student.firstname + ' ' + student.lastname
            }
            return Object.assign(obj, {
                text: JSON.stringify(obj)
            }, {})
        })
        localStorage.setItem("qr_list", JSON.stringify(students))
        window.open('/qrcode','_blank');
    }

    $scope.on_click_one = (is_checked) => {
        console.log('[on_click_one] is_checked ', is_checked)
        console.log($scope.students)
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
