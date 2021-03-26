class Dog:
    def __init__(self, name, age, breed):
        self.name = name
        self.age = age
        self.breed = breed

    def __str__(self):
        return f"My name is '{self.name}', I am a {self.breed}. I am {self.age}"

    def bark(self, times):
        for i in range(times):
            print(f"{self.name} says 'woof'")


def main():
    fido = Dog("Fido", 6, "Collie")
    print(fido)

    fido.bark(3)


if __name__ == "__main__":
    main()

