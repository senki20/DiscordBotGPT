val= {
  "id": "modr-XXXXX",
  "model": "text-moderation-005",
  "results": [
    {
      "flagged": True,
      "categories": {
        "sexual": False,
        "hate": False,
        "harassment": False,
        "self-harm": False,
        "sexual/minors": False,
        "hate/threatening": False,
        "violence/graphic": False,
        "self-harm/intent": False,
        "self-harm/instructions": False,
        "harassment/threatening": True,
        "violence": True,
      },
      "category_scores": {
        "sexual": 1.2282071e-06,
        "hate": 0.010696256,
        "harassment": 0.29842457,
        "self-harm": 1.5236925e-08,
        "sexual/minors": 5.7246268e-08,
        "hate/threatening": 0.0060676364,
        "violence/graphic": 4.435014e-06,
        "self-harm/intent": 8.098441e-10,
        "self-harm/instructions": 2.8498655e-11,
        "harassment/threatening": 0.63055265,
        "violence": 0.99011886,
      }
    }
  ]
}

print(str(val["results"][0]["flagged"]))