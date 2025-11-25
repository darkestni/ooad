public class RealtimePanel implements Observer<SensorEvent> {

    private String panelName;

    public RealtimePanel(String panelName) {
        this.panelName = panelName;
    }

    @Override
    public void update(SensorEvent event) {
        // 这里简单地把收到的数据打印出来
        System.out.println("[" + panelName + "] "
                + event.getSensorType() + " in " + event.getRoomName()
                + ": " + event.getValue());
    }
}
