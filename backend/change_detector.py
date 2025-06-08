from difflib import SequenceMatcher

def detect_changes(text1, text2):
    changes = []
    
    paras1 = [p.strip() for p in text1.strip().split('\n\n') if p.strip()]
    paras2 = [p.strip() for p in text2.strip().split('\n\n') if p.strip()]

    sm = SequenceMatcher(None, paras1, paras2)

    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'replace':
            max_len = max(i2 - i1, j2 - j1)
            for i in range(max_len):
                old = paras1[i1 + i] if i1 + i < i2 else ""
                new = paras2[j1 + i] if j1 + i < j2 else ""
                changes.append({
                    "old": old,
                    "new": new
                })
        elif tag == 'delete':
            for old in paras1[i1:i2]:
                changes.append({
                    "old": old,
                    "new": ""
                })
        elif tag == 'insert':
            for new in paras2[j1:j2]:
                changes.append({
                    "old": "",
                    "new": new
                })

    return changes
