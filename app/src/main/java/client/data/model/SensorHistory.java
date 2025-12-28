@Entity
public class SensorHistory {

    @PrimaryKey(autoGenerate = true)
    public int id;

    public double temperature;
    public long timestamp;
}
