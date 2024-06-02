from app.db_classes import Student

CURRENT_YEAR = 2023 # rok konani festivalu

def class_name_from_code(student_code):
    student_code = str(student_code)
    start_year = student_code[:2]
    study_type = student_code[2]
    class_number = student_code[3]
    roman_numerals = {
        '1': 'I',
        '2': 'II',
        '3': 'III',
        '4': 'IV',
        '5': 'V',
        '6': 'VI',
        '7': 'VII',
        '8': 'VIII'
    }
    study_length = CURRENT_YEAR - (int(start_year)+2000) + 1
    if study_length < 1 or study_length > 8: return 'Invalid code'
    if study_type == '8':
        return roman_numerals[str(study_length)]
    class_letter = 'A' if class_number == '1' else 'B'
    return f'{study_length}.{class_letter}'

def search(query):
    results = set()
    results.update(Student.query.filter(Student.name.icontains(query)))
    for student in results:
        student.name = student.name.replace(query.capitalize(), f'<mark>{query.capitalize()}</mark>').replace(query.lower(), f'<mark>{query}</mark>') 
    return results