public class DashboardViewModel extends ViewModel {

    private MutableLiveData<StatusResponse> status = new MutableLiveData<>();

    public LiveData<StatusResponse> getStatus() {
        load();
        return status;
    }

    private void load() {
        ApiClient.getApi().getStatus().enqueue(new Callback<>() {
            @Override
            public void onResponse(Call<StatusResponse> call, Response<StatusResponse> response) {
                status.postValue(response.body());
            }

            @Override
            public void onFailure(Call<StatusResponse> call, Throwable t) {
                status.postValue(null);
            }
        });
    }
}
