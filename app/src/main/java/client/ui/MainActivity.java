public class MainActivity extends AppCompatActivity {

    private ActivityMainBinding binding;
    private DashboardViewModel vm;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        vm = new ViewModelProvider(this).get(DashboardViewModel.class);

        vm.getStatus().observe(this, status -> {
            if (status == null) return;

            binding.tempText.setText(status.temperature + " °C");
            binding.modeText.setText(status.mode);
            binding.relayText.setText(status.relay ? "ON" : "OFF");
        });

        binding.modeSwitch.setOnCheckedChangeListener((v, isChecked) -> {
            ApiClient.getApi()
                    .setMode(new RelayModeRequest(isChecked ? "AUTO" : "MANUAL"))
                    .enqueue(new Callback<>() {
                        @Override public void onResponse(Call<Void> c, Response<Void> r) {}
                        @Override public void onFailure(Call<Void> c, Throwable t) {}
                    });
        });
        binding.exportButton.setOnClickListener(v -> {

            Executors.newSingleThreadExecutor().execute(() -> {
                try {
                    List<SensorHistory> history =
                            AppDatabase.get(this).sensorDao().getAllSync();
        
                    File file = ExcelExporter.export(this, history);
        
                    runOnUiThread(() ->
                        Toast.makeText(this,
                                "Excel сохранён:\n" + file.getAbsolutePath(),
                                Toast.LENGTH_LONG).show()
                    );
        
                } catch (Exception e) {
                    e.printStackTrace();
                }
            });
        });
    }
}
