
class Helper():
    def format_number(self, number):
        if isinstance(number, float):
            if number.is_integer():
                return int(number)
            else:
                return f"{number:.2f}"
        return number