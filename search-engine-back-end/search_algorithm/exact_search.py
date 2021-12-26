import collections
import sys
import json


def main(argv):
    terms = argv[1].split(" ")
    category = terms[0].upper()
    course_list = collections.defaultdict(dict)

    try:
        file = open('./search_algorithm/' + category, 'r')
        for line in file.readlines():
            l = line.strip().split(':')
            course_list[l[0]]['title'] = l[1]
            course_list[l[0]]['description'] = l[2]

        file.close()
    except:
        print("error Incorrect information!")
        return

    if len(terms) == 2:
        if terms[0] + terms[1] not in course_list:
            print("error Could not find such course, please check the course id then try again!")
            return

        result = course_list[terms[0]+terms[1]]
        print(json.dumps({'department': terms[0], 'courseNumber': terms[1], \
            'courseTitle': result['title'], 'courseDescription': result['description']}))
    elif len(terms) == 1:
        for course, info in course_list.items():
            print(json.dumps({'department': terms[0], 'courseNumber': course[len(terms[0]):], \
            'courseTitle': info['title'], 'courseDescription': info['description']}))
            

    return



if __name__ == "__main__":
   main(sys.argv)
