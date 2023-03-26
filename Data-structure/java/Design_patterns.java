public class Design_patterns {
    
}

public class Singleton {
    private static Singleton instance;
    private Singleton() {
        // private constructor to prevent instantiation from outside
    }
    public static synchronized Singleton getInstance() {
        if (instance == null) {
            instance = new Singleton();
        }
        return instance;
    }
}

public abstract class Vehicle {
    public abstract void start();
}

public class Car extends Vehicle {
    @Override
    public void start() {
        System.out.println("Car started");
    }
}

public class Motorcycle extends Vehicle {
    @Override
    public void start() {
        System.out.println("Motorcycle started");
    }
}

public interface VehicleFactory {
    Vehicle createVehicle();
}

public class CarFactory implements VehicleFactory {
    @Override
    public Vehicle createVehicle() {
        return new Car();
    }
}

public class MotorcycleFactory implements VehicleFactory {
    @Override
    public Vehicle createVehicle() {
        return new Motorcycle();
    }
}




public interface Observer {
    void update(String message);
}

public interface Subject {
    void attach(Observer observer);
    void detach(Observer observer);
    void notifyObservers(String message);
}

public class MessagePublisher implements Subject {
    private List<Observer> observers = new ArrayList<>();
    @Override
    public void attach(Observer observer) {
        observers.add(observer);
    }
    @Override
    public void detach(Observer observer) {
        observers.remove(observer);
    }
    @Override
    public void notifyObservers(String message) {
        for (Observer observer : observers) {
            observer.update(message);
        }
    }
}

public class MessageSubscriberOne implements Observer {
    @Override
    public void update(String message) {
        System.out.println("Subscriber One received: " + message);
    }
}

public class MessageSubscriberTwo implements Observer {
    @Override
    public void update(String message) {
        System.out.println("Subscriber Two received: " + message);
    }
}






public interface Coffee {
    double getCost();
    String getDescription();
}

public class SimpleCoffee implements Coffee {
    @Override
    public double getCost() {
        return 1;
    }
    @Override
    public String getDescription() {
        return "Simple coffee";
    }
}

public abstract class CoffeeDecorator implements Coffee {
    protected final Coffee decoratedCoffee;
    public CoffeeDecorator(Coffee decoratedCoffee) {
        this.decoratedCoffee = decoratedCoffee;
    }
    public double getCost() {
        return decoratedCoffee.getCost();
    }
    public String getDescription() {
        return decoratedCoffee.getDescription();
    }
}

public class Milk extends CoffeeDecorator {
    public Milk(Coffee decoratedCoffee) {
        super(decoratedCoffee);
    }
    public double getCost() {
        return super.getCost() + 0.5;
    }
    public String getDescription() {
        return super.getDescription() + ", milk";
    }
}

public class Whip extends CoffeeDecorator {
    public Whip(Coffee decoratedCoffee) {
        super(decoratedCoffee);
    }
    public double getCost() {
        return super.getCost() + 0.7;
    }
    public String getDescription() {
        return super.getDescription() + ", whip";
    }
}







