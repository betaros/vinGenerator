import json
from random import randrange


class VINTool:
    brand_list = []
    vehicle_descriptor_list = []
    vehicle_identifier = []
    available_chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                       'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K',
                       'L', 'M', 'N', 'P', 'R', 'S', 'T', 'U', 'V', 'W',
                       'X', 'Y', 'Z']

    def __init__(self):
        with open("data/brands.json", "r") as fileJSON:
            self.brand_list = json.load(fileJSON)

    def check_vin_characters(self, vin) -> bool:
        for character in vin:
            if character not in self.available_chars:
                print("Invalid character: ", character)
                return False
        return True

    def check_vin_length(self, vin) -> bool:
        if len(vin) < 17:
            print("VIN too short")
            return False
        elif len(vin) > 17:
            print("VIN too long")
            return False
        else:
            return True

    def check_vin(self, vin) -> bool:
        if not self.check_vin_length(vin):
            return False

        if not self.check_vin_characters(vin):
            return False

        return True

    def encode_vin(self, brand=None, country=None, descriptor=None, year=None, factory=None, identifier=None) -> str:
        result = ""
        if brand is None:
            print("Random brand")
            brand_number = randrange(0, len(self.brand_list))
            result = self.brand_list[brand_number]["vin"]
        else:
            if country is None:
                for element in self.brand_list:
                    if brand in element["brand"]:
                        result = element["vin"]
            else:
                for element in self.brand_list:
                    if brand in element["brand"] and country in element["country"]:
                        result = element["vin"]

        if descriptor is None:
            print("Random descriptor")
            for x in range(0, 6):
                result = result + self.available_chars[randrange(0, len(self.available_chars))]
        else:
            result = result + descriptor

        if year is None:
            print("Random year")
            result = result + self.available_chars[randrange(0, len(self.available_chars))]
        else:
            year_value = self.available_chars[(year - 2000) % len(self.available_chars)]
            result = result + year_value

        if factory is None:
            print("Random factory")
            result = result + self.available_chars[randrange(0, len(self.available_chars))]
        else:
            result = result + factory

        if identifier is None:
            print("Random identifier")
            for x in range(0, 6):
                result = result + self.available_chars[randrange(0, 10)]
        else:
            result = result + identifier

        return result

    def decode_vin(self, vin):
        if not self.check_vin(vin):
            return
        result = {}
        vin_structure = {"brand": vin[0:3],
                         "descriptor": vin[3:9],
                         "year": vin[9],
                         "factory": vin[10],
                         "identifier": vin[11:17]}
        for element in self.brand_list:
            if vin_structure["brand"] in element["vin"]:
                result["brand"] = element["brand"]
                result["location"] = element["country"]

        result["year"] = 2000 + self.available_chars.index(vin_structure["year"])

        return result


tool = VINTool()

encoded_vin_test = tool.encode_vin(brand="Audi", country="Germany", year=2015)
print(encoded_vin_test)

decoded_vin_test = tool.decode_vin(encoded_vin_test)
print(decoded_vin_test)
