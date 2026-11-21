import re
import time
import random


def normalise_number(raw):
    digits = re.sub(r"\D", "", raw or "")
    return digits[-10:] if len(digits) >= 10 else digits


def normalise_name(name):
    name = (name or "").lower()
    name = re.sub(r"\b(dr|mr|mrs|ms|prof)\b\.?", "", name)
    name = re.sub(r"[^a-z\s]", "", name)
    return " ".join(name.split())


def merge_contacts(all_contacts):
    people = []     # each: {"names": set, "numbers": set, "emails": set, "alive": bool}
    index = {}      # normalised number -> person id

    for c in all_contacts:
        nums = {normalise_number(n) for n in c.get("numbers", []) if normalise_number(n)}
        mails = {e.strip().lower() for e in c.get("emails", []) if e and e.strip()}
        name = normalise_name(c.get("name", ""))

        owners = {index[n] for n in nums if n in index}

        if not owners:
            people.append({"names": set(), "numbers": set(), "emails": set(), "alive": True})
            pid = len(people) - 1
        else:
            pid = min(owners)
            for other in owners:
                if other != pid:                      # merge two existing people
                    people[pid]["names"] |= people[other]["names"]
                    people[pid]["numbers"] |= people[other]["numbers"]
                    people[pid]["emails"] |= people[other]["emails"]
                    people[other]["alive"] = False
                    for n in people[other]["numbers"]:
                        index[n] = pid

        if name:
            people[pid]["names"].add(name)
        people[pid]["numbers"] |= nums
        people[pid]["emails"] |= mails
        for n in nums:
            index[n] = pid

    return [p for p in people if p["alive"]]


# ---------- Test with a small list (verify by hand) ----------
phone1 = [
    {"name": "Dr. Ravi", "numbers": ["+91 98400 12345"], "emails": ["ravi@mail.com"]},
    {"name": "Anita", "numbers": ["98765-43210"], "emails": []},
]
phone2 = [
    {"name": "ravi kumar", "numbers": ["9840012345", "044 2345 6789"], "emails": ["RAVI@mail.com"]},
    {"name": "Kiran", "numbers": [], "emails": ["kiran@mail.com"]},   # missing number
]
sim = [
    {"name": "Anita S", "numbers": ["+919876543210"], "emails": ["anita@mail.com"]},
    {"name": "Ravi K", "numbers": ["04423456789"], "emails": []},
]

result = merge_contacts(phone1 + phone2 + sim)
for p in result:
    print("Names  :", sorted(p["names"]))
    print("Numbers:", sorted(p["numbers"]))
    print("Emails :", sorted(p["emails"]))
    print("-" * 30)
print("Total people:", len(result))


# ---------- Timing for 1,000 and 100,000 contacts ----------
def generate(n):
    contacts = []
    for _ in range(n):
        base = random.randint(9000000000, 9000000000 + n // 2)   # forces duplicates
        fmt = random.choice(["+91 {}", "{}", "0{}", "{}-"])
        contacts.append({
            "name": random.choice(["Dr. Ravi", "ravi kumar", "Anita", "Kiran"]),
            "numbers": [fmt.format(base)],
            "emails": [f"user{base}@mail.com"],
        })
    return contacts


for n in (1000, 100000):
    data = generate(n)
    start = time.perf_counter()
    merged = merge_contacts(data)
    elapsed = time.perf_counter() - start
    print(f"n = {n:>7}: {len(merged):>7} unique people, time = {elapsed:.4f} s")
