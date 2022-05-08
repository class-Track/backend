testCurriculum = {
    "name": "Different",
    "user_id": 126,
    "degree_id": 46,
    "degree_name": "Software Engineering",
    "department_id": 2,
    "department_name": "Computer Science and Engineering",
    "deptCode": "CIICv2",
    "curriculum_sequence": "totally_different",
    "length": 6,
    "credits": 132,
    "year_list": {
            "id": "year_list",
            "name": "Year List",
            "year_ids": [
                "2022"
            ]
    },
    "course_list": {
        "id": "course_list",
        "name": "Course List",
        "course_ids": [
                "INSO3001",
                "INSO3003",
                "INEL3001",
                "INEL3002",
                "INGL3001",
                "INSO3004"
        ]
    },
    "category_list": {
    },
    "2022": {
        "id": "2022",
        "name": "2022",
        "semester_ids": [
                "46_2022_spring",
                "46_2022_fall",
                "46_2022_summer",
                "46_2022_ext_summer"
        ]
    },
    "INSO3001": {
        "id": "INSO3001",
        "course_id": 7,
        "prereqs": [],
        "coreqs": [],
        "category": "LIBR"
    },
    "INSO3003": {
        "id": "INSO3003",
        "course_id": 8,
        "prereqs": [
                {
                    "classification": "INSO3001",
                    "course_id": 7,
                    "department_id": 41,
                    "name": "INSO Course A",
                    "id": "INSO3001"
                }
        ],
        "coreqs": [
            {
                "classification": "INEL3002",
                "course_id": 11,
                "department_id": 46,
                "name": "INEL Course B",
                "id": "INEL3002"
            }
        ],
        "category": "LIBR"
    },
    "INEL3001": {
        "id": "INEL3001",
        "course_id": 10,
        "prereqs": [],
        "coreqs": [],
        "category": "LIBR"
    },
    "INEL3002": {
        "id": "INEL3002",
        "course_id": 11,
        "prereqs": [],
        "coreqs": [
                {
                    "classification": "INEL3001",
                    "course_id": 10,
                    "department_id": 46,
                    "name": "INEL Course A",
                    "id": "INEL3001"
                }
        ],
        "category": "LIBR"
    },
    "INGL3001": {
        "id": "INGL3001",
        "course_id": 12,
        "prereqs": [],
        "coreqs": [],
        "category": "LIBR"
    },
    "INSO3004": {
        "id": "INSO3004",
        "course_id": 13,
        "prereqs": [
                {
                    "classification": "INSO3003",
                    "course_id": 8,
                    "department_id": 41,
                    "name": "INSO Course B",
                    "id": "INSO3003"
                },
            {
                    "classification": "INEL3002",
                    "course_id": 11,
                    "department_id": 46,
                    "name": "INEL Course B",
                    "id": "INEL3002"
                    }
        ],
        "coreqs": [],
        "category": "LIBR"
    },
    "46_2022_spring": {
        "id": "46_2022_spring",
        "name": "Spring",
        "year": "2022",
        "courses": [
                {
                    "id": "INSO3001",
                    "course_id": 7,
                    "department_id": 41,
                    "name": "INSO Course A",
                    "classification": "INSO3001"
                },
            {
                    "id": "INEL3001",
                    "course_id": 10,
                    "department_id": 46,
                    "name": "INEL Course A",
                    "classification": "INEL3001"
            }
        ]
    },
    "46_2022_fall": {
        "id": "46_2022_fall",
        "name": "Fall",
        "year": "2022",
        "courses": [
                {
                    "id": "INSO3003",
                    "course_id": 8,
                    "department_id": 41,
                    "name": "INSO Course B",
                    "classification": "INSO3003"
                },
            {
                    "id": "INEL3002",
                    "course_id": 11,
                    "department_id": 46,
                    "name": "INEL Course B",
                    "classification": "INEL3002"
            }
        ]
    },
    "46_2022_summer": {
        "id": "46_2022_summer",
        "name": "Summer",
        "year": "2022",
        "courses": [
                {
                    "id": "INSO3004",
                    "course_id": 13,
                    "department_id": 41,
                    "name": "INSO Course C",
                    "classification": "INSO3004"
                }
        ]
    },
    "46_2022_ext_summer": {
        "id": "46_2022_ext_summer",
        "name": "Extended Summer",
        "year": "2022",
        "courses": []
    }
}


# Admin account credentials
admin_account = {
    "email": "admin@account.com",
    "password": "admin"
}

# User account credentials
user_account = {
    "email": "juliantest2@test.com",
    "password": "test"
}

# Error account credentials
error_account = {
    "email": "error@account.com",
    "password": "test"
}

#Error messages

userM = {"err": "User is not an admin. They are a student"}

invalidSession = {"err": "Invalid Session"}

depNotFound = {"err": "Department not found"}

degNotFound = {"err": "Degree not found"}

uniError = {"err": "University is not administered by this user"}
