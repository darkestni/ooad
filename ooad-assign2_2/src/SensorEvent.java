public class SensorEvent {

    // 1. 私有字段
    private String sensorType;
    private String roomName;
    private double value;

    // 2. 构造函数（一次性传入三个字段）
    public SensorEvent(String sensorType, String roomName, double value) {
        this.sensorType = sensorType;
        this.roomName = roomName;
        this.value = value;
    }

    // 3. Getter 方法
    public String getSensorType() {
        return sensorType;
    }

    public String getRoomName() {
        return roomName;
    }

    public double getValue() {
        return value;
    }

    // 4. toString()，方便调试打印
    @Override
    public String toString() {
        return "SensorEvent{" +
                "sensorType='" + sensorType + '\'' +
                ", roomName='" + roomName + '\'' +
                ", value=" + value +
                '}';
    }
}
