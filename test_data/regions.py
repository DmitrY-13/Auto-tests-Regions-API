class RegionsTestData:
    TOTAL_ITEMS = 22

    Q_STRINGS = 'нов', 'Нов', 'НОВ', 'ний но', 'a' * 30
    Q_STRINGS_IDS = (
        'lower case min value',
        'mixed case min value',
        'medium value',
        'upper case min value',
        'max value',
    )

    ACCEPTABLE_COUNTRY_CODES = 'cz', 'kg', 'kz', 'ru'
    UNACCEPTABLE_COUNTRY_CODES = ('ua',)

    DEFAULT_PAGE_NUMBER = 1
    UNACCEPTABLE_PAGE_NUMBERS = -3, 0

    DEFAULT_PAGE_SIZE = 15
    ACCEPTABLE_PAGES_SIZES = 5, 10, 15
    UNACCEPTABLE_PAGES_SIZES = 3, 8, 13, 18

    NON_INTEGERS_VALUES = 'string', 1.1, ''
    NON_INTEGERS_VALUES_IDS = 'non-numeric', 'fractional', 'empty'


class RegionsErrorMessages:
    Q_VALUE_LENGTH_GRATER_THAN_30_SYMBOLS = 'Параметр \'q\' должен быть не более 30 символов'
    Q_VALUE_LENGTH_LESS_THAN_3_SYMBOLS = 'Параметр \'q\' должен быть не менее 3 символов'

    UNACCEPTABLE_COUNTRY_CODE = (
        'Параметр \'country_code\' может быть одним из следующих значений: ru, kg, kz, cz'
    )

    NON_INTEGER_PAGE_NUMBER = 'Параметр \'page\' должен быть целым числом'
    PAGE_NUMBER_LESS_THAN_1 = 'Параметр \'page\' должен быть больше 0'

    UNACCEPTABLE_PAGE_SIZE = (
        'Параметр \'page_size\' может быть одним из следующих значений: 5, 10, 15'
    )
    NON_INTEGER_PAGE_SIZE = 'Параметр \'page_size\' должен быть целым числом'
