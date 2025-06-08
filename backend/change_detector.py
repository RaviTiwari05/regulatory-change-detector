from difflib import SequenceMatcher

def detect_changes(text1, text2):
    changes = []
    paras1 = text1.strip().split('\n\n')
    paras2 = text2.strip().split('\n\n')

    sm = SequenceMatcher(None, paras1, paras2)

    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'replace':
            for old, new in zip(paras1[i1:i2], paras2[j1:j2]):
                if old.strip() != new.strip():
                    changes.append({
                        "old": old.strip(),
                        "new": new.strip()
                    })
        elif tag == 'delete':
            for old in paras1[i1:i2]:
                changes.append({
                    "old": old.strip(),
                    "new": ""
                })
        elif tag == 'insert':
            for new in paras2[j1:j2]:
                changes.append({
                    "old": "",
                    "new": new.strip()
                })

    return changes
