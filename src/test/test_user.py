from src.lib.user import iso_time_to_epoch_second, get_rating


def test_iso_time_to_epoch_second():
    queries = ["2021-11-27T22:40:00+09:00", "2021-11-20T22:40:00+09:00", "2021-11-13T22:40:00+09:00"]
    expect = [1638014400 + 6000, 1637409600 + 6000, 1636804800 + 6000]
    for i in range(3):
        assert iso_time_to_epoch_second(queries[i]) == expect[i]


def test_get_rating():
    user_id = "yuto1115"
    epoch_seconds = [1610194106, 1616324772, 1621767984, 1640520181]
    expect = [2277, 2488, 2536, 2594]
    for i in range(4):
        assert get_rating([(user_id, epoch_seconds[i])])[0] == expect[i]
