import unittest
import PostalCode


class KnownValues(unittest.TestCase):
    knownValues= (
        ('Wrocław; Admiralska', '51-218'),
        ('Wrocław; ul. Ananasowa', '54-054'),
        ('Wrocław; ul. Biała', '54-044'),
        ('Wrocław; ul. Ceglana', '51-505'),
        ('Wrocław;  ul. Norweska 3', '54-403'),
        ('Wrocław; ul. Rybnicka', '52-016'),
        ('Warszawa; ul. Papieska', '03-159'),
        ('Warszawa; ul. Patriotów 2', '04-972'),
        ('Warszawa; ul. Penelopy', '03-642'),
        ('Warszawa; ul. Peonii', '04-794'),
        ('Warszawa; ul. Prawdziwka', '02-973'),
        ('Warszawa; ul. Lawinowa', '04-846'),
        ('Kraków; ul. Aliny', '31-417'),
        ('Kraków; ul. Barska', '30-307'),
        ('Kraków; ul.  Bolesława Chrobrego 19', '31-519'),
        ('Kraków; ul. Bystra', '30-623'),
        ('Gdańsk; ul. Achillesa', '80-299'),
        ('Poznań; ul. Morawskiego', '60-239'),
        ('Piła; al. Piastów 3', '64-920'),
        ('Wrocław; ul. Hercena Aleksandra 3', '50-453'),
    )


def testGetCode():
    for city, code in KnownValues.knownValues:
        PostalCode.get_key()
        test_name = 'test_%s' % (city)
        print(test_name)
        try:
            result = PostalCode.get_code(city)
            if not result:
                lattitude, longtitude = PostalCode.get_coordinates(city)
                result = PostalCode.get_code_from_coord(lattitude, longtitude)
        except IndexError:
            result = ""
        test = generator(code, result)
        setattr(KnownValues, test_name, test)

def generator(correct, ret):
    def test(self):
        self.assertEqual(correct, ret)
    return test


testGetCode()