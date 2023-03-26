@Service
public class MyService {
    private MyDao myDao;
    
    public MyService(MyDao myDao) {
        this.myDao = myDao;
    }
    
    public void doSomething() {
        myDao.doSomething();
    }
}

@Repository
public class MyDao {
    public void doSomething() {
        // Do something
    }
}
