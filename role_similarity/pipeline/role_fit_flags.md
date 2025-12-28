* Gate for answering is player good example of role
* input a small set of conditions based on our non z adjusted features
* other inputs: df
* compare players within combined sample
* output a new df which only contains players which meet the cutoff with their metric so we can sort by that

* Percentile rank largely makes sense, although for some stats we may want a simple cut off for others
* score based cut off, e.g cutoff_score = weighted mean of rule pass/fail

* pick rules based on stat distribution (ie long right tail have a higher percentile cutoff ), example players for the role and whether they are role-defining behaviours or support behaviours. Role definers should have stricter thresholds.
* start loose, tighten after.

Rules should be structured as such in the corresponding role file (e.g channel_forward.py):
    { 
       "feature" : "nameofstat",
       "type" : "percentile" | "absolute", 
       "threshold" : 0.65,
       "op" : "gte" | "lte",
       "weight" : 0.0-1.0,
       "required" : bool,
    }

