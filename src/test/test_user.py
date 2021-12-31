from src.lib.user import iso_time_to_epoch_second


def test_iso_time_to_epoch_second():
    queries = ["2021-11-27T22:40:00+09:00", "2021-11-20T22:40:00+09:00", "2021-11-13T22:40:00+09:00"]
    expect = [1638014400 + 6000, 1637409600 + 6000, 1636804800 + 6000]
    for i in range(3):
        assert iso_time_to_epoch_second(queries[i]) == expect[i]
