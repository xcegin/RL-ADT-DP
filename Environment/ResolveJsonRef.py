def resolveRef(entry, dictWithEntries):
    if isinstance(entry, dict):
        if "$id" in entry:
            dictWithEntries[entry["$id"]] = entry

    if not isinstance(entry, dict):
        if isinstance(entry, list):
            for i, item in enumerate(entry):
                entry[i] = resolveRef(item, dictWithEntries)

    if isinstance(entry, dict):
        for subkey in entry:
            if subkey == "$ref":
                entry = dictWithEntries[entry[subkey]]
                return entry
            else:
                entry[subkey] = resolveRef(entry[subkey], dictWithEntries)

    return entry
