from abc import ABC, abstractmethod
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Vehicle(ABC):
    """Абстрактний базовий клас для всіх транспортних засобів."""

    def __init__(self, make: str, model: str, region_spec: str) -> None:
        self.make: str = make
        self.model: str = model
        self.region_spec: str = region_spec

    @abstractmethod
    def start_engine(self) -> None:
        """Запуск двигуна транспортного засобу."""
        pass


class Car(Vehicle):
    """Клас, що представляє автомобіль."""

    def start_engine(self) -> None:
        """Запуск двигуна автомобіля."""
        logger.info(f"{self.make} {self.model} ({self.region_spec}): Двигун запущено")


class Motorcycle(Vehicle):
    """Клас, що представляє мотоцикл."""

    def start_engine(self) -> None:
        """Запуск двигуна мотоцикла."""
        logger.info(f"{self.make} {self.model} ({self.region_spec}): Мотор заведено")


class VehicleFactory(ABC):
    """Абстрактна фабрика для створення транспортних засобів."""

    @abstractmethod
    def create_car(self, make: str, model: str) -> Car:
        """Створення автомобіля."""
        pass

    @abstractmethod
    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        """Створення мотоцикла."""
        pass


class USVehicleFactory(VehicleFactory):
    """Фабрика для створення транспортних засобів за стандартами США."""

    def create_car(self, make: str, model: str) -> Car:
        """Створення автомобіля за стандартами США."""
        return Car(make, model, "US Spec")

    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        """Створення мотоцикла за стандартами США."""
        return Motorcycle(make, model, "US Spec")


class EUVehicleFactory(VehicleFactory):
    """Фабрика для створення транспортних засобів за стандартами ЄС."""

    def create_car(self, make: str, model: str) -> Car:
        """Створення автомобіля за стандартами ЄС."""
        return Car(make, model, "EU Spec")

    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        """Створення мотоцикла за стандартами ЄС."""
        return Motorcycle(make, model, "EU Spec")


def main() -> None:
    us_factory = USVehicleFactory()
    eu_factory = EUVehicleFactory()

    us_car = us_factory.create_car("Ford", "Mustang")
    us_motorcycle = us_factory.create_motorcycle("Harley-Davidson", "Sportster")

    eu_car = eu_factory.create_car("Volkswagen", "Golf")
    eu_motorcycle = eu_factory.create_motorcycle("Ducati", "Monster")

    us_car.start_engine()
    us_motorcycle.start_engine()
    eu_car.start_engine()
    eu_motorcycle.start_engine()


if __name__ == "__main__":
    main()