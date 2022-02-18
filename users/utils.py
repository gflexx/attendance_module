def course_code_extractor(reg_num):
    '''
        extract course code from
        spliting reg_number
    '''
    reg_number = reg_num.split('/')
    code = reg_number[0]
    course_code = code.upper()
    return course_code

def course_year_extractor(reg_num):
    '''
        extract course year from 
        spliting reg_number
    '''
    reg_number = reg_num.split('/')
    year = reg_number[2]
    return year
