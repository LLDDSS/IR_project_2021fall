class CourseLists:

    def extractCourses(self, courseType):
        file = open('course.txt', 'r', encoding='latin-1')
        courses = open(courseType, 'w')
        line = " "

        while line:
            title = file.readline()
            description = file.readline()

            if not title:
                break

            title = title.strip().split(' ')

            if title[0] == courseType:
                courses.write("{}:{}:{}".format(title[0]+title[1], " ".join(title[2:]), description))
            line = file.readline()

            while '---' not in line:
                line = file.readline().strip()
        
        courses.close()
        file.close()
        return 
    