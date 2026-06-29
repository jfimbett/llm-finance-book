from tools.grade import faithfulness, relevance, grade


CHUNKS = [
    "Consolidated gross margin was 64% in fiscal 2024 compared to 61% in fiscal 2023.",
    "Revenue increased 18% to 1.14 billion dollars in fiscal 2024.",
]


def test_grounded_answer_scores_high_faithfulness():
    grounded = "Gross margin was 64% in fiscal 2024 compared to 61% in fiscal 2023."
    assert faithfulness(grounded, CHUNKS) >= 0.8


def test_hallucinated_answer_scores_much_lower():
    grounded = "Gross margin was 64% in fiscal 2024 compared to 61% in fiscal 2023."
    invented = "Gross margin collapsed to 12% after a goodwill writedown in Brazil."
    # the invented figures ('12', 'writedown', 'brazil') are distinctive and absent,
    # so IDF weighting must push the hallucination far below the grounded answer
    assert faithfulness(invented, CHUNKS) < 0.5 < faithfulness(grounded, CHUNKS)


def test_relevance_rewards_on_topic_retrieval():
    q = "How did gross margin change year over year?"
    off_topic = ["The company opened a new marketing office in Berlin this spring."]
    assert relevance(q, CHUNKS) > relevance(q, off_topic)
    assert grade(q, "Gross margin was 64%.", CHUNKS)["relevance"] > 0.0
