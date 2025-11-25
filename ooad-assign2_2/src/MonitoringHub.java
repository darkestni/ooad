import java.util.ArrayList;
import java.util.List;

public class MonitoringHub implements Subject<SensorEvent> {

    // 存放所有注册的观察者（面板）
    private List<Observer<SensorEvent>> observers;

    public MonitoringHub() {
        this.observers = new ArrayList<>();
    }

    // 注册观察者
    @Override
    public void registerObserver(Observer<SensorEvent> observer) {
        if (observer != null && !observers.contains(observer)) {
            observers.add(observer);
        }
    }

    // 移除观察者
    @Override
    public void removeObserver(Observer<SensorEvent> observer) {
        observers.remove(observer);
    }

    // 通知所有观察者：有新的事件发生了
    @Override
    public void notifyObservers(SensorEvent event) {
        for (Observer<SensorEvent> observer : observers) {
            observer.update(event);
        }
    }

    // 对外提供的“上报数据”方法
    public void reportData(String sensorType, String roomName, double value) {
        // 1. 封装成一个事件对象
        SensorEvent event = new SensorEvent(sensorType, roomName, value);
        // 2. 通知所有观察者
        notifyObservers(event);
    }
}
