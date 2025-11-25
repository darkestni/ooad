public class AlarmPanel implements Observer<SensorEvent> {

    private String panelName;
    private double smokeThreshold;

    public AlarmPanel(String panelName, double smokeThreshold) {
        this.panelName = panelName;
        this.smokeThreshold = smokeThreshold;
    }

    @Override
    public void update(SensorEvent event) {
        // 只对烟雾（smoke）感兴趣
        if ("smoke".equalsIgnoreCase(event.getSensorType())) {
            double value = event.getValue();
            if (value > smokeThreshold) {
                System.out.println("ALARM [" + panelName + "]! High smoke detected: " + value);
            }
        }
    }
}
