from tools.evaluate import run_pipeline, train_test_split


ACCURACY_FLOOR = 0.8


def test_held_out_accuracy_clears_floor():
    report = run_pipeline(test_frac=0.3, seed=42)
    assert report["accuracy"] >= ACCURACY_FLOOR, report


def test_confusion_counts_sum_to_test_size():
    report = run_pipeline(test_frac=0.3, seed=42)
    c = report["confusion"]
    assert c["tp"] + c["tn"] + c["fp"] + c["fn"] == report["n_test"]


def test_split_is_deterministic_and_disjoint():
    train_a, test_a = train_test_split(50, test_frac=0.3, seed=42)
    train_b, test_b = train_test_split(50, test_frac=0.3, seed=42)
    assert (train_a, test_a) == (train_b, test_b)
    assert set(train_a).isdisjoint(test_a)
    assert len(train_a) + len(test_a) == 50
