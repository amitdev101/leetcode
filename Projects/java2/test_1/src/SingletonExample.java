import com.sun.xml.internal.ws.api.message.Message;

public class SingletonExample {
    private static volatile SingletonExample instance;
    private Integer i;

//    private SingletonExample(Integer i){
//        this.i = i;
//    }

    private SingletonExample(){

    }
    public static SingletonExample getInstance(){
        if(instance==null){
            synchronized (SingletonExample.class){
                if(instance==null){
                    instance = new SingletonExample();
                }
            }
        }
        return instance;
    }

    public static void main(String[] args){
        System.out.println("Testing Singleton Example");
//        SingletonExample first = new SingletonExample(1);
//        SingletonExample second = new SingletonExample(2);
//        System.out.println(first.i + " " + second.i);
        SingletonExample first = SingletonExample.getInstance();
        SingletonExample second = SingletonExample.getInstance();
        if(first == second){
            System.out.println("== true");
        }
        if(first.equals(second)){
            System.out.println("equals true");
        }

    }


}
