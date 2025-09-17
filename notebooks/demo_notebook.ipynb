Python 3.13.7 (v3.13.7:bcee1c32211, Aug 14 2025, 19:10:51) [Clang 16.0.0 (clang-1600.0.26.6)] on darwin
Enter "help" below or click "Help" above for more information.
>>> # Quick demo script you can run in Jupyter (or convert to .ipynb)
... from app.classifier import batch_classify
... from app.risk import score_risk
... from app.render import render_markdown
... import json
... 
... with open("../sample_data/meeting.json") as f:
...     meeting = json.load(f)
... 
... classified = batch_classify(meeting["utterances"], attendees=meeting.get("attendees", []))
... 
... # Fake workload to showcase risk scoring
... owner_loads = {a: 0 for a in meeting.get("attendees", [])}
... owner_loads.update({"Carlos": 5})
... 
... scored = []
... for it in classified:
...     if it.get("type") == "Risk":
...         load = owner_loads.get((it.get("owner") or it.get("speaker") or ""), 0)
...         scored.append(score_risk(it, owner_high_pri_open=load))
...     else:
...         scored.append(it)
... 
... md = render_markdown(meeting, scored)
... print(md)
